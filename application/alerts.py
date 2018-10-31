from .mssqlserver import ConnectSqlServer


class Alerts:


    def __init__(self):
        ''' Get MSSQl Connection'''
        sqlServer = ConnectSqlServer()


    def get_alerts(self, dayRange, facility):

        cursor = self.conn.cursor()
        try:
            results = cursor.execute("{CALL p_MEnrollmentTrackingResidentByActivitydateFacility(?,?,?)}",None,1, None)
        except:
            print("Error :: Cannot Connect to Server")

        return results
    ''' Returns Dict of result obj'''
    def get_fields(self, result):

        return dict(
            first_name = getattr(result, "FirstName"),
            last_name = getattr(result, "LastName"),
            ssn = getattr(result, "SSN"),
            dob = getattr(result, "DOB"),
            facility_id = getattr(result, "Facility_Skey"),
            payor = getattr(result, "PrimaryPayorName"),
            secondary_Payor= getattr(result, "SecondaryPayorName"),
            activity_date= getattr(result, "ActivityDate"),
            actual_activity_type_flag= getattr(result, "Actual_Activity_Type_Flag"),
            track = None,

        )
    def import_fields(self, alerts):

        for alert in alerts:
            obj = self.get_fields(alert)

            insert_stmt = insert(self.meta.tables['application_alert']).values(obj)

            self.con.execute(stmt)



alert = Alerts()
