#!/bin/bash

# This script runs the long_horizon tracking algorithm with NormalFlow
# on the normalflow dataset. It will run on gsmini_long_tracking.

# Usage function to display help
usage() {
    echo "Usage: $0 [-d dataset_dir]"
    exit 1
}

# Parse command-line arguments
while getopts ":d:" opt; do
    case ${opt} in
    d)
        dataset_dir=$OPTARG
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

# Track for the gsmini_tracking dataset
long_horizon_track -p "${dataset_dir}/gsmini_long_tracking/bead0" -c "${gsmini_config_dir}"
long_horizon_track -p "${dataset_dir}/gsmini_long_tracking/table0" -c "${gsmini_config_dir}"
long_horizon_track -p "${dataset_dir}/gsmini_long_tracking/wrench0" -c "${gsmini_config_dir}"