from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from Records import *
import configparser
import logging

logging.basicConfig(format='%(module)s : %(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class DatabaseHelper:

    config = configparser.ConfigParser()
    config.read('config')
    if 'db' not in config['DEFAULT']:
        logger.error('config not loaded!')
        exit(1)
    db = config['DEFAULT'].get('db')
    engine = create_engine(db)

    def __init__(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def __del__(self):
        self.session.commit()

    def insert(self, record):
        self.session.add(record)
    
    def create_database(self):
        Base.metadata.create_all(self.engine)
