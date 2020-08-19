#!/usr/bin/python
# -*- coding: UTF-8  -*-
# -------------------------------------------------------------------------
# Script generates voltage pulses from ML-52 controller: when power supply
# is connected to ML-52, then voltage pulse is generated on the ML-52 output.
# Voltage pulse polarity changes (posit./negat.) after each power supply
# appliance. Posit./negat.pulses are controlling latching contactor
# Albright SW2000A-43M.
# --------------------------------------------------------------------------
import time
# Custom module
import errordetection
 

try:
    # Start the GUI test
    print ("Load contactor test starts")
    time.sleep(60)
    # Simulate error - division by zero
    value = 3 / 0

except:
    # Exception occurred - error is reported to text file
    errordetection.writeError()
    print ("Error in Load contactor script occurred!")

finally:
    # Make cleanup after all
    print ("Load contactor script finished!")
