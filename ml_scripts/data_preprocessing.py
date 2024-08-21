from helper_functions import merge_files, preprocessing, read_file
import argparse
from tqdm import tqdm
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Preprocess Data',
                    description='Data Preprocessing for Random Forest',
                    epilog='Text at the bottom of help')
    parser.add_argument('filepath') # "C:/...../Collected Data/"
    parser.add_argument('-i', '--interval', type=float, required=True, help="Specify The Interval For Preprocessed Data")
    parser.add_argument('-imu', '--imuOnly', action='store_true', help="Only Include IMU Data")

    args = parser.parse_args()
    progress_bar = tqdm(total=20)

    if not os.path.exists(f"{args.filepath}/preprocessed"):
        os.makedirs(f"{args.filepath}/preprocessed")

    for i in range (1, 21):
            preprocessing(i, read_file(f"0{i}" if i < 10 else str(i), args.filepath, args.imuOnly), float(args.interval), args.filepath, args.imuOnly)

    for i in range (1, 21):
        if not os.path.exists(f"{args.filepath}/preprocessed/{i}"):
            os.makedirs(f"{args.filepath}/preprocessed/{i}")
        merge_files(i, args.filepath)
        progress_bar.update(1)

    progress_bar.close()

