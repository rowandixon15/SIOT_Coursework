# SIOT_Coursework
WiFi Monotoring and Weather API collection and posting to google sheets
#
#
This script will run once. It will call on Open Weather Map API for weather data in the specified city. It will also search for the specified MAC addresses in the specified port on the local letwork. Once it has this data the script will publish it to a Google Sheet via an API.
#
It is recomended to run the scrip using Cron, with root permissions (sudo crontab -e). 
