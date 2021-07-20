from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .main import get_feed_items
import logging
import asyncio

logging.basicConfig()
logging.getLogger("apscheduler").setLevel(logging.DEBUG)


URL = "http://www.nu.nl/rss/Algemeen"


if __name__ == "__main__":
    user_input = input("start background tasks? (y/n/stop) ")

    scheduler = AsyncIOScheduler()
    scheduler.start()

    if user_input == "y":
        scheduler.print_jobs()
        scheduler.add_job(lambda: scheduler.print_jobs(), "interval", seconds=5)
        scheduler.add_job(
            get_feed_items,
            "interval",
            seconds=10,
            args=[URL],
            name="get-feed-items-job",
            replace_existing=True,
            misfire_grace_time=120,
            coalesce=True,
        )

    if user_input == "n":
        scheduler.print_jobs()

    if user_input == "stop":
        scheduler.print_jobs()
        scheduler.shutdown()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
