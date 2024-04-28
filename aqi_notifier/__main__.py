import argparse
import sys

from dotenv import dotenv_values

from aqi_notifier import fetch_aqi, parse_sensor_list_file


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
        api_key = config["api_key"]

        arguments = argument_parser()
        file = arguments.sensor_ID_list
        sensor_list = parse_sensor_list_file(file)
        current_avg_aqi = fetch_aqi(sensor_list, api_key)

        print(current_avg_aqi)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
