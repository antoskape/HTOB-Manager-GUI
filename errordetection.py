'''
Description:
Module to write an error event into text file.
After that the HTOB GUI status changes to "Error detected".
Author: petantsk
'''

import time
import os

# Working directory path setup for Linux OS!
#os.chdir('/home/pi/Documents/newHTOB')

def writeError():
    # Date/time for records (10/05/2016_00:30:25)
    now = time.strftime("%d.%m.%Y") + "_" + time.strftime("%H:%M:%S")
    # Write down an error event into text file
    file_object = open("error-detection.txt", "a")  # opening the error status file for appending a record.
    file_object.write(now + " - error detected\n")  # write down new error date. New records are always on new line.
    file_object.close()

#writeError()