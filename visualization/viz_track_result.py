import argparse
import os

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import numpy as np

from normalflow.utils import transform2pose

"""
This script compares the tracking results of different methods for each object.
With the dataset that comes with the paper, the script can generate the comparison 
figure in Fig. 5 of the paper.

Pre-requisite:
    - Please download the official dataset that comes with the paper.
    - Use the instructions in the README.md file to compute the tracked poses using different methods.

Usage:
    python viz_track_result.py [-p PARENT_DIR]

Arguments:
    --parent_dir: The directory where the dataset is located.

Before running, each trial in the dataset should have:
    - true_transforms.npy: The ground truth transformation of sensor poses.
    - nf_transforms.npy: The estimated transformation using NormalFlow.
    - filterreg_transforms.npy: The estimated transformation using FilterReg.
    - icp_transforms.npy: The estimated transformation using ICP.
    - fpfh_transforms.npy: The estimated transformation using FPFH+RI.

After running, the dataset will additionally generate the comparison plots between each
method for each object. The comparison plots will be saved in the parent directory.
"""


def viz_track_result():
    # Argument Parser
    parser = argparse.ArgumentParser(description="Visualize the tracking result")
    parser.add_argument(
        "-p",
        "--parent_dir",
        type=str,
        help="path to the tracking dataset",
    )
    args = parser.parse_args()

    # Plotting parameters
    parent_dir = args.parent_dir
    methods = ["nf", "filterreg", "icp", "fpfh"]
    method_fullnames = ["NormalFlow", "FilterReg", "ICP", "FPFH+RI"]
    plt.rcParams["font.family"] = "Times New Roman"
    colors = [
        "#5161e0",
        "#51e075",
        "#e05159",
        "#e0c051",
    ]

    # Group the trials by the object
    trial_names = [
        name
        for name in os.listdir(parent_dir)
        if os.path.isdir(os.path.join(parent_dir, name))
    ]
    object_names, idxs = np.unique(
        [trial_name[:-1] for trial_name in trial_names], return_inverse=True
    )
    for object_idx, object_name in enumerate(object_names):
        # The trials belong to this object
        method_data = {"nf": [], "filterreg": [], "icp": [], "fpfh": []}
        matching_indices = np.where(idxs == object_idx)[0]
        for idx in matching_indices:
            trial_name = trial_names[idx]
            trial_dir = os.path.join(parent_dir, trial_name)
            gt_start_T_currs = np.load(os.path.join(trial_dir, "true_transforms.npy"))
            for method in methods:
                data = {"est_poses": [], "gt_poses": []}
                est_start_T_currs = np.load(
                    os.path.join(trial_dir, "%s_transforms.npy" % method)
                )
                for gt_start_T_curr, est_start_T_curr in zip(
                    gt_start_T_currs[1:], est_start_T_currs[1:]
                ):
                    est_pose = transform2pose(est_start_T_curr)
                    data["est_poses"].append(est_pose)
                    gt_pose = transform2pose(gt_start_T_curr)
                    data["gt_poses"].append(gt_pose)
                est_poses = np.array(data["est_poses"])
                gt_poses = np.array(data["gt_poses"])
                pose_ae = np.abs(est_poses - gt_poses)
                method_data[method].extend(pose_ae)
        # Print the result for each methods
        fig = plt.figure(figsize=(10.0, 3.5))
        gs = GridSpec(2, 2, height_ratios=[4, 1.0])
        axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])]
        for i, method in enumerate(methods):
            pose_mae = np.mean(np.array(method_data[method]), axis=0)
            axes[0].bar(
                np.arange(3) + i * 0.17,
                np.clip(pose_mae[:3], 0.0, 2.0),
                width=0.17,
                color=colors[i],
                label=method,
            )
            axes[1].bar(
                np.arange(3) + i * 0.17,
                np.clip(pose_mae[3:], 0.0, 10.0),
                width=0.17,
                color=colors[i],
                label=method,
            )
        axes[0].set_ylim(0.0, 2.0)
        axes[1].set_ylim(0.0, 10.0)
        axes[0].set_xticks(np.arange(3) + 0.17 * (len(methods) - 1) / 2)
        axes[1].set_xticks(np.arange(3) + 0.17 * (len(methods) - 1) / 2)
        axes[0].set_xticklabels(["x", "y", "z"])
        axes[1].set_xticklabels([r"$\theta_x$", r"$\theta_y$", r"$\theta_z$"])
        axes[0].set_ylabel("Error (mm)", fontsize=26)
        axes[1].set_ylabel(r"Error ($^{\circ}$)", fontsize=26)
        axes[1].yaxis.set_label_coords(-0.1, 0.5)
        axes[0].tick_params(axis="both", which="major", labelsize=24)
        axes[1].tick_params(axis="both", which="major", labelsize=24)
        # Add the legend
        patches = [
            mpatches.Patch(color=colors[i], label=method_fullnames[i])
            for i in range(len(methods))
        ]
        fig.legend(
            handles=patches,
            loc="lower center",
            ncol=4,
            fontsize=24,
            columnspacing=1.0,
            bbox_to_anchor=(0.5, 0.0),
        )
        # Save the comparison figure
        plt.subplots_adjust(bottom=0.3)
        plt.tight_layout()
        save_path = os.path.join(parent_dir, object_name + "_error.png")
        plt.savefig(save_path, dpi=300)
        plt.close()


if __name__ == "__main__":
    viz_track_result()
