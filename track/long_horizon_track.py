import argparse
import os

import numpy as np
import yaml

from gs_sdk.gs_reconstruct import poisson_dct_neumaan
from normalflow.registration import normalflow
from normalflow.utils import gxy2normal, erode_contact_mask, transform2pose


"""
This script demonstrates long-horizon tracking the object poses using normalflow.

Usage:
    python long_horizon_track.py [--parent_dir PARENT_DIR] [--config_path CONFIG_PATH]

Arguments:
    --parent_dir: The directory where the data are stored.
    --config_path: (Optional) The path of the configuration file for the GelSight sensor.
            The configuration file specifies the specifications of the sensor.
            The default is GelSight Mini configuration.

Before running, the required dataset needs to have:
    - contact_masks.npy: The contact masks of the frames.
    - gradient_maps.npy: The gradient maps of the frames.

After running, the dataset will additionally includes:
    - nf_transforms.npy: The estimated transformation matrices of the object poses.
"""

config_path = os.path.join(os.path.dirname(__file__), "../configs/gsmini.yaml")


def long_horizon_track():
    # Arugment Parser
    parser = argparse.ArgumentParser(description="Long-horizon Track the 3D poses.")
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
    args = parser.parse_args()

    # Read the configuration
    with open(args.config_path, "r") as f:
        config = yaml.safe_load(f)
        ppmm = config["ppmm"]
    # Load the initial frame and set as the reference frame
    parent_dir = args.parent_dir
    gradient_maps = np.load(os.path.join(parent_dir, "gradient_maps.npy"))
    contact_masks = np.load(os.path.join(parent_dir, "contact_masks.npy"))
    G_ref = gradient_maps[0].astype(np.float32)
    C_ref = contact_masks[0]
    C_ref = erode_contact_mask(C_ref)
    H_ref = poisson_dct_neumaan(G_ref[:, :, 0], G_ref[:, :, 1]).astype(np.float32)
    N_ref = gxy2normal(G_ref)
    # Set up the previous frame
    G_prev = None
    C_prev = None
    H_prev = None
    N_prev = None

    # Track the sensor transformation relative to the initial frame
    start_T_ref = np.eye(4)
    est_transforms = [np.eye(4)]
    n_resets = 0
    for G_curr, C_curr in zip(gradient_maps[1:], contact_masks[1:]):
        # Load and compute the surface information of the target frame
        G_curr = G_curr.astype(np.float32)
        C_curr = erode_contact_mask(C_curr)
        H_curr = poisson_dct_neumaan(G_curr[:, :, 0], G_curr[:, :, 1]).astype(
            np.float32
        )
        N_curr = gxy2normal(G_curr)
        if N_prev is not None:
            curr_T_ref = normalflow(
                N_ref,
                C_ref,
                H_ref,
                N_curr,
                C_curr,
                H_curr,
                prev_T_ref,
                ppmm,
            )
        else:
            curr_T_ref = normalflow(
                N_ref,
                C_ref,
                H_ref,
                N_curr,
                C_curr,
                H_curr,
                np.eye(4),
                ppmm,
            )
        # Check if reference frame need to be resetted
        if N_prev is not None:
            curr_T_prev = normalflow(
                N_prev,
                C_prev,
                H_prev,
                N_curr,
                C_curr,
                H_curr,
                np.eye(4),
                ppmm,
            )
            T_error = np.linalg.inv(curr_T_ref) @ curr_T_prev @ prev_T_ref
            pose_error = transform2pose(T_error)
            rot_error = np.linalg.norm(pose_error[3:])
            trans_error = np.linalg.norm(pose_error[:3])
            is_reset = rot_error > 3.0 or trans_error > 1.0
            if is_reset:
                n_resets += 1
                G_ref = G_prev.copy()
                C_ref = C_prev.copy()
                H_ref = H_prev.copy()
                N_ref = N_prev.copy()
                start_T_ref = start_T_ref @ np.linalg.inv(prev_T_ref)
                curr_T_ref = curr_T_prev.copy()
        G_prev = G_curr.copy()
        C_prev = C_curr.copy()
        H_prev = H_curr.copy()
        N_prev = N_curr.copy()
        prev_T_ref = curr_T_ref.copy()
        start_T_curr = start_T_ref @ np.linalg.inv(curr_T_ref)
        est_transforms.append(start_T_curr)
    save_path = os.path.join(parent_dir, "nf_transforms.npy")
    np.save(save_path, np.array(est_transforms))
    print(
        "Long-horizon object pose tracked for data in %s, reference reset %d times"
        % (parent_dir, n_resets)
    )


if __name__ == "__main__":
    long_horizon_track()
