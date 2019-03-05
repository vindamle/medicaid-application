from database import Database
from queries import Queries
from alert_generator import Generate_Alert
from alert_import import ImportAlerts

try:
    data_import = Queries(Database().get_engine())
    try:
        alerts = Generate_Alert().recert_deadline_alert(data_import.recert_alert(),data_import.alert_data())
        try:
            ImportAlerts().import_alerts(alerts)
            
        except:
            print("Error: Importing Error")
    except Exception as e:
        print("Error: Generating Alerts Cannot be Completed\n"+ str(e))
except:
    print("Cannot Access Connection")
