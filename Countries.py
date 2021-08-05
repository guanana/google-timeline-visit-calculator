class Countries:
    def __init__(self, country_code):
        self.country_code = country_code
        self.total_time = 0
        self.visits = []

    def add_visit_time(self, visit):
        self.total_time = self.total_time + visit.get_total_visit_time()

    def add_visit_to_list(self, visit):
        self.visits.append(visit)
