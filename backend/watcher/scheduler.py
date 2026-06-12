from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from backend.watcher.watcher import (
    run_watcher
)

scheduler = (
    BackgroundScheduler()
)

scheduler.add_job(
    run_watcher,

    "interval",

    minutes=5,
)

scheduler.start()