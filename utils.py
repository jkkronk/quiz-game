from moviepy.editor import VideoFileClip
import json
from create_video import quiz, audio, video, street_view_collector
import asyncio

def create_new_video():
    path_coordinates = []
    while len(path_coordinates) == 0:
        num_points, city, path_coordinates = create_new_quiz()

    # Create the video
    images = street_view_collector.fetch_street_view_images(path_coordinates, "desktop")
    movie = video.images_to_video(images, "static/quiz.mp3", add_logo=False)
    movie.write_videofile(f"static/quiz.mp4", fps=24, codec="libx264", audio_codec="aac")

def create_new_quiz():
    # Create a new quiz
    city = quiz.random_destination()
    city_quiz = quiz.create_quiz(city)
    #city_quiz = QuizClues.open("static/quiz.json")
    city_quiz.save(city, f"static/quiz.json")

    # Create the audio
    host_voice = "echo"
    sound = asyncio.run(audio.quiz_2_speech_openai(city_quiz, host_voice))
    host = quiz.QuizHost("What city is our destination?...", f"... And the correct answer is... {city}")
    sound_intro = asyncio.run(audio.text_2_speech_openai(host.intro, host_voice))
    sound = sound_intro + sound
    sound.export("static/quiz.mp3", format="mp3")
    #sound = AudioSegment.from_mp3("static/quiz.mp3")

    # Create the video
    duration = sound.duration_seconds
    num_points = street_view_collector.duration_to_num_points(duration)

    path_coordinates = []
    for i in range(50):
        print(f"Attempt {i} to get a path with {num_points} points")
        # Try to get a path with the correct number of points
        path_coordinates = street_view_collector.get_path_coordinates(city, "", num_points)
        print(f"Got {len(path_coordinates)} points")
        if len(path_coordinates) == num_points:
            break

    return num_points, city, path_coordinates

def clear_daily_high_scores():
    from server import db, HighScore  # Import necessary modules
    try:
        # Reset daily scores for all users
        HighScore.query.update({HighScore.daily_score: 0})
        db.session.commit()
    except Exception as e:
        print("Error resetting daily high scores:", e)
        db.session.rollback()


# Function to calculate the score
def calculate_score(time_taken, video_file_path):
    with VideoFileClip(video_file_path) as video:
        video_duration = video.duration

    # Calculate the score as a percentage
    if time_taken > video_duration:
        return 0  # If the time taken is more than the video duration, return 0%
    else:
        return int(((video_duration - time_taken) / video_duration) * 100)

def get_answer(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data["city"]

def get_explanations(file_path):
    # Load the JSON data
    with open(file_path) as f:
        quiz_data = json.load(f)
    explanations = quiz_data.get('explanations', [])
    clues = quiz_data.get('clues', [])
    clues_and_explanations = []
    for idx, clue in enumerate(clues):
        clues_and_explanations.append("<b>" + clue + "</b>")
        clues_and_explanations.append("Explanation: " + explanations[idx] + "<br><br>")

    return clues_and_explanations

def save_high_score_to_json(user_name, score, file_name, add_if_existing=False):
    # Load existing high scores
    try:
        with open(file_name, 'r') as file:
            high_scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        high_scores = []

    # Add the new score
    if add_if_existing:
        for entry in high_scores:
            if entry['user_name'] == user_name:
                entry['score'] += score
                break
        high_scores.append({'user_name': user_name, 'score': score})
    else:
        high_scores.append({'user_name': user_name, 'score': score})

    # Save back to file
    with open(file_name, 'w') as file:
        json.dump(high_scores, file, indent=4)
