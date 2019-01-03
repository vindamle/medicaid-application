from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
import pytz

class RFIDeadline:
    def __init__(self):

        self.user = 'postgres'
        self.password = 'Aug.2018'
        self.database_name = 'medicaid'

        self.database_url = 'postgresql://{user}:{password}@localhost/{database_name}'.format(
            user=self.user,
            password=self.password,
            database_name=self.database_name,
        )

        self.engine = create_engine(self.database_url, echo=False)

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

        alert_table= alert_table.rename(index = str , columns = {'tracking_id':'application_id'})
        print(list(alert_table))
        # for i in range(1, 30):
        #     alert_table.loc[(alert_table.phase_id == 4)&(alert_table.alert_date == 30) ,["alert_message"]] = "No Medicaid Response in 30 Days"
        #     alert_table.loc[(alert_table.phase_id == 4)&(alert_table.alert_date == 30) ,["alert_priority"]] = 3
        #     alert_table.loc[(alert_table.phase_id == 4)&(alert_table.alert_date == 30),(cols.values())].\
        #     to_sql("application_alert",self.engine,if_exists = 'append', index = False)

RFIDeadline().check_alerts_test()
