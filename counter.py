'''
Description:
Module to update HTOB test cycles counter.
Author: petantsk
'''

import os
import re
from datetime import datetime


# Get timestamp to add it to the log-file name
LogTime = datetime.now()
# Format:  DD-MM-YYYY hh:mm:ss.msm like 11-04-2016 10:09:35.699
logg_timestamp = LogTime.strftime("%d") + "-" + LogTime.strftime("%m") + "-" + LogTime.strftime("%Y") + "_" + LogTime.strftime("%H") + "-" + LogTime.strftime("%M") + "-" + LogTime.strftime("%S")


# Working directory path setup
os.chdir('/home/pi/Documents/HTOB')

#--------------------------------------------------------------------------------------------------------
# Update counter values from htob-cycles.txt file
#--------------------------------------------------------------------------------------------------------
file_object = open("htob-cycles.txt","r")    # opening the counter file for reading
value = re.findall("\d+", file_object.read())    # extract all numbers from file
elapsed_cycles = int(value[0]) # convert the string to int number
remaining_cycles = int(value[1]) # convert the string to int number
CyclArray = [elapsed_cycles + 1, remaining_cycles - 1] # update the counter
file_object.close()

file_object = open("htob-cycles.txt","w")    # opening the counter file for writing
file_object.write(str(CyclArray))  # write updated counter
file_object.close()

file_object = open("htob-cycles.txt","r")    # opening the counter file for writing
print ('HTOB counter updated (' + logg_timestamp + '): [elapsed, remaining]=' + file_object.read())
file_object.close()
