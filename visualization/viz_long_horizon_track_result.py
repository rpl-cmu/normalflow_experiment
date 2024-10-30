import argparse
import cv2
import os
from os import path as osp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.spatial.transform import Rotation as R

from normalflow.utils import transform2pose
from matplotlib.lines import Line2D

# TODO: This code runs but can be cleaned up.


def viz_long_horizon_track_result():
    # Argument Parser
    parser = argparse.ArgumentParser(
        description="Visualize the long horizon tracking result."
    )
    parser.add_argument(
        "-p",
        "--parent_dir",
        type=str,
        help="path to the tracking dataset",
    )
    args = parser.parse_args()

    # Plotting parameters
    parent_dir = args.parent_dir
    dimension_names = ["True X", "True Y", "True Z"]
    error_names = ["Error X", "Error Y", "Error Z"]
    plt.rcParams["font.family"] = "Times New Roman"
    colors = [(1, 0, 0), (0, 0, 0), (0, 0, 1.0)]

    # # Plot the legends first
    # dimension_patches = [Line2D([0],[0],color=colors[i], label=dimension_name, lw=5) for i, dimension_name in enumerate(dimension_names)]
    # error_patches = [mpatches.Patch(facecolor=colors[i], alpha=0.2, label=error_name, edgecolor='none') for i, error_name in enumerate(error_names)]
    # patches = [dimension_patches[0], error_patches[0], dimension_patches[1], error_patches[1], dimension_patches[2], error_patches[2]]
    # fig, ax = plt.subplots(figsize=(15, 3))
    # ax.legend(handles=patches, ncol=3, fontsize=13, columnspacing=2.0)
    # ax.axis('off')  # Hide the axes
    # save_path = osp.join(parent_dir, "legend.png")
    # plt.savefig(save_path, dpi=500)
    # plt.close()

    # Compare the tracked pose and true pose for each trial
    trial_names = [
        name
        for name in os.listdir(parent_dir)
        if os.path.isdir(os.path.join(parent_dir, name))
    ]
    for trial_name in trial_names:
        trial_dir = os.path.join(parent_dir, trial_name)
        cap = cv2.VideoCapture(os.path.join(trial_dir, "gelsight.mp4"))
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        data = {"est_poses": [], "gt_poses": []}
        gt_start_T_currs = np.load(os.path.join(trial_dir, "true_transforms.npy"))
        est_start_T_currs = np.load(
            os.path.join(trial_dir, "nf_transforms.npy")
        )
        for gt_start_T_curr, est_start_T_curr in zip(
            gt_start_T_currs[1:], est_start_T_currs[1:]
        ):
            est_pose = transform2pose(est_start_T_curr)
            data["est_poses"].append(est_pose)
            gt_pose = transform2pose(gt_start_T_curr)
            data["gt_poses"].append(gt_pose)
        est_poses = np.array(data["est_poses"])
        est_poses[:, 3:] = np.rad2deg(np.unwrap(np.deg2rad(est_poses[:, 3:]), axis=0))
        gt_poses = np.array(data["gt_poses"])
        gt_poses[:, 3:] = np.rad2deg(np.unwrap(np.deg2rad(gt_poses[:, 3:]), axis=0))
        times = np.arange(len(est_poses)) / fps

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(5, 6))
        for idx in range(3):
            ax1.plot(times, gt_poses[:, idx], color=colors[idx], linewidth=5)
            ax1.fill_between(
                times, est_poses[:, idx], gt_poses[:, idx], color=colors[idx], alpha=0.3
            )
        ax1.tick_params(axis="both", which="major", labelsize=33)
        for idx in range(3):
            ax2.plot(times, gt_poses[:, 3 + idx], color=colors[idx], linewidth=5)
            ax2.fill_between(
                times, est_poses[:, 3 + idx], gt_poses[:, 3 + idx], color=colors[idx], alpha=0.3
            )
        ax2.tick_params(axis="both", which="major", labelsize=33)
        ax2.set_xlabel("Time (s)", fontsize=37)
        plt.tight_layout()
        save_path = osp.join(parent_dir, "%s_result.png"%trial_name)
        plt.savefig(save_path, dpi=300)
        plt.close()


if __name__ == "__main__":
    viz_long_horizon_track_result()
