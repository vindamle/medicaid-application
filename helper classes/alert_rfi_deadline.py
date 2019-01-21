from datetime import datetime, timedelta, timezone,tzinfo
import pandas as pd
from sqlalchemy import create_engine
import pytz

class RFIDeadline:
    def __init__(self):

        self.user = 'marc'
        self.password = 'Aug.2018'
        self.database_name = 'medicaid'

        self.database_url = 'postgresql://{user}:{password}@localhost/{database_name}'.format(
            user=self.user,
            password=self.password,
            database_name=self.database_name,
        )

        self.engine = create_engine(self.database_url, echo=False)

    def check_alerts_test(self, day):
        sql = """SELECT * FROM application_application;"""
        sql2 = """SELECT * FROM application_resident;"""
        sql3 = """SELECT * FROM application_response;"""
        sql4 = """SELECT * FROM application_rfi;"""

        df = pd.read_sql(sql, con=self.engine)
        df2 = pd.read_sql(sql2, con=self.engine)
        df3 = pd.read_sql(sql3, con=self.engine)
        df4 = pd.read_sql(sql4, con=self.engine)

        # print(list(df),list(df2),list(df3),list(df4))

        alert_table  = pd.merge(df2, pd.merge(df , pd.merge(df3, df4, how = 'inner', on = 'response_id'), how = 'inner', on = 'application_id'), how = 'inner', on = 'resident_id')


        cols = {"a":"alert_priority","b":"alert_status","d":"alert_type_id","e":"application_id","f":"resident_id"}

        alert_table["alert_type_id"] = 0
        alert_table["alert_message"] = ""
        alert_table["alert_priority"]= 0
        alert_table["alert_status"] = False

        alert_table= alert_table.rename(index = str , columns = {'tracking_id':'application_id'})

        for i in range(1, 30):
            alert_table["alert_date"] = (alert_table['rfi_due_date']-pytz.utc.localize(datetime.now()+timedelta(days = i ))).dt.days
            if day == 10:
                alert_table.loc[(alert_table.phase_id == 5)&(alert_table.alert_date == day)&(alert_table.document_id.isna()), ["alert_type_id"]] = 9
                alert_table.loc[(alert_table.phase_id == 5)&(alert_table.alert_date == day)&(alert_table.document_id.isna()),["alert_priority"]] = 4
                alert_table.loc[(alert_table.phase_id == 5)&(alert_table.alert_date == day)&(alert_table.document_id.isna()),["alert_message"]] = "RFI Due in 10 days"
            elif day == 0:
                alert_table.loc[(alert_table.phase_id == 5)&(alert_table.alert_date == day)&(alert_table.document_id.isna()), ["alert_type_id"]] = 10
                alert_table.loc[(alert_table.phase_id == 5)&(alert_table.alert_date == day)&(alert_table.document_id.isna()),["alert_priority"]] = 5
                alert_table.loc[(alert_table.phase_id == 5)&(alert_table.alert_date == day)&(alert_table.document_id.isna()),["alert_message"]] = "RFI Due Today"
            elif day == -1:
                alert_table.loc[(alert_table.phase_id == 5)&(alert_table.alert_date == day)&(alert_table.document_id.isna()), ["alert_type_id"]] = 11
                alert_table.loc[(alert_table.phase_id == 5)&(alert_table.alert_date == day)&(alert_table.document_id.isna()),["alert_priority"]] = 5
                alert_table.loc[(alert_table.phase_id == 5)&(alert_table.alert_date == day)&(alert_table.document_id.isna()),["alert_message"]] = "RFI Overdue"
            alert_table.loc[(alert_table.phase_id == 5)&(alert_table.alert_date == day)&(alert_table.document_id.isna()),(cols.values())].\
            to_sql("application_alert",self.engine,if_exists = 'append', index = False)

RFIDeadline().check_alerts_test(10)
RFIDeadline().check_alerts_test(0)
RFIDeadline().check_alerts_test(-1)
