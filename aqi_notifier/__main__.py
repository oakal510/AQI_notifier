import argparse
import sys

from dotenv import dotenv_values

from aqi_notifier import fetch_aqi, parse_sensor_list_file
from aqi_notifier.notify import Notifier


def argument_parser():
    parser = argparse.ArgumentParser(
        prog="AQI Notifier", description="Monitor air quality sensors."
    )
    parser.add_argument(
        "sensor_ID_list",
        type=str,
        help="A text file containing a list of Purple Air sensor IDs to monitor.",
    )
    args = parser.parse_args()

    return args


def main():

    try:

        config = dotenv_values()
        purple_air_api_key = config["purple_air_api_key"]

        arguments = argument_parser()
        file = arguments.sensor_ID_list
        sensor_list = parse_sensor_list_file(file)
        current_avg_aqi = fetch_aqi(sensor_list, purple_air_api_key)

        notifier = Notifier(config["telnyx_api_key"], config["telnyx_number"])
        message = f"The current average AQI is {current_avg_aqi.aqi}. The status is {current_avg_aqi.status}. {current_avg_aqi.recommendations}"
        notifier.send_sms(config["my_number"], message)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
