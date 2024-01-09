import os
import cv2
from moviepy.editor import VideoFileClip, AudioFileClip

def images_to_video(folder, image_duration=0.4, frame_rate=24, video_codec=cv2.VideoWriter_fourcc(*'MP4V')):
    frame_folder = os.path.join(folder, "frames")
    # Get sorted list of image filenames
    filenames = [f for f in os.listdir(frame_folder) if f.endswith((".jpg", ".jpeg"))]
    sorted_filenames = sorted(filenames, key=lambda x: int(x.split('.')[0]))

    if not sorted_filenames:
        raise ValueError("No images found in the folder")

    # Read the first image to get the size
    first_image = cv2.imread(os.path.join(frame_folder, sorted_filenames[0]))
    height, width, layers = first_image.shape

    # Define the codec and create VideoWriter object
    out = cv2.VideoWriter(os.path.join(folder,"quiz_no_audio.mp4"), video_codec, frame_rate, (width, height))

    frame_count = int(frame_rate * image_duration)

    for filename in sorted_filenames:
        frame = cv2.imread(os.path.join(frame_folder, filename))

        # Check if image sizes are consistent
        if frame.shape[0] != height or frame.shape[1] != width:
            raise ValueError(f"Image size for {filename} does not match the first image size")

        # Write the frame multiple times to meet the desired duration per image
        for _ in range(frame_count):
            out.write(frame)

    out.release()

def create_new_video(data_dir="/var/data/"):
    # Load all images from data_dir
    images_to_video(data_dir)
    # Load the video file
    video_clip = VideoFileClip(os.path.join(data_dir, "quiz_no_audio.mp4"))
    # Load the audio file
    audio_clip = AudioFileClip(os.path.join(data_dir, "quiz.mp3"))
    final_clip = video_clip.set_audio(audio_clip)

    # Write the result to a file
    final_clip.write_videofile(os.path.join(data_dir, "quiz.mp4"), codec='libx264', audio_codec='aac')
