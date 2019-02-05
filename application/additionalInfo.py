from .mssqlserver import ConnectSqlServer
import pyodbc


class AdditionalInfo:


    def __init__(self):
        ''' Get MSSQl Connection'''
        sqlServer = ConnectSqlServer()
        self.conn = sqlServer.connect_sql_server()

    def get_info(self, resident_id, facility_Skey, SSN):

        cursor = self.conn.cursor()
        try:
            results = cursor.execute("{CALL p_MEnrollmentTrackingResidentByPatientIdResidentSkeyFacilityId(?,?,?)}",facility_Skey,resident_id,SSN)
        except:
            print("Error :: Cannot Connect to Server")



        return results


# ai = AdditionalInfo()
# results = ai.get_Info(2383,1,"081264382")
#
#
# for result in results:
#     print(result)
