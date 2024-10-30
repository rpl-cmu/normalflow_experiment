import argparse
import os

import numpy as np
import yaml

from baselines.registration import fpfh, icp, filterreg
from gs_sdk.gs_reconstruct import poisson_dct_neumaan
from normalflow.registration import normalflow
from normalflow.utils import gxy2normal, erode_contact_mask

"""
This script demonstrates tracking the object poses using different methods.
Users can choose the following methods: normalflow, icp, filterreg, fpfh.

Usage:
    python track.py [--parent_dir PARENT_DIR] [--config_path CONFIG_PATH] [--method METHOD {nf, icp, filterreg, fpfh}]

Arguments:
    --parent_dir: The directory where the data are stored.
    --config_path: (Optional) The path of the configuration file for the GelSight sensor.
            The configuration file specifies the specifications of the sensor.
            The default is GelSight Mini configuration.
    --method: (Optional) The method to track the object poses.
            The default is 'nf', representing the normal flow method.

Before running, the required dataset needs to have:
    - contact_masks.npy: The contact masks of the frames.
    - gradient_maps.npy: The gradient maps of the frames.

After running, the dataset will additionally includes:
    - {method}_transforms.npy: The estimated transformation matrices of the object poses.
"""

config_path = os.path.join(os.path.dirname(__file__), "../configs/gsmini.yaml")


def track():
    # Arugment Parser
    parser = argparse.ArgumentParser(description="Track the 3D poses.")
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
    # Load the initial frame
    parent_dir = args.parent_dir
    gradient_maps = np.load(os.path.join(parent_dir, "gradient_maps.npy"))
    contact_masks = np.load(os.path.join(parent_dir, "contact_masks.npy"))
    G_ref = gradient_maps[0].astype(np.float32)
    C_ref = contact_masks[0]
    C_ref = erode_contact_mask(C_ref)
    H_ref = poisson_dct_neumaan(G_ref[:, :, 0], G_ref[:, :, 1]).astype(np.float32)
    N_ref = gxy2normal(G_ref)

    # Track the sensor transformation relative to the reference frame
    curr_T_ref_init = np.eye(4)
    start_T_ref = np.eye(4)
    est_transforms = [np.eye(4)]
    for G_curr, C_curr in zip(gradient_maps[1:], contact_masks[1:]):
        # Load and compute the surface information of the target frame
        G_curr = G_curr.astype(np.float32)
        C_curr = erode_contact_mask(C_curr)
        H_curr = poisson_dct_neumaan(G_curr[:, :, 0], G_curr[:, :, 1]).astype(
            np.float32
        )
        N_curr = gxy2normal(G_curr)
        if args.method == "nf":
            curr_T_ref = normalflow(
                N_ref,
                C_ref,
                H_ref,
                N_curr,
                C_curr,
                H_curr,
                curr_T_ref_init,
                ppmm,
            )
        elif args.method == "icp":
            curr_T_ref = icp(
                N_ref, C_ref, H_ref, N_curr, C_curr, H_curr, curr_T_ref_init, ppmm
            )
        elif args.method == "filterreg":
            curr_T_ref = filterreg(
                C_ref, H_ref, N_curr, C_curr, H_curr, curr_T_ref_init, ppmm
            )
        elif args.method == "fpfh":
            curr_T_ref = fpfh(
                N_ref, C_ref, H_ref, N_curr, C_curr, H_curr, curr_T_ref_init, ppmm
            )
        else:
            raise ValueError("Invalid tracking method %s" % args.method)
        curr_T_ref_init = curr_T_ref
        est_transforms.append(np.linalg.inv(curr_T_ref))
    save_path = os.path.join(parent_dir, "%s_transforms.npy" % (args.method))
    np.save(save_path, np.array(est_transforms))
    print(
        "Object pose tracked with %s method for data in %s" % (args.method, parent_dir)
    )


if __name__ == "__main__":
    track()
