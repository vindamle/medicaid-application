from db import Db

db = Db()
connection = db.connect_postgres()
conn = connection[0]
meta = connection[1]

print(db.get_all_tables(meta))
print(meta.tables['application_trackingdata'])
