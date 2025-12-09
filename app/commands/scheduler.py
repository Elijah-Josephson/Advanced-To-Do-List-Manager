import schedule

from commands.autoclose_overdue import *

schedule.every().day.at("00:00").do(close_overdue())