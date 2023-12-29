from moviepy.editor import *
from moviepy import *
import split_video

def create(outputFile, audioFile, samplePath, splitPath, soundDuration, width, height, startingPoint, durationPart, transcript):
    audio = AudioFileClip(audioFile).subclip(0, soundDuration)
    audio = CompositeAudioClip([audio])

    clip = VideoFileClip(samplePath).subclip(0, soundDuration)
    (w, h) = clip.size
    clip = clip.crop(width=width, height=height, x_center=w/2, y_center=h/2) # TODO: Make sure alignment is correct

    clip.audio = audio

    # TODO: Add subtitles
    subtitles=[]
    subtitles.append(clip)
    #print(TextClip.list('font'))
    for segment in transcript["segments"]:
        for word in segment["words"]:
            text = word["text"]
            start = word["start"]
            end = word["end"]
            word_duration = (end - start)
            txt_clip = TextClip(txt=text, fontsize=80, font="MontserratBlack", stroke_width=3, stroke_color="black", color="white", method="caption")
            txt_clip = txt_clip.set_start(start).set_duration(word_duration).set_position(("center", "center"))
            subtitles.append(txt_clip)
    clip = CompositeVideoClip(subtitles)
    clip.write_videofile(outputFile)

    clip.close()

    split_video.split(
        video_path=outputFile,
        segment_length=durationPart,
        output=splitPath
    )

if __name__ == "__main__":
    create()