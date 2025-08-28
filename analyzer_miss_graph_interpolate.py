## Christopher "Joe" Horne
## HVAC/Smart Building - Task 3
import matplotlib.pyplot as plt 
import numpy as np

# .txt file columns
# [AHT Temp, AHT Hum, DHT Temp, DHT Hum]

'''
Process/average Data
      - Get average of data from 5-minute blocks
      - Hourly files: Get averages from sensors AND store them
          > Columns: 'AHT20 Temp', 'AHT20 Humidity', 'DHT11 Temp', 'DHT11 Humidity'.
'''
def Read_In_txt(file): 
        temp_AHT20, humid_AHT20, temp_DHT11, humid_DHT11 = 0, 0, 0, 0 
        t_A, h_A, t_D, h_D = [], [], [], []
        read_lines  = file.readlines()
        for line_N in read_lines:
            line_N      = line_N.strip()
            sensor_data = line_N.split(',')

            try:
                temp_AHT20  = float(sensor_data[1])
                humid_AHT20 = float(sensor_data[2])
                temp_DHT11  = float(sensor_data[3])
                humid_DHT11 = float(sensor_data[4])
                
                if temp_AHT20 != 0 :
                    t_A.append(temp_AHT20)
                if humid_AHT20 != 0:
                    h_A.append(humid_AHT20)
                if temp_DHT11 != 0:
                    t_D.append(temp_DHT11)
                if humid_DHT11 != 0:
                    h_D.append(humid_DHT11)
            except: 
                continue

        t_A_avg = sum(t_A)/len(t_A)
        h_A_avg = sum(h_A)/len(h_A)
        t_D_avg = sum(t_D)/len(t_D)
        h_D_avg = sum(h_D)/len(h_D)

        return t_A_avg, h_A_avg, t_D_avg, h_D_avg,


'''
Comparison plots
      - Two visual plots
          > Avg temps from both sensors
          > Avg humidity from both sensors
      - Requirements (from task sheet)
          > Title
          > Labeled x-axis (Time) and y-axis (Temp/Humidity)
          > Legends for each sensor (Refer to columns from part 3?)
'''


'''
Save plots
       - Save as image files with date
           Ex: "temperature_comparison_2025-07-16.png"
'''

def main():
    temp_A_avg, humid_A_avg, temp_D_avg, humid_D_avg = 0, 0, 0, 0
    t_A_list, h_A_list, t_D_list, h_D_list, known_hour, unknown_hour = [], [], [], [], [], []
    year = input("Enter desired year. (Format as 20XX.): ")
    day = input("Enter desired day. (Choose from 1-31.): ")
    month = input("Enter desired month. (Choose from 1-12.): ")
    #could add error thing here for date and month gw 
      
    for hour in range(24):
        try:
            hour_file = str(hour)
            file_name = f"{year}-{month}-{day}_{hour_file}.txt"
            with open(file_name,"r") as file:
                temp_A_avg, humid_A_avg, temp_D_avg, humid_D_avg = Read_In_txt(file)
            
            t_A_list.append(temp_A_avg)
            h_A_list.append(humid_A_avg)
            t_D_list.append(temp_D_avg)
            h_D_list.append(humid_D_avg) 
            known_hour.append(hour) #Keep track of hours that we know

            #print("\nAHT20 Temps [deg C]: ", temp_A, "\nAHT20 Humidity [%]:  ", humid_A, "\nDHT11 Temps [deg C]: ", temp_D, "\nDHT11 Humidity [%]:  ", humid_D)
            #print("\nAHT20 Temp Average:  ", temp_A_avg, "\nAHT20 Humid Average: ", humid_A_avg, "\nDHT11 Temp Average:  ", temp_D_avg, "\nAHT20 Humid Average: ", humid_D_avg, "\n\n")
        except: 
            t_A_list.append(np.nan)
            h_A_list.append(np.nan)
            t_D_list.append(np.nan)
            h_D_list.append(np.nan) 
            unknown_hour.append(hour) #Keep track of hours that we don't know
            continue 
    
    ## Interpolate the missing data. Won't bother with missing hours before first recorded hour 
    
    #Convert to numpy array for use in numpy functions 
    t_A_list = np.array(t_A_list, dtype = float) 
    h_A_list = np.array(h_A_list, dtype = float) 
    t_D_list = np.array(t_D_list, dtype = float)
    h_D_list = np.array(h_D_list, dtype = float) 

    #Find known values from the list
    known_t_A = t_A_list[~np.isnan(t_A_list)] 
    known_h_A = h_A_list[~np.isnan(h_A_list)]
    known_t_D = t_D_list[~np.isnan(t_D_list)]
    known_h_D = h_D_list[~np.isnan(h_D_list)] 
    
    #Interpolate the data for the missing hours 
    interp_t_A = np.interp(unknown_hour, known_hour, known_t_A) 
    interp_h_A = np.interp(unknown_hour, known_hour, known_h_A) 
    interp_t_D = np.interp(unknown_hour, known_hour, known_t_D) 
    interp_h_D = np.interp(unknown_hour, known_hour, known_h_D) 

    #Go through each missing hour and insert the interpolated values
    for i in range(len(unknown_hour)): 
        miss = unknown_hour[i]
        t_A_list[miss] = interp_t_A[i] 
        h_A_list[miss] = interp_h_A[i] 
        t_D_list[miss] = interp_t_D[i] 
        h_D_list[miss] = interp_h_D[i] 

    #print("\n\nAHT20 Temp Avg: ", t_A_list, "\nAHT20 Humid Avg: ", h_A_list, "\n\nDHT11 Temp Avg: ", t_D_list, "\nDHT11 Humid Avg: ", h_D_list)
    time = list(range(0,24)) 

    plot_temp = f"Hourly Temperature Average for {year}-{month}-{day}"
    name_temp = f"temperature_comparison_{year}-{month}-{day}.png"
    plot_humid = f"Hourly Humidity Average for {year}-{month}-{day}"
    name_humid = f"humidity_comparison_{year}-{month}-{day}.png"

    try:
        # AHT20 vs DHT11 - Temperature
        plt.figure()
        plt.title(plot_temp)
        plt.xlabel("Time [hr]")
        plt.ylabel("Temperature [°C]")
        plt.axis([0, 23, 0, 50])
        plt.plot(time, t_A_list, label="AHT20 Temperature", marker="o")
        plt.plot(time, t_D_list, label="DHT11 Temperature", marker="x")
        plt.legend()
        plt.grid(True)
        plt.savefig(name_temp)
        plt.close()

        # AHT20 vs DHT11 - Humidity
        plt.figure()
        plt.title(plot_humid)
        plt.xlabel("Time [hr]")
        plt.ylabel("Humidity [%]")
        plt.axis([0, 23, 0, 100])
        plt.plot(time, h_A_list, label="AHT20 Humidity", marker="o")
        plt.plot(time, h_D_list, label="DHT11 Humidity", marker="x")
        plt.legend()
        plt.grid(True)
        plt.savefig(name_humid)
        plt.close()
    except:
        print("\n\nError!")
        print("\nWhat went wrong?")
        print("- Check the date entered.")
        print("- Make sure you have all 24 files. (0-23 needed.)\n")

if __name__ == "__main__":
    main()


