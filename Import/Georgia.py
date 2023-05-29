# -*- coding: utf-8 -*-
import csv
# Handles Raw data import methods for Georgia data

import datetime
import io
import zipfile

import Warehouse.GeorgiaSQL
from Import.State import State
from Warehouse.GeorgiaCodes import __counties__
from Warehouse.GeorgiaCodes import __election_types__
from Warehouse.GeorgiaCodes import __parties__


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

    history_keys = [
        "county_code",
        "voter_id",
        "election_date",
        "election_type",
        "party",
        "ballot_style",
        "absentee",
        "provisional",
        "supplemental"
    ]

    @property
    def voter_keys(self):
        pass

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
                                        getattr(Warehouse.GeorgiaSQL, self.valid_import_types[t]["sql"])(),
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
                                    getattr(Warehouse.GeorgiaSQL, self.valid_import_types[t]["sql"])(),
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

    def parse_history_into_tuple(self, history: dict) -> tuple[str | None, ...]:
        """
        Build a temporary dictionary from raw voter binary string

        :param bytes history: A byte string containing a raw row of history data
        :return: A tuple of SQL ready prepared parameters
        :rtype: tuple[str | None, ...]
        """
        history = dict(zip(self.history_keys, list(history.values())))
        history['county_code'] = Georgia.get_county_code(history['county_code'])
        history['party'] = Georgia.get_party_code(history['party'])

        if history['election_type'] == '':
            history['election_type'] = "UNKNOWN"
        history['election_type'] = list(__election_types__.keys())[
            list(__election_types__.values()).index(history['election_type'])
        ]
        if history['voter_id'] == '':
            history['voter_id'] = 0
        for k in ["election_date"]:
            history[k] = datetime.datetime.strptime(history[k], "%m/%d/%Y").strftime('%Y-%m-%d')
        for k in ["absentee", "provisional", "supplemental"]:
            if history[k].upper() == 'Y':
                history[k] = 1
            else:
                history[k] = 0
        return tuple(history.values())
