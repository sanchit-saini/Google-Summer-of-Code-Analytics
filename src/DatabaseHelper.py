import mongoengine
from Records import *


class DatabaseHelper:

    db_name = 'gsoc'

    def __init__(self):
        mongoengine.connect(self.db_name)

    def __del__(self):
        mongoengine.disconnect()

    def insert(self, **kwds):

        Records(
            name=kwds['name'],
            slots=kwds['slots'],
            tagline=kwds['tagline'],
            technologies=kwds['technologies'],
            year=kwds['year']
        ).save()
