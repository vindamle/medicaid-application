from .mssqlserver import ConnectSqlServer
from .db import Db
import pyodbc
import os
from .models import *

# This class fetches the NCS Refesh data and updates database.
class Refresh():
    def __init__(self):
        # Get MSSQl Connection
        sqlServer = ConnectSqlServer()
        self.conn = sqlServer.connect_sql_server()

        # Get PSQL Connection
        db = Db()
        connection = db.connect_postgres()
        self.con = connection[0]
        self.meta = connection[1]

    # Calls SP to recieve NCS - demographics data
    def demographics(self,resident, facility):
        try:
            cursor = self.conn.cursor()
            print(facility, resident)
            # facility = 'Ellicott'
            # resident = '974'
            results = cursor.execute("{CALL p_GetResidentInfoBySystemNo_FacilityID(?,?)}",(facility,resident))
        except Exception as e:
            print("Error :: Cannot Connect to Server" + str(e))
        # assert False
        for result in results:

            resident = Resident.objects.get(facility_name = str(facility), resident_number = str(resident))

            resident.first_name = getattr(result,"Resident_Name").split(" ")[0]
            resident.last_name = getattr(result,"Resident_Name").split(" ")[1]
            resident.dob = getattr(result,"DOB")
            resident.address =  getattr(result,"Address")
            resident.city = getattr(result,"City")
            resident.state = getattr(result,"State")
            resident.zip = getattr(result,"Zip")
            resident.marital_status  = getattr(result,"Maritial_Status")
            resident.phone = getattr(result,"Phone_Number")
            resident.save()

            break;

    # def payor_info(resident, facilty):
    #
    #     try:
    #         results = self.conn.cursor.execute("{CALL p_MEnrollmentTrackingResidentByActivitydateFacility(?,?)}",(resident, facility))
    #     except:
    #         print("Error :: Cannot Conenct to Server")
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
