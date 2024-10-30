import numpy as np
import open3d as o3d
import probreg

from normalflow.utils import height2pointcloud

"""
Baseline algorithms for tactile registration for sensor pose estimation.

Reference:
[1] J. Lu, Z. Wan, and Y. Zhang, “Tac2structure: Object surface reconstruction only through multi times touch,” IEEE Robotics and Automation Letters, vol. 8, no. 3, pp. 1391–1398, 2023.
[2] P. Sodhi, M. Kaess, M. Mukadanr, and S. Anderson, “Patchgraph: In-hand tactile tracking with learned surface normals,” in 2022 International Conference on Robotics and Automation (ICRA). IEEE Press, 2022, p. 2164–2170.
[3] S. Suresh, H. Qi, T. Wu, T. Fan, L. Pineda, M. Lambeta, J. Malik, M. Kalakrishnan, R. Calandra, M. Kaess, J. Ortiz, and M. Mukadam, “Neural feels with neural fields: Visuo-tactile perception for in-hand manipulation,” 2023.
[4] M. Bauza, E. Valls, B. Lim, T. Sechopoulos, and A. Rodriguez, “Tactile object pose estimation from the first touch with geometric contact rendering,” in Conference on Robot Learning, 2020."
"""


def fpfh(
    N_ref,
    C_ref,
    H_ref,
    N_tar,
    C_tar,
    H_tar,
    tar_T_ref_init=np.eye(4),
    ppmm=0.0634,
    n_samples=None,
):
    """
    The FPFH based algorithm to estimate the homogeneous transformation of the sensor between two frames.
    Given the normal map, contact map, and height map of two frames, return the sensor transformation.

    This algorithm extracts FPFH features from the pointclouds and find the transformation by
    RANSAC matching the FPFH features.
    The obtained transformation is then fine-tuned by the point-to-plane ICP.

    The algorithm is applied in Tac2structure [1].

    :param N_ref: np.ndarray (H, W, 3); the normal map of the reference frame.
    :param C_ref: np.ndarray (H, W); the contact map of the reference frame.
    :param H_ref: np.ndarray (H, W); the height map of the reference frame. (unit: pixel)
    :param N_tar: np.ndarray (H, W, 3); the normal map of the target frame.
    :param C_tar: np.ndarray (H, W); the contact map of the target frame.
    :param H_tar: np.ndarray (H, W); the height map of the target frame. (unit: pixel)
    :param tar_T_ref_init: np.2darray (4, 4); the initial guess homogeneous transformation matrix.
    :param ppmm: float; pixel per millimeter.
    :param n_samples: int; the number of samples to use for the optimization. If None, use all the pixels in contact.
    :return: np.ndarray (4, 4); the homogeneous transformation matrix from frame t to frame t+1.
    """
    # FPFH feature extraction in the reference frame
    masked_N_ref = N_ref.reshape(-1, 3)[C_ref.reshape(-1)]
    if n_samples is not None and n_samples < masked_N_ref.shape[0]:
        # Randomly sample the points to speed up
        sample_mask_ref = np.random.choice(
            masked_N_ref.shape[0], n_samples, replace=False
        )
    else:
        sample_mask_ref = np.arange(masked_N_ref.shape[0])
    pointcloud_ref = height2pointcloud(H_ref, ppmm)
    masked_pointcloud_ref = pointcloud_ref[C_ref.reshape(-1)]
    pcd_ref = o3d.geometry.PointCloud()
    pcd_ref.points = o3d.utility.Vector3dVector(masked_pointcloud_ref[sample_mask_ref])
    pcd_ref.normals = o3d.utility.Vector3dVector(masked_N_ref[sample_mask_ref])
    fpfh_ref = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_ref, o3d.geometry.KDTreeSearchParamHybrid(radius=0.001, max_nn=100)
    )

    # FPFH feature extraction in the target frame
    ref_T_tar_init = np.linalg.inv(tar_T_ref_init)
    masked_N_tar = N_tar.reshape(-1, 3)[C_tar.reshape(-1)]
    masked_N_tar = np.dot(ref_T_tar_init[:3, :3], masked_N_tar.T).T
    if n_samples is not None and n_samples < masked_N_tar.shape[0]:
        # Randomly sample the points to speed up
        sample_mask_tar = np.random.choice(
            masked_N_tar.shape[0], n_samples, replace=False
        )
    else:
        sample_mask_tar = np.arange(masked_N_tar.shape[0])
    pointcloud_tar = height2pointcloud(H_tar, ppmm)
    masked_pointcloud_tar = pointcloud_tar[C_tar.reshape(-1)]
    masked_pointcloud_tar = (
        np.dot(ref_T_tar_init[:3, :3], masked_pointcloud_tar.T).T
        + ref_T_tar_init[:3, 3]
    )
    pcd_tar = o3d.geometry.PointCloud()
    pcd_tar.points = o3d.utility.Vector3dVector(masked_pointcloud_tar[sample_mask_tar])
    pcd_tar.normals = o3d.utility.Vector3dVector(masked_N_tar[sample_mask_tar])
    fpfh_tar = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_tar, o3d.geometry.KDTreeSearchParamHybrid(radius=0.001, max_nn=100)
    )

    # Matching the FPFH features using RANSAC
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        pcd_ref,
        pcd_tar,
        fpfh_ref,
        fpfh_tar,
        True,
        0.001,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        ransac_n=4,
        checkers=[
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(0.001),
        ],
        criteria=o3d.pipelines.registration.RANSACConvergenceCriteria(10000, 0.99),
    )
    T = result.transformation
    tar_T_ref_fpfh = np.dot(tar_T_ref_init, T)

    # Apply point-to-plane ICP to fine-tune the transformation
    masked_N_tar = N_tar.reshape(-1, 3)[C_tar.reshape(-1)]
    masked_pointcloud_tar = pointcloud_tar[C_tar.reshape(-1)]
    pcd_tar = o3d.geometry.PointCloud()
    pcd_tar.points = o3d.utility.Vector3dVector(masked_pointcloud_tar[sample_mask_tar])
    pcd_tar.normals = o3d.utility.Vector3dVector(masked_N_tar[sample_mask_tar])
    reg_p2p = o3d.pipelines.registration.registration_icp(
        pcd_ref,
        pcd_tar,
        0.1,
        tar_T_ref_fpfh,
        o3d.pipelines.registration.TransformationEstimationPointToPlane(),
    )
    tar_T_ref = reg_p2p.transformation
    return tar_T_ref


def icp(
    N_ref,
    C_ref,
    H_ref,
    N_tar,
    C_tar,
    H_tar,
    tar_T_ref_init=np.eye(4),
    ppmm=0.0634,
    n_samples=None,
):
    """
    Using point-to-plane ICP to estimate the homogeneous transformation of the sensor between two frames.
    Given the normal map, contact map, and height map of two frames, return the sensor transformation.

    The algorithm is applied in many papers, including PatchGraph [2] and NeuralFeels [3].

    :param N_ref: np.ndarray (H, W, 3); the normal map of the reference frame.
    :param C_ref: np.ndarray (H, W); the contact map of the reference frame.
    :param H_ref: np.ndarray (H, W); the height map of the reference frame. (unit: pixel)
    :param N_tar: np.ndarray (H, W, 3); the normal map of the target frame.
    :param C_tar: np.ndarray (H, W); the contact map of the target frame.
    :param H_tar: np.ndarray (H, W); the height map of the target frame. (unit: pixel)
    :param tar_T_ref_init: np.2darray (4, 4); the initial guess homogeneous transformation matrix.
    :param ppmm: float; pixel per millimeter.
    :param n_samples: int; the number of samples to use for the optimization. If None, use all the pixels in contact.
    :return: np.ndarray (4, 4); the homogeneous transformation matrix from frame t to frame t+1.
    """
    # Pointcloud of the reference frame
    masked_N_ref = N_ref.reshape(-1, 3)[C_ref.reshape(-1)]
    if n_samples is not None and n_samples < masked_N_ref.shape[0]:
        # Randomly sample the points to speed up
        sample_mask_ref = np.random.choice(
            masked_N_ref.shape[0], n_samples, replace=False
        )
    else:
        sample_mask_ref = np.arange(masked_N_ref.shape[0])
    pointcloud_ref = height2pointcloud(H_ref, ppmm)
    masked_pointcloud_ref = pointcloud_ref[C_ref.reshape(-1)]
    pcd_ref = o3d.geometry.PointCloud()
    pcd_ref.points = o3d.utility.Vector3dVector(masked_pointcloud_ref[sample_mask_ref])
    pcd_ref.normals = o3d.utility.Vector3dVector(masked_N_ref[sample_mask_ref])
    # Pointcloud of the target frame
    masked_N_tar = N_tar.reshape(-1, 3)[C_tar.reshape(-1)]
    if n_samples is not None and n_samples < masked_N_tar.shape[0]:
        # Randomly sample the points to speed up
        sample_mask_tar = np.random.choice(
            masked_N_tar.shape[0], n_samples, replace=False
        )
    else:
        sample_mask_tar = np.arange(masked_N_tar.shape[0])
    pointcloud_tar = height2pointcloud(H_tar, ppmm)
    masked_pointcloud_tar = pointcloud_tar[C_tar.reshape(-1)]
    pcd_tar = o3d.geometry.PointCloud()
    pcd_tar.points = o3d.utility.Vector3dVector(masked_pointcloud_tar[sample_mask_tar])
    pcd_tar.normals = o3d.utility.Vector3dVector(masked_N_tar[sample_mask_tar])

    # Apply point-to-plane ICP
    reg_p2p = o3d.pipelines.registration.registration_icp(
        pcd_ref,
        pcd_tar,
        0.1,
        tar_T_ref_init,
        o3d.pipelines.registration.TransformationEstimationPointToPlane(),
    )
    tar_T_ref = reg_p2p.transformation
    return tar_T_ref


def filterreg(
    C_ref,
    H_ref,
    N_tar,
    C_tar,
    H_tar,
    tar_T_ref_init=np.eye(4),
    ppmm=0.0634,
    n_samples=None,
):
    """
    Using FilterReg registration to estimate the homogeneous transformation of the sensor between two frames.
    Given the normal map, contact map, and height map of two frames, return the sensor transformation.

    FilterReg is a probabilistic point cloud registration algorithm, which is robust to noise and outliers.

    The algorithm is applied in Tac2pose [4].

    :param N_ref: np.ndarray (H, W, 3); the normal map of the reference frame.
    :param C_ref: np.ndarray (H, W); the contact map of the reference frame.
    :param H_ref: np.ndarray (H, W); the height map of the reference frame. (unit: pixel)
    :param N_tar: np.ndarray (H, W, 3); the normal map of the target frame.
    :param C_tar: np.ndarray (H, W); the contact map of the target frame.
    :param H_tar: np.ndarray (H, W); the height map of the target frame. (unit: pixel)
    :param tar_T_ref_init: np.2darray (4, 4); the initial guess homogeneous transformation matrix.
    :param ppmm: float; pixel per millimeter.
    :param n_samples: int; the number of samples to use for the optimization. If None, use all the pixels in contact.
    :return: np.ndarray (4, 4); the homogeneous transformation matrix from frame t to frame t+1.
    """
    # Pointcloud of the reference frame in mm for better performance
    pointcloud_ref = height2pointcloud(H_ref, ppmm) * 1000.0
    masked_pointcloud_ref = pointcloud_ref[C_ref.reshape(-1)]
    if n_samples is not None and n_samples < masked_pointcloud_ref.shape[0]:
        # Randomly sample the points to speed up
        sample_mask_ref = np.random.choice(
            masked_pointcloud_ref.shape[0], n_samples, replace=False
        )
    else:
        sample_mask_ref = np.arange(masked_pointcloud_ref.shape[0])
    pcd_ref = o3d.geometry.PointCloud()
    pcd_ref.points = o3d.utility.Vector3dVector(masked_pointcloud_ref[sample_mask_ref])
    # Pointcloud of the target frame
    masked_N_tar = N_tar.reshape(-1, 3)[C_tar.reshape(-1)]
    if n_samples is not None and n_samples < masked_N_tar.shape[0]:
        # Randomly sample the points to speed up
        sample_mask_tar = np.random.choice(
            masked_N_tar.shape[0], n_samples, replace=False
        )
    else:
        sample_mask_tar = np.arange(masked_N_tar.shape[0])
    pointcloud_tar = height2pointcloud(H_tar, ppmm) * 1000.0
    masked_pointcloud_tar = pointcloud_tar[C_tar.reshape(-1)]
    pcd_tar = o3d.geometry.PointCloud()
    pcd_tar.points = o3d.utility.Vector3dVector(masked_pointcloud_tar[sample_mask_tar])

    # Apply point-to-plane FilterReg
    reg_p2p = probreg.filterreg.registration_filterreg(
        pcd_ref,
        pcd_tar,
        masked_N_tar[sample_mask_tar],
        tol=1e-5,
        sigma2=0.01,
        objective_type="pt2pl",
        tf_init_params={
            "rot": tar_T_ref_init[:3, :3],
            "t": tar_T_ref_init[:3, 3] * 1000.0,
        },
    )
    tar_T_ref = np.eye(4)
    tar_T_ref[:3, :3] = reg_p2p.transformation.rot
    tar_T_ref[:3, 3] = reg_p2p.transformation.t / 1000.0
    return tar_T_ref
