#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone
import RPi.GPIO as GPIO

"""
### Constants
### THRESHOLD is the KP value at which the LED turns on
### PIN is the GPIO pin that is set to high to turn on the LED.
### BRIGHTNESS is how bright the LED should be (from 0 to 100).
"""
THRESHOLD: float = 4.5
PIN: int = 13
BRIGHTNESS: int = 5

# Fetch the KP data from Alaska's Geophysical Institute.
gi = requests.get("https://www.gi.alaska.edu/monitors/aurora-forecast")

# Only continue if it was successful.
if not gi.ok:
    exit(-1)

soup = BeautifulSoup(gi.text, 'html.parser')

# data = soup.find(id="db-data")
# twentysevenday = soup.find(id="db-data-27-day")
threeday = soup.find(id="db-data-3-day")

# data_json = json.loads(data.text)
# twentysevenday_json = json.loads(twentysevenday.text)
threeday_json = json.loads(threeday.text)

# Get the current UTC time and round it to the nearest 3rd hour (so 00:00:00, 03:00:00, 06:00:00...).
now = datetime.now(timezone.utc)
formattedTime: str = f"{now.year:04d}-{now.month:02d}-{now.day:02d} {int(now.hour/3)*3:02d}:00:00"

kp_value = 0.0
for entry in threeday_json:
    if entry["predicted_time"] == formattedTime:
        kp_value = float(entry["kp"])
        break

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
p = GPIO.PWM(PIN, 60)  # channel=12 frequency=60Hz
if kp_value >= THRESHOLD:
    # pass
    # GPIO.output(PIN, GPIO.HIGH)
    p.start(BRIGHTNESS)

else:
    # pass
    # GPIO.output(PIN, GPIO.LOW)
    p.stop()

# Exit with 0 marking success.
exit(0)
