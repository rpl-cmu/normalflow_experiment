import argparse
import os

import cv2
import numpy as np
import yaml

from normalflow.viz_utils import annotate_coordinate_system

"""
This script visualize the tracking results by creating a tracking video.

Usage:
    python create_track_video.py [--parent_dir PARENT_DIR] [--config_path CONFIG_PATH] [--method METHOD]

Arguments:
    --parent_dir: The directory where the data are stored.
    --config_path: (Optional) The path of the configuration file for the GelSight sensor.
            The configuration file specifies the specifications of the sensor.
            The default is GelSight Mini configuration.
    --method: (Optional) The method to track the object poses.
            The default is 'nf', representing the normal flow method.

Before running, the required dataset needs to have:
    - gelsight.mp4: The GelSight video.
    - contact_masks.npy: The contact masks of the frames.
    - {method}_transforms.npy: The estimated transformation matrices of the object poses.
    - (Optional) true_transforms.npy: The ground truth transformation matrices of the object poses.

After running, the dataset will additionally includes:
    - {method}_tracking.mp4: The tracking video.
"""

config_path = os.path.join(os.path.dirname(__file__), "../configs/gsmini.yaml")


def viz_track():
    # Argument parser
    parser = argparse.ArgumentParser(
        description="Vizualize the tracking results by creating tracking video."
    )
    parser.add_argument(
        "-p",
        "--parent_dir",
        type=str,
        help="path to save data",
    )
    parser.add_argument(
        "-c",
        "--config_path",
        type=str,
        default=config_path,
        help="path to the sensor configuration file",
    )
    parser.add_argument(
        "-m",
        "--method",
        type=str,
        default="nf",
        choices=["nf", "icp", "filterreg", "fpfh"],
        help="Registration method",
    )
    args = parser.parse_args()

    # Read the configuration
    with open(args.config_path, "r") as f:
        config = yaml.safe_load(f)
        ppmm = config["ppmm"]
        imgw = config["imgw"]
        imgh = config["imgh"]

    # Load the tactile images
    parent_dir = args.parent_dir
    cap = cv2.VideoCapture(os.path.join(parent_dir, "gelsight.mp4"))
    fps = cap.get(cv2.CAP_PROP_FPS)
    images = []
    while cap.isOpened():
        ret, image = cap.read()
        if not ret:
            break
        images.append(image)
    cap.release()
    contact_masks = np.load(os.path.join(parent_dir, "contact_masks.npy"))
    est_start_T_currs = np.load(
        os.path.join(parent_dir, args.method + "_transforms.npy")
    )
    if os.path.exists(os.path.join(parent_dir, "true_transforms.npy")):
        gt_start_T_currs = np.load(os.path.join(parent_dir, "true_transforms.npy"))

    # Load, compute the center, and annotate the initial frame
    F_start = images[0]
    C_start = contact_masks[0]
    contours_start, _ = cv2.findContours(
        (C_start * 255).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    M_start = cv2.moments(max(contours_start, key=cv2.contourArea))
    cx_start, cy_start = int(M_start["m10"] / M_start["m00"]), int(
        M_start["m01"] / M_start["m00"]
    )
    annotated_F_start = F_start.copy()
    cv2.putText(
        annotated_F_start,
        "Initial Frame",
        (20, 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (255, 255, 255),
        1,
    )
    center_start = np.array([cx_start, cy_start]).astype(np.int32)
    unit_vectors_start = np.eye(3)[:, :2]
    annotate_coordinate_system(annotated_F_start, center_start, unit_vectors_start)
    center_3d_start = (
        np.array([(cx_start - imgw / 2 + 0.5), (cy_start - imgh / 2 + 0.5), 0])
        * ppmm
        / 1000.0
    )
    unit_vectors_3d_start = np.eye(3) * ppmm / 1000.0

    # Create the tracking tactile images
    tracked_frames = []
    for image_idx in range(len(images)):
        # Load the target frame and transformations
        F_curr = images[image_idx]
        start_T_curr = est_start_T_currs[image_idx]
        curr_T_start = np.linalg.inv(start_T_curr)

        # Create the tracked frame
        annotated_F_curr = F_curr.copy()
        remapped_center_3d_start = (
            np.dot(curr_T_start[:3, :3], center_3d_start) + curr_T_start[:3, 3]
        )
        remapped_cx_start = remapped_center_3d_start[0] * 1000 / ppmm + imgw / 2 - 0.5
        remapped_cy_start = remapped_center_3d_start[1] * 1000 / ppmm + imgh / 2 - 0.5
        remapped_center_start = np.array([remapped_cx_start, remapped_cy_start]).astype(
            np.int32
        )
        remapped_unit_vectors_start = (
            np.dot(curr_T_start[:3, :3], unit_vectors_3d_start.T).T * 1000 / ppmm
        )[:, :2]
        annotate_coordinate_system(
            annotated_F_curr, remapped_center_start, remapped_unit_vectors_start
        )

        # Annotate the true transformation if available
        if os.path.exists(os.path.join(parent_dir, "true_transforms.npy")):
            gt_start_T_curr = gt_start_T_currs[image_idx]
            gt_curr_T_start = np.linalg.inv(gt_start_T_curr)

            remapped_center_3d_start = (
                np.dot(gt_curr_T_start[:3, :3], center_3d_start)
                + gt_curr_T_start[:3, 3]
            )
            remapped_cx_start = (
                remapped_center_3d_start[0] * 1000 / ppmm + imgw / 2 - 0.5
            )
            remapped_cy_start = (
                remapped_center_3d_start[1] * 1000 / ppmm + imgh / 2 - 0.5
            )
            remapped_center_start = np.array(
                [remapped_cx_start, remapped_cy_start]
            ).astype(np.int32)
            remapped_unit_vectors_start = (
                np.dot(gt_curr_T_start[:3, :3], unit_vectors_3d_start.T).T * 1000 / ppmm
            )[:, :2]
            annotate_coordinate_system(
                annotated_F_curr,
                remapped_center_start,
                remapped_unit_vectors_start,
                alpha=0.5,
            )
            cv2.putText(
                annotated_F_curr,
                "Current Frame (Solid: %s, Transparent: MoCap)" % args.method,
                (20, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (255, 255, 255),
                1,
            )
        else:
            cv2.putText(
                annotated_F_curr,
                "Current Frame",
                (20, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.35,
                (255, 255, 255),
                1,
            )

        tracked_frames.append(cv2.hconcat([annotated_F_start, annotated_F_curr]))
    # Save the video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    save_path = os.path.join(parent_dir, args.method + "_tracking.mp4")
    video = cv2.VideoWriter(save_path, fourcc, fps, (imgw * 2, imgh))
    for tracked_frame in tracked_frames:
        video.write(tracked_frame)
    video.release()


if __name__ == "__main__":
    viz_track()
