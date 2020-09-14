#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""sample module for dataset loading into redistimeseries from csv file
"""

import argparse
import redis
import csv
import datetime
import logging
from tqdm import tqdm


def parse_dataset_row(line):
    # Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);NOx(GT);PT08.S3(NOx);NO2(GT);PT08.S4(NO2);PT08.S5(O3);T;RH;AH;;
    # 0 Date	(DD/MM/YYYY)
    # 1 Time	(HH.MM.SS)
    # 2 True hourly averaged concentration CO in mg/m^3 (reference analyzer)
    # 3 PT08.S1 (tin oxide) hourly averaged sensor response (nominally CO targeted)
    # 4 True hourly averaged overall Non Metanic HydroCarbons concentration in microg/m^3 (reference analyzer)
    # 5 True hourly averaged Benzene concentration in microg/m^3 (reference analyzer)
    # 6 PT08.S2 (titania) hourly averaged sensor response (nominally NMHC targeted)
    # 7 True hourly averaged NOx concentration in ppb (reference analyzer)
    # 8 PT08.S3 (tungsten oxide) hourly averaged sensor response (nominally NOx targeted)
    # 9 True hourly averaged NO2 concentration in microg/m^3 (reference analyzer)
    # 10 PT08.S4 (tungsten oxide) hourly averaged sensor response (nominally NO2 targeted)
    # 11 PT08.S5 (indium oxide) hourly averaged sensor response (nominally O3 targeted)
    # 12 Temperature in Â°C
    # 13 Relative Humidity (%)
    # 14 AH Absolute Humidity
    # Missing values are tagged with -200 value.

    result = False
    date = None
    Time = None
    unix_ts = None
    carbon_monoxide = None
    temperature_c = None
    relative_humidity = None
    # check if we have 15 fields or more, and all fields have something on it
    if len(line) > 14 and sum([len(line[x]) > 0 for x in range(0, 14)]) == 14:
        str_date = line[0]
        str_time = line[1]
        carbon_monoxide = (
            float(line[2].replace(",", "."))
            if (float(line[2].replace(",", ".")) > -200.0)
            else None
        )
        temperature_c = (
            float(line[12].replace(",", "."))
            if (float(line[12].replace(",", ".")) > -200.0)
            else None
        )
        relative_humidity = (
            float(line[13].replace(",", "."))
            if (float(line[13].replace(",", ".")) > -200.0)
            else None
        )
        unix_ts = int(
            datetime.datetime.strptime(
                "{0} {1}".format(str_date, str_time), "%d/%m/%Y %H.%M.%S"
            ).timestamp()
        )
        result = True

    return result, unix_ts, carbon_monoxide, temperature_c, relative_humidity


parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, help="redis instance port", default=6379)
parser.add_argument(
    "--password", type=int, help="redis instance password", default=None
)
parser.add_argument("--verbose", help="enable verbose output", action="store_true")
parser.add_argument("--host", type=str, help="redis instance host", default="127.0.0.1")
parser.add_argument(
    "--csv",
    type=str,
    help="csv file containing the dataset",
    default="./AirQualityUCI/AirQualityUCI.csv",
)
parser.add_argument(
    "--csv_delimiter", type=str, help="csv file field delimiter", default=";"
)
args = parser.parse_args()

log_level = logging.ERROR
if args.verbose is True:
    log_level = logging.INFO
logging.basicConfig(level=log_level)

# redis setup
redis_obj = redis.Redis(host=args.host, port=args.port, password=args.password)
temperature_key = "ts:temperature"
carbon_monoxide_key = "ts:carbon_monoxide"
relative_humidity_key = "ts:relative_humidity"

with open(args.csv, newline="") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=args.csv_delimiter)
    next(csv_reader, None)  # skip the headers
    for row in tqdm(csv_reader):
        (
            result,
            unix_ts,
            carbon_monoxide,
            temperature_c,
            relative_humidity,
        ) = parse_dataset_row(row)
        if result is True:
            try:
                if temperature_c is not None:
                    redis_obj.execute_command(
                        "ts.add", temperature_key, unix_ts, temperature_c
                    )
                    logging.info(
                        "ts.add {0} {1} {2}".format(
                            temperature_key, unix_ts, temperature_c
                        )
                    )
                if carbon_monoxide is not None:
                    redis_obj.execute_command(
                        "ts.add", carbon_monoxide_key, unix_ts, carbon_monoxide
                    )
                    logging.info(
                        "ts.add {0} {1} {2}".format(
                            carbon_monoxide_key, unix_ts, carbon_monoxide
                        )
                    )
                if relative_humidity is not None:
                    redis_obj.execute_command(
                        "ts.add", relative_humidity_key, unix_ts, relative_humidity
                    )
                    logging.info(
                        "ts.add {0} {1} {2}".format(
                            relative_humidity_key, unix_ts, relative_humidity
                        )
                    )
            except redis.RedisError as err:
                logging.error(err)
