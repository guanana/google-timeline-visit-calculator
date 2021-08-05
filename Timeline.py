import json
import sys

from Countries import Countries


class Timeline:
    def __init__(self, no_show_visits=False, output_file=None, min_time_consider=43200):
        self.countries = {}
        self.show_visits = not no_show_visits
        self.output_file = output_file
        self.min_total_time_to_print = min_time_consider

    def add_country(self, country_code):
        try:
            self.countries[country_code]
        except KeyError:
            self.countries.update({country_code: Countries(country_code)})

    def add_finished_visit_time(self, visit):
        self.countries[visit.country].add_visit_time(visit)

    def add_finished_to_list(self, visit):
        self.countries[visit.country].add_visit_to_list(visit)

    def __str__(self):
        s = "\n"
        s += "Finish processing\n"
        s += "-----------------\n"
        for code, countries in self.countries.items():
            if countries.total_time > self.min_total_time_to_print:
                s += f"Total seconds in {code}: {countries.total_time}\n"
                s += f"Total days in {code}: {countries.total_time / 86400}\n"
                s += f"Total years in {code}: {countries.total_time / 3.154e+7}\n"
                s += "----------\n"
                if self.show_visits:
                    s += "==VISITS==\n"
                    for idx, visits in enumerate(countries.visits):
                        s += f"Visit {idx}: {visits}\n"
                    s += "==========\n"
        s += "-----------------\n"
        return s

    def write_file(self):
        record = {}
        for code, countries in self.countries.items():
            if countries.total_time > self.min_total_time_to_print:
                record.update({
                    code: {
                        "time": countries.total_time
                    }
                })
                if countries.visits and self.show_visits:
                    record[code].update({"visits": {}})
                    for idx, visit in enumerate(countries.visits):
                        visit = vars(visit)
                        visit.pop("radius")
                        visit["initial_point"] = {
                         "latitude": visit["initial_point"].latitude,
                         "longitude": visit["initial_point"].longitude
                        }
                        record[code]["visits"].update({idx: visit})
        self.output_file.write(json.dumps(record, separators=(',', ':')))
        self.output_file.close()

    def final(self):
        print(self)
        if self.output_file:
            self.write_file()


def add_visit_to_timeline(timeline, visit):
    # Add time to country regardless
    timeline.add_finished_visit_time(visit)
    # Add visit to final list of visits just if it's at least X long
    if visit.get_total_visit_time() > timeline.min_total_time_to_print:
        timeline.add_finished_to_list(visit)
