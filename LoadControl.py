# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 16:45:28 2016

@author: Peter
"""

import dcload
import time
import csv

# COM Port that the load is on
port = 10

# Baudrate of the port
baudrate = 4800

# List of Current Levels to Test at, in amps
currents = [0.1, 0.2, 0.25]

# Corresponding time lengths for each Current Level, in seconds
times = [1, 2, 1]

current_milli_time = lambda: int(round(time.time() * 1000))

def main():
    print "Test Started"    
    
    if len(currents) == len(times):
        load = dcload.DCLoad()
        load.Initialize(port, baudrate)
        load.SetRemoteControl()
        load.SetMaxCurrent(5)
        load.SetMode("cc")
        
        output = open(str(load.TimeNow()).replace(":", "_") + ".csv", "wb")
        writer = csv.writer(output, delimiter=',')
        writer.writerow(["Time (mS)", "Voltage (V)", "Current (A)", "Power (W)"])
        
        load.TurnLoadOn()        
        beginTest = current_milli_time()        
        
        for current in currents:
            load.SetCCCurrent(current)
            start = current_milli_time()
            
            while current_milli_time() < start + (times[currents.index(current)] * 1000):
                state = load.GetInputValues()
                values = []

                for num in state.split():
                    try:
                        values.append(float(num))
                    except ValueError:
                        pass
                
                writer.writerow([current_milli_time() - beginTest, values[0], values[1], values[2]])
        
        load.TurnLoadOff()
        print "Test Ended"
    else:
        print "Currents and Times must have equal length"
    return 0

#Call the main function
main()