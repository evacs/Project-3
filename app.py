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
# ---------------------------------------------------------------------------------
# DB_USERNAME = 'postgres'
# DB_PASSWORD = 'PASSWORD'
# DB_HOST = 'localhost'  # e.g., localhost or database server IP
# DB_PORT = '5432'  # PostgreSQL default port is 5432
# DB_NAME = 'hatecrimes' # your db name
# db_uri = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
# --------------------------------------------------------------------------------------

# # ONLINE DB:
db_uri = 'postgresql://admin:fRFTp6MgD7AgfQYMYmyM5jaR8KAfKyXV@dpg-ck56k66ru70s738p5s4g-a.oregon-postgres.render.com:5432/us_hate_crimes'


engine = create_engine(db_uri)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

#print(Base.classes.keys())
session = Session(engine)

# ---------------------------------------
# DEFINE YOUR ROUTES:
# ---------------------------------------

# @app.route('/general')
# def get_data():
#     try:
#         your code    
#         return jsonify(data)
#     except Exception as e:
#         print("Error accessing the table:", str(e))
#         return jsonify({"error": "Table access failed"}), 500

# #Define static routes
# # Variables for related tables
# bias = Base.classes.bias
# bias_categories = Base.classes.bias_categories
# main_inc = Base.classes.main_incidents

# # query statement
# sel = [main_inc.data_year, main_inc.state_name, main_inc.bias_desc,
#         main_inc.incident_id, bias_categories.category]

# # join statement
# query = session.query(*sel)\
#         .filter(bias.bias == main_inc.bias_desc)\
#         .filter(bias.category_id == bias_categories.category_id)

# # Query statement
# result = query.group_by(
#     main_inc.state_name,
#     bias_categories.category,
#     main_inc.data_year).all()

# # Create a list of dictionaries
# keys = ["year","state","bias","id","category"]
# bias_dict = []
# bias_dict = [dict(zip(keys, item)) for item in result]
# # Assign the metadata list to the "metadata" key in the data dictionary
# dataToReturn = {"bias_data": bias_dict}
# print(dataToReturn[:5])




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

        return jsonify(dataToReturn)        
        #return jsonify(data_list)
    except Exception as e:
        print("Error accessing the table:", str(e))
        return jsonify({"error": "Table access failed"}), 500
    


# THIS GOES AT THE END OF THE FILE ONLY 
session.close()   
if __name__ == '__main__':
    app.run(debug=True)


