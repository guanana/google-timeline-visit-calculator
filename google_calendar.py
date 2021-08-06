import urllib
from datetime import datetime
from urllib.parse import urlencode


def create_link(visit):
    _GCAL_HEADER = "https://calendar.google.com/calendar/r/eventedit?"
    utc_initial = datetime.fromtimestamp(visit.initial_date).strftime('%Y%m%dT%H%M%SZ')
    utc_final = datetime.fromtimestamp(visit.final_date).strftime('%Y%m%dT%H%M%SZ')
    string = f'text={urllib.parse.quote(visit.country_name)}&' \
             f'details={urllib.parse.quote(f"Visit to country {visit.country.country_code}")}&' \
             f'location={urllib.parse.quote(f"{visit.city}, {visit.postcode}, {visit.country.country_code}")}&' \
             f'dates={utc_initial}/{utc_final}'
    result = f"{_GCAL_HEADER}{string}"
    return result
