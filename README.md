# Project 3: Hate Crimes in the US

https://us-hate-crimes-dev.onrender.com/

The purpose of this project was to analyze hate crimes in the United States between 2009 and 2021, looking at trends by state, type of hate crime and offenses committed. 

## Repository Contents
This repository contains the following files:
1. README.md - This file
2. app.py - Python file for flask application
3. render_reqs.txt - Text file used by hosting service, Render.com. This file contains a list of all Python libraries needed to host the website.
4. etl\ - Folder with Jupyter and Python files for data extraction and transformation
5. etl\data - Folder with exported CSV files for loading the database
6. etl\schema-erd - Folder with ERD and SQL files to create PostgreSQL database
7. static\js - Folder with all Javascript files for web page
8. resources - Source data files for ETL and support documents from data source
9. templates - Folder for HTML files (SQLAlchemy requires files in this folder to render them from a Flask app

## Challenges

There were several challenges in this project:
1. FBI Hate Crime Dataset - Several fields in the dataset (offense, bias, location, victim type) contained multiple values in one record. These were distiguished as separate records during extraction and transformation but resulted in a complex schema and normalized PostgreSQL database. The dataset also did not include information regarding the city or state where the hate crime was committed. It did include information regarding the reporting agency which included the state and in some cases the city as the name or unit of the agency. The dashboards were based on this state field and it's very possible that some of the incidents occurred in a different state from the reporting agency. This was not noted in any documentation on the FBI site.
2. Party Control by State - The initial question posed by the team was 1) is there a relationship between the increase or decrease of hate crimes based on the political climate over time and 2) is there a relationship between hate crimes and local political affiliation by state. After much onine research, the only available free data were annual pdfs from the National Conference of State Legislatures (NCSL). The team was able to extract data from these pdfs using a tabula-py, a wrapper for tabula-java, a java library, but there was not sufficent time to fully clean and transform the data into validated csv files.
3. PostgreSQL Database - As stated above, the normalized PostgreSQL database was complex and contained many tables and relationships. The process of extracting and transforming the data into csv files to create the database was time-consuming and delayed the creation of the flask apps and dashboards. As a result, some of the flask apps were based on a table that mirrored the initial hate critme dataset with multiple values in one record. In hindsight, it may have been more effective to use MongoDB or simplify the database schema.
4. Database and Website Hosting - The advantage of using a hosting service (Render) was the ability for everyone to use the same database and test the code and html using the same service, rather than doing this locally. The challenge in this was learning how to publish the database and website for Render and then discovering the limitations of their free plan, specifically the reliability of remote connections when the hosted server spun down due to inactivity. Although a final published site is up and running, local testing was most effective.
5. Github - The group is still learning Github and the best way to effectively manage and merge code. Juypter notebooks for data cleaning were not integrated and some code in the app.py and app.js needed to be manually updated in the main branch due to merging issues.
6. Project Management - As with Github, the group is still learning how best to divide up work and adequately estimate the time needed for that work. This created delays and impacted the final product. The dashboard was created the last two days of the project and did not include several planned interactive charts and information. 

## Conclusions



