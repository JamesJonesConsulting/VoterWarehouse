# -*- coding: utf-8 -*-

# Handles Raw data import methods for Georgia data

import csv
import datetime
import io
import zipfile

import Warehouse.GeorgiaSQL as StateSQL
from Import.State import State
from Import.GeorgiaCodes import __counties__
from Import.GeorgiaCodes import __election_types__
from Import.GeorgiaCodes import __parties__
from Import.GeorgiaCodes import __history_import_map__


class Georgia(State):
    """
    Import.Georgia class provides methods to import voter and voter history from provided Zip files
    """

    valid_import_types = {
        "voters": {
            "sql": "set_voter",
            "parse": "parse_raw_voter_into_tuple"
        },
        "histories": {
            "sql": "set_history",
            "parse": "parse_history_into_tuple"
        }
    }

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
                            io.TextIOWrapper(f, newline='')
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
                                        getattr(StateSQL, self.valid_import_types[t]["sql"])(),
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
                                    getattr(StateSQL, self.valid_import_types[t]["sql"])(),
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
    def get_party_code(name: str) -> str:
        """
        Convert a party name to it's party code

        :param str name: The long name for a party
        :return: The party code
        :rtype: str
        """
        # Sanitize the raw value
        name = name.strip().replace(" ", "").replace("-", "").lower()
        if name == '':
            return ''
        else:
            return list(__parties__.keys())[
                list(
                    map(
                        lambda x: x.replace(" ", "").replace("-", "").lower()[0:len(name)], __parties__.values()
                    )
                ).index(name)
            ]

    @staticmethod
    def get_county_code(name: str) -> str:
        """
        Convert a county name to its code

        :param str name: The long name for the county
        :return: The county code
        :rtype str
        """
        name = name.replace(" ", "").lower()
        if name in list(
            map(lambda x: x.replace(" ", "").lower(), __counties__.values())
        ):
            return list(__counties__.keys())[
                list(
                    map(
                        lambda x: x.replace(" ", "").lower(),
                        __counties__.values()
                    )
                ).index(name)
            ]
        else:
            return list(__counties__.keys())[
                list(__counties__.values()).index('UNKNOWN')
            ]

    @staticmethod
    def get_election_type(name: str) -> str:
        """
        Convert a county name to its code

        :param str name: The long name for election tpe
        :return: The election type code
        :rtype str
        """
        if name == '':
            name = "UNKNOWN"
        return list(__election_types__.keys())[
            list(__election_types__.values()).index(name)
        ]

    @staticmethod
    def parse_history_into_tuple(history: dict) -> tuple[str | None, ...]:
        """
        Build a temporary dictionary from raw voter binary string

        :param bytes history: A byte string containing a raw row of history data
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
        for k in ["absentee", "provisional", "supplemental"]:
            if row[k].upper() == 'Y':
                row[k] = 1
            else:
                row[k] = 0
        row['county_code'] = Georgia.get_county_code(row['county_code'])
        row['party'] = Georgia.get_party_code(row['party'])
        row['election_type'] = Georgia.get_election_type(row['election_type'])
        if row['voter_id'] == '':
            row['voter_id'] = 0
        return tuple(row.values())
