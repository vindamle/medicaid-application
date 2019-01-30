# Medicaid Tracker Documentation
## Installation
### Dependencies
* PostgreSQL 10 or Higher
* Python 3.5 or Higher

Create Virtual Environment and run: `pip install -r requirements.txt`  in your terminal.

### Database Setup
#### Windows
In Command Prompt:


Type the following and press enter:

```bash
psql -u <username> -W
```
This will prompt you to enter your database password. 

After the sign-in is completed, create a database `CREATE DATABASE <DATABASE_NAME>`.


Switch to your new database in the shell and type the following:

```bash 
\connect <DATABASE_NAME> or \c <DATABASE_NAME>
```

You now want to add the `pgcrypto`  to your new database.

Within the psql shell type the following and press enter:
```bash
CREATE EXTENSION pgcrypto;
```

You database setup is now complete....


#### Linux
Open Terminal (ctrl -alt -t):

Type the following and press enter:
```bash 
sudo su postgres
```
Login and type the following:

```bash
psql -u <username> -W
```
This will prompt you to enter your database password. 

After the sign-in is completed, create a database `CREATE DATABASE <DATABASE_NAME>`.


Switch to your new database in the shell and type the following:

```bash 
\connect <DATABASE_NAME> or \c <DATABASE_NAME>
```

You now want to add the `pgcrypto`  to your new database.

Within the psql shell type the following and press enter:
```bash
CREATE EXTENSION pgcrypto;
```

You database setup is now complete....

### Migrations
Before you migrate the project to your new dabase, you will be required to edit `path/medicaid_application/app/settings.py` and change the database name, username and passwaord respectivly.

If database, username, passoword are setup correctly, executing the following will run rather harmlessly.

In your Terminal:

```bash 

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
The last command will walk you through the superuser account setup. After the account setup is completed run the following.]

```bash 
python manage.py runserver
```

The application should start up on 127.0.0.1:8000, the application should be 'live' and setup is complete.

## Receiving Resident Data
You've probably noticed that there is no actual resident data and the application consists of empty tables, after unzipping env.zip, and populate your database credentials into the proper fields, you will be able to run the following:

```bash
path/medicaid-application/helper classes> python resident_update.py
``` 

When the script finishes, you will notice the activity page of the application should be populated with residents and corresponding actions.

## CRON JOBS

`THIS AREA IS CURRENTLY UNDER CONSTRUCTION`





### HAPPY TRACKING!!!
