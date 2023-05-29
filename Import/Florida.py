# -*- coding: utf-8 -*-

# Handles Raw data import methods for Florida data

import datetime
import zipfile

import Warehouse.FloridaSQL
from Import.State import State


class Florida(State):
    """
    Import.Florida class provides methods to import voter and voter history from provided Zip files
    """

    valid_import_types = {
        "voters": {
            "sql": "set_voter",
            "parse": "parse_raw_voter_into_tuple",
            "batch_size": 200000
        },
        "histories": {
            "sql": "set_history",
            "parse": "parse_raw_history_into_tuple",
            "batch_size": 200000
        }
    }

    history_keys = [
        "county_code",
        "voter_id",
        "election_date",
        "election_type",
        "history_code"
    ]

    voter_keys = [
        "county_code",
        "voter_id",
        "name_last",
        "name_suffix",
        "name_first",
        "name_middle",
        "suppress_address",
        "residence_address_line_1",
        "residence_address_line_2",
        "residence_city",
        "residence_state",
        "residence_zipcode",
        "mailing_address_line_1",
        "mailing_address_line_2",
        "mailing_address_line_3",
        "mailing_city",
        "mailing_state",
        "mailing_zipcode",
        "mailing_country",
        "gender",
        "race",
        "birth_date",
        "registration_date",
        "party_affiliation",
        "precinct",
        "precinct_group",
        "precinct_split",
        "precinct_suffix",
        "voter_status",
        "congressional_district",
        "house_district",
        "senate_district",
        "county_commission_district",
        "school_board_district",
        "daytime_area_code",
        "daytime_phone_number",
        "daytime_phone_extension",
        "email_address"
    ]

    suppress_keys = [
        "name_last",
        "name_suffix",
        "name_first",
        "name_middle",
        "residence_address_line_1",
        "residence_address_line_2",
        "residence_city",
        "residence_state",
        "residence_zipcode",
        "mailing_address_line_1",
        "mailing_address_line_2",
        "mailing_address_line_3",
        "mailing_city",
        "mailing_state",
        "mailing_zipcode",
        "mailing_country",
        "precinct",
        "precinct_group",
        "precinct_split",
        "precinct_suffix",
        "congressional_district",
        "house_district",
        "senate_district",
        "county_commission_district",
        "school_board_district",
        "daytime_area_code",
        "daytime_phone_number",
        "daytime_phone_extension",
        "email_address"
    ]

    def parse_raw_history_into_tuple(self, history_raw: bytes, export_date: str) -> tuple[str | None, ...]:
        """
        Build a temporary dictionary from raw voter binary string

        :param bytes history_raw: A byte string containing a raw row of history data
        :param str export_date: Export date string in YYYY-MM-DD format
        :return: A tuple of SQL ready prepared parameters
        :rtype: tuple[str | None, ...]
        """
        row: dict[str, bytes | str | None] = dict(
            zip(
                self.history_keys,
                history_raw.strip().split(b"\t")
            )
        )
        # Ensure all values are converted from binary to utf-8 strings and fill in missing keys
        for k in self.history_keys:
            if k not in row:
                row[k] = ""
            else:
                row[k] = row[k].decode('utf-8')
        # Appending the export date to the dictionary
        row["export_date"] = export_date
        # Converting dates to the right format and fixing any dates that have been suppressed or invalid to None
        for k in ["election_date"]:
            if len(row[k]) < 10:
                row[k] = None
            else:
                row[k] = datetime.datetime.strptime(row[k], "%m/%d/%Y").strftime('%Y-%m-%d')
        return tuple(row.values())

    def parse_raw_voter_into_tuple(self, voter_raw: bytes, export_date: str) -> tuple[str | None, ...]:
        """
        Build a temporary dictionary from raw voter binary string

        :param bytes voter_raw: A byte string containing a raw row of voter data
        :param str export_date: Export date string in YYYY-MM-DD format
        :return: A tuple of SQL ready prepared parameters
        :rtype: tuple[str | None, ...]
        """
        row: dict[str, bytes | str | None] = dict(
            zip(
                self.voter_keys,
                voter_raw.strip().split(b"\t")
            )
        )
        # Ensure all values are converted from binary to utf-8 strings and fill in missing keys
        for k in self.voter_keys:
            if k not in row:
                row[k] = ""
            else:
                row[k] = row[k].decode('utf-8')
        # Appending the export date to the dictionary
        row["export_date"] = export_date
        # Converting dates to the right format and fixing any dates that have been suppressed or invalid to None
        for k in ["birth_date", "registration_date"]:
            if len(row[k]) < 10:
                row[k] = None
            else:
                row[k] = datetime.datetime.strptime(row[k], "%m/%d/%Y").strftime('%Y-%m-%d')
        # Blanking out any suppressed fields with * to empty string
        for k in self.suppress_keys:
            if row[k] == "*":
                row[k] = ""
        # Ensuring email addresses are in lower case
        row["email_address"] = row["email_address"].lower()
        return tuple(row.values())

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
                    for line in archive.read(info.filename).split(b"\n"):
                        if len(line.strip()) >= 3:
                            if t in self.valid_import_types.keys():
                                if len(data) < self.db.batch_limits[t]:
                                    data.append(getattr(self, self.valid_import_types[t]["parse"])(
                                        line,
                                        datetime.datetime(*info.date_time).strftime("%Y-%m-%d")
                                    ))
                                else:
                                    print(f"Importing batch of {len(data)} records from {info.filename}..")
                                    self.db.executemany_prepared_sql(
                                        getattr(Warehouse.FloridaSQL, self.valid_import_types[t]["sql"])(),
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
                                getattr(Warehouse.FloridaSQL, self.valid_import_types[t]["sql"])(),
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
