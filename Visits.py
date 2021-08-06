from datetime import datetime
from geopy import distance
from google_calendar import create_link


class Visits:
    def __init__(self, country, point, radius):
        self.city = None
        self.postcode = None
        self.country_name = None
        self.initial_date = None
        self.final_date = None
        self.initial_point = point
        self.records = 1
        self.country = country
        self.radius = radius
        self.visit_link = ""

    def __str__(self):
        return f"\n---\n" \
               f"Country: {self.country_name}\n" \
               f"City: {self.city}\n" \
               f"Arrival: {datetime.fromtimestamp(self.initial_date)}({self.initial_date})\n" \
               f"Departure: {datetime.fromtimestamp(self.final_date)}({self.final_date})\n" \
               f"Google Calendar Link: {self.visit_link}" \
               f"---"

    def start_count(self, timestamp):
        self.initial_date = timestamp

    def stop_count(self, timestamp):
        self.final_date = timestamp
        self.visit_link = create_link(self)

    def add_records(self, xtimes):
        self.records = xtimes

    def get_total_visit_time(self):
        return self.final_date - self.initial_date

    def big_change(self, new_point):
        if distance.great_circle(self.initial_point[:2], new_point[:2]).km < self.radius:
            return False
        return True

    def add_details(self, country_name, city, postcode):
        self.city = city
        self.postcode = postcode
        self.country_name = country_name

def new_visit(timestamp, new_country, point, radius):
    new_visit_object = Visits(new_country, point, radius)
    new_visit_object.start_count(timestamp)
    return new_visit_object


def close_visit(visit, xrecords, final_timestamp):
    visit.stop_count(final_timestamp)
    visit.add_records(xrecords)
