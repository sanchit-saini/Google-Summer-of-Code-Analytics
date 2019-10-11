from mongoengine import *


class Records(Document):
    name = StringField(required=True)
    slots = IntField(required=True)
    tagline = StringField()
    technologies = StringField()
    year = IntField(required=True)
