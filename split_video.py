
import os
import sys
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

def split(video_path, segment_length, output):
    clip = VideoFileClip(video_path)
    duration = clip.duration

    start_time = 0
    end_time = segment_length
    i = 1

    # Extract the video_path without extension
    basename = os.path.basename(video_path).split('.')[0]

    # Extract directory path
    dir_path = os.path.dirname(video_path)

    output_path = os.path.join(dir_path, output)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    while start_time < duration:
        if start_time >= (segment_length - 0.5):
            start_time += 0.7
        output = os.path.join(output_path, f"{basename}_part{i}.mp4")
        ffmpeg_extract_subclip(video_path, start_time, end_time + 0.7, targetname=output)
        print(f"Start time: {start_time}")
        print(f"End time: {end_time}")
        start_time = end_time
        end_time += segment_length
        i += 1
    print(f'Video split into {i-1} parts.')

if __name__ == "__main__":
    video_path = sys.argv[1]  # first argument from command line
    segment_length = int(sys.argv[2])  # second argument from command line
    output = sys.argv[3]  # third argument from command line
    split(video_path, segment_length, output)