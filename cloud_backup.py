# cloud_backup.py
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from database import DB_PATH

def backup_database_to_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Opens browser for login (first time only)
    
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'title': 'billing_backup.db'})
    file.SetContentFile(DB_PATH)
    file.Upload()

    print("Backup successful!")
    return "Backup successful!"
