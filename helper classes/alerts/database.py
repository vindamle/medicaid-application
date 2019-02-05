"""
This class pulls gets data from psql database
"""
from sqlalchemy import create_engine
from os.path import join, dirname, os
from dotenv import load_dotenv



class Database:

    def __init__(self):

        dotenv_path = join(dirname(__file__), '../../.env')
        load_dotenv(dotenv_path)

        self.user =  os.getenv("POSTGRES_USERNAME")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.database_name = os.getenv("POSTGRES_DATABASE")

        # self.user = 'marc'
        # self.password ='Aug.2018'
        # self.database_name = 'medicaid'

        self.database_url = 'postgresql://{user}:{password}@localhost/{database_name}'.format(
            user=self.user,
            password=self.password,
            database_name=self.database_name,
        )

        self.engine = create_engine(self.database_url, echo=False)

    def get_engine(self):
        return self.engine
