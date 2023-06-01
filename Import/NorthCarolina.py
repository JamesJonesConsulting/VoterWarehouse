# -*- coding: utf-8 -*-
import csv
# Handles Raw data import methods for North Carolina data

import datetime
import io
import zipfile

import Warehouse.NorthCarolinaSQL
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

    history_keys = [
        "county_code",
        "county_name",
        "voter_id",
        "election_date",
        "election_type",
        "voting_method",
        "party_code",
        "party_name",
        "precinct_code",
        "precinct_name",
        "ncid",
        "voted_county_code",
        "voted_county_name",
        "voter_tabulated_district_code",
        "voter_tabulated_district_name"
    ]

    voter_keys = {
        "voter_id": ["voter_reg_num"],
        "county_code": ["county_id"],
        "county_name": ["county_desc"],
        "ncid": [],
        "name_last": ["last_name"],
        "name_first": ["first_name"],
        "name_middle": ["middle_name"],
        "name_suffix": ["name_suffix_lbl"],
        "voter_status": ["status_cd"],
        "voter_status_desc": [],
        "voter_status_reason_code": ["reason_cd"],
        "voter_status_reason_desc": [],
        "residence_address": ["res_street_address"],
        "residence_city": ["res_city_desc"],
        "residence_state": ["state_cd"],
        "residence_zipcode": ["zip_code"],
        "mailing_address_line_1": ["mail_addr1"],
        "mailing_address_line_2": ["mail_addr2"],
        "mailing_address_line_3": ["mail_addr3"],
        "mailing_address_line_4": ["mail_addr4"],
        "mailing_city": ["mail_city"],
        "mailing_state": ["mail_state"],
        "mailing_zipcode": ["mail_zipcode"],
        "daytime_phone": ["full_phone_number"],
        "confidential": ["confidential_ind"],
        "registration_date": ["registr_dt"],
        "race_code": [],
        "ethnic_code": [],
        "party_code": ["party_cd"],
        "gender_code": [],
        "birth_year": [],
        "age_at_year_end": [],
        "birth_state": [],
        "drivers_lic": [],
        "precinct": ["precinct_abbrv"],
        "precinct_desc": [],
        "municipality": ["municipality_abbrv"],
        "municipality_desc": [],
        "ward": ["ward_abbrv"],
        "ward_desc": [],
        "congressional_district": ["cong_dist_abbrv"],
        "superior_court_jurisdiction": ["super_court_abbrv"],
        "judicial_district": ["judic_dist_abbrv"],
        "senate_district": ["nc_senate_abbrv"],
        "house_district": ["nc_house_abbrv"],
        "county_commission_district": ["county_commiss_abbrv"],
        "county_commission_district_desc": ["county_commiss_desc"],
        "township_jurisdiction": ["township_abbrv"],
        "township_jurisdiction_desc": ["township_desc"],
        "school_district": ["school_dist_abbrv"],
        "school_district_desc": ["school_dist_desc"],
        "fire_district": ["fire_dist_abbrv"],
        "fire_district_desc": ["fire_dist_desc"],
        "water_district": ["water_dist_abbrv"],
        "water_district_desc": ["water_dist_desc"],
        "sewer_district": ["sewer_dist_abbrv"],
        "sewer_district_desc": ["sewer_dist_desc"],
        "sanitation_district": ["sanit_dist_abbrv"],
        "sanitation_district_desc": ["sanit_dist_desc"],
        "rescue_district": ["rescue_dist_abbrv"],
        "rescue_district_desc": ["rescue_dist_desc"],
        "municipal_district": ["munic_dist_abbrv"],
        "municipal_district_desc": ["munic_dist_desc"],
        "prosecutorial_district": ["dist_1_abbrv"],
        "prosecutorial_district_desc": ["dist_1_desc"],
        "voter_tabulated_district_code": ["vtd_abbrv"],
        "voter_tabulated_district_name": ["vtd_desc"]
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

    def parse_history_into_tuple(self, history: dict) -> tuple[str | None, ...]:
        """
        Build a temporary dictionary from raw voter binary string

        :param bytes history: A byte string containing a raw row of history data
        :return: A tuple of SQL ready prepared parameters
        :rtype: tuple[str | None, ...]
        """
        history = dict(zip(self.history_keys, list(history.values())))
        if history['voter_id'] == '':
            history['voter_id'] = 0
        for k in ["election_date"]:
            history[k] = datetime.datetime.strptime(history[k], "%m/%d/%Y").strftime('%Y-%m-%d')
        return tuple(history.values())

    def parse_voter_into_tuple(self, voter: dict[str, str | None]) -> tuple[str | None, ...]:
        """
        Build a temporary dictionary from raw voter import dictionary

        :param dict voter: A raw dictionary of voter data
        :return: A tuple of SQL ready prepared parameters
        :rtype: tuple[str | None, ...]
        """
        row = {}
        for k, v in self.voter_keys.items():
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
