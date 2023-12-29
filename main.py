import sys
import math
import random
import os

import shutil
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import whisper_timestamped as whisper

sys.path.insert(0, "/Users/abnerstone/PythonTest/text-to-speech")
import text_to_speech
import create_video

def main():
    if os.path.exists("./Output"):     
        try:
            shutil.rmtree('./Output')
        except Exception as e:
            print(f'Failed to delete directory: {e}')
        os.makedirs("./Output")
    else:
        os.makedirs("./Output")


    sample_path = "./sample-videos/Subway_Surfers.mp4"

    # Specify the arguments
    voice = "en_us_007"
    file = "story.txt"
    session = "305428fc5ca1be825070e8b29a3e9320"
    output = "./Output/output.mp3"

    # TODO: Account for the introduction of the video in the tts
    # Call the start function with the specified arguments
    print("Generating text to speech audio")
    text_to_speech.start(
        voice=voice,
        file=file,
        session=session,
        name=output
    )

    sound_duration = get_sound_duration(output)
    video_parts = split_video(sound_duration)
    print(f"Sound Duration: {sound_duration}")
    print(f"Video Parts: {video_parts}")
    duration_part = math.ceil(sound_duration/video_parts)
    print(f"Sound Duration Per Each Part: {duration_part}")

    sample_duration = get_sample_duration(sample_path)
    print(f"Sample Duration: {sample_duration}")
    starting_point = random.randint(0, (sample_duration - (duration_part + 1)))
    print(starting_point)

    transcription = get_transcript("./Output/output.mp3")
    create_video.create(
        outputFile="./Output/output.mp4", 
        audioFile="./Output/output.mp3", 
        samplePath=sample_path,
        splitPath="./Split",
        soundDuration=sound_duration,
        width=1080, 
        height=1920, 
        startingPoint=starting_point,
        durationPart=duration_part, 
        transcript=transcription,
    ) #TODO: Edit this library


def split_video(sound_duration):
    max_duration = 60
    video_parts = int((sound_duration + max_duration - 1) / max_duration)
    return video_parts

def get_sound_duration(audio_file):
    try:
        audio = MP3(audio_file)
        sound_duration = audio.info.length
        return int(sound_duration)
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_sample_duration(sample_file):
    try:
        audio = MP4(sample_file)
        sample_duration = audio.info.length
        return int(sample_duration)
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def get_transcript(audio_file):
    print("Starting transcription of audio file")
    model = whisper.load_model("base")
    audio = audio_file
    transcript = whisper.transcribe(model, audio)
    with open("./Output/transcript.txt", "w") as file:
        file.write(transcript["text"])
    return transcript


if __name__ == "__main__":
    main()