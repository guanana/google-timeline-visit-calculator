#!/usr/bin/env python3

# Copyright 2021 @guanana
# https://github.com/guanana/google-timeline-visit-calculator
# Thanks to Gerwin Sturm for inspiration:
# https://github.com/Scarygami
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys
from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime, timedelta


def _valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise ArgumentTypeError(msg)


def _valid_time(s):
    try:
        return datetime.strptime(s, "%H:%M")
    except ValueError:
        msg = "Not a valid time: '{0}'.".format(s)
        raise ArgumentTypeError(msg)


def process_input(record):
    timestamp = int(record["timestampMs"]) / 1000
    latitude = float(record["latitudeE7"]) / 1e7
    longitude = float(record["longitudeE7"]) / 1e7

    return int(timestamp), float(latitude), float(longitude)


def write_json(out_file, timestamp, latitude, longitude):
    record = {
            "timestamp": timestamp,
            "latitude": latitude,
            "longitude": longitude
        }
    out_file.write(json.dumps(record, separators=(',', ':')))


def parsing(output, *raw_args):
    added = 0
    args = vars(raw_args[0])
    #Reading file
    try:
        with open(args["input"], "r") as f:
            json_raw = f.read()
    except OSError as e:
        print(f"Error opening input file {args['input']}: {e}")
        return
    except MemoryError:
        print("File too big, try to reduce the size")
        return

    try:
        data = json.loads(json_raw)
    except ValueError as e:
        print(f"Error decoding json: {e}")
        return
    output.write("{\"locations\":[")

    for item in data["locations"]:
        if "longitudeE7" not in item or "latitudeE7" not in item or "timestampMs" not in item:
            continue
        timestamp_parsed, latitude_parsed, longitude_parsed = process_input(item)
        print(f'\r{datetime.fromtimestamp(timestamp_parsed)}: Locations written: {added}', end="")
        item_time = datetime.fromtimestamp(timestamp_parsed)
        if args["start_date"] and item_time < args["start_date"]:
            continue
        if args["end_date"] and item_time > args["end_date"]:
            continue
        if args["accuracy"] and item["accuracy"] > args["accuracy"]:
            continue
        if item["source"] == "network":
            item["source"] = "CELL"
        if args["source"] and item["source"].upper() != args["source"]:
            continue

        if added != 0:
            output.write(",")
        write_json(output, timestamp_parsed, latitude_parsed, longitude_parsed)
        added +=1
    output.write("]}")
    output.close()


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-i", "--input", help="Input File (Location History.json)", default="Location History.json")
    arg_parser.add_argument("-o", "--output", help="Output File", default="location_processed.json")

    arg_parser.add_argument("-s", "--start_date", help="The Start Date - format YYYY-MM-DD (defaults to 0h00m)", type=_valid_date)
    arg_parser.add_argument("-e", "--end_date", help="The End Date - format YYYY-MM-DD (defaults to 23h59m59s)", type=_valid_date)
    arg_parser.add_argument("--start_time", help="The Start Time - format HH:MM, only used if Start Date is set", type=_valid_time)
    arg_parser.add_argument("--end_time", help="The End Time - format HH:MM, only used if End Date is set", type=_valid_time)
    arg_parser.add_argument("-a", "--accuracy", help="Maximum accuracy (in meters), lower is better.", type=int)

    arg_parser.add_argument(
        "-x", "--source",
        choices=["GPS", "CELL", "WIFI"],
        help="If you only care about data collected with specific source, like GPS, CELL, WIFI"
    )

    args = arg_parser.parse_args()

    if args.input == args.output:
        arg_parser.error("Input and output have to be different files")
        return

    try:
        f_out = open(args.output, "w")
    except OSError as error:
        print("Error creating output file for writing: %s" % error)
        return

    if args.start_date and args.start_time:
        args.start_date = args.start_date + timedelta(hours=args.start_time.hour,minutes=args.start_time.minute)

    if args.end_date:
        if args.end_time:
            args.end_date = args.end_date + timedelta(hours=args.end_time.hour,minutes=args.end_time.minute) - timedelta(microseconds=1)
        else:
            args.end_date = args.end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    parsing(f_out, args)

    f_out.close()


if __name__ == "__main__":
    sys.exit(main())
