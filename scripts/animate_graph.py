import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from tqdm import tqdm
import argparse

def animateGraph(filename, xLabel, yLabel):
    # Load CSV File
    df = pd.read_csv(filename)

    # Get Total Number of Readings
    totalReadings = len(df.index)

    frames_list = df.groupby(np.floor(df['Timestamp']).astype(int)).size().values
    current_rate = 0
    limit = 1

    # Init Progress Bar For Terminal Visualization
    progress_bar = tqdm(total=totalReadings)

    # Init Output Video Params
    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title='Movie Test', artist='Matplotlib',
                comment='a red circle following a blue sine wave')
    writer = FFMpegWriter(fps=frames_list[current_rate], metadata=metadata)

    x = df[xLabel].values
    y = df[yLabel].values

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.grid(True, linestyle='--', color='gray', linewidth=0.5)
    line, = ax.plot(x, y, color='black')
    circle, = ax.plot([], [], "ro", markersize=2)
    ax.set_title(f'{yLabel} vs {xLabel} Chart')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Init Graph Visible Area
    ax.set_xlim(x[0], x[1000])  

    with writer.saving(fig, f"{yLabel.lower()}_{xLabel.lower()}_chart.mp4", 100):
        for i in range(totalReadings):
            progress_bar.update(1)
            line.set_data(x[:i], y[:i])
            circle.set_data([x[i]], [y[i]])
            if i > 900 and i < totalReadings - 100:
                ax.set_xlim(x[i - 900], x[i + 100])
            
            if limit > frames_list[current_rate]:
                print(f'\n {i, limit, current_rate, frames_list[current_rate], x[i], writer.fps}')
                limit = 1
                current_rate += 1
                """ writer.finish()
                writer = manimation.FFMpegWriter(fps=frames_list[current_rate], metadata=metadata)
                writer.setup(fig, f"{yLabel.lower()}_{xLabel.lower()}_chart.mp4", 100) """

            limit += 1
            writer.grab_frame()

    progress_bar.close()
    writer.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Graph Animation Video Generator',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument('filename')
    parser.add_argument('-x', '--xLabel') 
    parser.add_argument('-y', '--yLabel')

    args = parser.parse_args()
    animateGraph(args.filename, args.xLabel, args.yLabel)














