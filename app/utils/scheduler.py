from app.api.recommendations import send_daily_analytics_pdf
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()


def start_scheduler() -> None:
    # Run every day at 17:00 (5 PM)
    scheduler.add_job(
        send_daily_analytics_pdf,
        CronTrigger(hour=17, minute=30, second=0),
    )
    scheduler.start()
