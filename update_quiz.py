import utils
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

if __name__ == '__main__':
    # Initialize Scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=utils.create_new_video, trigger="interval", minutes=10)
    scheduler.add_job(func=utils.clear_daily_high_scores, trigger="interval", minutes=10)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
