# -*- coding: utf-8 -*-

# Abstract class for handling Raw data import methods for State data

from abc import ABC, abstractmethod


class State(ABC):
    """
    Import.Florida class provides methods to import voter and voter history from provided Zip files
    """
    @property
    @abstractmethod
    def valid_import_types(self):
        pass

    @property
    @abstractmethod
    def history_keys(self):
        pass

    @property
    @abstractmethod
    def voter_keys(self):
        pass

    @property
    @abstractmethod
    def suppress_keys(self):
        pass

    def __init__(self, db):
        """
        __init__ Sets the instance of Warehouse.Florida to a class variable named 'db'.

        :param db: An instance of Warehouse.Florida
        :return: None
        """
        self.db = db

    def __enter__(self):
        """
        __enter__ Returns itself.

        :return: Instance of Import.Florida
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        __exit__ Sets Exits the class.

        :param exc_type: Execution Type
        :param exc_val: Execution Value
        :param exc_tb: Execution
        :return: self
        """
        return self

    @abstractmethod
    def import_source(self, file, t) -> None:
        """
        import_source Reads in a Voter or History File in Zip format and sends it to the datastore.

        :param t: String representing the type of zip file to import
        :param file: The full path to the Zip file
        :return: None
        """
        pass
