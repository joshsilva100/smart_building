## En "Grace" Wang, Colby Mcneely, Joshua Silva
## HVAC/Smart Building - Task 2
## Data Logging

import serial
import time
import glob
import sys
import datetime
import schedule
import socket
import subprocess


SIZE = 4096 # hard coded size, i don't trust it to make major issues when transporting a small string 

def read_data(serialcomm):
    data = serialcomm.readline().decode('ascii')
    while not data:
        time.sleep(.1)
        data = serialcomm.readline().decode('ascii')

    #print(data) #print the line to ensure correctnesss
    return data


def start_hotspot_IP(hotspot, PORT):
    if (int(hotspot) == 1): 
        subprocess.run(["nmcli","dev","wifi","hotspot","ifname","wlan0","ssid","HVACR","password","INNO4990~"])
    subprocess.run(["hostname","-I"])
    subprocess.run(["sudo","ufw","allow", str(PORT)])



def read_data_wireless(HOST, PORT, SIZE):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        
        s.listen()
        conn, addr = s.accept()
        data = 0
        with conn: 
            print(f"Connected at {addr}")
            while not data:
                data = conn.recv(SIZE)
                #time.sleep(.1); 
                #if not data:
                #   break
                print(f"Received: {data.decode()}")
            
        
        return data.decode()
        



def next_hour(): # find next hour or a half
    cur2 = datetime.datetime.now()
    if(cur2.minute < 30):
        #delta = datetime.timedelta(minutes=30)
        next = (cur2).replace(microsecond=0, second=0, minute=30)
    else:
        delta = datetime.timedelta(hours=1)
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


def interval(): #serialname):
    now = datetime.datetime.now()
    end_time = now + datetime.timedelta(minutes=5.1) 
    # seperate files now specified
    types = ["temp", "humid", "co2", "lux", "noise"]
    file_names = []
    for types in types: 
        file_names.append(f"data/{types}_{now.year}-{now.month}-{now.day}_{now.hour}.txt")
    #file_name = f"data/{now.year}-{now.month}-{now.day}_{now.hour}.txt"
    with open(file_names[0],"a") as file0,\
    open(file_names[1],"a") as file1,\
    open(file_names[2],"a") as file2,\
    open(file_names[3],"a") as file3,\
    open(file_names[4],"a") as file4: 
        file0.write(f"Timestamp,Temp\n")
        file1.write(f"Timestamp,Humid\n")
        file2.write(f"Timestamp,C02%\n")
        file3.write(f"Timestamp,Lux%\n")
        file4.write(f"Timestamp,Noise%\n")
        files = [file0,file1,file2,file3,file4]
        schedule.every(29.97).seconds.do(thejob, files=files)#, serialname=serialname)
        thejob(files)#, serialname)
        while datetime.datetime.now() < end_time:
            schedule.run_pending()
            time.sleep(.1)

        schedule.clear()
    

def thejob(files):#, serialname): #the job to occur every 30 seconds in this case the getting of temp humid and time and writing and flushing
    #data=read_data(serialname)
    data = read_data_wireless("10.42.0.1",5400,4096)
    #types = ["temp", "humid", "co2", "lux", "noise"]
    data_types = [temp,humid,co2,lux,noise] = data.split(',')
    now = datetime.datetime.now() 
    # set rounding line instead of truncating, has been done
    if now.microsecond > 500000: 
        now = now + datetime.timedelta(seconds=1)
    

    now = now.replace(microsecond=0)
    for i in range(5):
        files[i].write(f"{now},{float(data_types[i]):.5f}\n")
        files[i].flush()
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


#print("Hey Dr. Guo, Let's go gambling!")
hotspot = input("Turn hotspot on? (1 for yes or 0 for no):")
HOST = "10.42.0.1" 
PORT = input("Enter the Port number (1-39999): ")
start_hotspot_IP(hotspot,PORT)
#HOST = input("Enter the IP shown above: ")
input("Press Enter once ESP is connected: ")


#name_serial_port = serial_ports()
#print("The following serial port(s) detected: ", name_serial_port) # testing and to help user input correctly
#print("Current number of Serial ports: ", len(name_serial_port))


#if len(name_serial_port) == 1: #finds the port name and if only one serial port is detected puts it in for you 
#    print("Portname for the one port: ", name_serial_port[0])
#    serialcomm = serial.Serial(port=name_serial_port[0],baudrate=9600,timeout=1) # Replace portname here as fit 
#else :
#    user_input = input("Error detecting port\nEnter the Arduino Port: ") # if port not detected or too many copy one that should be shown or find it and input will make better
#    serialcomm = serial.Serial(port=user_input,baudrate=9600,timeout=1) 
#time.sleep(2)

schedule.clear()

print("Started at: ", datetime.datetime.now()) # for testing 
interval()#serialcomm)
while True:
    hour_break()
    print ("Break ended at: ", datetime.datetime.now()) # for testing
    interval()#serialcomm) 