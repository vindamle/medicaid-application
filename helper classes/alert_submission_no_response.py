from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
import pytz

class NoResponse:
    def __init__(self):

         # dotenv_path = join(dirname(__file__), '../.env')
        # load_dotenv(dotenv_path)

        # self.database = os.getenv("POSTGRES_DATABASE")
        # self.username = os.getenv("POSTGRES_USERNAME")
        # self.password = os.getenv("POSTGRES_PASSWORD")
        # self.hostname = os.getenv("POSTGRES_HOSTNAME")

        self.user = 'postgres'
        self.password = 'Oct.2018'
        self.database_name = 'medicaid'

        self.database_url = 'postgresql://{user}:{password}@localhost/{database_name}'.format(
            user=self.user,
            password=self.password,
            database_name=self.database_name,
        )

        self.engine = create_engine(self.database_url, echo=False)

    def check_alerts(self):
        sql = """SELECT * FROM application_applicationtracking;"""
        sql2 = """SELECT * FROM application_resident;"""

        df = pd.read_sql(sql, con=self.engine)
        df2 = pd.read_sql(sql2, con=self.engine)

        alert_table = pd.merge(df, df2, how = 'inner', on="resident_id")
        alert_table["alert_type_id"] = 0
        alert_table["alert_message"] = ""
        alert_table["alert_priority"]= 0
        alert_table["alert_status"] = False

        alert_table["alert_date"] = (pytz.utc.localize(datetime.now())-alert_table['date_of_medicaid_submission']).dt.days
        alert_table= alert_table.rename(index = str , columns = {'tracking_id':'application_id'})
        cols = {"a":"alert_priority","b":"alert_status","c":"alert_message","d":"alert_type_id","e":"application_id","f":"resident_id"}
        alert_table.loc[(alert_table.phase_id == 4)&(alert_table.alert_date == 30) ,["alert_type_id"]] = 8
        alert_table.loc[(alert_table.phase_id == 4)&(alert_table.alert_date == 30) ,["alert_message"]] = "No Medicaid Response in 30 Days"
        alert_table.loc[(alert_table.phase_id == 4)&(alert_table.alert_date == 30) ,["alert_priority"]] = 3
        alert_table.loc[(alert_table.phase_id == 4)&(alert_table.alert_date == 30),(cols.values())].\
        to_sql("application_alert",self.engine,if_exists = 'append', index = False)

    def check_alerts_test(self):
        sql = """SELECT * FROM application_applicationtracking;"""
        sql2 = """SELECT * FROM application_resident;"""

        df = pd.read_sql(sql, con=self.engine)
        df2 = pd.read_sql(sql2, con=self.engine)

        alert_table = pd.merge(df, df2, how = 'inner', on="resident_id")
        alert_table["alert_type_id"] = 0
        alert_table["alert_message"] = ""
        alert_table["alert_priority"]= 0
        alert_table["alert_status"] = False

        for i in range(1, 30):
            alert_table["alert_date"] = (pytz.utc.localize(datetime.now()+timedelta(days = i ))-alert_table['date_of_medicaid_submission']).dt.days
            alert_table= alert_table.rename(index = str , columns = {'tracking_id':'application_id'})
            cols = {"a":"alert_priority","b":"alert_status","c":"alert_message","d":"alert_type_id","e":"application_id","f":"resident_id"}
            alert_table.loc[(alert_table.phase_id == 4)&(alert_table.alert_date == 30) ,["alert_type_id"]] = 8
            alert_table.loc[(alert_table.phase_id == 4)&(alert_table.alert_date == 30) ,["alert_message"]] = "No Medicaid Response in 30 Days"
            alert_table.loc[(alert_table.phase_id == 4)&(alert_table.alert_date == 30) ,["alert_priority"]] = 3
            alert_table.loc[(alert_table.phase_id == 4)&(alert_table.alert_date == 30),(cols.values())].\
            to_sql("application_alert",self.engine,if_exists = 'append', index = False)

NoResponse().check_alerts_test()
