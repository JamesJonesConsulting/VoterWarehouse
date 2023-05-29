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
