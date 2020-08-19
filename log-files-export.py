'''
Description:
Module to copy HTOB log-files into archive folder.
Author: petantsk
'''

import os
from datetime import datetime
import shutil


'''
deleteContent() : function for deleting the content of file
Arguments :
fname (Str) - name of file the content is cleared for
Return :
Null
'''
# Function for deleting the content of file
# Command "with" will ensure that the file is correctly closed under all circumstances.
def deleteContent(fname):
    with open(fname, "w"):
        pass


# Working directory path setup
os.chdir('/home/pi/Documents/HTOB')
# Path for exported log files
logg_path = "/home/pi/Documents/HTOB/log-data-backups"
# Get timestamp to add it to the log-file name
LogTime = datetime.now()
# Format:  YYYY-MM-DD hh:mm:ss.msm like 2016-10-04 10:09:35.699
logg_timestamp = LogTime.strftime("%d") + "-" + LogTime.strftime("%m") + "-" + LogTime.strftime("%Y") + "_" + LogTime.strftime("%H") + "-" + LogTime.strftime("%M") + "-" + LogTime.strftime("%S")

# Export files to pre-defined folder
try:
    # File name format:  htob-test_15-10-2016_19-25-08.txt
    shutil.copyfile("htob-test.txt", os.path.join(logg_path, "htob-test_" + logg_timestamp + ".txt"))
    shutil.copyfile("htob-test-scripts.txt", os.path.join(logg_path, "htob-test-scripts_" + logg_timestamp + ".txt"))
except IOError:
    print ("Unable to copy log file to log-data-backups folder.")
else:
    # Clear source log files
    deleteContent("htob-test.txt")
    deleteContent("htob-test-scripts.txt")