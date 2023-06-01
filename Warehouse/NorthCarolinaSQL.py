# -*- coding: utf-8 -*-

# Handles Database SQL methods for Georgia data


def create_database(database: str) -> str:
    """
    create_database Returns SQL string to create the schema

    :param str database: The name of the schema
    :return: SQL String
    """
    return f"CREATE DATABASE IF NOT EXISTS `{database}` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE " \
           f"utf8mb4_unicode_ci */;"


def create_counties_table() -> str:
    """
    create_counties_table Returns SQL string to create the Voter Counties table

    :return: SQL String
    :rtype: str
    """
    return """CREATE TABLE IF NOT EXISTS `Counties` (
          `county_code` char(3) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `name` varchar(30) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          PRIMARY KEY (`county_code`),
          KEY `county_code` (`county_code`),
          KEY `name` (`name`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
    """


def set_county() -> str:
    """
    set_voter Returns SQL string to replace the Histories records

    :return: SQL String
    :rtype: str
    """
    return """INSERT IGNORE
        INTO
        Counties
    (county_code,
        name)
    VALUES(%s,
        %s);"""


def create_histories_table() -> str:
    """
    create_histories_table Returns SQL string to create the Voter Histories table

    :return: SQL String
    :rtype: str
    """
    return """CREATE TABLE IF NOT EXISTS `Histories` (
          `county_code` char(3) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `county_name` char(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voter_id` bigint(18) unsigned NOT NULL DEFAULT 0,
          `election_date` date NOT NULL,
          `election_type` varchar(230) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voting_method` varchar(60) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `party_code` char(3) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `party_name` varchar(60) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `precinct_code` varchar(6) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `precinct_name` varchar(60) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `ncid` varchar(12) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voted_county_code` char(3) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voted_county_name` char(60) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voter_tabulated_district_code` char(6) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voter_tabulated_district_name` char(60) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          PRIMARY KEY (`county_code`,`voter_id`,`election_date`,`election_type`,`party_code`),
          KEY `county_code` (`county_code`),
          KEY `voter_id` (`voter_id`),
          KEY `election_date` (`election_date`),
          KEY `election_type` (`election_type`),
          KEY `party_code` (`party_code`)
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
        county_name,
        voter_id,
        election_date,
        election_type,
        voting_method,
        party_code,
        party_name,
        precinct_code,
        precinct_name,
        ncid,
        voted_county_code,
        voted_county_name,
        voter_tabulated_district_code,
        voter_tabulated_district_name)
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
        %s);"""


def create_voters_table() -> str:
    """
    create_voters_table Returns SQL string to create the Voter table

    :return: SQL String
    :rtype: str
    """
    return """CREATE TABLE IF NOT EXISTS `Voters` (
          `voter_id` bigint(18) unsigned NOT NULL DEFAULT 0,
          `county_code` char(3) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `county_name` char(20) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `ncid` varchar(12) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `name_last` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `name_first` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `name_middle` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `name_suffix` varchar(5) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voter_status` char(2) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voter_status_desc` varchar(25) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voter_status_reason_code` varchar(2) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voter_status_reason_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `residence_address` varchar(65) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `residence_city` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `residence_state` varchar(2) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `residence_zipcode` char(9) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_address_line_1` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_address_line_2` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_address_line_3` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_address_line_4` varchar(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_city` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_state` varchar(2) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `mailing_zipcode` char(9) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `daytime_phone` varchar(12) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `confidential` char(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `registration_date` date NOT NULL,
          `race_code` char(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `ethnic_code` char(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `party_code` char(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `gender_code` char(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `birth_year` char(4) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `age_at_year_end` char(3) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `birth_state` varchar(2) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `drivers_lic` char(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `precinct` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `precinct_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `municipality` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `municipality_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `ward` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `ward_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `congressional_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `superior_court_jurisdiction` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `judicial_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `senate_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `house_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `county_commission_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `county_commission_district_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `township_jurisdiction` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `township_jurisdiction_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `school_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `school_district_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `fire_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `fire_district_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `water_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `water_district_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `sewer_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `sewer_district_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `sanitation_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `sanitation_district_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `rescue_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `rescue_district_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `municipal_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `municipal_district_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `prosecutorial_district` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `prosecutorial_district_desc` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voter_tabulated_district_code` varchar(6) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          `voter_tabulated_district_name` varchar(60) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
          PRIMARY KEY (`voter_id`,`county_code`),
          KEY `voter_id` (`voter_id`),
          KEY `county_code` (`county_code`),
          KEY `name_last` (`name_last`),
          KEY `name_first` (`name_first`),
          KEY `name_middle` (`name_middle`),
          KEY `residence_city` (`residence_city`),
          KEY `residence_zipcode` (`residence_zipcode`),
          KEY `mailing_city` (`mailing_city`),
          KEY `mailing_zipcode` (`mailing_zipcode`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;    
    """


def set_voter() -> str:
    """
    set_voter Returns SQL string to replace the Histories records

    :return: SQL String
    :rtype: str
    """
    return """REPLACE
        INTO
        Voters
    (`voter_id`,
        `county_code`,
        `county_name`,
        `ncid`,
        `name_last`,
        `name_first`,
        `name_middle`,
        `name_suffix`,
        `voter_status`,
        `voter_status_desc`,
        `voter_status_reason_code`,
        `voter_status_reason_desc`,
        `residence_address`,
        `residence_city`,
        `residence_state`,
        `residence_zipcode`,
        `mailing_address_line_1`,
        `mailing_address_line_2`,
        `mailing_address_line_3`,
        `mailing_address_line_4`,
        `mailing_city`,
        `mailing_state`,
        `mailing_zipcode`,
        `daytime_phone`,
        `confidential`,
        `registration_date`,
        `race_code`,
        `ethnic_code`,
        `party_code`,
        `gender_code`,
        `birth_year`,
        `age_at_year_end`,
        `birth_state`,
        `drivers_lic`,
        `precinct`,
        `precinct_desc`,
        `municipality`,
        `municipality_desc`,
        `ward`,
        `ward_desc`,
        `congressional_district`,
        `superior_court_jurisdiction`,
        `judicial_district`,
        `senate_district`,
        `house_district`,
        `county_commission_district`,
        `county_commission_district_desc`,
        `township_jurisdiction`,
        `township_jurisdiction_desc`,
        `school_district`,
        `school_district_desc`,
        `fire_district`,
        `fire_district_desc`,
        `water_district`,
        `water_district_desc`,
        `sewer_district`,
        `sewer_district_desc`,
        `sanitation_district`,
        `sanitation_district_desc`,
        `rescue_district`,
        `rescue_district_desc`,
        `municipal_district`,
        `municipal_district_desc`,
        `prosecutorial_district`,
        `prosecutorial_district_desc`,
        `voter_tabulated_district_code`,
        `voter_tabulated_district_name`)
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
