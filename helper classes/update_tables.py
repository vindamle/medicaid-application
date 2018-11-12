from db import Db
from datetime import date

db = Db()
connection = db.connect_postgres()

conn = connection[0]
meta = connection[1]

# print(db.get_all_tables(meta))
# print(meta.tables['application_trackingdata'])

table = meta.tables['application_trackingdata']
querySTR = table.select().where(((table.c.patient_id -790) > 440007000) &(table.c.is_medicaid_pending == 'No'))

print(date.today())
# update_statement = meta.tables['application_trackingdata'].update().where(meta.tables['application_trackingdata'].c.date_of_deadline - datetime.date() <10).values(rfi_deadline_alert = True)
results = conn.execute(querySTR)
for result in results:
    print(result)
