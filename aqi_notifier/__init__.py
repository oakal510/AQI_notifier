import statistics

import requests
import rich

from aqi_notifier import aqi


def check_api_key_status(api_key):
    url = "https://api.purpleair.com/v1/keys"
    headers = {"X-API-Key": api_key}

    r = requests.get(url, headers=headers)

    print(r.json())

    return 1


def get_sensor_data(relevant_sensors, api_key):

    sensor_data = []

    for sensor in relevant_sensors:
        url = f"https://api.purpleair.com/v1/sensors/{sensor}"
        headers = {"X-API-Key": api_key}
        r = requests.get(url, headers=headers)
        # rich.print(r.json())
        sensor_data.append(r.json())

    return sensor_data


def parse_sensor_list_file(file_name: str) -> list[str]:

    sensor_list = []

    try:
        with open(file_name) as file:
            for line in file:
                sensor_list.append(line.strip())
    except FileNotFoundError as e:
        raise ValueError(
            f"File {file_name} not found. Please use a valid .txt file."
        ) from e

    if len(sensor_list) == 0:
        raise ValueError(
            "No sensor IDs found in the file. Please provide a valid list of sensor IDs."
        )

    return sensor_list


def fetch_aqi(sensor_list: list[str], api_key) -> aqi.EPA_AQI:

    raw_data = get_sensor_data(sensor_list, api_key)
    average_pm25 = statistics.mean(
        [sensor["sensor"]["stats"]["pm2.5_60minute"] for sensor in raw_data]
    )

    return aqi.EPA_AQI.from_pm_raw(average_pm25)
