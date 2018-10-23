''' facility.py '''

from db import Db
from dotenv import load_dotenv
from os.path import join, dirname, os
from mssqlserver import ConnectSqlServer
import pathlib

from sqlalchemy.dialects.postgresql import insert
import pyodbc


class Facility:

    def __init__(self):
        ## Load .env values
        dotenv_path = join(dirname(__file__), '../.env')
        load_dotenv(dotenv_path)

        sqlServer = ConnectSqlServer()
        self.conn = sqlServer.connect_sql_server()

        # connect to postgres
        db = Db()
        connection = db.connect_postgres()
        self.con = connection[0]
        self.meta = connection[1]

    #places facility row into dict and returns specific values
    def get_facility_fields(self, facility):

        return dict(
            facility_id = facility[0],
            facility_number = facility[1],
            facility_name = facility[2],
            capacity = facility[3],
            downstate_upstate= facility[4],
            centers_grand = facility[5],
            start_date = facility[6],

        )

    ## get all the facilities from data warehouse
    def get_all_facilities(self):

        conn = self.conn
        cursor = conn.cursor()
        results = cursor.execute("{CALL p_facilityGetList}")

        return results

    ## import all the facilities into PSQL
    def import_facilities(self, results):

        for facility in results:

            # setup facility fields with
            o=self.get_facility_fields(facility)

            #CHECK IF FACILITY NUMBER EXISTS
            #if facility number exists insert to psql db otherwise ignore
            if bool(o["facility_number"]):

	            # setup insert statement
                insert_stmt = insert(self.meta.tables['application_facility']).values(o)

                # upsert
                stmt = insert_stmt.on_conflict_do_update(
                    constraint = 'application_facility_pkey',
                    set_ = o
                )
                # write to db
                self.con.execute(stmt)


f = Facility()
results =f.get_all_facilities()
f.import_facilities(results)
