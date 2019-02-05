from database import Database
from queries import Queries
from alert_generator import Generate_Alert
from alert_import import ImportAlerts

try:
    data_import = Queries(Database().get_engine())
    try:
        alerts = Generate_Alert().pick_up_date_alert(data_import.pick_up_date_data(),data_import.alert_data())
        try:
            ImportAlerts().import_alerts(alerts)
        except:
            print("Error: Importing Error")
    except:
        print("Error: Generating Alerts Cannot be Completed")
except:
    print("Cannot Access Connection")
