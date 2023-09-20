-- Project 3: US Hate Crimes

-- This SQL file includes:
-- 1. PostgreSQL schema and code to create database tables
-- 2. PostgreSQL code to review and verify imported data

-- 1. Create database tables

CREATE TABLE states (
	state_abbr VARCHAR(2) NOT NULL,
	state VARCHAR(20) NOT NULL, 
	division VARCHAR(20) NOT NULL,
	region VARCHAR(10) NOT NULL,
	PRIMARY KEY (state_abbr)
);

CREATE TABLE agency_types (
	agency_type_id INT NOT NULL, 
	agency_type VARCHAR(25) NOT NULL,
	PRIMARY KEY (agency_type_id)
);

CREATE TABLE agencies (
	agency_id INT NOT NULL, 
	agency VARCHAR(75) NOT NULL,
	PRIMARY KEY (agency_id)
);

CREATE TABLE agency_oris (
	ori VARCHAR(10) NOT NULL,
	agency_id INT NOT NULL,
	agency_unit VARCHAR(50) NOT NULL,
	agency_type_id INT NOT NULL,
	PRIMARY KEY (ori),
	FOREIGN KEY (agency_id) REFERENCES agencies(agency_id),
	FOREIGN KEY (agency_type_id) REFERENCES agency_types(agency_type_id)
);

CREATE TABLE population_groups (
	population_group_code VARCHAR(2) NOT NULL, 
	population_group VARCHAR(70) NOT NULL,
	PRIMARY KEY (population_group_code)
);

CREATE TABLE race (
	race_id INT NOT NULL,
	race VARCHAR(50) NOT NULL,
	PRIMARY KEY (race_id)
);

CREATE TABLE ethnicity (
	ethnicity_id INT NOT NULL,
	ethnicity VARCHAR(20) NOT NULL,
	PRIMARY KEY (ethnicity_id)
);

CREATE TABLE incidents (
	incident_id INT NOT NULL,
	ori VARCHAR(10) NOT NULL,
	agency_id INT NOT NULL,
	agency_unit_id INT NOT NULL,
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
	PRIMARY KEY (incident_id),
	FOREIGN KEY (ori) REFERENCES agency_oris(ori),
	FOREIGN KEY (population_group_code) REFERENCES population_groups(population_group_code),
	FOREIGN KEY (offender_race_id) REFERENCES race(race_id),
	FOREIGN KEY (offender_ethnicity_id) REFERENCES ethnicity(ethnicity_id)
);

CREATE TABLE offenses (
	offense_id INT NOT NULL,
	offense VARCHAR(25) NOT NULL,
	PRIMARY KEY (offense_id)
);

CREATE TABLE incident_offenses (
	incident_id INT NOT NULL,
	offense_id INT NOT NULL,
	PRIMARY KEY (incident_id, offense_id),
	FOREIGN KEY (incident_id) REFERENCES incidents(incident_id),
	FOREIGN KEY (offense_id) REFERENCES offenses(offense_id)
);

CREATE TABLE locations (
	location_id INT NOT NULL,
	location VARCHAR(25) NOT NULL,
	PRIMARY KEY (location_id)
);

CREATE TABLE incident_locations (
	incident_id INT NOT NULL,
	location_id INT NOT NULL,
	PRIMARY KEY (incident_id, location_id),
	FOREIGN KEY (incident_id) REFERENCES incidents(incident_id),
	FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

CREATE TABLE bias_categories (
	category_id INT NOT NULL,
	category VARCHAR(25) NOT NULL,
	PRIMARY KEY (category_id)
);

CREATE TABLE bias (
	bias_id INT NOT NULL,
	bias VARCHAR(60) NOT NULL,
	category_id INT NOT NULL,
	PRIMARY KEY (bias_id),
	FOREIGN KEY (category_id) REFERENCES bias_categories(category_id)
);	

CREATE TABLE incident_biases (
	incident_id INT NOT NULL,
	bias_id INT NOT NULL,
	PRIMARY KEY (incident_id, bias_id),
	FOREIGN KEY (incident_id) REFERENCES incidents(incident_id),
	FOREIGN KEY (bias_id) REFERENCES bias(bias_id)
);

CREATE TABLE victim_types (
	victim_type_id INT NOT NULL,
	victim_type VARCHAR(25) NOT NULL,
	PRIMARY KEY (victim_type_id)
);

CREATE TABLE incident_victim_types (
	incident_id INT NOT NULL,
	victim_type_id INT NOT NULL,
	PRIMARY KEY (incident_id, victim_type_id),
	FOREIGN KEY (incident_id) REFERENCES incidents(incident_id),
	FOREIGN KEY (victim_type_id) REFERENCES victim_types(victim_type_id)
);

CREATE TABLE census_data (
	id INT NOT NULL,
	year INT NOT NULL,
	state_abbr VARCHAR(2) NOT NULL,
	race_id INT NOT NULL,
	population INT NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (state_abbr) REFERENCES states(state_abbr),
	FOREIGN KEY (race_id) REFERENCES race(race_id)
);

-- 2. Review and verify imported data

SELECT * FROM agencies;
SELECT COUNT(*) FROM agencies;				-- x records
SELECT * FROM agency_oris;
SELECT COUNT(*) FROM agency_oris;			-- x records
SELECT * FROM agency_types;
SELECT COUNT(*) FROM agency_types;			-- x records
SELECT * FROM bias;
SELECT COUNT(*) FROM bias;					-- x records
SELECT * FROM bias_categories;
SELECT COUNT(*) FROM bias_categories;		-- x records
SELECT * FROM incident_biases;
SELECT COUNT(*) FROM incident_biases;		-- x records
SELECT * FROM incident_locations;	
SELECT COUNT(*) FROM incident_locations;	-- x records
SELECT * FROM incident_offenses;
SELECT COUNT(*) FROM incident_offenses;		-- x records
SELECT * FROM incident_victim_types;
SELECT COUNT(*) FROM incident_victim_types;	-- x records
SELECT * FROM incidents;
SELECT COUNT(*) FROM incidents;				-- x records
SELECT * FROM locations;
SELECT COUNT(*) FROM locations;				-- x records
SELECT * FROM ethnicity;
SELECT COUNT(*) FROM ethnicity;				-- x records
SELECT * FROM race;
SELECT COUNT(*) FROM race;					-- x records
SELECT * FROM offenses;
SELECT COUNT(*) FROM offenses;				-- x records
SELECT * FROM population_groups;
SELECT COUNT(*) FROM population_groups;		-- x records
SELECT * FROM states;
SELECT COUNT(*) FROM states;				-- x records
SELECT * FROM victim_types;
SELECT COUNT(*) FROM victim_types;			-- x records
SELECT * FROM census_data;
SELECT COUNT(*) FROM census_data;			-- x records