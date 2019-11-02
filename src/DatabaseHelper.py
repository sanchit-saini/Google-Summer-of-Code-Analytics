from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from Records import *

class DatabaseHelper:
    db_name = 'sqlite:///gsoc_records.db'
    engine = create_engine(db_name)

    def __init__(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __del__(self):
        self.session.commit()

    def insert(self, record):
        self.session.add(record)
    
    def create_database(self):
        Base.metadata.create_all(self.engine)
