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
"""
THRESHOLD: float = 4.5
PIN: int = 12

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

now = datetime.now(timezone.utc)
formattedTime: str = f"{now.year:04d}-{now.month:02d}-{now.day:02d} {now.hour:02d}:00:00"

kp_value = 0.0
for entry in threeday_json:
    if entry["predicted_time"] == formattedTime:
        kp_value = float(entry["kp"])
        break

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
if kp_value >= THRESHOLD:
    GPIO.output(PIN, GPIO.HIGH)

else:
    GPIO.output(PIN, GPIO.LOW)

# Exit with 0 marking success.
exit(0)
