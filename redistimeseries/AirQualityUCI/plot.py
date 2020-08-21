#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""sample module for dataset loading into redistimeseries from csv file
   2019 @fcosta_oliveira
"""

import argparse
import redis
import matplotlib.pyplot as plt
import matplotlib.collections as mcol
from matplotlib.legend_handler import HandlerLineCollection, HandlerTuple
from matplotlib.lines import Line2D
import numpy as np
import moment
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, help="redis instance port", default=6379)
parser.add_argument(
    "--password", type=int, help="redis instance password", default=None
)
parser.add_argument("--host", type=str, help="redis instance host", default="127.0.0.1")
parser.add_argument(
    "--dataset_serie",
    type=str,
    help="the dataset serie of one of the following to be plotted: temperature,carbon_monoxide,relative_humidity",
    default="carbon_monoxide",
)
parser.add_argument("--dod", help="comparing sets of 1 day", action="store_true")
parser.add_argument("--wow", help="comparing sets of 7 days", action="store_true")
parser.add_argument("--mom", help="comparing sets of 30 days", action="store_true")
parser.add_argument(
    "--set_timeframe",
    help="specify the timeframe size for the comparison",
    action="store_true",
)

parser.add_argument(
    "--baseline_start",
    type=str,
    help="start date and time for the baseline",
    required=True,
)
parser.add_argument(
    "--comparison_start", type=str, help="start date and time for the comparison"
)
parser.add_argument(
    "--agg_type",
    type=str,
    help="aggregation type one of the following: avg, min, max, none",
    default="avg",
)
parser.add_argument(
    "--bucket_size_seconds",
    type=int,
    help="time bucket for aggregation in seconds",
    default=3600,
)
parser.add_argument(
    "--timeframe_size_seconds",
    type=int,
    help="timeframe of analysis in seconds",
    default=86400,
)

args = parser.parse_args()

possible_timeframes = args.dod or args.wow or args.mom or args.set_timeframe
timeframe_size_seconds = None
if args.dod:
    timeframe_size_seconds = 60 * 60 * 24
if args.wow:
    timeframe_size_seconds = 60 * 60 * 24 * 7
if args.mom:
    timeframe_size_seconds = 60 * 60 * 24 * 30
if args.set_timeframe:
    timeframe_size_seconds = args.timeframe_size_seconds

if timeframe_size_seconds is None:
    pass
    # TODO: raise error and exit

print(possible_timeframes)
baseline_date = moment.date(args.baseline_start)
baseline_end_date = baseline_date.clone().add(seconds=timeframe_size_seconds)
baseline_date_unix_ts = baseline_date.epoch()
baseline_end_date_unix_ts = baseline_end_date.epoch()

baseline_values = []
comparison_values = []
comparison_date = None
comparison_end_date = None
comparison_date_unix_ts = None
comparison_end_date_unix_ts = None

if args.comparison_start is not None:
    comparison_date = moment.date(args.comparison_start)
    comparison_end_date = comparison_date.clone().add(seconds=timeframe_size_seconds)
    comparison_date_unix_ts = comparison_date.epoch()
    comparison_end_date_unix_ts = comparison_end_date.epoch()
    print("## {} >> {}".format(comparison_date_unix_ts, comparison_end_date_unix_ts))

possible_agg_types = ["avg", "min", "max", "none"]
if args.agg_type not in possible_agg_types:
    # TODO: raise error and exit
    pass


# redis setup
redis_obj = redis.Redis(host=args.host, port=args.port, password=args.password)

temperature_key = "ts:temperature"
temperature_description = "Temperature in Â°C variation"
temperature_y_label = "°C"
carbon_monoxide_key = "ts:carbon_monoxide"
carbon_monoxide_description = (
    "True averaged concentration CO in mg/m^3 (reference analyzer)"
)
carbon_monoxide_y_label = "mg/m^3"
relative_humidity_key = "ts:relative_humidity"
relative_humidity_description = "Relative Humidity (%) variation"
relative_humidity_y_label = "Relative Humidity (%)"

if args.dataset_serie == "temperature":
    y_label = temperature_y_label
    title = temperature_description
if args.dataset_serie == "carbon_monoxide":
    y_label = carbon_monoxide_y_label
    title = carbon_monoxide_description
if args.dataset_serie == "relative_humidity":
    y_label = relative_humidity_y_label
    title = relative_humidity_description

used_key = "ts:{0}".format(args.dataset_serie)

if args.agg_type == "none" or args.agg_type == "None":
    baseline_values = redis_obj.execute_command(
        "TS.RANGE", used_key, baseline_date_unix_ts, baseline_end_date_unix_ts
    )
    if comparison_date_unix_ts is not None:
        print(comparison_date_unix_ts, comparison_end_date_unix_ts)
        comparison_values = redis_obj.execute_command(
            "TS.RANGE", used_key, comparison_date_unix_ts, comparison_end_date_unix_ts
        )

else:
    agg_string = ""
    if args.agg_type == "avg":
        agg_string = "average"
    elif args.agg_type == "max":
        agg_string = "maximum"
    elif args.agg_type == "min":
        agg_string = "minimum"

    title = "{0} - aggregated by function {1} with buckets of {2} seconds".format(
        title, agg_string, args.bucket_size_seconds
    )
    baseline_values = redis_obj.execute_command(
        "TS.RANGE",
        used_key,
        baseline_date_unix_ts,
        baseline_end_date_unix_ts,
        "AGGREGATION",
        args.agg_type,
        args.bucket_size_seconds,
    )
    if comparison_date_unix_ts is not None:
        comparison_values = redis_obj.execute_command(
            "TS.RANGE",
            used_key,
            comparison_date_unix_ts,
            comparison_end_date_unix_ts,
            "AGGREGATION",
            args.agg_type,
            args.bucket_size_seconds,
        )


xx1_pos = []
xx1 = []
yy1 = []

xx2_pos = []
xx2 = []
yy2 = []

x_pos = 1
for tuple_value in baseline_values:
    x = datetime.datetime.fromtimestamp(tuple_value[0])
    y = float(tuple_value[1].decode("utf-8"))
    xx1.append(x)
    yy1.append(y)
    xx1_pos.append(x_pos)
    x_pos = x_pos + 1

draw_comparison = False
if len(comparison_values) > 0:
    x_pos = 1
    for tuple_value in comparison_values:
        x = datetime.datetime.fromtimestamp(tuple_value[0])
        y = float(tuple_value[1].decode("utf-8"))
        xx2.append(x)
        yy2.append(y)
        xx2_pos.append(x_pos)
        x_pos = x_pos + 1
    draw_comparison = True

if draw_comparison:
    figure, (ax1, ax2, ax3) = plt.subplots(3, sharex=False, sharey=True)

    ax1.plot(
        xx1,
        yy1,
        "b+",
        label="Baseline :: {} to {}".format(
            baseline_date.strftime("%Y-%m-%d"), baseline_end_date.strftime("%Y-%m-%d")
        ),
    )
    ax1.legend(loc="upper right")
    ax1.set_xlabel("time")
    ax1.set_ylabel(y_label)
    ax1.set_title("{}".format(title))

    ax2.plot(
        xx2,
        yy2,
        "rx",
        label="Comparison :: {} to {}".format(
            comparison_date.strftime("%Y-%m-%d"),
            comparison_end_date.strftime("%Y-%m-%d"),
        ),
    )
    ax2.legend(loc="upper right")
    ax2.set_xlabel("time")
    ax2.set_ylabel(y_label)

    ax3.plot(
        xx1_pos,
        yy1,
        "b+",
        label="Baseline :: {} to {}".format(
            baseline_date.strftime("%Y-%m-%d"), baseline_end_date.strftime("%Y-%m-%d")
        ),
    )
    ax3.plot(
        xx2_pos,
        yy2,
        "rx",
        label="Comparison :: {} to {}".format(
            comparison_date.strftime("%Y-%m-%d"),
            comparison_end_date.strftime("%Y-%m-%d"),
        ),
    )
    ax3.legend(loc="upper right")
    ax3.set_xlabel("# sample")
    ax3.set_ylabel(y_label)
    figure.set_size_inches(18.5, 10.5, forward=True)
    plt.subplots_adjust(
        left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.45
    )
    plt.show()

else:
    figure, (ax1) = plt.subplots(1, sharex=False, sharey=True)

    ax1.plot(
        xx1,
        yy1,
        "b+",
        label="From {} to {}".format(
            baseline_date.strftime("%Y-%m-%d"), baseline_end_date.strftime("%Y-%m-%d")
        ),
    )
    ax1.legend(loc="upper right")
    ax1.set_xlabel("time")
    ax1.set_ylabel(y_label)
    ax1.set_title("{}".format(title))

    figure.set_size_inches(18.5, 10.5, forward=True)
    plt.subplots_adjust(
        left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.45
    )
    plt.show()
