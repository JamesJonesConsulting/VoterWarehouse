# -*- coding: utf-8 -*-

import csv
# Handles Raw data import methods for North Carolina data

import datetime
import io
import zipfile

import Warehouse.NorthCarolinaSQL
from Warehouse.NorthCarolinaCodes import __history_import_map__
from Warehouse.NorthCarolinaCodes import __voter_import_map__
from Import.State import State


class NorthCarolina(State):
    """
    Import.NorthCarolina class provides methods to import voter and voter history from provided Zip files
    """

    valid_import_types = {
        "voters": {
            "sql": "set_voter",
            "parse": "parse_voter_into_tuple"
        },
        "histories": {
            "sql": "set_history",
            "parse": "parse_history_into_tuple"
        }
    }

    suppress_keys = []

    def import_source(self, file: str, t: str) -> None:
        """
        import_source Reads in a Voter or History File in Zip format and sends it to the datastore.

        :param str t: String representing the type of zip file to import
        :param str file: The full path to the Zip file
        :return: None
        """
        self.db.init_schema()
        try:
            with zipfile.ZipFile(file, mode="r") as archive:
                for info in archive.infolist():
                    print(f"Filename: {info.filename}")
                    print(f"Modified: {datetime.datetime(*info.date_time)}")
                    print(f"Normal size: {info.file_size} bytes")
                    print(f"Compressed size: {info.compress_size} bytes")
                    print("-" * 20)
                    data = []
                    records_imported = 0
                    with archive.open(info.filename, "r") as f:
                        reader = csv.DictReader(
                            io.TextIOWrapper(
                                f,
                                newline='\r\n',
                                encoding='utf-8',
                                errors='ignore'
                            ),
                            delimiter="\t"
                        )
                        for row in reader:
                            if t in self.valid_import_types.keys():
                                if len(data) < self.db.batch_limits[t]:
                                    data.append(getattr(self, self.valid_import_types[t]["parse"])(
                                        row
                                    ))
                                else:
                                    print(f"Importing batch of {len(data)} records from {info.filename}..")
                                    self.db.executemany_prepared_sql(
                                        getattr(Warehouse.NorthCarolinaSQL, self.valid_import_types[t]["sql"])(),
                                        data
                                    )
                                    records_imported += len(data)
                                    data = []
                            else:
                                raise ValueError(f"Usage: Type 't' {t} is not valid")
                        if len(data) > 0:
                            if t in self.valid_import_types.keys():
                                print(f"Importing batch of {len(data)} records from {info.filename}..")
                                self.db.executemany_prepared_sql(
                                    getattr(Warehouse.NorthCarolinaSQL, self.valid_import_types[t]["sql"])(),
                                    data
                                )
                                records_imported += len(data)
                            else:
                                raise ValueError(f"Usage: Type 't' {t} is not valid")
                        print(f"{records_imported} total records imported")
                        print("-" * 20)
        except Exception as error:
            print('Caught this error: ' + repr(error))
            raise

    @staticmethod
    def parse_history_into_tuple(history: dict[str, str | None]) -> tuple[str | None, ...]:
        """
        Build a temporary dictionary from raw voter binary string

        :param dict history: A byte string containing a raw row of history data
        :return: A tuple of SQL ready prepared parameters
        :rtype: tuple[str | None, ...]
        """
        row = {}
        for k, v in __history_import_map__.items():
            if k in history:
                # handle matching keys
                row[k] = history[k].strip()
            else:
                # handle non-matching keys
                row[k] = ''
                for match in v:
                    if match in history:
                        row[k] = history[match].strip()
                        break
        for k in ["election_date"]:
            if len(row[k]) < 10:
                row[k] = None
            else:
                row[k] = datetime.datetime.strptime(row[k], "%m/%d/%Y").strftime('%Y-%m-%d')
        return tuple(row.values())

    @staticmethod
    def parse_voter_into_tuple(voter: dict[str, str | None]) -> tuple[str | None, ...]:
        """
        Build a temporary dictionary from raw voter import dictionary

        :param dict voter: A raw dictionary of voter data
        :return: A tuple of SQL ready prepared parameters
        :rtype: tuple[str | None, ...]
        """
        row = {}
        for k, v in __voter_import_map__.items():
            if k in voter:
                # handle matching keys
                row[k] = voter[k].strip()
            else:
                # handle non-matching keys
                row[k] = ''
                for match in v:
                    if match in voter:
                        row[k] = voter[match].strip()
                        break
        for k in ["registration_date"]:
            if len(row[k]) < 10:
                row[k] = None
            else:
                row[k] = datetime.datetime.strptime(row[k], "%m/%d/%Y").strftime('%Y-%m-%d')
        return tuple(row.values())
