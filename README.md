# NormalFlow Experiments

This repository houses the baseline implementation and scripts to run the main experiment presented in our paper *NormalFlow: Fast, Robust, and Accurate Contact-based Object 6DoF Pose Tracking with Vision-based Tactile Sensors* ([Paper Link](TODO: Link)). It compares the tracking performance of NormalFlow and baseline algorithms on our dataset. If you use this package, please cite our paper:

[TODO: Citation block]

Before starting, please download our object tracking dataset ([Dataset Link](TODO: link)) and install our NormalFlow package ([NormalFlow Package Link](TODO: link)).


## Support System
* Tested on Ubuntu 22.04
* Python >= 3.9
* Install the [gs_sdk](TODO: link)
* Install the [normalflow](TODO: link)

## Installation
Clone and install normalflow_experiment from source:
```bash
git clone [TODO: link]
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

## (Optional) Visualize Tracking Results
We also provide tools to visualize tracking results. After running the `track` command above, you can visualize the tracking outcome of a specific method on a particular trial within the dataset by running:
```bash
viz_track [-p TRIAL_DIR ] [-m {nf|filterreg|icp|fpfh}]
```
This will save a tracking video named `{method}_tracking.avi` in the specified `TRIAL_DIR`.



