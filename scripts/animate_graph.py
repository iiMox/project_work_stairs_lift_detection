import os
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
from tqdm import tqdm
from moviepy.editor import VideoFileClip, concatenate_videoclips
import argparse

def animateGraph(filepath, xLabel, yLabel, num):

    # Create Folder To Store The Video Segments
    os.mkdir(f"{filepath}\participant_videos")
    os.mkdir(f"{filepath}\participant_videos\{num}")
    os.mkdir(f"{filepath}\participant_videos\{num}\\video_segments")

    # Load CSV File
    df = pd.read_csv(f"{filepath}\participant {num}.csv")

    # Get Total Number of Readings
    totalReadings = len(df.index)

    # Group data by timestamp and calculate frame rates
    frames_list = df.groupby(np.floor(df[xLabel]).astype(int)).size().values
    limit = 1
    current_frame = 0

    # Init Progress Bar For Terminal Visualization
    progress_bar = tqdm(total=len(frames_list))

    # List to store individual video clips
    video_clips = []

    x = df[xLabel].values
    y = df[yLabel].values

    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title='Movie Test', artist='Matplotlib', comment='a red circle following a blue sine wave')

    for j in range(len(frames_list)):
        progress_bar.update(1)
        writer = FFMpegWriter(fps=frames_list[j], metadata=metadata)
        fig, ax = plt.subplots(figsize=(10, 5))
        with writer.saving(fig, f"{filepath}\participant_videos\{num}\\video_segments\{yLabel.lower()}_{xLabel.lower()}_chart_{j}.mp4", 100):
            plt.grid(True, linestyle='--', color='gray', linewidth=0.5)
            line, = ax.plot(x, y, color='black')
            circle, = ax.plot([], [], "ro", markersize=2)
            ax.set_title(f'{yLabel} vs {xLabel} Chart')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_xlim(x[0], x[1000])

            for i in range(0 if j == 0 else np.sum(frames_list[:j]), np.sum(frames_list[:j+1])):
                if i > 900 and i < totalReadings - 100:
                    ax.set_xlim(x[i - 900], x[i + 100])
                if i > totalReadings - 100:
                    ax.set_xlim(x[totalReadings - 999], x[totalReadings - 1])
                    
                line.set_data([x[:i], y[:i]])
                circle.set_data([x[i]], [y[i]])

                if limit > frames_list[current_frame]:
                    limit = 1
                    current_frame += 1
                else:
                    limit += 1
                writer.grab_frame()
        video_clip = VideoFileClip(f"{filepath}\participant_videos\{num}\\video_segments\{yLabel.lower()}_{xLabel.lower()}_chart_{j}.mp4")
        video_clips.append(video_clip)

    # Close Progress Bar
    progress_bar.close()  
        
    final_video = concatenate_videoclips(video_clips) # Concatenate all video clips into one final video

    final_video.write_videofile(f"{filepath}\participant_videos\{num}\\final.mp4", codec="libx264") # Save the final video

    print(f"Video was successfully saved '{filepath}\participant_videos\{num}\\final.mp4")

    shutil.rmtree("{filepath}\participant_videos\{num}\\video_segments")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Graph Animation Video Generator',
                    description='Generate An Animated Graph for The Participant Collected Data',
                    epilog='Text at the bottom of help')
    parser.add_argument('filepath')
    parser.add_argument('-x', '--xLabel') 
    parser.add_argument('-y', '--yLabel')
    parser.add_argument('-np', '--numberParticipant')

    args = parser.parse_args()
    animateGraph(args.filepath, args.xLabel, args.yLabel, args.numberParticipant)














