#some logic
#load modules
#set some contants
#create KPA object
#interrogate KPA object for offsets

import csv
from datetime import date, timedelta

import clr # provided by pythonnet, .NET interface layer
import sys


import schedule #for timing logging
import time

from pathlib import Path

# this is seriously nasty.  Points for a better way of fixing this!
sys.path.append(r"C:\Program Files\Thorlabs\Kinesis_2")

# C:\Program Files\Thorlabs\Kinesis_2

# .NET for Kinesis
#ppak addition
clr.AddReference("Thorlabs.MotionControl.KCube.PositionAlignerCLI")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("System")


# idk why these are underlined, something to do with the dir of source(dll) files
# file still works
#ppak addition
# from Thorlabs.MotionControl.KCube.PositionAlignerCLI import PositionAlignerCLI
from Thorlabs.MotionControl.KCube.PositionAlignerCLI import KCubePositionAligner
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from System import Decimal


# CONSTANTS
# specific to our KPA
serial=str(69252058)
header_str1 = "t [s], x_cal [au], y_cal [au], x_mm, y_mm\n"
header_str2 = "t [s], x_cal [au], y_cal [au]\n"
# antenna under test for filename
ap='data_'
polling_interval = 4  # polling milliseconds
sampling_interval = 0.005  # interval seconds, how fast the code samples the poll

def list_devices():
    """Return a list of Kinesis serial numbers"""
    DeviceManagerCLI.BuildDeviceList()
    return DeviceManagerCLI.GetDeviceList()

def fetch_position():
    '''
    Get PDP90A Raw position
    Strip out Xdiff, Ydiff, Sum values
    Calculate x and y offset in mm according to datasheet
    Format results nicely in order to write to file
    '''

    #the time is when we get the status reading
    t=time.time()
    #get one status reading for each cycle
    status=kpa101.Status

    #split out the data from the reading
    x_diff=status.PositionDifference.X
    y_diff=status.PositionDifference.Y
    tsum=status.Sum
    #calculate x and y in mm
    x_mm=x_diff*10/2/tsum
    y_mm=y_diff*10/2/tsum

    # calculate the unitless number
    x_cal = x_diff/tsum
    y_cal = y_diff/tsum

    #format result string and return
    result_str1 = [t-start_time, x_cal, y_cal, x_mm, y_mm]
    result_str2 = [t-start_time, x_cal, y_cal]
    #print("---2 %s seconds ---" % (time.time() - start_time))
    return(result_str1)

def write_position():
    position_line=fetch_position()
    print(position_line)
    writer = csv.writer(f)
    writer.writerow(position_line)
    # f.write(position_line + "/n")

#time
#lets create and open a file every time it is run.

try:
    #input("Press enter to continue")

    #help(KCubePositionAligner)
    print('Thor_logger: [antenna %s] [kpa101 polling %i ms] [file sampling %2.3f s]'%( ap,  polling_interval, sampling_interval))
    print('Kinesis serials numbers found: ', list_devices())

    kpa101 = KCubePositionAligner.CreateKCubePositionAligner(serial)
    try:
        kpa101.Connect(serial)
    except:
        print('Connect failed is the K-Cube plugged in and switched on?')

    # pause before recording data
    time.sleep(2) # ThorLabs have this in their example...

    kpa101.StartPolling(polling_interval)

    print(f'Home directory: {Path.home()}')
    print(f'Current directory: {Path.cwd()}')
    #The f or F in front of strings tell Python to look at the values inside {} and substitute them with the variables values if exists.

    # file_time=str(int(time.time()))
    file_time=str(date.today())
    file_name=str('position_'+ap+file_time+'.csv')
    file_path=Path.cwd()  / 'output' / file_name
    print('Log file location:', file_path)

    # open the file and write the header
    f = open(file_path, 'w', newline='')
    f.write(header_str1)

    # delcare start time
    start_time = time.time()

    # write the postion
    schedule.every(sampling_interval).seconds.do(write_position)

    while True:
       schedule.run_pending()
       #time.sleep(0.05)

except KeyboardInterrupt:
    print("Did you press break?")
except SyntaxError:
    print('SyntaxError: ', SyntaxError )
finally:
    schedule.clear()  #otherwise you end up with multiple instances of scheduled jobs
    kpa101.StopPolling()  #give the kpa101 a rest
    kpa101.Disconnect()   #disconnect cleanly so Kinesis or other programs can connect
    f.close()  #close the file for writing.
    print("This is the end as we know it")
