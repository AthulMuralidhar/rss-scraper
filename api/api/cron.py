from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .main import get_feed_items


scheduler = AsyncIOScheduler()

URL = "http://www.nu.nl/rss/Algemeen"

def start_background_tasks():

    import ipdb; ipdb.set_trace()

    scheduler.start()
    scheduler.add_job(lambda : scheduler.print_jobs(),'interval',seconds=5)

    # job = scheduler.add_job(get_feed_items,'interval', minutes=5, args)
    # job.remove()

    scheduler.shutdown()
