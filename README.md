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
\connect <DATABASE_NAME>` or `\c <DATABASE_NAME>
```

You now want to add the `pgcrypto`  to your new database.

Within the psql shell type the following and press enter:
```bash
CREATE EXTENSION pgcypto;
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
\connect <DATABASE_NAME>` or `\c <DATABASE_NAME>
```

You now want to add the `pgcrypto`  to your new database.

Within the psql shell type the following and press enter:
```bash
CREATE EXTENSION pgcypto;
```

You database setup is now complete....

