import os
import logging
from records import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


logging.basicConfig(format='%(module)s : %(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class DatabaseHelper:
    def __init__(self):
        path = os.path.dirname(__file__) + '/../../Database/gsoc_records.db'
        db = 'sqlite:///' + os.path.join(os.path.abspath(path))
        self.engine = create_engine(db)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __del__(self):
        self.session.commit()

    def insert(self, record):
        self.session.add(record)

    def create_database(self):
        Base.metadata.create_all(self.engine)
