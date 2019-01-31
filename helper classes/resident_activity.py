from mssqlserver import ConnectSqlServer
from db import Db
from datetime import datetime
import pyodbc
import os

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select, update, func



class Alerts:


    def __init__(self):

        self.db_secret_key = os.getenv("SECRET_KEY")

        ''' Get MSSQl Connection'''
        sqlServer = ConnectSqlServer()
        self.conn = sqlServer.connect_sql_server()
     
        ''' Get PSQL Connection'''
        db = Db()
        connection = db.connect_postgres()
        self.con = connection[0]
        self.meta = connection[1]

    def get_alerts(self, dayRange, facility):

        cursor = self.conn.cursor()
        try:
            # ('2018-10-31')
            results = cursor.execute("{CALL p_MEnrollmentTrackingResidentByActivitydateFacility(?,?,?)}",(datetime.now()).strftime("%Y-%m-%d"), 2, None)
        except:
            print("Error :: Cannot Connect to Server")

        return results

    ''' Returns Dict of result obj'''
    def get_fields(self, result):

        ssn_encrypt = func.pgp_sym_encrypt(
            getattr(result, "SSN").replace('-',''),
            self.db_secret_key,
        )

        return dict(
            resident_id = getattr(result, "Facility_Skey")*(10**7) + getattr(result,"PatientID"),
            resident_number = getattr(result,"PatientID"),
            ssn = ssn_encrypt,
            first_name = getattr(result, "FirstName").capitalize(),
            last_name = getattr(result, "LastName").capitalize(),
            dob = getattr(result, "DOB"),
            facility_id = getattr(result, "Facility_Skey"),
            facility_name= getattr(result, "Facility"),
            primary_payor_id = getattr(result, "PrimaryPayorSkey"),
            primary_payor_grp = " ".join(getattr(result, "PrimaryPayor").split()),
            primary_payor = getattr(result, "PrimaryPayorName"),
            secondary_payor_id = getattr(result, "Secondary_payor_skey"),
            secondary_payor_grp = " ".join(getattr(result, "SecondaryPayorName").split()) if getattr(result, "SecondaryPayorName") else None,
            secondary_payor= getattr(result, "SecondaryPayorName"),
            activity_date= getattr(result, "ActivityDate"),
            activity_type = getattr(result, "Actual_Activity_Type_Flag"),
            sex = getattr(result, 'Sex'),
            dismiss = False

        )

    '''Imports Data to PSQL DB'''
    def import_fields(self, alerts):

        for alert in alerts:
            obj = self.get_fields(alert)


            insert_stmt = insert(self.meta.tables['application_resident']).values(obj)


            stmt = insert_stmt.on_conflict_do_update(
                constraint = 'application_resident_pkey',
                set_ = obj
            )
            self.con.execute(stmt)


alert = Alerts()
results = alert.get_alerts(1,None)
alert.import_fields(results)

