# Stairs vs Lift Detection

This project consist of a dataset collected from an activity recognition experiment using Bangle.js 2 Smart Watch. This collected data was used to train a machine learning model in order to detect stairs and lift usage.

## Table of Contents

-   Installation
-   File Structure
-   Scripts
-   Contributing
-   License

## Installation

You just need to clone the repository to your local machine.

```bash
git clone https://github.com/iiMox/project_work_stairs_lift_detection.git
```

To use the scripts, run the following commands to install the required packages.

-   `"./ml_scripts"`:

    ```bash
    pip install -r "ML scripts/requirements.txt"
    ```

-   `"./scripts"`:

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

## Scripts

-   `./ml_scripts`:

    -   `data_preprocessing.py`: calculate the different features using the collected labeled sensor data.

        ```bash
        python data_preprocessing.py "C:\Desktop\project_work_stairs_lift_detection\collected_data\" -i 4 -imu
        ```

        -   `-i` : specify the interval value in seconds.

        -   `-imu`: if specified, only imu data will be used. else all data will be used.

        <br />

    -   `random_forest.py`: calculate the different features using the collected labeled sensor data.

        ```bash
        python random_forest.py "C:\Desktop\project_work_stairs_lift_detection\collected_data\" -tp 9
        ```

        -   `-tp` : specify the test participant before running the model.

    <br />

-   `./scripts`:

    -   `animate_graph.py`: generate a video of the reading change for the specified participant.

        ```bash
        python animate_graph.py "C:\Desktop\project_work_stairs_lift_detection\collected_data\collected_labeled_data_phase_01\" -x Timestamp -y Pressure -np 05
        ```

        -   `-x`: column to be considered for x axis.
        -   `-y`: column to be considered for y axis.
        -   `-np`: participant number for the loading the correct data file.

        <br />

    -   `label_matcher.py`: implement the correct label to different collected reading rows (null, stairs, lift classes).

        ```bash
        python label_matcher.py "C:\Desktop\project_work_stairs_lift_detection\collected_data\raw_data\datalogs_participant1.csv" -l "C:\Desktop\project_work_stairs_lift_detection\collected_data\annotation_data-updated\data_participant1.csv" -o "C:\Desktop\project_work_stairs_lift_detection\collected_data\" -np 01
        ```

        -   `-l`: path to labels file.
        -   `-o`: output folder path.
        -   `-np`: participant number for the loading the correct data file.

        <br />

    -   `plot.py`: plot accelerometer and pressure values in same graph with timestamps.

        ```bash
        python plot.py "C:\Desktop\project_work_stairs_lift_detection\collected_data\raw_data\datalogs_participant1.csv\"
        ```

        <br />

    -   `time_calculator.py`: calculate time amount for each class of specific participant file.

        ```bash
        python time_calculator.py "C:\Desktop\project_work_stairs_lift_detection\collected_data\collected_labeled_data_phase_01\participant 01.csv\"
        ```

## Contributing

You are welcome to use the dataset for further research projects or training other machine learning models.

## License
This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
