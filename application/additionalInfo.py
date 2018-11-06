from mssqlserver import ConnectSqlServer
import pyodbc
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime
class AdditionalInfo:


    def __init__(self):
        ''' Get MSSQl Connection'''
        sqlServer = ConnectSqlServer()
        self.conn = sqlServer.connect_sql_server()

    def get_Info(self, patient_id, facility_Skey, SSN):

        cursor = self.conn.cursor()
        try:
            # ('2018-10-31')
            results = cursor.execute("{CALL p_MEnrollmentTrackingResidentByPatientIdResidentSkeyFacilityId(?,?,?)}",(facility_Skey,patient_id,SSN))
        except:
            print("Error :: Cannot Connect to Server")

        return results


ai = AdditionalInfo()
