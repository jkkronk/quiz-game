from moviepy.editor import VideoFileClip
import json
import os
import shutil

def clear_daily_high_scores():
    from server import app, db, HighScore
    with app.app_context():  # This line creates the application context
        try:
            # Reset daily scores for all users
            HighScore.query.update({HighScore.daily_score: -1})
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
        clues_and_explanations.append(explanations[idx] + "<br><br>")

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


def remove_files_and_folders(folder_path):
    # Check each item in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # If the item is a file, remove it
        if os.path.isfile(item_path):
            os.remove(item_path)
        # If the item is a directory, remove the directory and its contents
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

