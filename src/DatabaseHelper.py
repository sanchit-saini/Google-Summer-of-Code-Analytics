import mongoengine
from YearSupport import *
from Records import *


class DatabaseHelper:

    db_name = 'gsoc'
    year_support = YearSupport()

    def __init__(self):
        mongoengine.connect(self.db_name)

    def __del__(self):
        mongoengine.disconnect()

    def insert(self, **kwds):

        if self.year_support.check_year_support(kwds['year']):
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
