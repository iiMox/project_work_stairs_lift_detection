import pandas as pd
from datetime import datetime, timedelta
import argparse
from tqdm import tqdm
import os

def process_timestamp(str):
    if "." not in str:
        return str +".0"
    
    return str

def compare_timestamps(row_a, row_b, previous_row):
    timestamp_reading = datetime.strptime(process_timestamp(str(timedelta(seconds=row_a["Timestamp"]))), "%H:%M:%S.%f").time()
    timestamp_label = datetime.strptime(row_b["Elapsedtime"], "%H:%M:%S.%f").time()
    if previous_row is None:
        previous_timestamp = datetime.strptime("00:00:00.0", "%H:%M:%S.%f").time()
    else:
        previous_timestamp = datetime.strptime(previous_row["Elapsedtime"], "%H:%M:%S.%f").time()
    return timestamp_reading > previous_timestamp and timestamp_reading <= timestamp_label

def label_data(readingsFile, labelsFile, outputFolder, participant):

    df_readings = pd.read_csv(readingsFile)
    df_labels = pd.read_csv(labelsFile)

    matched_rows_labels = []
    matched_rows_start = []
    matched_rows_end = []

    previous_row = None

    # Init Progress Bar For Terminal Visualization
    progress_bar = tqdm(total=len(df_labels))

    for index, row_label in df_labels.iterrows():
        matched_rows_readings = df_readings[df_readings.apply(compare_timestamps, axis=1, args=(row_label,previous_row), )]

        matched_label = row_label["Comment"]
        #matched_start = row_label["Start"]
        #matched_end = row_label["End"]

        for _ in range(len(matched_rows_readings)):
            matched_rows_labels.append(matched_label)
            #matched_rows_start.append(matched_start)
            #matched_rows_end.append(matched_end)

        previous_row = row_label.copy()

        progress_bar.update(1)

    if len(matched_rows_labels) != len(df_readings):
        diff = len(df_readings) - len(matched_rows_labels) # Calculate the difference in length
        df_readings = df_readings[:-diff] # Remove the extra rows from the DataFrame

    progress_bar.close() 

    df_readings["Label"] = matched_rows_labels
    #df_readings["Start"] = matched_rows_start
    #df_readings["End"] = matched_rows_end
    df_readings.to_csv(f"{outputFolder}/participant {participant} - labeled.csv", index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Label Matcher',
                    description='Append Correct Label To Each Reading Row',
                    epilog='Text at the bottom of help')
    parser.add_argument('filepath')
    parser.add_argument('-l', '--labelsFile')
    parser.add_argument('-o', '--outputFolder')
    parser.add_argument('-np', '--numberParticipant')

    args = parser.parse_args()
    label_data(args.filepath, args.labelsFile, args.outputFolder, args.numberParticipant)
