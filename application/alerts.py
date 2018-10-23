from .mssqlserver import ConnectSqlServer
import pandas as pd
class Alerts:

    def __init__(self):
        ''' Get MSSQl Connection'''
        sqlServer = ConnectSqlServer()
        self.conn = sqlServer.connect_sql_server()


    def get_alerts(self, dayRange, facility):


        ''' if ALL facility data is requested '''

        if facility == "All":
            facility = None

        ''' Get Requested Data '''
        cursor = self.conn.cursor()
        try:
            results = cursor.execute("{CALL p_MEnrollmentTrackingResidentoByActivitydateFacility(?,?,?)}",None,dayRange, facility)
        except:
            print("Error :: Cannot Connect to Server")
        
        return results

    def get_fields(self, result, facility):

        return dict(
            first_name = getattr(result, "FirstName"),
            last_name = getattr(result, "LastName"),
            # id = getattr(result,"Resident_SKey"),
            SSN = getattr(result, "SSN"),
            DOB = getattr(result, "DOB"),
            facility = facility,
            payor = getattr(result, "Payor"),
            Is_Primary_Payor= getattr(result, "Is_Primary_Payor"),
            ActivityDate= getattr(result, "ActivityDate"),
            Actual_Activity_Type_Flag= getattr(result, "Actual_Activity_Type_Flag"),
        )
