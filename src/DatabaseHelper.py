import mongoengine
from YearSupport import *
from Records import *


class DatabaseHelper:

    dbName = 'gsoc'
    yearSupport = YearSupport()

    def __init__(self):
        mongoengine.connect(self.dbName)

    def __del__(self):
        mongoengine.disconnect()

    def insert(self, **kwds):

        if self.yearSupport.checkYearSupport(kwds['year']):
            Records(
                name=kwds['name'],
                slots=kwds['slots'],
                year=kwds['year']
            ).save()

        else:
            Records(
                name=kwds['name'],
                slots=kwds['slots'],
                tagline=kwds['tagline'],
                technologies=kwds['technologies'],
                year=kwds['year']
            ).save()
