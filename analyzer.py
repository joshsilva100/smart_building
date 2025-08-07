## Christopher "Joe" Horne
## HVAC/Smart Building - Task 3
import matplotlib.pyplot as plt # type: ignore

## Steps

# Variables to track (remove from list as they're added):
# time          hours 0 - 23
# temp_avg      Temperature average from both sensors
# humid_avg     Humidity average from both sensors 

# .txt file columns
# [AHT Temp, AHT Hum, DHT Temp, DHT Hum]

'''
2.) Full day's worth of data
    **- Pick the day (Start with hardcode, upgrade later)
      - Code generates filenames for logged data for each specific hour
          Ex: "2025-07-11" yields '2025-07-16_00.txt', '2025-07-16_01.txt' ..., '2025-07-16_23.txt
          - MAKE SURE IT LOOPS THROUGH EACH HOUR, 0 - 23.
'''
def ReadIn_txt(): 

    with open('2025-7-24_2.txt',"r") as file:
        #values = [float(line.split()[0]) for line in file if line]
        first_line = file.readline().strip()
        vars = first_line.split(',')

        temp_AHT20  = float(vars[1])
        humid_AHT20 = float(vars[2])
        temp_DHT11  = float(vars[3])
        humid_DHT11 = float(vars[4])

        return temp_AHT20, humid_AHT20, temp_DHT11, humid_DHT11

    


'''
3.) Process/average Data
      - Get average of data from 5-minute blocks
      - Hourly files: Get averages from sensors AND store them
          > Columns: 'AHT20 Temp', 'AHT20 Humidity', 'DHT11 Temp', 'DHT11 Humidity'.
'''



'''
4.) Comparison plots
      - Two visual plots
          > Avg temps from both sensors
          > Avg humidity from both sensors
      - Requirements (from task sheet)
          > Title
          > Labeled x-axis (Time) and y-axis (Temp/Humidity)
          > Legends for each sensor (Refer to columns from part 3?)
'''
# plt.title("Hourly Temperature Average for [Date]")
# plt.xlabel("Time [hr]")
# plt.ylabel("Temperature [deg F]")
# plt.plot(time, temp_avg)
# plt.savefig('temperature_comparison_[Date].png')

# plt.title("Hourly Humidity Average for [Date]")
# plt.xlabel("Time [hr]")
# plt.ylabel("Humidity [%]")
# plt.plot(time, humid_avg)
# plt.savefig('humidity_comparison_[Date].png')


'''
5.) Save plots
       - Save as image files with date
           Ex: "temperature_comparison_2025-07-16.png"
'''

