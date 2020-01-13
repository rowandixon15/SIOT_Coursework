#
# WIP Script to log who is on a wifi network and the local weather 
#

import sys
import os
import nmap
from datetime import datetime
from time import sleep

import gspread
import csv
import time 
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import requests
import pygsheets
import requests


# Wifi scanning is done by this function
def scan():
    # Define an array to hold  our results in. 
    scan_results = [0] * len(tracked_mac_addrs)
    # Repeat scan 8 times - Done as some devices(specifically Apple, dont show up all the time, this is to catch them)#with a 5s gap between all scans
    for x in range(0, 8):
        # Perform the scan
        nm = nmap.PortScanner()
        nm.scan("192.168.0.0/24", arguments='-sn')
        # Search for our target MAC addresses in the scan results 
        for h in nm.all_hosts():
            if 'mac' in nm[h]['addresses']: # MAC address doesn't always exist
                mac_addr = nm[h]['addresses']['mac']
                if mac_addr in tracked_mac_addrs:
                    scan_results[tracked_mac_addrs.index(mac_addr)] |= 1
        # Sleep 5 seconds if not the last loop
        if x != 2: sleep(1)
    return scan_results


i = 1
def export():
    i = 1
    i = i + 1
    
    # API address for this programs access to Open Weather Maps API
    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=171e8a3c87c06fcfce4aa64c220ad84e&q='

    # Define city name here 
    city = 'Hammersmith'


    url = api_address + city

    #Gathers data from the .json file provided by the api and selects atributes wanted
    #Here the temperature and description of location are gathered. More can be added.
    json_data = requests.get(url).json()
    formatted_data_main = json_data['weather'][0]['main']
    formatted_data_temp = json_data['main']['temp']
    true_temp = formatted_data_temp - 273.15
    now = datetime.now()
    timestamp1 = now.strftime("%m/%d/%Y")
    timestamp2 = now.strftime("%H:%M:%S")
    weather_data = [timestamp1, timestamp2, formatted_data_main, true_temp]
    
    final_input = weather_data + scan_result
    sheet.insert_row(final_input, i)



# Checks that the script is being run in root
if os.geteuid() != 0:
    print("Must be run as root!")
    exit(-1)

# Check we have the correct number of arguments
if len(sys.argv) != 2:
    print("Usage: %s [logfile]" % (sys.argv[0]))
    exit(-1)

###### Options that can be changed ######
subnet = "192.168.0.0/24" # Define the subnet to scan here
tracked_mac_addrs = [ # List the MAC addresses to track here - must be uppercase!
    "FF:FF:FF:FF:FF:FF", #Person A
    "FF:FF:FF:FF:FF:FF", #Person B
    "FF:FF:FF:FF:FF:FF", #Person C
    "FF:FF:FF:FF:FF:FF", #Person D
    "FF:FF:FF:FF:FF:FF"  #Person E
]

###### End of options to be changed ######

# Setup our log file
log_file = None
if not (os.path.exists(sys.argv[1]) and os.path.isfile(sys.argv[1])):
    # Create the file and write the headers to it
    print("Logfile does not exist. Creating it")
    try:
        log_file = open(sys.argv[1], 'w')
        log_file.write("time")
        for mac in tracked_mac_addrs:
            log_file.write(", %s" % (mac))
        log_file.write("\n")
    except:
        print("Failed to open log file %s" % (sys.argv[1]))
        exit(-1)
else:
    # Just open the log file and append to it
    print("Opening already created log file")
    try:
        log_file = open(sys.argv[1], 'a')
    except:
        print("Failed to open log file %s" % (sys.argv[1]))
        exit(-1)


#-------------------------------------------------
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Desktop/client_id_tracking.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("phone_tracking").sheet1


i = 1
# Main loop
while i<2:
    i = i+1
    # Perform the scan
    print("Performing scan... ")
    scan_result = scan()
    print("done.")
    print("Exporting")
    exporting = export()
    print("Exporting Done!!")
    
    # Write a line to the logfile
    log_file.write("%s" % (datetime.now().strftime("%d-%m-%y %H:%M:%s")))
    for res in scan_result:
        log_file.write(", %s" % (res))
    log_file.write("\n")
    log_file.flush()
    print("Logfile written")
    # Sleep until the next scan
 