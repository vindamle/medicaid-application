''' mssqlserver.py '''

import os
import logging
import pyodbc
from dotenv import load_dotenv
from os.path import join, dirname, os

''' ConnectSqlServer '''
class ConnectSqlServer:

    def __init__(self):
        ## Load .env values
        dotenv_path = join(dirname(__file__), '../.env')
        load_dotenv(dotenv_path)

        ## load environment values from .env
        self.server = os.getenv("MSSQL_SERVER")
        self.database = os.getenv("MSSQL_DATABASE")
        self.driver = os.getenv("MSSQL_DRIVER")
        self.username = os.getenv("MSSQL_USERNAME")
        self.password = os.getenv("MSSQL_PASSWORD")

    '''
        connect to sql server
    '''
    def connect_sql_server(self):
        try:
            conn = pyodbc.connect(r'''DRIVER=''' + self.driver + r''';
                Server=''' + self.server + r''';
                UID=''' + self.username + r''';
                PWD=''' + self.password + r''';
                DATABASE=''' + self.database + r''';''')

            return conn

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print("Connection Failed Error Code:" + sqlstate)
            return 0

    '''
        returns all the tables and views in the database
    '''
    def get_all_tables(self, conn):
        cursor = conn.cursor()
        tables = []
        for row in cursor.tables():
            tables.append(row.table_name)

        return tables

    '''
        call a generic stored proc with no parameters
        returns total rows
    '''
    def call_stored_procedure(self, conn, storedProc):
        cursor = conn.cursor()
        results = cursor.execute("{CALL " + storedProc + "}")

        counter = 0
        for result in results:
            counter += 1

        return counter

    '''
        returns a specific table in the database if it exists
    '''
    def does_table_exist(self, conn, tableName):
        pass

    '''
        basic select statement
    '''
    def get_rows_from_table(self, conn, fields, table, query =''):
        pass

    '''
        get drug orders for current date
    '''
    def get_all_drug_orders(self, conn):
        cursor = conn.cursor()
        results = cursor.execute("{CALL p_PCCDrugOrderGetList}")
        counter = 0
        for result in results:
            counter += 1

        print("All Drug Orders = " + str(counter))
        return results ## for now this will be a sql object

    '''
        get drugs orders for any date
    '''
    def get_drug_orders_by_date(self, conn, date):
        cursor = conn.cursor()
        results = cursor.execute("{CALL p_PCCDrugOrderGetListByDate (?)}", date)

        return results
