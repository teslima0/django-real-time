import schedule
import time as tm
from datetime import datetime,timedelta, time

def job():
    print("subscribe to tamarom channels")


#schedule.every().second.do(job)
schedule.every().day.at("10:30").do(job)
while True:
    schedule.run_pending()
    tm.sleep(1)