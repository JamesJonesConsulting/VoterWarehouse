import Warehouse.NorthCarolinaSQL
from Warehouse.State import State
from Warehouse.NorthCarolinaCodes import __counties__


class NorthCarolina(State):
    """
    Warehouse.NorthCarolina class provides methods for storage of voter and voter history records and
    associated assistive methods,
    """

    country_designation = "UnitedStates"
    state_designation = "NorthCarolina"

    def init_schema(self) -> None:
        """
        init_schema Initializes the database, tables, etc.

        :return: None
        """
        try:
            for sql in [
                Warehouse.NorthCarolinaSQL.create_database(self.config["database"]["schema"]),
                Warehouse.NorthCarolinaSQL.create_voters_table(),
                Warehouse.NorthCarolinaSQL.create_counties_table(),
                Warehouse.NorthCarolinaSQL.create_histories_table()
            ]:
                self.execute_sql(sql)
            for k, v in __counties__.items():
                self.execute_prepared_sql(
                    Warehouse.NorthCarolinaSQL.set_county(),
                    tuple([k, v])
                )
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise
