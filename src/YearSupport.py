class YearSupport:

    start_year = 2009
    end_year = 2019
    old_year = 2015

    def get_start_year(self):
        return self.start_year

    def get_end_year(self):
        return self.end_year

    def get_old_year(self):
        return self.old_year

    def get_year_range(self):
        return str(self.start_year) + '-' + str(self.end_year)

    def check_year(self, year):
        if year >= self.start_year and year <= self.end_year:
            return year

        return None

    def check_year_support(self, year):
        if year >= self.start_year and year <= self.old_year:
            return True

        elif year > self.old_year and year <= self.end_year:
            return False
