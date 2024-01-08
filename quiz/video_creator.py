import moviepy.editor as mpy
import os

def images_to_video(folder, audio_file=None, image_duration = 0.4):
    clips = []

    audio = None
    audio_duration = 0

    # If audio is provided and its duration is shorter than the total image duration, cut excess frames
    if audio_file:
        audio = mpy.AudioFileClip(audio_file)
        audio_duration = audio.duration
        print("Audio duration:", audio_duration)

    filenames = [filename for filename in os.listdir(folder) if filename.endswith(".jpg") or filename.endswith(".jpeg")]
    sorted_filenames = sorted(filenames, key=lambda x: int(x.split('.')[0]))

    for filename in sorted_filenames:
        print(filename)
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            clip = mpy.ImageClip(os.path.join(folder, filename)).set_duration(image_duration)
            clips.append(clip)
            if audio_duration < len(clips) * image_duration:
                break

    print("Number of frames:", len(clips))
    movie = mpy.concatenate_videoclips(clips, method="compose")

    if audio_file:
        movie = movie.set_audio(audio)

    return movie

def create_new_video(data_dir="/var/data/"):
    # Load all images from data_dir
    folder = os.path.join(data_dir, "frames")
    movie = images_to_video(folder, os.path.join(data_dir, "quiz.mp3"))
    movie.write_videofile(os.path.join(data_dir, "quiz.mp4"), fps=24, codec="libx264", audio_codec="aac")
