from apscheduler.schedulers.background import (
    BackgroundScheduler
)

from backend.monitoring.service import (
    run_monitoring
)

scheduler = BackgroundScheduler()


def start_scheduler():

    scheduler.add_job(

        run_monitoring,

        trigger="interval",

        minutes=5,

        id="docker_monitor",

        replace_existing=True,
    )

    scheduler.start()

    print(
        "Docker Monitoring Scheduler Started"
    )