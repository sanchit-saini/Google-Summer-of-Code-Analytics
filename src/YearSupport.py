class YearSupport:

    startYear = 2009
    endYear = 2019
    oldYear = 2015

    def getStartYear(self):
        return self.startYear

    def getEndYear(self):
        return self.endYear

    def getOldYear(self):
        return self.oldYear

    def getYearRange(self):
        return str(self.startYear) + '-' + str(self.endYear)

    def checkYear(self, year):
        if year >= self.startYear and year <= self.endYear:
            return year

        return None

    def checkYearSupport(self, year):
        if year >= self.startYear and year <= self.oldYear:
            return True

        elif year > self.oldYear and year <= self.endYear:
            return False
