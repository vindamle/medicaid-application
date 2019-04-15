from .mssqlserver import ConnectSqlServer
from .db import Db
import pyodbc
import os

# This class fetches the NCS Refesh data and updates database.
class Refresh():
    def init(self):
        # Get MSSQl Connection
        sqlServer = ConnectSqlServer()
        self.conn = sqlServer.connect_sql_server()

        # Get PSQL Connection
        db = Db()
        connection = db.connect_postgres()
        self.con = connection[0]
        self.meta = connection[1]

    # Calls SP to recieve NCS - demographics data
    def demographics(resident, facility):
        try:
            results = self.conn.cursor.execute("{CALL p_MEnrollmentTrackingResidentByActivitydateFacility(?,?)}",(resident, facility))
        except:
            print("Error :: Cannot Connect to Server")

        for result in results:
            print(result)

    # def payor_info(resident, facilty):
    #
    #     try:
    #         results = self.conn.cursor.execute("{CALL p_MEnrollmentTrackingResidentByActivitydateFacility(?,?)}",(resident, facility))
    #     except:
    #         print("Error :: Cannot Connect to Server")
    #
    #     for result in results:
    #         print(result)
    #
    # def admission_data(resident, facilty):
    #     try:
    #         results = self.conn.cursor.execute("{CALL p_MEnrollmentTrackingResidentByActivitydateFacility(?,?)}",(resident, facility))
    #     except:
    #         print("Error :: Cannot Connect to Server")
    #
    #     for result in results:
    #         print(result)
