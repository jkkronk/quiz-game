from moviepy.editor import VideoFileClip
import json
from create_video import quiz, audio, video, street_view_collector

def create_new_video():
    # Your logic to create a new video
    pass

def clear_daily_high_scores():
    high_scores_file = 'static/daily_high_scores.json'
    # Save back to file
    with open(high_scores_file, 'w') as file:
        json.dump([], file, indent=4)

# Function to calculate the score
def calculate_score(time_taken, video_file_path):
    with VideoFileClip(video_file_path) as video:
        video_duration = video.duration

    # Calculate the score as a percentage
    if time_taken > video_duration:
        return 0  # If the time taken is more than the video duration, return 0%
    else:
        return int(((video_duration - time_taken) / video_duration) * 100)

def save_high_score(user_name, score):
    daily_high_scores_file = 'static/daily_high_scores.json'
    save_high_score_to_file(user_name, score, daily_high_scores_file)

    all_time_high_scores_file = 'static/all_time_high_scores.json'
    save_high_score_to_file(user_name, score, all_time_high_scores_file, add_if_existing=True)

def save_high_score_to_file(user_name, score, file_name, add_if_existing=False):
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

def has_played_today(user_name):
    daily_high_score_file = 'static/daily_high_scores.json'
    try:
        with open(daily_high_score_file, 'r') as file:
            high_scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        high_scores = []

    for entry in high_scores:
        if entry['user_name'] == user_name:
            return True
    return False

def get_daily_high_scores(limit=10):
    high_scores_file = 'static/daily_high_scores.json'
    return get_high_scores(high_scores_file, limit)

def get_all_time_high_scores(limit=10):
    high_scores_file = 'static/all_time_high_scores.json'
    return get_high_scores(high_scores_file, limit)

def get_high_scores(path, limit=10):
    try:
        with open(path, 'r') as file:
            high_scores = json.load(file)
            high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)
            return high_scores[:limit]  # Return top scores
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if no high scores
