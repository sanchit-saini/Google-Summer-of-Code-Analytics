from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Records(Base):
    __tablename__ = 'records'
    index = Column(Integer,primary_key=True)
    name = Column(String)
    slots = Column(Integer)
    tagline = Column(String)
    technologies = Column(String)
    year = Column(Integer)

    def __init__(self, name, slots, tagline, technologies, year):
        self.name = name
        self.slots = slots
        self.tagline = tagline
        self.technologies = technologies
        self.year = year
