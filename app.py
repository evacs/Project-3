# Hate Crimes in the US
# Flask App

from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine, text, func, extract
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt

app = Flask(__name__)

# # LOCAL DB:
# ---------------------------------------------------------------------------------
# DB_USERNAME = 'postgres'
# DB_PASSWORD = 'PASSWORD'
# DB_HOST = 'localhost'  # e.g., localhost or database server IP
# DB_PORT = '5432'  # PostgreSQL default port is 5432
# DB_NAME = 'hatecrimes' # your db name
# db_uri = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
# --------------------------------------------------------------------------------------


# Create a SQLAlchemy database engine
# Jeff's Login:
db_url = 'postgresql://postgres:bootcamp2023@localhost:5432/us_hate_crimes'
# Online Server:
# db_url = 'postgresql://admin:fRFTp6MgD7AgfQYMYmyM5jaR8KAfKyXV@dpg-ck56k66ru70s738p5s4g-a.oregon-postgres.render.com:5432/us_hate_crimes'
engine = create_engine(db_url)

# Reflect an existing database and tables
Base = automap_base()
Base.prepare(autoload_with=engine)

session = Session(engine)

print('Connected to database and session initiated')

# Define static routes

# Launches site
@app.route('/') 
def index():
    return render_template('index.html')


# gets data based on bias
@app.route('/bias')
def get_data_bias():

    try:
        # Variables for related tables
        bias = Base.classes.bias
        bias_categories = Base.classes.bias_categories
        main_inc = Base.classes.main_incidents
        
        # query statement
        sel = [main_inc.data_year, main_inc.state_name, main_inc.bias_desc,
               main_inc.incident_id, bias_categories.category]

        # join statement
        query = session.query(*sel)\
                .filter(bias.bias == main_inc.bias_desc)\
                .filter(bias.category_id == bias_categories.category_id)

        # Query statement
        result = query.all()

        # Create a list of dictionaries
        keys = ["year","state","bias","id","category"]
        bias_dict = []
        bias_dict = [dict(zip(keys, item)) for item in result]
        # Assign the metadata list to the "metadata" key in the data dictionary
        dataToReturn = {"bias_data": bias_dict}
                
        return jsonify(dataToReturn)   
       

    except Exception as e:
        # Handle and log any exceptions
        print("Error accessing the table:", str(e))
        return jsonify({"error": "Table access failed"}), 500

# Route to access data for time vs bias per state chart
@app.route('/matt')
def get_data_matt():
    try:
        # Variables for related tables
        bias = Base.classes.bias
        bias_categories = Base.classes.bias_categories
        main_inc = Base.classes.main_incidents

        # Query statement
        result = session.query(
            main_inc.data_year,
            main_inc.state_name,
            bias_categories.category,  # Use category instead of bias_desc
            func.count(main_inc.incident_id).label("count")
        ).join(bias, bias.bias == main_inc.bias_desc)\
         .join(bias_categories, bias_categories.category_id == bias.category_id)\
         .group_by(main_inc.data_year, main_inc.state_name, bias_categories.category)\
         .order_by(main_inc.data_year.asc()).all()

        # Create a list of dictionaries
        keys = ["year", "state", "category", "count"]  # Update keys to include "category"
        category_dict = [dict(zip(keys, item)) for item in result]

        # Assign the metadata list to the "metadata" key in the data dictionary
        dataToReturn = {"state_data": category_dict}

        return jsonify(dataToReturn)

    except Exception as e:
        # Handle and log any exceptions
        print("Error accessing the table:", str(e))
        return jsonify({"error": "Table access failed"}), 500


@app.route('/time')
def get_data_time():
    try:
        
        main_incidents = Base.classes.main_incidents
        
        result = session.query(
            main_incidents.data_year,
            func.count(main_incidents.incident_id).label("count")  # Change label to "count"
        ).group_by(
            main_incidents.data_year
        ).order_by(main_incidents.data_year.asc()).all()               
                
        # Convert the query result to a list of dictionaries
        data_list = [{"data_year": row.data_year, "count": row.count} for row in result]

        dataToReturn = {"time_data": data_list}

        # Print a success message
        print("Table access successful")
        
        # return jsonify(data_list)
        return jsonify(dataToReturn)        
        
    except Exception as e:
        print("Error accessing the table:", str(e))
        return jsonify({"error": "Table access failed"}), 500
    
@app.route('/top10Data')
def get_top10_data():

    try:
        # Create dictionary to hold all data
        dataToReturn = {}

        # Store tables in variables
        C = Base.classes.census_data
        S = Base.classes.states
        I = Base.classes.incidents

        # Create list of all states and add to data dictionary
        states = []
        # Don't include Federal Government and Guam in list of states
        query = session.query(S).filter(S.state_abbr != 'FS').filter(S.state_abbr != 'GM')
        for row in query.all():
            states.append(row.state)
        dataToReturn['states'] = states

        # Query to get population and incident counts by state and year
        sel = [C.year, S.state, C.population, I.incident_id]
        query = session.query(C.year, S.state, func.min(C.population).label('population'), func.count(I.incident_id).label('incidents'))
        query = query.filter(C.state_abbr == S.state_abbr).filter(C.race_id == -1)
        query = query.filter(I.state_abbr == S.state_abbr).filter(extract('year', I.incident_date) == C.year)
        query = query.group_by(C.year, S.state)
        query = query.order_by(func.count(I.incident_id).desc())

        # Create lists for data and years
        data = []
        years = []
        
        # Set years in list
        [years.append(year) for year in range(2009, 2022)]

        # Loop through each year to create data lists
        for year in years:
            states = []
            population = []
            incidents = []
            incident_rate = []
            
            # Loop through every row for the year
            for row in query.filter(C.year == year).all():
                # Append data to list for the year
                states.append(row.state)
                population.append(row.population)
                incidents.append(row.incidents)
                incident_rate.append(round(row.incidents / row.population * 10000000, 2))
            
            # Store lists in a dictionary and append to data list
            current_year = {'year': year, 'states': states, 'population': population,
                            'incidents': incidents, 'incident_rate': incident_rate}
            data.append(current_year)
        
        dataToReturn['years'] = years
        dataToReturn['data'] = data
        return jsonify(dataToReturn)

    except Exception as e:
        # Handle and log any exceptions
        print("Error accessing the table:", str(e))
        return jsonify({"error": "Table access failed"}), 500    


# THIS GOES AT THE END OF THE FILE ONLY 
session.close()   
if __name__ == '__main__':
    app.run(debug=True)


