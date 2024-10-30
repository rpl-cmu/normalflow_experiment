#!/bin/bash

# This script runs the specified tracking algorithms on the dataset.

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

# Track for the dataset
track -p "${dataset_dir}/avocado0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/avocado1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/avocado2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/avocado3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/avocado4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/avocado5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/avocado6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/ball0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/ball1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/ball2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/ball3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/ball4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/ball5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/ball6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/baseball0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/baseball1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/baseball2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/baseball3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/baseball4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/baseball5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/baseball6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/bead0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/bead1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/bead2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/bead3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/bead4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/bead5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/bead6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/can0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/can1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/can2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/can3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/can4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/can5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/can6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/corner0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/corner1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/corner2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/corner3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/corner4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/corner5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/corner6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/cylinder0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/cylinder1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/cylinder2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/cylinder3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/cylinder4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/cylinder5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/cylinder6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/hammer0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/hammer1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/hammer2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/hammer3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/hammer4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/hammer5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/hammer6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/key0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/key1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/key2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/key3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/key4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/key5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/key6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/seed0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/seed1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/seed2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/seed3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/seed4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/seed5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/seed6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/table0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/table1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/table2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/table3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/table4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/table5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/table6" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/wrench0" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/wrench1" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/wrench2" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/wrench3" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/wrench4" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/wrench5" -c "${gsmini_config_dir}" -m "${method}"
track -p "${dataset_dir}/wrench6" -c "${gsmini_config_dir}" -m "${method}"