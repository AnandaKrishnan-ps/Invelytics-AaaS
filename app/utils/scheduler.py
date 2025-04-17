from app.api.recommendations import send_daily_analytics_pdf
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()


def start_scheduler() -> None:
    # Run every day at 17:30 (5.30 PM)
    scheduler.add_job(
        send_daily_analytics_pdf,
        CronTrigger(hour=17, minute=4, second=20),
    )
    scheduler.start()
