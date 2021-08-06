import logging
import time
from geopy import Nominatim


geolocator = Nominatim(user_agent=f"google-timeline-visit-calculator")


def get_details(geo_location, raw_data, coord, country_code):
    try:
        country_name = geo_location.raw["address"]["country"]
    except (AttributeError, KeyError):
        logging.info(f"Unknown country details for {raw_data['timestamp']}: {coord}: {country_code}")
        country_name = "unknown"
    try:
        city = geo_location.raw["address"]["town"]
    except (AttributeError, KeyError):
        try:
            city = geo_location.raw["address"]["city"]
        except (AttributeError, KeyError):
            logging.info(f"Unknown city details for {raw_data['timestamp']}: {coord}: {country_code}")
            city = "unknown"
    try:
        postcode = geo_location.raw["address"]["postcode"]
    except (AttributeError, KeyError):
        logging.info(f"Unknown postcode details for {raw_data['timestamp']}: {coord}: {country_code}")
        postcode = "unknown"
    return country_name, city, postcode


def get_location(point):
    # Avoid possible overload of Nominatim service
    time.sleep(1.3)
    geo_location = geolocator.reverse(point, timeout=15)
    try:
        country_code = geo_location.raw["address"]["country_code"]
    except (ValueError, AttributeError):
        logging.error(f"Error with {point}")
        country_code = "unknown"
    return geo_location, country_code
