from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
import pytz

class Pickupdate:
    def __init__(self):

 

        self.user = 'postgres'
        self.password = 'Oct2018!'
        self.database_name = 'medicaid'

        self.database_url = 'postgresql://{user}:{password}@localhost/{database_name}'.format(
            user=self.user,
            password=self.password,
            database_name=self.database_name,
        )

        self.engine = create_engine(self.database_url, echo=False)

    def check_alert_test(self, days, alert_priority, alert_id):

        sql = """SELECT * FROM application_applicationtracking;"""
        sql2 = """SELECT * FROM application_resident;"""
        sql3 = """SELECT * FROM application_alerttype;"""

        df = pd.read_sql(sql, con=self.engine)
        df2 = pd.read_sql(sql2, con=self.engine)
        df3 = pd.read_sql(sql3, con=self.engine)
        print(df['medicaid_pickup_date'].dt.tz_convert('en_us'))
        # remove after implemented
       
        shift= pd.TimedeltaIndex(90 - (df['medicaid_pickup_date'].dt.day),unit='D')
        print(shift)
        # shift= pd.TimedeltaIndex(90+pd.to_datetime((df['medicaid_pickup_date'] + pd.DateOffset(days = 90)).dt.daysinmonth-(df['medicaid_pickup_date'] + pd.DateOffset(days = 90)).dt.day, unit = "D"),utc = True)
        # df["medicaid_pickup_deadline"]=df['medicaid_pickup_date']+ shift

        # alert_table = pd.merge(df, df2, how = 'inner', on="resident_id")
        # alert_table["alert_type_id"] = 0
        # alert_table["alert_message"] = ""
        # alert_table["alert_priority"]= 0
        # alert_table["alert_status"] = False

        # alert_table= alert_table.rename(index = str , columns = {'tracking_id':'application_id'})
        # cols = {"a":"alert_priority","b":"alert_status","c":"alert_message","d":"alert_type_id","e":"application_id","f":"resident_id"}
        # for i in range(0,100):

        #     alert_table["daysLeft"] = (alert_table["medicaid_pickup_deadline"]-pd.to_datetime(pytz.utc.localize(datetime.now()+ timedelta(days=i)))).dt.days
        #     if days > 0:
        #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_type_id"]] = alert_id
        #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_message"]] = str(days) + " Days to Application Due"
        #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_priority"]] = alert_priority
        #     elif days == 0:
        #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_type_id"]] = alert_id
        #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_message"]] = "Application Due"
        #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_priority"]] = alert_priority
        #     else:
        #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_type_id"]] = alert_id
        #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_message"]] = "Application Overdue"
        #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_priority"]] = alert_priority
        #     alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days),(cols.values())].\
        #     to_sql("application_alert",self.engine,if_exists = 'append', index = False)

    # def check_alert(self, days, alert_priority, alert_id):

    #     sql = """SELECT * FROM application_applicationtracking;"""
    #     sql2 = """SELECT * FROM application_resident;"""
    #     sql3 = """SELECT * FROM application_alerttype;"""

    #     df = pd.read_sql(sql, con=self.engine)
    #     df2 = pd.read_sql(sql2, con=self.engine)
    #     df3 = pd.read_sql(sql3, con=self.engine)
    #     print(df3)
    #     shift= pd.TimedeltaIndex(90+(df['medicaid_pickup_date'] + pd.DateOffset(days = 90)).dt.daysinmonth-(df['medicaid_pickup_date'] + pd.DateOffset(days = 90)).dt.day, unit = "D")
    #     df["medicaid_pickup_deadline"]=df['medicaid_pickup_date']+ shift

    #     alert_table = pd.merge(df, df2, how = 'inner', on="resident_id")
    #     alert_table["alert_type_id"] = 0
    #     alert_table["alert_message"] = ""
    #     alert_table["alert_priority"]= 0
    #     alert_table["alert_status"] = False

    #     alert_table= alert_table.rename(index = str , columns = {'tracking_id':'application_id'})
    #     cols = {"a":"alert_priority","b":"alert_status","c":"alert_message","d":"alert_type_id","e":"application_id","f":"resident_id"}

    #     alert_table["daysLeft"] = (alert_table["medicaid_pickup_deadline"]-pd.to_datetime(pytz.utc.localize(datetime.now()+ timedelta(days=i)))).dt.days
    #     if days > 0:
    #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_type_id"]] = alert_id
    #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_message"]] = str(days) + " Days to Application Due"
    #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_priority"]] = alert_priority
    #     elif days == 0:
    #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_type_id"]] = alert_id
    #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_message"]] = "Application Due"
    #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_priority"]] = alert_priority
    #     else:
    #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_type_id"]] = alert_id
    #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_message"]] = "Application Overdue"
    #         alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days) ,["alert_priority"]] = alert_priority
    #     alert_table.loc[(alert_table.phase_id == 3)&(alert_table.daysLeft == days),(cols.values())].\
    #     to_sql("application_alert",self.engine,if_exists = 'append', index = False)



pud = Pickupdate().check_alert_test(90,1,1)
pud = Pickupdate().check_alert_test(60,1,2)
pud = Pickupdate().check_alert_test(45,2,3)
pud = Pickupdate().check_alert_test(30,3,4)
pud = Pickupdate().check_alert_test(15,4,5)
pud = Pickupdate().check_alert_test(0,5,6)
pud = Pickupdate().check_alert_test(-1,5,7)
