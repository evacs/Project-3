# Hate Crimes in the US
# Flask App

from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import func

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


#Define static routes

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
    
@app.route('/matt')
def get_data_matt():

    try:
        
        # Save a reference to the main_incidents table as `main_incidents`
        main_incidents = Base.classes.main_incidents

        # Design a query that lists the count of hate crimes by state and bias description
        state_data = session.query(
            main_incidents.state_name,
            main_incidents.bias_desc,
            main_incidents.data_year,
            func.count(main_incidents.incident_id).label("count")
        ).group_by(
            main_incidents.state_name,
            main_incidents.bias_desc,
            main_incidents.data_year
        ).order_by(main_incidents.state_name.asc()).all()

        # Convert the query result to a list of dictionaries              
        state_data_list = [{"data_year": row.data_year, "state_name": row.state_name, "bias_desc": row.bias_desc, "count": row.count} for row in state_data]
        
        # Assign the metadata list to the "metadata" key in the data dictionary
        dataToReturn = {"state_data": state_data_list}

        # Print a success message
        print("Table access successful")

        return jsonify(dataToReturn)

    except Exception as e:
        # Handle and log any exceptions
        print("Error accessing the table:", str(e))
        return jsonify({"error": "Table access failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/api/app2')
# def app2():
#     return 'Application 2'



