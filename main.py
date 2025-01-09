import requests
from datetime import datetime
import smtplib

MY_LAT = 37.901760 # Your latitude
MY_LONG = -122.061923 # Your longitude
my_email = "jakeeb05@gmail.com"
password = "jsyvqmqwkfxilewg"


iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_response.raise_for_status()
data = iss_response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = float(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = float(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
current_hour = time_now.hour

def check_lat():
    if (MY_LAT > iss_latitude - 5) and (MY_LAT < iss_latitude + 5):
        return True
    
def check_long():
    if (MY_LONG > iss_longitude-5 and MY_LONG < iss_longitude +5):
        return True
    
def check_sun():
    if (current_hour > sunset or current_hour < sunrise):
        return True

if check_lat() and check_long() and check_sun():
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs=my_email,
                        msg="Look up the ISS is above and you can see it!!")
    connection.close()

    


#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



