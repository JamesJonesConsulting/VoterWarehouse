import Warehouse.GeorgiaSQL
from Warehouse.State import State
from Warehouse.GeorgiaCodes import __counties__


class Georgia(State):
    """
    Warehouse.Florida class provides methods for storage of voter and voter history records and
    associated assistive methods,
    """

    country_designation = "UnitedStates"
    state_designation = "Georgia"

    def init_schema(self) -> None:
        """
        init_schema Initializes the database, tables, etc.

        :return: None
        """
        try:
            for sql in [
                Warehouse.GeorgiaSQL.create_database(self.config["database"]["schema"]),
                # Warehouse.GeorgiaSQL.create_voters_table(),
                Warehouse.GeorgiaSQL.create_counties_table(),
                Warehouse.GeorgiaSQL.create_histories_table()
            ]:
                self.execute_sql(sql)
            for k, v in __counties__.items():
                self.execute_prepared_sql(
                    Warehouse.GeorgiaSQL.set_county(),
                    tuple([k, v])
                )
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise
