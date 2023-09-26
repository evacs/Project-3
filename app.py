# Hate Crimes in the US
# Flask App

from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

app = Flask(__name__)

# Create a SQLAlchemy database engine
db_uri = 'postgresql://admin:fRFTp6MgD7AgfQYMYmyM5jaR8KAfKyXV@dpg-ck56k66ru70s738p5s4g-a.oregon-postgres.render.com:5432/us_hate_crimes'
engine = create_engine(db_uri)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

print(Base.classes.keys())
session = Session(engine)

# Define static routes

# Launches site
@app.route('/') 
def index():
    return render_template('index.html')

# Turns main_incidents table into a JSON dictionary
@app.route('/data')
def get_data():

    try:

        result = session.query(Base.classes.main_incidents).all()
        # Convert the query result to a list of dictionaries              
        dataToReturn = {}

        incident_ids = []
        state_names = []
        bias_descs = []

        for row in result:
            incident_ids.append(row.__dict__["incident_id"])
            state_names.append(row.__dict__["state_name"])
            bias_descs.append(row.__dict__["bias_desc"])

        dataToReturn["incident_id"] = incident_ids
        dataToReturn["state_name"] = state_names
        dataToReturn["bias_desc"] = bias_descs
        # Print a success message
        print("Table access successful")

        return jsonify(dataToReturn)

    except Exception as e:
        # Handle and log any exceptions
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

        # Create session
        session = Session(engine)

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
                incident_rate.append(row.incidents / row.population * 10000000)
            
            # Store lists in a dictionary and append to data list
            current_year = {'year': year, 'states': states, 'population': population,
                            'incidents': incidents, 'incident_rate': incident_rate}
            data.append(current_year)
        
        dataToReturn['years'] = years
        dataToReturn['data'] = data
        
        session.close()

        # Print a success message
        print("Table access successful")

        return jsonify(dataToReturn)

    except Exception as e:
        # Handle and log any exceptions
        print("Error accessing the table:", str(e))
        return jsonify({"error": "Table access failed"}), 500    


if __name__ == '__main__':
    app.run(debug=True)