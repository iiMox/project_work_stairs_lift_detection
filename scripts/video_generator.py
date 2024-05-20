from animate_graph import animateGraph
from moviepy.editor import VideoFileClip, CompositeVideoClip
from moviepy.video.VideoClip import ColorClip
import argparse

def createFootage(video, mVideo, pVideo):

    footage = VideoFileClip(video)
    magnitude_chart = VideoFileClip(mVideo)
    pressure_chart = VideoFileClip(pVideo)

    if None in [footage, magnitude_chart, pressure_chart]:
        print("Error: One or more video clips failed to load.")
    else:
        # Resize clips to have the same height
        footage = footage.resize((720, 960))
        magnitude_chart = magnitude_chart.resize(width=720, height=480)
        pressure_chart = pressure_chart.resize(width=720, height=480)
        white_background = ColorClip(size=(1920, 1080), color=(255, 255, 255), duration=footage.duration)

        final_clip = CompositeVideoClip([white_background, footage.set_position((120, "center")), magnitude_chart.set_position((960, 0)), pressure_chart.set_position((960, 580))], size=(1920,1080))

        # Write the final video
        final_clip.write_videofile("combined_video.mp4")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Graph Animation Video Generator', description='What the program does', epilog='Text at the bottom of help')
    parser.add_argument('-f', "--footage")
    parser.add_argument('-r', '--readings_file') 

    args = parser.parse_args()
    """ animateGraph(args.readings_file, "Timestamp", "Magnitude")
    animateGraph(args.readings_file, "Timestamp", "Pressure") """

    createFootage(args.footage, "magnitude_timestamp.mp4", "pressure_timestamp.mp4")