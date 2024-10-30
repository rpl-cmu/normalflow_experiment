#!/bin/bash

# This script runs the tracking algorithms on the normalflow dataset.
# It will run the specified method on gsmini_tracking and digit_tracking.

# Usage function to display help
usage() {
    echo "Usage: $0 [-d dataset_dir] [-m {nf|icp|filterreg|fpfh}]"
    exit 1
}

# Parse command-line arguments
while getopts ":d:m:" opt; do
    case ${opt} in
    d)
        dataset_dir=$OPTARG
        ;;
    m)
        case $OPTARG in
        nf | icp | filterreg | fpfh)
            method=$OPTARG
            ;;
        *)
            echo "Invalid value for -m. Allowed values are: nf, icp, filterreg, fpfh"
            usage
            ;;
        esac
        ;;
    \?)
        usage
        ;;
    esac
done
shift $((OPTIND - 1))

# Get the configuration directories
script_dir=$(dirname "$(realpath "$0")")
gsmini_config_dir=$(realpath "${script_dir}/../configs/gsmini.yaml")
digit_config_dir=$(realpath "${script_dir}/../configs/digit.yaml")

# Track for the gsmini_tracking dataset
track -p "${dataset_dir}/gsmini_tracking/avocado0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/avocado1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/avocado2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/avocado3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/avocado4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/avocado5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/avocado6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/ball0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/ball1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/ball2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/ball3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/ball4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/ball5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/ball6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/baseball0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/baseball1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/baseball2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/baseball3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/baseball4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/baseball5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/baseball6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/bead0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/bead1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/bead2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/bead3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/bead4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/bead5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/bead6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/can0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/can1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/can2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/can3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/can4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/can5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/can6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/corner0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/corner1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/corner2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/corner3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/corner4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/corner5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/corner6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/cylinder0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/cylinder1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/cylinder2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/cylinder3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/cylinder4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/cylinder5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/cylinder6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/hammer0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/hammer1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/hammer2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/hammer3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/hammer4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/hammer5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/hammer6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/key0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/key1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/key2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/key3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/key4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/key5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/key6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/seed0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/seed1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/seed2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/seed3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/seed4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/seed5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/seed6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/table0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/table1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/table2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/table3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/table4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/table5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/table6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/wrench0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/wrench1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/wrench2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/wrench3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/wrench4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/wrench5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/gsmini_tracking/wrench6" -c "${gsmini_config_dir}" -m "${method}"

# Track for the digit_tracking dataset
track -p "${dataset_dir}/digit_tracking/seed0" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/seed1" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/seed2" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/seed3" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/seed4" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/seed5" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/seed6" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/wrench0" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/wrench1" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/wrench2" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/wrench3" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/wrench4" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/wrench5" -c "${digit_config_dir}" -m "${method}"
track -p "${dataset_dir}/digit_tracking/wrench6" -c "${digit_config_dir}" -m "${method}"