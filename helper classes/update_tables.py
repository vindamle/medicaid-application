
import pandas as pd
from sqlalchemy import *

from dotenv import load_dotenv
from os.path import join, dirname, os
from datetime import datetime


dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

user = os.getenv("POSTGRES_USERNAME")
password = os.getenv("POSTGRES_PASSWORD")
database_name = os.getenv("POSTGRES_DATABASE")

database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
    user=user,
    password=password,
    database_name=database_name,
)

engine = create_engine(database_url, echo=False)
query = 'SELECT * FROM application_patient'
pd.read_sql()
