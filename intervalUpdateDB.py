from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from dbTools import update_table, Database


def update_db():
    with Database() as connection:
        update_table(connection)


def daily_update_db():
    schedule = BackgroundScheduler()

    schedule.add_job(func=update_db, trigger='interval', hours=24)

    schedule.start()
    atexit.register(lambda: schedule.shutdown())
