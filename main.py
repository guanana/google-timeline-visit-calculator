#!/usr/bin/env python3

# Copyright 2021 @guanana
# https://github.com/guanana/google-timeline-visit-calculator

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
from argparse import ArgumentParser
from datetime import datetime
from geopy.point import Point
import location_helpers, Visits, Timeline


def main():
    arg_parser = ArgumentParser(description='Process Google Timeline data from a previously formatted file '
                                            'only containing one key, {"locations":[ and elements to parse with '
                                            'timestamp, latitude and longitude. '
                                            'ie: {"locations":[{"timestamp":1436144486,"latitude":45.4594378,"longitude":1.2674159}]}')
    arg_parser.add_argument("-i", "--input", help="Input parsed file", default="location_processed.json")
    arg_parser.add_argument(
        "--no_show_visits",
        help="If you want to disable visits details",
        action='store_true',
        default=False
    )
    arg_parser.add_argument(
        "--disable_output",
        help="Output to file is by default, if you set this you'll disable it",
        action='store_true',
        default=False
    )
    arg_parser.add_argument("-o", "--output_file", help="Output file name", default="visits.json")
    arg_parser.add_argument("-r", "--radius", help="Min movement in KM to consider it a visit", default=120)
    arg_parser.add_argument(
        "-t",
        "--min_time_consider",
        help="Min time to record a visit, time will be regardless added to country",
        default=43200
    )
    args = arg_parser.parse_args()
    if not args.disable_output:
        try:
            out_file = open(args.output_file, "w")
        except OSError as e:
            print(f"Error creating output file: {e}")
            print(f"Continuing only with stdout output")
            out_file = None
    else:
        out_file = None

    my_timeline = Timeline.Timeline(args.no_show_visits, out_file, args.min_time_consider)

    with open(args.input) as json_file:
        data = json.load(json_file)

    xrecords = 0
    for raw_data in data["locations"]:
        point = Point(raw_data["latitude"], raw_data["longitude"])
        if xrecords != 0:
            # Avoid doing hundreds of API calls per day
            if not visit_object.big_change(point):
                xrecords += 1
                continue
            # Stop for 1sec and 1/2 to avoid overloading geolocator API
            # We are here because there's been a change big enough in Coord
            Visits.close_visit(visit_object, xrecords, raw_data["timestamp"])
            Timeline.add_visit_to_timeline(my_timeline, visit_object)

        geo_location, country_code = location_helpers.get_location(point)
        country_object = my_timeline.add_country(country_code)
        visit_object = Visits.new_visit(raw_data["timestamp"], country_object, point, args.radius)
        country_name, city, postcode = location_helpers.get_details(geo_location, raw_data, point, country_code)
        visit_object.add_details(country_name, city, postcode)
        xrecords = 1
        print(f"\r{datetime.fromtimestamp(raw_data['timestamp'])}: New Locations written: {country_code}", end="")
    return my_timeline


if __name__ == "__main__":
    sys.exit(main().final())
