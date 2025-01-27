from apscheduler.schedulers.blocking import BlockingScheduler
from main import main  # Assuming 'main.py' is in the same 'app' directory

# Initialize the scheduler
scheduler = BlockingScheduler()

# Schedule the `main` function to run every day at 10:00 AM UTC
scheduler.add_job(main, 'cron', hour=10, minute=0, second=0, timezone='UTC')

if __name__ == "__main__":
    print("Scheduler started. Waiting for the next run...")
    scheduler.start()
