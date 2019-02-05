''' db.py '''

import sqlalchemy
from dotenv import load_dotenv
from os.path import join, dirname, os


''' Db '''
class Db:

    def __init__(self):
        ## load environment values from .env
        dotenv_path = join(dirname(__file__), '../../.env')
        load_dotenv(dotenv_path)

        self.database = os.getenv("POSTGRES_DATABASE")
        self.username = os.getenv("POSTGRES_USERNAME")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.hostname = os.getenv("POSTGRES_HOSTNAME")
        self.port = os.getenv("POSTGRES_PORT")

    def connect_postgres(self):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(
            self.username,
            self.password,
            self.hostname,
            self.port,
            self.database
        )

        # The return value of create_engine() is our connection object
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        meta = sqlalchemy.MetaData(bind=con, reflect=True)

        return con, meta

    def get_all_tables(self, meta):
        for table in meta.tables:
            print(table)
