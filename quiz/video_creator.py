import moviepy.editor as mpy
import os


def images_to_video(folder, audio_file=None, image_duration=0.4, batch_size=100):
    audio = None
    audio_duration = 0

    # Load audio if provided
    if audio_file:
        audio = mpy.AudioFileClip(audio_file)
        audio_duration = audio.duration

    # Get sorted list of image filenames
    filenames = [f for f in os.listdir(folder) if f.endswith((".jpg", ".jpeg"))]
    sorted_filenames = sorted(filenames, key=lambda x: int(x.split('.')[0]))

    intermediate_files = []
    batch_clips = []

    for i, filename in enumerate(sorted_filenames):
        print(filename)
        clip = mpy.ImageClip(os.path.join(folder, filename)).set_duration(image_duration)
        batch_clips.append(clip)

        # Process in batches and save to disk
        if (i + 1) % batch_size == 0 or i == len(sorted_filenames) - 1:
            intermediate_clip = mpy.concatenate_videoclips(batch_clips, method="compose")
            intermediate_filename = f"intermediate_{len(intermediate_files)}.mp4"
            intermediate_clip.write_videofile(os.path.join(folder, intermediate_filename), codec="libx264")
            intermediate_files.append(os.path.join(folder, intermediate_filename))
            batch_clips = []  # Reset batch clips

            # Break if audio is shorter than the processed video duration
            if audio_duration and audio_duration < sum([mpy.VideoFileClip(f).duration for f in intermediate_files]):
                break

    print("Number of frames:", len(sorted_filenames))
    print("Number of intermediate files:", len(intermediate_files))

    # Concatenate video files from disk
    final_clips = [mpy.VideoFileClip(f) for f in intermediate_files]
    final_clip = mpy.concatenate_videoclips(final_clips, method="compose")

    # Set audio if available
    if audio_file:
        final_clip = final_clip.set_audio(audio)

    # Optional: Delete intermediate files
    for f in intermediate_files:
        os.remove(f)

    return final_clip

def create_new_video(data_dir="/var/data/"):
    # Load all images from data_dir
    folder = os.path.join(data_dir, "frames")
    movie = images_to_video(folder, os.path.join(data_dir, "quiz.mp3"))
    movie.write_videofile(os.path.join(data_dir, "quiz.mp4"), fps=24, codec="libx264", audio_codec="aac")
