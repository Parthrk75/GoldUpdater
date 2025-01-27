from apscheduler.schedulers.blocking import BlockingScheduler
# scheduler.py
from main import main  # Assuming 'main.py' is in the same 'app' directory


# Initialize the scheduler
scheduler = BlockingScheduler()

# Schedule the `main` function to run every day at 12:00 PM UTC
scheduler.add_job(main, 'cron', hour=10, minute=0)

if __name__ == "__main__":
    print("Scheduler started. Waiting for the next run...")
    scheduler.start()
