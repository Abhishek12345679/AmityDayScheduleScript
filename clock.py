from apscheduler.schedulers.blocking import BlockingScheduler
from script import main

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=5)
def timed_job():
    print('This job is run every five minutes.')
    main()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=7)
def scheduled_job():
    print('This job is run every weekday at 0730.')
    main()


sched.start()
