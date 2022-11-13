import yaml
import pymysql
import pymysql.cursors
import Warehouse.FloridaSQL


class Florida:
    """
    Warehouse.Florida class provides methods for storage of voter and voter history records and
    associated assistive methods,
    """

    def __init__(self, config_file):
        """
        __init__ Sets the config dictionary of database credentials into variable named 'db'.

        :param config_file: Path to the YAML config file
        :return: None
        """
        try:
            with open(config_file) as file:
                self.config = yaml.full_load(file)['UnitedStates']['Florida']
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise

    def __enter__(self):
        """
        __enter__ Creates the database connection and sets it to the class as 'db'

        :return: Instance of Warehouse.Florida
        """
        try:
            self.db = pymysql.connect(
                host=self.config["database"]["host"],
                port=self.config["database"]["port"],
                user=self.config["database"]["user"],
                password=self.config["database"]["password"],
                database=self.config["database"]["schema"],
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        __exit__ Sets Exits the class and closes the database connection

        :param exc_type: Execution Type
        :param exc_val: Execution Value
        :param exc_tb: Execution
        :return: self
        """
        try:
            self.db.close()
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise
        return self

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

