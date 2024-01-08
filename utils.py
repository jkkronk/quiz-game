from moviepy.editor import VideoFileClip
import json
import os
import glob

def clear_daily_high_scores():
    from server import app, db, HighScore
    with app.app_context():  # This line creates the application context
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


def remove_files_in_folder(folder_path):
    """
    Removes all files in the specified folder.

    Args:
    folder_path (str): The path to the folder from which files will be removed.
    """
    # Create a pattern to match all files in the folder
    file_pattern = os.path.join(folder_path, '*')

    # List all files in the folder
    files = glob.glob(file_pattern)

    # Loop through the files and remove each one
    for file in files:
        if os.path.isfile(file):
            os.remove(file)
