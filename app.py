# Hate Crimes in the US
# Flask App

# Import dependencies
from flask import Flask, render_template
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
from flask import Flask, render_template

connection_string = "postgresql://admin:fRFTp6MgD7AgfQYMYmyM5jaR8KAfKyXV@dpg-ck56k66ru70s738p5s4g-a.oregon-postgres.render.com:5432/us_hate_crimes"

engine = create_engine(connection_string)


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

print(Base.classes.keys())
session = Session(engine)

# Create app
app = Flask(__name__)

# Define static routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/app1')
def app1():
    return 'Application 1'

@app.route('/api/app2')
def app2():
    return 'Application 2'

@app.route('/api/stateIncidents')
def stateIncidents():

    incident_biases = session.query(bias,incident_biases_2,incedents).join(bias.bias_id==incidents_biases_2.bias_id).join(incidents, incidents_id=incidents_biases_2.incident_id).group_by(incidents.state_abbr).all()
    data_dict_list = [row.as_dict() for row in incident_biases]

    # Use jsonify to pretty print the JSON response
    return jsonify(incident_biases=data_dict_list), 200

if __name__ == '__main__':
    app.run(debug=True)  

