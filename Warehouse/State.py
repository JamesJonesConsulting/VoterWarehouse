# -*- coding: utf-8 -*-
from types import TracebackType
from typing import Optional, Type

# Abstract Class Handles Database methods for State data

import pymysql
import pymysql.cursors
import yaml
from abc import ABC, abstractmethod


class State(ABC):
    """
    Warehouse.State abstract class provides methods for storage of voter and voter history records and
    associated assistive methods,
    """

    @abstractmethod
    def init_schema(self) -> None:
        pass

    @property
    @abstractmethod
    def country_designation(self):
        pass

    @property
    @abstractmethod
    def state_designation(self):
        """
        State/Province/etc. - Any top level area for a country
        """
        pass

    def __init__(self, config_file: str) -> None:
        """
        __init__ Sets the config dictionary of database credentials into variable named 'db'.

        :param str config_file: Path to the YAML config file
        :return: None
        """

        try:
            with open(config_file) as file:
                self.config = yaml.full_load(file)[type(self).country_designation][type(self).state_designation]
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise

    def execute_sql(self, sql: str) -> None:
        """
        execute_prepared_sql Executes a SQL Command with provided prepared values

        :param str sql: A SQL Command
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

    def execute_prepared_sql(self, prepared_sql: str, prepared_tuple: tuple) -> None:
        """
        execute_prepared_sql Executes a SQL Command with provided prepared values

        :param str prepared_sql: A SQL Command with prepared values
        :param tuple prepared_tuple: A tuple of values to run against provided prepared SQL
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

    def __enter__(self):
        """
        __enter__ Creates the database connection and sets it to the class as 'db'

        :return: Instance of Warehouse.State
        :rtype: Warehouse.State
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

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> bool:
        """
        __exit__ Sets Exits the class.

        :param Optional[Type[BaseException]] exc_type: Execution Type
        :param Optional[BaseException] exc_val: Execution Value
        :param Optional[TracebackType] exc_tb: Execution
        :return: Always true unless otherwise implemented in the future
        :rtype: bool
        """
        try:
            self.db.close()
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise
        return True
