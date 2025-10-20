import socket 

# turn on hotspot: nmcli dev Wifi hotspot ifname wlan0 ssid HVACR password INNO4990~
# IP address: hostname -I

HOST = "10.42.0.1" #put IP address of pi here
PORT = 4269 # match numbers on Arduino 
SIZE = 2048 # size of the amount of data being recieved, will need to be adjusted

# IMPORTANT POTENTIALLY: use the "sudo ufw allow ####" command in terminal 
# replace the #### with the number in PORT, the placeholder is just funny

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    s.bind((HOST,PORT))
    s.listen()
    conn, addr = s.accept()

    with conn: 
        print(f"Connected at {addr}")
        while True:
            data = conn.recv(SIZE)
            if not data:
                break
            print(f"Received: {data.decode()}")