# Stairs vs Lift Detection

This project consist of a dataset collected from an activity recognition experiment using Bangle.js 2 Smart Watch. This collected data was used to train a machine learning model in order to detect stairs and lift usage.

## Table of Contents

-   Installation
-   File Structure
-   Usage
-   Scripts
-   Contributing
-   License

## Installation

You just need to clone the repository to your local machine.

```bash
git clone https://github.com/iiMox/project_work_stairs_lift_detection.git
```

To use the scripts, run the following commands to install the required packages.

-   "ML scripts" folder

    ```bash
    pip install -r "ML scripts/requirements.txt"
    ```

-   "script" folder

    ```bash
    pip install -r "scripts/requirements.txt"
    ```

## File Structure

```
project_work_stairs_lift_detection
├── assets
│
├── collected_data
│   ├── annotation_data                    # Annotated labels with timestamps.
│   │
│   ├── annotation_data_updated            # updated annotated labels with timestamps.
│   │
│   ├── collected_labeled_data_phase_01    # Label raw data.
│   │
│   ├── preprocessed                       # Preprocessed raw data with labels.
│   │
│   ├── preprocessed_imu                   # Preprocessed raw data with labels (Only IMU data).
│   │
│   ├── raw_data                           # Collected raw data from the watch sensors.
│   │
│   └── sanity_check                       # Data collected before experiment to check watch functionality.
│
│
├── ml_scripts                             # Scripts for data preprocessing and ML model training.
│   ├── data_preprocessing.py
│   ├── helper_functions.py
│   ├── random_forest.py
│   └── requirements.txt
│
│
├── scripts                                # Scripts for data visual representation
│   ├── animate_graph.py
│   ├── label_matcher.py
│   ├── time_calculator.py
│   ├── video_generator.py
│   └── requirements.txt
│
├── watch_apps                             # Code implemented on the watch to gather the data.
│
├── overleaf_paper                         # Files related to the published paper.
│
└── README.md
```

## Usage

## Scripts

## Contributing

You are welcome to use the dataset for further research projects or training other machine learning models.

## License

[CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/deed.en)
