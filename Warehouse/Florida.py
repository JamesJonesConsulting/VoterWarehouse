# -*- coding: utf-8 -*-

# Handles Database methods for Florida data

import Warehouse.FloridaSQL
from Warehouse.State import State


class Florida(State):
    """
    Warehouse.Florida class provides methods for storage of voter and voter history records and
    associated assistive methods,
    """
    country_designation = "UnitedStates"
    state_designation = "Florida"

    def execute_prepared_sql(self, prepared_sql, prepared_tuple) -> None:
        """
        execute_prepared_sql Executes a SQL Command with provided prepared values

        :param prepared_sql: A SQL Command with prepared values
        :param prepared_tuple: A tuple of values to run against provided prepared SQL
        :return: None
        """
        with self.db.cursor() as cursor:
            # print(prepared_sql)
            try:
                cursor.execute(prepared_sql, prepared_tuple)
            except Exception as error:
                print('Caught this error: ' + repr(error))
                raise
        self.db.commit()

    def execute_sql(self, sql) -> None:
        """
        execute_prepared_sql Executes a SQL Command with provided prepared values

        :param sql: A SQL Command
        :return: None
        """
        with self.db.cursor() as cursor:
            # print(sql)
            try:
                cursor.execute(sql)
            except Exception as error:
                print('Caught this error: ' + repr(error))
                raise
        self.db.commit()

    def init_schema(self) -> None:
        """
        init_schema Initializes the database, tables, etc.

        :return: None
        """
        try:
            for sql in [
                Warehouse.FloridaSQL.create_database(self.config["database"]["schema"]),
                Warehouse.FloridaSQL.create_voters_table(),
                Warehouse.FloridaSQL.create_histories_table()
            ]:
                self.execute_sql(sql)
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise
