from os import path, listdir, makedirs
from shutil import copyfile
from time import time, localtime, strftime, sleep
from datetime import datetime

"""
automatic DSR backup file creation
(1) creates backups upon start
(2) creates backups every MINUTES minutes defined below. Default: 5
note: the documents folder has to be set as FOLDER_documents below. Default: 'documents'
note: auto save only for files which have been modified in the last 10 minutes
note: should be compiled using PyInstaller
"""

# variables
# insert the name of the windows documents folder
# depends either on locale (by default) or user setting
DOCSNAME = "documents"
MINUTES = 5

# Constants
UserPath = path.expandvars("%userprofile%")
DsrPath = path.join(UserPath, DOCSNAME, "NBGI", "DARK SOULS REMASTERED")

def backup_saves(init):
    # Goes through sub directories in DSR save folder
    for subDir in listdir(DsrPath):
        
        # find and print save folder
        subDirFull = path.join(DsrPath, subDir)
        print(subDirFull)

        # Makes sure subDirFull is a directory
        if path.isdir(subDirFull):
            # Iterates through file
            for file in listdir(subDirFull):
                # Makes sure file is a file    
                if path.isfile(file):
                    # Get name and path for original save
                    name_save, name_extension = path.splitext(file)
                    path_save = path.join(subDirFull, file)
                    subDirBackup = path.join(subDirFull, f"{name_save}-BACKUP")
                    
                    # get timestamp of original save file
                    tSave = path.getmtime(path_save)
                    tNow = time()

                    # If init or last save was less than 600 seconds
                    if init or (tNow - tSave) < 600:
                        # If backup dir doesnt exist, makes it
                        if not path.exists(subDirBackup):
                            makedirs(subDirBackup)
                        
                        # Sets time stamp for backup file and prints it
                        timeStamp = strftime("%Y_%H_%M_%S", localtime(tNow))
                        timePrint = strftime("%H:%M", localtime(tNow))

                        # Sets backup's name and path
                        name_backup = f"{name_save}-BACKUP_{timeStamp}{name_extension}"
                        path_backup = path.join(subDirBackup, name_backup)

                        # Copies original to path_backup
                        copyfile(path_save, path_backup)
                        print(f"{timePrint}   saving backup of {name_save}:")
                        spacing = " " * len(timePrint)
                        print(f"{spacing}   -> {name_backup}")

def main():
    # Initializes first run
    backup_saves(True)
    
    # Runs until keyboard interrupt, ctrl+c
    while True:
        # Backs up save, init = false
        backup_saves(False)

        # Sleep time in seconds
        sleepSeconds = 60 * MINUTES
        print(f"\nsleeping for {MINUTES} minutes\n")
        sleep(sleepSeconds)

if __name__ == '__main__':
    main()