# Hate Crimes in the US
# Flask App

from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine, text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from collections import Counter
from sqlalchemy import func


app = Flask(__name__)

# # LOCAL DB:

DB_USERNAME = 'postgres'
DB_PASSWORD = 'E745040s'
DB_HOST = 'localhost'  # e.g., localhost or database server IP
DB_PORT = '5432'  # PostgreSQL default port is 5432
DB_NAME = 'hatecrimes'
db_uri = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# # ONLINE DB:
# db_uri = 'postgresql://admin:fRFTp6MgD7AgfQYMYmyM5jaR8KAfKyXV@dpg-ck56k66ru70s738p5s4g-a.oregon-postgres.render.com:5432/us_hate_crimes'


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

# Route accesses table data and returns json array of dicts
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


# @app.route('/time')
# def get_data():
#     data = [1,2,3]
#     return jsonify(data)

@app.route('/time')
def get_data():
    try:
        
        main_incidents = Base.classes.main_incidents
        
        result = session.query(
            main_incidents.data_year,
            func.count(main_incidents.incident_id).label("count")  # Change label to "count"
        ).group_by(
            main_incidents.data_year
        ).order_by(main_incidents.data_year.asc()).all()

        session.close()
        
                
        # Convert the query result to a list of dictionaries
        data_list = [{"data_year": row.data_year, "count": row.count} for row in result]

        dataToReturn = {"time_data": data_list}

        # Print a success message
        print("Table access successful")

        return jsonify(dataToReturn)        
        #return jsonify(data_list)
    except Exception as e:
        print("Error accessing the table:", str(e))
        return jsonify({"error": "Table access failed"}), 500

# THIS GOES AT THE END OF THE FILE ONLY    
if __name__ == '__main__':
    app.run(debug=True)


