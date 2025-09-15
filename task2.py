## En "Grace" Wang, Colby Mcneely, Joshua Silva
## HVAC/Smart Building - Task 2
## Data Logging

import serial
import time
import glob
import sys
import datetime
import schedule


def read_data(serialcomm):
    data = serialcomm.readline().decode('ascii')
    while not data:
        time.sleep(.1)
        data = serialcomm.readline().decode('ascii')

    #print(data) #print the line to ensure correctnesss
    return data

def next_hour(): # find next hour
    delta = datetime.timedelta(hours=1)
    cur2 = datetime.datetime.now()
    next = (cur2 + delta).replace(microsecond=0, second=0, minute=0)
    return next


def hour_break():
    diff = next_hour()
    cur = datetime.datetime.now()
    print("Current time: ", cur.time())
    print("Next hour: ", diff.time())
    totalsecs = diff - cur 
    totalsecs = totalsecs.total_seconds()
    print("Seconds till next hour: ", totalsecs)
    time.sleep(totalsecs)


def interval(serialname):
    now = datetime.datetime.now()
    end_time = now + datetime.timedelta(minutes=5.1) 

    file_name = f"data/{now.year}-{now.month}-{now.day}_{now.hour}.txt"
    with open(file_name,"a") as file: 
        file.write(f"Timestamp,AHT20_Temp_C,AHT20_Hum_%,DHT11_Temp_C,DHT11_Hum_%\n")
        schedule.every(29.97).seconds.do(thejob, file=file, serialname=serialname)
        thejob(file, serialname)
        while datetime.datetime.now() < end_time:
            schedule.run_pending()
            time.sleep(.1)

        schedule.clear()
    

def thejob(file, serialname): #the job to occur every 30 seconds in this case the getting of temp humid and time and writing and flushing
    data=read_data(serialname)
    
    now = datetime.datetime.now() 
    # set rounding line instead of truncating, has been done
    if now.microsecond > 500000: 
        now = now + datetime.timedelta(seconds=1)
    
    now = now.replace(microsecond=0)
    file.write(f"{now},{data}")
    file.flush()
    print ("Interval Started at: ", datetime.datetime.now(), "and printed: ", now)

def serial_ports(): # finds all serial ports connected to the computer and puts them in a list of portnames
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

#start code here


print("Hey Dr. Guo, Let's go gambling!")

name_serial_port = serial_ports()
print("The following serial port(s) detected: ", name_serial_port) # testing and to help user input correctly
print("Current number of Serial ports: ", len(name_serial_port))


if len(name_serial_port) == 1: #finds the port name and if only one serial port is detected puts it in for you 
    print("Portname for the one port: ", name_serial_port[0])
    serialcomm = serial.Serial(port=name_serial_port[0],baudrate=9600,timeout=1) # Replace portname here as fit 
else :
    user_input = input("Error detecting port\nEnter the Arduino Port: ") # if port not detected or too many copy one that should be shown or find it and input will make better
    serialcomm = serial.Serial(port=user_input,baudrate=9600,timeout=1) 
time.sleep(2)

schedule.clear()

print("Started at: ", datetime.datetime.now()) # for testing 
interval(serialcomm)
while True:
    hour_break()
    print ("Break ended at: ", datetime.datetime.now()) # for testing
    interval(serialcomm) 