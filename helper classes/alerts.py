from mssqlserver import ConnectSqlServer
from db import Db
import pyodbc
from sqlalchemy.dialects.postgresql import insert

class Alerts:


    def __init__(self):
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

            results = cursor.execute("{CALL p_MEnrollmentTrackingResidentByActivitydateFacility(?,?,?)}",None, 1, None)
        except:
            print("Error :: Cannot Connect to Server")

        return results

    ''' Returns Dict of result obj'''
    def get_fields(self, result):

        return dict(
            patient_id = getattr(result,"Resident_Skey"),
            ssn = getattr(result, "SSN"),
            fisrt_name = getattr(result, "FirstName").capitalize(),
            last_name = getattr(result, "LastName").capitalize(),
            primary_payor = getattr(result, "PrimaryPayorName"),
            secondary_payor= getattr(result, "SecondaryPayorName"),
            activity_date= getattr(result, "ActivityDate"),
            activity_type = getattr(result, "Actual_Activity_Type_Flag"),
            tracking_status = None,

        )

    '''Imports Data to PSQL DB'''
    def import_fields(self, alerts):

        for alert in alerts:
            obj = self.get_fields(alert)

            insert_stmt = insert(self.meta.tables['application_alert']).values(obj)
            stmt = insert_stmt.on_conflict_do_update(
                constraint = 'application_alert_pkey',
                set_ = obj
            )
            self.con.execute(stmt)


alert = Alerts()
results = alert.get_alerts(10,None)
alert.import_fields(results)
