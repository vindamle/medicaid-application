from db import Db
from datetime import datetime

db = Db()
connection = db.connect_postgres()

conn = connection[0]
meta = connection[1]


table = meta.tables['application_trackingdata']


querySTR = table.select().where(datetime.now().strftime("%Y-%m-%d")-table.c.date_of_medicaid_approval.strftime("%Y-%m-%d")>0)

print(datetime.now().strftime("%Y-%m-%d"))
# update_statement = meta.tables['application_trackingdata'].update().where(meta.tables['application_trackingdata'].c.date_of_deadline - datetime.date() <10).values(rfi_deadline_alert = True)
results = conn.execute(querySTR)
for result in results:
    print(result)
