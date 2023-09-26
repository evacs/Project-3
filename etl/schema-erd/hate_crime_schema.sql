-- Project 3: US Hate Crimes

-- This SQL file includes:
-- 1. PostgreSQL schema and code to create database tables
-- 2. PostgreSQL code to review and verify imported data

-- 1. Create database tables

CREATE TABLE states (
	state_abbr VARCHAR(2) NOT NULL,
	state VARCHAR(25) NOT NULL, 
	division VARCHAR(20) NOT NULL,
	region VARCHAR(20) NOT NULL,
	CONSTRAINT state_abbr_pkey PRIMARY KEY (state_abbr)
);

CREATE TABLE agency_types (
	agency_type_id INT NOT NULL, 
	agency_type VARCHAR(25) NOT NULL,
	CONSTRAINT agency_type_id PRIMARY KEY (agency_type_id)
);

CREATE TABLE agencies (
	agency_id INT NOT NULL, 
	agency VARCHAR(75) NOT NULL,
	CONSTRAINT agency_id_pkey PRIMARY KEY (agency_id)
);

CREATE TABLE agency_oris (
	ori VARCHAR(10) NOT NULL,
	agency_id INT NOT NULL,
	agency_unit VARCHAR(50), -- This column is empty for cities and other agencies
	agency_type_id INT NOT NULL,
	CONSTRAINT ori_pkey PRIMARY KEY (ori),
	FOREIGN KEY (agency_id) REFERENCES agencies(agency_id),
	FOREIGN KEY (agency_type_id) REFERENCES agency_types(agency_type_id)
);

CREATE TABLE population_groups (
	population_group_code VARCHAR(2) NOT NULL, 
	population_group VARCHAR(70) NOT NULL,
	CONSTRAINT population_group_pkey PRIMARY KEY (population_group_code)
);

CREATE TABLE race (
	race_id INT NOT NULL,
	race VARCHAR(50) NOT NULL,
	CONSTRAINT race_id_pkey PRIMARY KEY (race_id)
);

CREATE TABLE ethnicity (
	ethnicity_id INT NOT NULL,
	ethnicity VARCHAR(50) NOT NULL,
	CONSTRAINT ethnicity_id_pkey PRIMARY KEY (ethnicity_id)
);

CREATE TABLE incidents (
	incident_id INT NOT NULL,
	ori VARCHAR(10) NOT NULL,
	agency_id INT NOT NULL,
	state_abbr VARCHAR(2) NOT NULL,
	population_group_code VARCHAR(2) NOT NULL,
	incident_date DATE NOT NULL,
	adult_victim_count INT NOT NULL,
	juvenile_victim_count INT NOT NULL,
	total_offender_count INT NOT NULL,
	adult_offender_count INT NOT NULL,
	juvenile_offender_count INT NOT NULL,
	offender_race_id INT NOT NULL,
	offender_ethnicity_id INT NOT NULL,
	victim_count INT NOT NULL,
	total_individual_victims INT NOT NULL,
	CONSTRAINT incident_id_pkey PRIMARY KEY (incident_id),
	FOREIGN KEY (ori) REFERENCES agency_oris(ori),
	FOREIGN KEY (population_group_code) REFERENCES population_groups(population_group_code),
	FOREIGN KEY (offender_race_id) REFERENCES race(race_id),
	FOREIGN KEY (offender_ethnicity_id) REFERENCES ethnicity(ethnicity_id)
);

CREATE TABLE offenses (
	offense_id INT NOT NULL,
	offense VARCHAR(50) NOT NULL,
	CONSTRAINT offense_id_pkey PRIMARY KEY (offense_id)
);

CREATE TABLE incident_offenses (
	incident_id INT NOT NULL,
	offense_id INT NOT NULL,
	CONSTRAINT incident_offense_pkey PRIMARY KEY (incident_id, offense_id),
	FOREIGN KEY (incident_id) REFERENCES incidents(incident_id),
	FOREIGN KEY (offense_id) REFERENCES offenses(offense_id)
);

CREATE TABLE locations (
	location_id INT NOT NULL,
	location VARCHAR(50) NOT NULL,
	CONSTRAINT location_id_pkey PRIMARY KEY (location_id)
);

CREATE TABLE incident_locations (
	incident_id INT NOT NULL,
	location_id INT NOT NULL,
	CONSTRAINT incident_location_pkey PRIMARY KEY (incident_id, location_id),
	FOREIGN KEY (incident_id) REFERENCES incidents(incident_id),
	FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

CREATE TABLE bias_categories (
	category_id INT NOT NULL,
	category VARCHAR(25) NOT NULL,
	CONSTRAINT category_id_pkey PRIMARY KEY (category_id)
);

CREATE TABLE bias (
	bias_id INT NOT NULL,
	bias VARCHAR(60) NOT NULL,
	category_id INT NOT NULL,
	CONSTRAINT bias_id_pkey PRIMARY KEY (bias_id),
	FOREIGN KEY (category_id) REFERENCES bias_categories(category_id)
);	

CREATE TABLE incident_biases (
	incident_id INT NOT NULL,
	bias_id INT NOT NULL,
	CONSTRAINT incident_bias_pkey PRIMARY KEY (incident_id, bias_id),
	FOREIGN KEY (incident_id) REFERENCES incidents(incident_id),
	FOREIGN KEY (bias_id) REFERENCES bias(bias_id)
);

CREATE TABLE victim_types (
	victim_type_id INT NOT NULL,
	victim_type VARCHAR(25) NOT NULL,
	CONSTRAINT victim_type_id_pkey PRIMARY KEY (victim_type_id)
);

CREATE TABLE incident_victim_types (
	incident_id INT NOT NULL,
	victim_type_id INT NOT NULL,
	CONSTRAINT incident_victim_type_pkey PRIMARY KEY (incident_id, victim_type_id),
	FOREIGN KEY (incident_id) REFERENCES incidents(incident_id),
	FOREIGN KEY (victim_type_id) REFERENCES victim_types(victim_type_id)
);

CREATE TABLE census_data (
	id INT NOT NULL,
	year INT NOT NULL,
	state_abbr VARCHAR(2) NOT NULL,
	race_id INT NOT NULL,
	population INT NOT NULL,
	CONSTRAINT id_pkey PRIMARY KEY (id),
	FOREIGN KEY (state_abbr) REFERENCES states(state_abbr),
	FOREIGN KEY (race_id) REFERENCES race(race_id)
);

CREATE TABLE main_incidents (
	incident_id INT NOT NULL,
	data_year INT NOT NULL,
	state_abbr VARCHAR(2) NOT NULL,
	state_name VARCHAR(25) NOT NULL, 
	total_offender_count INT NOT NULL,
	offender_race VARCHAR(50) NOT NULL,
	offender_ethnicity VARCHAR(50) NOT NULL,
	victim_count INT,
	offense_name VARCHAR(255) NOT NULL,
	total_individual_victims NUMERIC,
	bias_desc VARCHAR(255) NOT NULL,
	victim_types VARCHAR(255) NOT NULL,
	multiple_offense VARCHAR(1) NOT NULL,
	multiple_bias VARCHAR(2) NOT NULL,
	CONSTRAINT incident_pkey PRIMARY KEY (incident_id)
);


-- 2. Review and verify imported data

SELECT * FROM agencies;					-- 5313 records
SELECT * FROM agency_oris;				-- 7669 records
SELECT * FROM agency_types;				-- 8 records
SELECT * FROM bias;						-- 35 records
SELECT * FROM bias_categories;			-- 6 records
SELECT * FROM incident_biases;			-- 91298 records
SELECT * FROM incident_locations;		-- 89556 records
SELECT * FROM incident_offenses;		-- 86384 records
SELECT * FROM incident_victim_types;	-- 90950 records
SELECT * FROM incidents;				-- 89405 records
SELECT * FROM locations;				-- 46 records
SELECT * FROM ethnicity;				-- 5 records
SELECT * FROM race;						-- 8 records
SELECT * FROM offenses;					-- 41 records
SELECT * FROM population_groups			-- 20 records
SELECT * FROM states;					-- 53 records
SELECT * FROM victim_types;				-- 9 records
SELECT * FROM census_data;				-- 4641 records
SELECT * FROM main_incidents;			-- 89405 records