# auto_backup.py

import os
import sys

# ----- FIX FOR MODULE NOT FOUND -----
# This forces Python to load modules from the same folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------

import schedule
import time

# Now Python will ALWAYS find cloud_backup.py
from cloud_backup import backup_database_to_drive


def auto_backup():
    print("Auto Backup Scheduler Started...")

    schedule.every().day.at("23:55").do(backup_database_to_drive)

    while True:
        schedule.run_pending()
        time.sleep(10)


auto_backup()
