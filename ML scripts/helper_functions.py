import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
from collections import Counter
import glob
import shutil



def read_file(num, dataDir):
    dataset = pd.read_csv(dataDir+'Collected Updated Labeled Data - Phase 01/participant '+ num +'.csv')
    if 'Time' in dataset.columns:
        dataset.drop('Time', axis=1, inplace=True)
    if 'Start' in dataset.columns:
        dataset.drop('Start', axis=1, inplace=True)
    if 'End' in dataset.columns:
        dataset.drop('End', axis=1, inplace=True)
    dataset['Label'] = dataset['Label'].apply(
        lambda x: x.lower() if x != 'Null' else x
    )
        
    strings_to_replace = ['null', ' null', 'Null ', 'null ']
    replacement_string = 'Null'
    dataset = dataset.replace(strings_to_replace, replacement_string)
    return dataset

def calculate_slope(data):
    data = data.replace(np.inf, np.nan).replace(-np.inf, np.nan).dropna()
    x = np.arange(len(data))
    if len(x)>1:
        slope = np.polyfit(x, data, 1)[0]
    else: 
        slope = 0
    return slope

def summarize_interval(group, interval):
    start_time = group['Timestamp'].min()
    end_time = group['Timestamp'].max()
    elapsed_time = end_time-start_time
    label_mode = group['Label'].mode().iloc[0] #calculating mode value to assign label
    labeldict = Counter(group['Label']) #getting the count of each value in label
    label_percentage = (labeldict[label_mode] / len(group['Label']) ) * 100 #calculating the percentage of values that are same as mode
    if ((label_percentage > 79) and (elapsed_time > interval - 0.2)): #calculating the values only if the label is atleast 80% else return and if it's more than 3 / 7 seconds and also if the interval is atleast 3.8 / 7.8 seconds long
        summary = {
            'avg_accX': group['X'].mean(),
            'min_accX': group['X'].min(),
            'max_accX': group['X'].max(),
            'var_accX': group['X'].var(),
            'std_accX': np.std(group['X']),
            'avg_accY': group['Y'].mean(),
            'min_accY': group['Y'].min(),
            'max_accY': group['Y'].max(),
            'var_accY': group['Y'].var(),
            'std_accY': np.std(group['Y']),
            'avg_accZ': group['Z'].mean(),
            'min_accZ': group['Z'].min(),
            'max_accZ': group['Z'].max(),
            'var_accZ': group['Z'].var(),
            'std_accZ': np.std(group['Z']),
            'avg_magnitude': group['Magnitude'].mean(),
            'min_magnitude': group['Magnitude'].min(),
            'max_magnitude': group['Magnitude'].max(),
            'var_magnitude': group['Magnitude'].var(),
            'std_magnitude': np.std(group['Magnitude']),
            'var_pressure': group['Pressure'].var(),
            'range_pressure': (group['Pressure'].max() - group['Pressure'].min()),
            'std_pressure': np.std(group['Pressure']),
            'slope_pressure': calculate_slope(group['Pressure']),
            'kurtosis_pressure': kurtosis(group['Pressure']),
            'skew_pressure': skew(group['Pressure']),
            'Label': label_mode,  # Most frequent label in the interval
        }
        return pd.Series(summary)
    
def preprocessing(num, dataset, interval, dataDir):
    result_df = dataset.groupby(dataset['Timestamp'] // interval).apply(lambda x: summarize_interval(x, interval)) # Applying the summarize_interval function to each interval
    
    result_df = result_df.reset_index(drop=True) # Reset index to flatten the DataFrame and remove the multi-index

    result_df = result_df.dropna(how='any') # Remove rows with any NaN values
    
    result_df.to_csv(dataDir+'preprocessed/preprocessed_data'+str(num)+'.csv', index=False) #save the preprocessed data to a new CSV file

def merge_files(test_participant, dataDir):
    csv_files = glob.glob(dataDir+'preprocessed/*.csv')

    dfs = []

    filtered_files = [f for f in csv_files if dataDir+'preprocessed/preprocessed_data'+str(test_participant)+'.csv' not in f]
    
    for file in filtered_files: # Loop through each CSV file and append its DataFrame to the list
        df = pd.read_csv(file)
        dfs.append(df)
    
    merged_df = pd.concat(dfs, ignore_index=True) # Concatenate all DataFrames in the list along rows (axis=0)

    shutil.copy2(dataDir+'preprocessed/preprocessed_data'+str(test_participant)+'.csv', dataDir+'preprocessed/'+str(test_participant)+'/preprocessed_testdata.csv')
    merged_df.to_csv(dataDir+'preprocessed/'+str(test_participant)+'/preprocessed_traindata.csv', index=False)