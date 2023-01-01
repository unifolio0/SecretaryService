import schedule
import time
from telegram_bot import *

schedule.every().day.at("08:00").do(telegram_msg)

while True:
    schedule.run_pending()
    time.sleep(1)