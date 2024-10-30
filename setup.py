from setuptools import setup, find_packages

setup(
    name="normalflow_experiments",
    version="0.1.0",
    description="The main experiments of the NormalFlow paper",
    author="Hung-Jui Huang",
    author_email="hungjuih@andrew.cmu.edu",
    packages=["baselines"],
    install_requires=[
        "open3d>=0.16.0",
        "probreg",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'track=track.track:track',
            "long_horizon_track=track.long_horizon_track:long_horizon_track",
            'viz_track=visualization.viz_track:viz_track',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
