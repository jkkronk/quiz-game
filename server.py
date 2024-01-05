from flask import Flask, request, render_template, redirect, url_for
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

import utils

app = Flask(__name__)

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Retrieve user's name from the form
        user_name = request.form['name']
        if utils.has_played_today(user_name):
            message = "You have already played today. Please choose a new name."
            return render_template('home.html', message=message)

        return redirect(url_for('video', user_name=user_name))
    return render_template('home.html')

# Route for the video page
@app.route('/video/<user_name>')
def video(user_name):
    # Path to the text file with the answer
    correct_answer = utils.get_answer(os.path.join(app.static_folder, 'quiz.json'))

    start_time = time.time()
    return render_template('video.html', user_name=user_name, start_time=start_time, correct_answer=correct_answer)


@app.route('/submit_answer/<user_name>', methods=['POST'])
def submit_answer(user_name):
    answer_file_path = os.path.join(app.static_folder, 'answer.txt')

    with open(answer_file_path, 'r') as file:
        correct_answer = file.read().strip().lower()

    user_answer = request.form['answer'].lower()
    if user_answer == correct_answer:
        video_file_path = os.path.join(app.static_folder, 'quiz.mp4')

        start_time = float(request.form['start_time'])
        end_time = time.time()
        time_taken = end_time - start_time
        score = utils.calculate_score(time_taken, video_file_path)
        utils.save_high_score(user_name, score)

        return redirect(url_for('score', user_name=user_name, score=score))
    else:
        # Redirect back to the video page if the answer is incorrect
        return redirect(url_for('video', user_name=user_name))

# Route for the score page
@app.route('/score/<user_name>/<score>')
def score(user_name, score):
    daily_high_scores = utils.get_daily_high_scores()  # This function should return today's high scores
    return render_template('score.html', user_name=user_name, score=score, daily_high_scores=daily_high_scores)

@app.route('/high_scores')
def high_scores():
    all_time_high_scores = utils.get_all_time_high_scores()  # Function to get all-time high scores
    daily_high_scores = utils.get_daily_high_scores()  # Function to get today's high scores
    return render_template('high_scores.html', all_time_high_scores=all_time_high_scores, daily_high_scores=daily_high_scores)

# Initialize Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=utils.create_new_video, trigger="cron", hour=0)
scheduler.add_job(func=utils.clear_daily_high_scores, trigger="cron", hour=0)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True)
