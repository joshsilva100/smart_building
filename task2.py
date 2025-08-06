
import serial
import time
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

    file_name = f"{now.year}-{now.month}-{now.day}_{now.hour}.txt"
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


#start code here


print("Hey Dr. Guo, Let's go gambling!")

serialcomm = serial.Serial(port="COM7",baudrate=9600,timeout=1) # Replace portname here as seen fit 
time.sleep(2)

schedule.clear()

print("Started at: ", datetime.datetime.now())
interval(serialcomm)
while True:
    hour_break()
    print ("Break ended at: ", datetime.datetime.now())
    interval(serialcomm) 