import moviepy.editor as mpy
import os


def images_to_video(folder, audio_file=None, image_duration=0.4, batch_size=50):
    audio = None
    audio_duration = 0

    # Load audio if provided
    if audio_file:
        audio = mpy.AudioFileClip(audio_file)
        audio_duration = audio.duration
        print("Audio duration:", audio_duration)

    # Get sorted filenames
    filenames = [f for f in os.listdir(folder) if f.endswith((".jpg", ".jpeg"))]
    sorted_filenames = sorted(filenames, key=lambda x: int(x.split('.')[0]))

    final_clips = []
    batch_clips = []

    for i, filename in enumerate(sorted_filenames):
        print(filename)
        if filename.endswith((".jpg", ".jpeg")):
            clip = mpy.ImageClip(os.path.join(folder, filename)).set_duration(image_duration)
            batch_clips.append(clip)

            # Process in batches
            if (i + 1) % batch_size == 0 or (i + 1) == len(sorted_filenames):
                batch_movie = mpy.concatenate_videoclips(batch_clips, method="compose")
                final_clips.append(batch_movie)
                batch_clips = []

            # Check audio duration limit
            if audio_duration < len(final_clips) * image_duration:
                break

    # Concatenate final clips
    movie = mpy.concatenate_videoclips(final_clips, method="compose")

    # Add audio if available
    if audio_file:
        movie = movie.set_audio(audio)

    return movie

def create_new_video(data_dir="/var/data/"):
    # Load all images from data_dir
    folder = os.path.join(data_dir, "frames")
    movie = images_to_video(folder, os.path.join(data_dir, "quiz.mp3"))
    movie.write_videofile(os.path.join(data_dir, "quiz.mp4"), fps=24, codec="libx264", audio_codec="aac")
