import sys
import subprocess

def handler(event, context):
    subprocess.run(["/venv/bin/python", "-m", "aqi_notifier", "test_sensor_list.txt"])
    return "Success!"