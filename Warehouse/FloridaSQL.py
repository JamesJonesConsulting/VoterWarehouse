# -*- coding: utf-8 -*-

# Handles Database SQL methods for Florida data

def create_database(database: str) -> str:
    """
    create_database Returns SQL string to create the schema

    :param str database: The name of the schema
    :return: SQL String
    """
    return f"CREATE DATABASE IF NOT EXISTS `{database}` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE " \
           f"utf8mb4_unicode_ci */;"


def create_histories_table() -> str:
    """
    create_histories_table Returns SQL string to create the Voter Histories table

    :return: SQL String
    :rtype: str
    """
    return """CREATE TABLE IF NOT EXISTS `Histories` (
          `county_code` char(3) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voter_id` bigint(18) unsigned NOT NULL DEFAULT 0,
          `election_date` date NOT NULL,
          `election_type` char(3) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `history_code` char(1) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `export_date` date NOT NULL,
          PRIMARY KEY (`county_code`,`voter_id`,`election_date`,`election_type`,`history_code`),
          KEY `county_code` (`county_code`),
          KEY `voter_id` (`voter_id`),
          KEY `election_date` (`election_date`),
          KEY `election_type` (`election_type`),
          KEY `history_code` (`history_code`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
    """


def set_history() -> str:
    """
    set_voter Returns SQL string to replace the Histories records

    :return: SQL String
    :rtype: str
    """
    return """REPLACE
        INTO
        Histories
    (county_code,
        voter_id,
        election_date,
        election_type,
        history_code,
        export_date)
    VALUES(%s,
        %s,
        %s,
        %s,
        %s,
        %s);"""


def set_voter() -> str:
    """
    set_voter Returns SQL string to replace the Voter records

    :return: SQL String
    :rtype str
    """
    return """REPLACE
        INTO
        Voters
    (county_code,
        voter_id,
        name_last,
        name_suffix,
        name_first,
        name_middle,
        suppress_address,
        residence_address_line_1,
        residence_address_line_2,
        residence_city,
        residence_state,
        residence_zipcode,
        mailing_address_line_1,
        mailing_address_line_2,
        mailing_address_line_3,
        mailing_city,
        mailing_state,
        mailing_zipcode,
        mailing_country,
        gender,
        race,
        birth_date,
        registration_date,
        party_affiliation,
        precinct,
        precinct_group,
        precinct_split,
        precinct_suffix,
        voter_status,
        congressional_district,
        house_district,
        senate_district,
        county_commission_district,
        school_board_district,
        daytime_area_code,
        daytime_phone_number,
        daytime_phone_extension,
        email_address,
        export_date)
    VALUES(%s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s);"""


def create_voters_table() -> str:
    """
    create_voters_table Returns SQL string to create the Voter table

    :return: SQL String
    :rtype: str
    """
    return """CREATE TABLE IF NOT EXISTS `Voters` (
          `voter_id` bigint(18) unsigned NOT NULL,
          `county_code` varchar(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `name_last` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `name_suffix` varchar(5) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `name_first` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `name_middle` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `suppress_address` varchar(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `residence_address_line_1` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `residence_address_line_2` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `residence_city` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `residence_state` varchar(2) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `residence_zipcode` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_address_line_1` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_address_line_2` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_address_line_3` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_city` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_state` varchar(2) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_zipcode` varchar(12) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_country` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `gender` varchar(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `race` bigint(18) unsigned DEFAULT NULL,
          `birth_date` date DEFAULT NULL,
          `registration_date` date DEFAULT NULL,
          `party_affiliation` varchar(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `precinct` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `precinct_group` varchar(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `precinct_split` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `precinct_suffix` varchar(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voter_status` varchar(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `congressional_district` varchar(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `house_district` varchar(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `senate_district` varchar(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `county_commission_district` varchar(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `school_board_district` varchar(2) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `daytime_area_code` varchar(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `daytime_phone_number` varchar(7) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `daytime_phone_extension` varchar(4) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `email_address` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `export_date` date NOT NULL,
          PRIMARY KEY (`voter_id`),
          KEY `voter_id_index` (`voter_id`),
          KEY `county_code_index` (`county_code`),
          KEY `name_last_index` (`name_last`),
          KEY `name_first_index` (`name_first`),
          KEY `name_middle_index` (`name_middle`),
          KEY `residence_city_index` (`residence_city`),
          KEY `residence_zipcode_index` (`residence_zipcode`),
          KEY `mailing_city_index` (`mailing_city`),
          KEY `mailing_zipcode_index` (`mailing_zipcode`),
          KEY `export_date_index` (`export_date`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;    
    """
