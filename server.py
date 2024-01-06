import random

from flask import Flask, request, render_template, redirect, url_for, jsonify
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import json

import utils

app = Flask(__name__)

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


# Route for the video page
@app.route('/video')
def video():
    # Path to the text file with the answer
    correct_answer = utils.get_answer(os.path.join(app.static_folder, 'quiz.json'))
    start_time = time.time()
    return render_template('video.html', start_time=start_time, correct_answer=correct_answer)


@app.route('/high_scores')
def high_scores():
    all_time_high_scores = utils.get_all_time_high_scores()  # Function to get all-time high scores
    daily_high_scores = utils.get_daily_high_scores()  # Function to get today's high scores
    return render_template('high_scores.html', all_time_high_scores=all_time_high_scores, daily_high_scores=daily_high_scores)


@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    video_file_path = os.path.join(app.static_folder, 'quiz.mp4')
    start_time = float(request.form['start_time'])
    end_time = time.time()
    time_taken = end_time - start_time
    score = utils.calculate_score(time_taken, video_file_path)
    return redirect(url_for('score', score=score))

# Route for the score page
@app.route('/score/<score>')
def score(score):
    daily_high_scores = utils.get_daily_high_scores()  # This function should return today's high scores
    return render_template('score.html', score=score, daily_high_scores=daily_high_scores)


@app.route('/explanations')
def explanations():
    clues_and_explanations = utils.get_explanations(os.path.join(app.static_folder, 'quiz.json'))
    return render_template('explanations.html', explanations=clues_and_explanations)


# Initialize Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=utils.create_new_video, trigger="cron", hour=0)
scheduler.add_job(func=utils.clear_daily_high_scores, trigger="cron", hour=0)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True)
