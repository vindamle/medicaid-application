
import pandas as pd
from sqlalchemy import create_engine


class Queries:

    def __init__(self, engine):
        self.engine = engine

    def pick_up_date_data(self):
        application_table = """SELECT * FROM application_application;"""
        resident_table = """SELECT * FROM application_resident;"""

        data = pd.merge(
            left =pd.read_sql(application_table, con=self.engine),
            right = pd.read_sql(resident_table, con=self.engine),
            how = 'inner',
            on="resident_id"
        )

        data["alert_type_id"] = 1
        data["alert_message"] = ""
        data["alert_priority"]= 0
        data["alert_status"] = False


        return data
    def no_response_data(self):
        application_table = """SELECT * FROM application_application;"""
        resident_table = """SELECT * FROM application_resident;"""

        data = pd.merge(
            left =pd.read_sql(application_table, con=self.engine),
            right = pd.read_sql(resident_table, con=self.engine),
            how = 'inner',
            on="resident_id"
        )

        data["alert_type_id"] = 1
        data["alert_message"] = ""
        data["alert_priority"]= 0
        data["alert_status"] = False


        return data

    def rfi_data(self):
        application_table = """SELECT * FROM application_application;"""
        resident_table = """SELECT * FROM application_resident;"""
        response_table = """SELECT * FROM application_response;"""
        rfi_table = """SELECT * FROM application_rfi;"""


        data = pd.merge(

            left = pd.merge(
                left =pd.read_sql(application_table, con=self.engine),
                right = pd.read_sql(resident_table, con=self.engine),
                how = 'inner',
                on="resident_id"
            ),

            right = pd.merge(
                left =pd.read_sql(response_table, con=self.engine),
                right = pd.read_sql(rfi_table, con=self.engine),
                how = 'inner',
                on="response_id"

            ),
            how = 'inner',
            on ='application_id'
        )

        data["alert_message"] = ""
        data["alert_priority"]= 0
        data["alert_status"] = False

        return data


    def alert_data(self):

        alert_table = """
            SELECT * FROM application_alert WHERE application_alert.alert_status = false;
        """
        data = pd.read_sql(alert_table, con=self.engine)

        return data
