# -*- coding: utf-8 -*-

# Handles Raw data import methods for Florida data

import csv
import datetime
import io
import zipfile

import Warehouse.FloridaSQL as StateSQL
from Import.State import State
from Import.FloridaCodes import __history_import_map__
from Import.FloridaCodes import __voter_import_map__
from Import.FloridaCodes import __suppress_keys__


class Florida(State):
    """
    Import.Florida class provides methods to import voter and voter history from provided Zip files
    """

    valid_import_types = {
        "voters": {
            "sql": "set_voter",
            "parse": "parse_voter_into_tuple",
            "batch_size": 200000,
            "fields": __voter_import_map__.keys()
        },
        "histories": {
            "sql": "set_history",
            "parse": "parse_history_into_tuple",
            "batch_size": 200000,
            "fields": __history_import_map__.keys()
        }
    }

    @staticmethod
    def parse_history_into_tuple(history: dict, export_date: str) -> tuple[str | None, ...]:
        """
        Build a temporary dictionary from raw voter binary string

        :param dict history: A dictionary containing a raw row of history data
        :param str export_date: Export date string in YYYY-MM-DD format
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
        # Appending the export date to the dictionary
        row["export_date"] = export_date
        for k in ["election_date"]:
            if len(row[k]) < 10:
                row[k] = None
            else:
                row[k] = datetime.datetime.strptime(row[k], "%m/%d/%Y").strftime('%Y-%m-%d')
        return tuple(row.values())

    @staticmethod
    def parse_voter_into_tuple(voter: dict[str, str | None], export_date: str) -> tuple[str | None, ...]:
        """
        Build a temporary dictionary from raw voter binary string

        :param dict[str, str | None] voter: A byte string containing a raw row of voter data
        :param str export_date: Export date string in YYYY-MM-DD format
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
        # Appending the export date to the dictionary
        row["export_date"] = export_date
        # Converting dates to the right format and fixing any dates that have been suppressed or invalid to None
        for k in ["birth_date", "registration_date"]:
            if len(row[k]) < 10:
                row[k] = None
            else:
                row[k] = datetime.datetime.strptime(row[k], "%m/%d/%Y").strftime('%Y-%m-%d')
        # Blanking out any suppressed fields with * to empty string
        for k in __suppress_keys__:
            if row[k] == "*":
                row[k] = ""
        # Ensuring email addresses are in lower case
        row["email_address"] = row["email_address"].lower()
        if row["race"] == '':
            row["race"] = None
        return tuple(row.values())

    def import_source(self, file: str, t: str) -> None:
        """
        import_source Reads in a Voter or History File in Zip format and sends it to the datastore.

        :param str t: String representing the type of zip file to import
        :param str file: The full path to the Zip file
        :return: None
        """
        self.db.init_schema()
        if t in self.valid_import_types.keys():
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
                                    newline='',
                                    encoding='utf-8',
                                    errors='ignore'
                                ),
                                delimiter="\t",
                                fieldnames=self.valid_import_types[t]["fields"]
                            )
                            for row in reader:
                                if len(data) < self.db.batch_limits[t]:
                                    data.append(getattr(self, self.valid_import_types[t]["parse"])(
                                        row,
                                        datetime.datetime(*info.date_time).strftime("%Y-%m-%d")
                                    ))
                                else:
                                    print(f"Importing batch of {len(data)} records from {info.filename}..")
                                    self.db.executemany_prepared_sql(
                                        getattr(StateSQL, self.valid_import_types[t]["sql"])(),
                                        data
                                    )
                                    records_imported += len(data)
                                    data = []
                            if len(data) > 0:
                                print(f"Importing batch of {len(data)} records from {info.filename}..")
                                self.db.executemany_prepared_sql(
                                    getattr(StateSQL, self.valid_import_types[t]["sql"])(),
                                    data
                                )
                                records_imported += len(data)
                            print(f"{records_imported} total records imported")
                            print("-" * 20)
            except Exception as error:
                print('Caught this error: ' + repr(error))
                raise
        else:
            raise ValueError(f"Usage: Type 't' {t} is not valid")
