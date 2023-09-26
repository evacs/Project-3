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


#Define static routes

# Launches site
@app.route('/') 
def index():
    return render_template('index.html')

# Turns main_incidents table into a JSON dictionary
@app.route('/data')
def get_data():

    try:

        sel = [states.state_abbr, census_data.year, census_data.population, incidents.incident_id]
        query1 = db.session.query(*sel)
        query1 = query1.filter(states.state_abbr == census_data.state_abbr)
        query1 = query1.filter(states.state_abbr == incidents.state_abbr)
    
        result = query1.all()
    
        # You can customize the format of the response as needed
        response_data = {
            'state_abbr': result[0],
            'year': result[1],
            'population': result[2],
            'incident_id': result[3]
        }
    
        return jsonify(response_data)

    except Exception as e:
        # Handle and log any exceptions
        print("Error accessing the table:", str(e))
        return jsonify({"error": "Table access failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)

    
# @app.route('/api/app1')
# def app1():
#     return 'Application 1'

# @app.route('/api/app2')
# def app2():
#     return 'Application 2'



