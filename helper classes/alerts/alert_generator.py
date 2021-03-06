from datetime import datetime, timedelta, date
import pandas as pd
import pytz

class Generate_Alert:

    def __init__(self):
        self.alerts = []

    def pick_up_date_alert(self, data, alert_data):

        alert_columns = {
            "priority":"alert_priority",
            "status":"alert_status",
            "type_id":"alert_type_id",
            "application":"application_id",
            "resident_id":"resident_id",
            "alert_id":"alert_id"
        }
        numdays = 90+ (data['medicaid_pickup_date'] + pd.DateOffset(days = 90)).dt.daysinmonth
        days_used = (data['medicaid_pickup_date']+ pd.DateOffset(days = 90)).dt.day
        dates = numdays-days_used



        data["medicaid_pickup_deadline"]=pd.to_datetime(data['medicaid_pickup_date'],utc = True)+ pd.TimedeltaIndex(data = dates, unit = "D")
        day_alerts = [90, 60, 45, 30, 15, 0, -1]

        # Remove Loop For CRON JOB
        # Remove timedelta(days = i) For CRON JOB

        # for i in range(30,60):
        data["daysLeft"] = (data["medicaid_pickup_deadline"]-pd.to_datetime(pytz.utc.localize(datetime.now()+ timedelta(days=0)))).dt.days

        alerts = pd.merge(data,alert_data, how = 'left', on = 'resident_id',suffixes = ('','_y'))
        print(alerts.loc[:,("phase_id", 'alert_status_y', 'alert_id')])
        alerts.loc[(alerts.phase_id == 3)&(alerts.daysLeft == 90)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 1
        alerts.loc[(alerts.phase_id == 3)&(alerts.daysLeft == 60)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 2
        alerts.loc[(alerts.phase_id == 3)&(alerts.daysLeft == 45)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 3
        alerts.loc[(alerts.phase_id == 3)&(alerts.daysLeft == 30)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 4
        alerts.loc[(alerts.phase_id == 3)&(alerts.daysLeft == 15)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 5
        alerts.loc[(alerts.phase_id == 3)&(alerts.daysLeft ==  0)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 6
        alerts.loc[(alerts.phase_id == 3)&(alerts.daysLeft == -1)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 7

        self.alerts += alerts.loc[(alerts.phase_id == 3)&(alerts.daysLeft.isin(day_alerts))&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,alert_columns.values()].to_dict('records')
        print('*' * 50)
        print(self.alerts)

        return self.alerts

    def rfi_alert(self, data, alert_data):

        alert_columns = {
            "priority":"alert_priority",
            "status":"alert_status",
            "type_id":"alert_type_id",
            "application":"application_id",
            "resident_id":"resident_id",
            "alert_id":"alert_id"
        }

        day_alerts = [-10,-20, -21]

        # Remove Loop For CRON JOB
        # Remove timedelta(days = i) For CRON JOB

        # for i in range(30):
        data["daysLeft"] = (data["rfi_due_date"]-pd.to_datetime(pytz.utc.localize(datetime.now()+ timedelta(days=0)))).dt.days
        print(data['daysLeft'])
        alerts = pd.merge(data,alert_data, how = 'left', on = 'application_id',suffixes = ('','_y'))

        alerts.loc[(alerts.phase_id == 5)&(alerts.daysLeft == -10)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 9
        alerts.loc[(alerts.phase_id == 5)&(alerts.daysLeft == -20)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 10
        alerts.loc[(alerts.phase_id == 5)&(alerts.daysLeft == -21)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 11

        self.alerts += alerts.loc[(alerts.phase_id == 5)&(alerts.daysLeft.isin(day_alerts))&((alerts.alert_status_y== False)|alerts.alert_id.isna()) ,alert_columns.values()].to_dict('records')

        return self.alerts

    def no_response_alert(self, data, alert_data):

        alert_columns = {
            "priority":"alert_priority",
            "status":"alert_status",
            "type_id":"alert_type_id",
            "application":"application_id",
            "resident_id":"resident_id",
            "alert_id":"alert_id"
        }
        day_alerts  = [30,]
        # for i in range(1000):
        data["alert_date"] = (pytz.utc.localize(datetime.now()+timedelta(days = 0 ))-data['date_of_application_submission']).dt.days
        alerts = pd.merge(data,alert_data, how = 'left', on = 'application_id',suffixes = ('','_y'))
        print(data["alert_date"])

        alerts.loc[(alerts.phase_id == 4)&(alerts.alert_date == 30)&((alerts.alert_status_y == False)|alerts.alert_id.isna()),["alert_type_id"]] = 8

        print(alerts.alert_date, alerts.phase_id)
        print(alerts.loc[(alerts.phase_id == 4)&(alerts.alert_date == 30.0)&((alerts.alert_status_y == False)|alerts.alert_id.isna()),["alert_type_id"]])

        self.alerts += alerts.loc[(alerts.phase_id == 4)&(alerts.alert_date.isin(day_alerts))&((alerts.alert_status_y == False)|alerts.alert_id.isna()),(alert_columns.values())].to_dict('records')
        # self.alerts += alerts.loc[(alerts.phase_id == 4)&(alerts.alert_date.isin(day_alerts))&((alerts.alert_status_y == False)|alerts.alert_id.isna()),(alert_columns.values())].to_dict('records')
        return self.alerts

    def meeting_deadline_alert(self, data, alert_data):
        alert_columns = {
            "priority":"alert_priority",
            "status":"alert_status",
            "type_id":"alert_type_id",
            "application":"application_id",
            "resident_id":"resident_id",
            "alert_id":"alert_id"
        }
        day_alerts = [3, 0, -1]

        # for i in range(5):

        data["daysLeft"] = (date.today()-data["application_creation_date"]).dt.days
        print(data["daysLeft"])
        alerts = pd.merge(data,alert_data, how = 'left', on = 'application_id',suffixes = ('','_y'))

        alerts.loc[(alerts.phase_id == 1)&(alerts.daysLeft == 0)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 12
        alerts.loc[(alerts.phase_id == 1)&(alerts.daysLeft ==  -3)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 13
        alerts.loc[(alerts.phase_id == 1)&(alerts.daysLeft == -4)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 14

        self.alerts += alerts.loc[(alerts.phase_id == 1)&(alerts.daysLeft.isin(day_alerts))&((alerts.alert_status_y== False)|alerts.alert_id.isna()) ,alert_columns.values()].to_dict('records')

        return self.alerts

    def recert_deadline_alert(self,data,alert_data):

        alert_columns = {
            "priority":"alert_priority",
            "status":"alert_status",
            "type_id":"alert_type_id",
            "application":"application_id",
            "resident_id":"resident_id",
            "alert_id":"alert_id"
        }


        data["medicaid_recert_deadline"]=(data['approval_recertification_date'] + pd.DateOffset(days = -90))
        day_alerts = [90, 60, 45, 30, 15, 0, -1]
        print(data["medicaid_recert_deadline"])
        # # Remove Loop For CRON JOB
        # # Remove timedelta(days = i) For CRON JOB
        #
        # for i in range(0,30):

        data["daysLeft"] = (data["approval_recertification_date"]-pd.to_datetime(pytz.utc.localize(datetime.now()+ timedelta(days=0)))).dt.days

        alerts = pd.merge(data,alert_data, how = 'left', on = 'resident_id',suffixes = ('','_y'))

        alerts.loc[(alerts.phase_id == 6)&(alerts.daysLeft == 90)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 15
        alerts.loc[(alerts.phase_id == 6)&(alerts.daysLeft == 60)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 16
        alerts.loc[(alerts.phase_id == 6)&(alerts.daysLeft == 45)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 17
        alerts.loc[(alerts.phase_id == 6)&(alerts.daysLeft == 30)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 18
        alerts.loc[(alerts.phase_id == 6)&(alerts.daysLeft == 15)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 19
        alerts.loc[(alerts.phase_id == 6)&(alerts.daysLeft ==  0)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 20
        alerts.loc[(alerts.phase_id == 6)&(alerts.daysLeft == -1)&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,"alert_type_id"] = 21

        self.alerts += alerts.loc[(alerts.phase_id == 6)&(alerts.daysLeft.isin(day_alerts))&((alerts.alert_status_y == False)|alerts.alert_id.isna()) ,alert_columns.values()].to_dict('records')

        return self.alerts
