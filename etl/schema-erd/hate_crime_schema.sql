-- Project 3: US Hate Crimes

-- This SQL file includes:
-- 1. PostgreSQL schema and code to create database tables
-- 2. PostgreSQL code to review and verify imported data

-- 1. Create database tables

CREATE TABLE states (
	state_abbr VARCHAR(2) NOT NULL,
	state_name VARCHAR(20) NOT NULL, 
	division_name VARCHAR(20) NOT NULL,
	region_name VARCHAR(10) NOT NULL,
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
	agency_type_id INT NOT NULL, 
	PRIMARY KEY (agency_id)
);

CREATE TABLE agency_units (
	agency_unit_id INT NOT NULL, 
	agency_id INT NOT NULL, 
	agency_unit VARCHAR(50) NOT NULL,
	PRIMARY KEY (agency_unit_id)
);

CREATE TABLE population_groups (
	population_group_code VARCHAR(2) NOT NULL, 
	population_group VARCHAR(50) NOT NULL,
	PRIMARY KEY (population_group_code)
);

CREATE TABLE offender_race (
	offender_race_id INT NOT NULL,
	offender_race VARCHAR(50) NOT NULL,
	PRIMARY KEY (offender_race_id)
);

CREATE TABLE offender_ethnicity (
	offender_ethnicity_id INT NOT NULL,
	offender_ethnicity VARCHAR(20) NOT NULL,
	PRIMARY KEY (offender_ethnicity_id)
);

CREATE TABLE multiple_options (
	option VARCHAR(1) NOT NULL,
	PRIMARY KEY (option)
);

CREATE TABLE incidents (
	incident_id INT NOT NULL,
	ori INT NOT NULL,
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
	offender_ethnicity_ID INT NOT NULL,
	victim_count INT NOT NULL,
	total_individual_victims INT NOT NULL,
	multiple_offense VARCHAR(2) NOT NULL,
	multiple_bias VARCHAR(2) NOT NULL,
	PRIMARY KEY (incident_id),
	FOREIGN KEY (agency_id) REFERENCES agencies(agency_id),
	FOREIGN KEY (population_group_code) REFERENCES population_groups(population_group_code),
	FOREIGN KEY (offender_race_id) REFERENCES offender_race(offender_race_id),
	FOREIGN KEY (offender_ethnicity_ID) REFERENCES offender_ethnicity(offender_ethnicity_ID),
	FOREIGN KEY (multiple_offense) REFERENCES multiple_options(option),
	FOREIGN KEY (multiple_bias) REFERENCES multiple_options(option)
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

CREATE TABLE bias (
	bias_id INT NOT NULL,
	bias VARCHAR(25) NOT NULL,
	PRIMARY KEY (bias_id)
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


-- 2. Review and verify imported data

SELECT * FROM agencies;
SELECT COUNT(*) FROM agencies;				-- x records
SELECT * FROM agency_types;
SELECT COUNT(*) FROM agency_types;			-- x records
SELECT * FROM agency_units;
SELECT COUNT(*) FROM agency_units;			-- x records
SELECT * FROM bias;
SELECT COUNT(*) FROM bias;					-- x records
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
SELECT * FROM multiple_options;
SELECT COUNT(*) FROM multiple_options;		-- x records
SELECT * FROM offender_ethnicity;
SELECT COUNT(*) FROM offender_ethnicity;	-- x records
SELECT * FROM offender_race;
SELECT COUNT(*) FROM offender_race;			-- x records
SELECT * FROM offenses;
SELECT COUNT(*) FROM offenses;				-- x records
SELECT * FROM population_groups;
SELECT COUNT(*) FROM population_groups;		-- x records
SELECT * FROM states;
SELECT COUNT(*) FROM states;				-- x records
SELECT * FROM victim_types;
SELECT COUNT(*) FROM victim_types;			-- x records