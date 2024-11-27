# NormalFlow Experiments
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &nbsp;[<img src="assets/rpl.png" height=20px>](https://rpl.ri.cmu.edu/)

This repository contains the baseline implementation and scripts to run the main experiment presented in our paper [*NormalFlow: Fast, Robust, and Accurate Contact-based Object 6DoF Pose Tracking with Vision-based Tactile Sensors*](https://ieeexplore.ieee.org/document/10766628). It compares the tracking performance of NormalFlow against baseline algorithms on our dataset. Please check our paper for more details.

Before starting, please download our [tactile-based object tracking dataset](https://huggingface.co/datasets/joehjhuang/TactileTracking), install our [NormalFlow package](https://github.com/rpl-cmu/normalflow), and install the [GelSight SDK](https://github.com/joehjhuang/gs_sdk).


## Support System
* Tested on Ubuntu 22.04
* Python >= 3.9

## Installation
Clone and install normalflow_experiment from source:
```bash
git clone git@github.com:rpl-cmu/normalflow_experiment.git
cd normalflow_experiment
pip install -e .
```

## Run Experiments
In the instructions below, `DATASET_DIR` denotes the path to the downloaded and extracted dataset. Run the following commands to track objects in all trials of the dataset using all four methods:
```bash
bash script/track_dataset.sh -d DATASET_DIR -m nf
bash script/track_dataset.sh -d DATASET_DIR -m filterreg
bash script/track_dataset.sh -d DATASET_DIR -m icp
bash script/track_dataset.sh -d DATASET_DIR -m fpfh
```

Then, generate tracking performance comparison figures for all 12 objects in the dataset with:
```bash
viz_track_result -p DATASET_DIR
```
The comparison figures will be saved in `DATASET_DIR` and should reproduce Fig. 5 from our NormalFlow paper.

## Visualize Tracking Results
We also provide tools to visualize tracking results. After running the `track` command above, you can visualize the tracking outcome of a specific method on a particular trial within the dataset by running:
```bash
viz_track [-p TRIAL_DIR ] [-m {nf|filterreg|icp|fpfh}]
```
This will save a tracking video named `{method}_tracking.avi` in the specified `TRIAL_DIR`.

## Cite Us
If you find this package useful, please consider citing our paper:
```
@ARTICLE{huang2024normalflow,
    author={Huang, Hung-Jui and Kaess, Michael and Yuan, Wenzhen},
    journal={IEEE Robotics and Automation Letters}, 
    title={NormalFlow: Fast, Robust, and Accurate Contact-based Object 6DoF Pose Tracking with Vision-based Tactile Sensors}, 
    year={2024},
    volume={},
    number={},
    pages={1-8},
    keywords={Force and Tactile Sensing, 6DoF Object Tracking, Surface Reconstruction, Perception for Grasping and Manipulation},
    doi={10.1109/LRA.2024.3505815}}
```



