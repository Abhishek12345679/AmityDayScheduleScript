from apscheduler.schedulers.blocking import BlockingScheduler
from script import main

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=7, minutes=30)
def scheduled_job():
    print('This job is run every weekday at 0730.')
    main()


sched.start()
