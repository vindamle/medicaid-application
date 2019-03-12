
from db import Db
from sqlalchemy.dialects.postgresql import insert
import pyodbc
from datetime import datetime



class ImportAlerts:

    def __init__(self):
        # connect to postgres
        db = Db()
        connection = db.connect_postgres()
        self.con = connection[0]
        self.meta = connection[1]


    def get_fields(self, result):

        try:
            return dict(
                alert_id = int(result["alert_id"]),

                alert_status= result["alert_status"],
                alert_type_id= result["alert_type_id"],
                application_id= result["application_id"],
                resident_id= result['resident_id'],
                trigger_date = datetime.now()
            )
        except:
            return dict(

                alert_status= result["alert_status"],
                alert_type_id= result["alert_type_id"],
                application_id= result["application_id"],
                resident_id= result['resident_id'],
                trigger_date = datetime.now()
            )

    def import_alerts(self, alerts):

        for alert in alerts:

            obj = self.get_fields(alert)
            print(obj)

            # setup insert statement
            insert_stmt = insert(self.meta.tables['application_alert']).values(obj)

            # upsert
            stmt = insert_stmt.on_conflict_do_update(
            constraint = 'application_alert_pkey',
            set_ = obj
            )
            # write to db
            self.con.execute(stmt)
