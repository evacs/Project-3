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

years = []
states = []
biases = []
bias_categories = []

[years.append(year) for year in range(2009, 2022)]

for row in session.query(Base.classes.states).all():
    states.append(row.__dict__['state'])

for row in session.query(Base.classes.bias).all():
    biases.append(row.__dict__['bias'])

for row in session.query(Base.classes.bias_categories).all():
    bias_categories.append(row.__dict__['category'])

#Define static routes

# Launches site
@app.route('/') 
def index():
    return render_template('index.html')



# Turns main_incidents table into a JSON dictionary
@app.route('/data')
def get_data():

    try:
        
        c = Base.classes.census_data
        s = Base.classes.states
        pop_data = session.query(c, s).filter(c.states_abbr == s.states_abbr).filter(c.race_id == -1).all()
        
        state_pop = []
        for record in pop_data:
            (c, s) = record
            state_pop.append()

            

        
        
        for record in session.query(Base.classes.census_data).all():
            for year in years:
                state_pop.append()
                



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

@app.route('/jeff')
def get_data_jeff():

    try:

        result = session.query(Base.classes.main_incidents).all()
        # Convert the query result to a list of dictionaries              
        dataToReturn = {}

        dataToReturn['states'] = states
        dataToReturn['years'] = years
        dataToReturn['biases'] = biases


        
        print("Table access successful")

        return jsonify(dataToReturn)

    except Exception as e:
        # Handle and log any exceptions
        print("Error accessing the table:", str(e))
        return jsonify({"error": "Table access failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)