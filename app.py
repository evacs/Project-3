# US Hate Crimes App 

# Import dependencies
from flask import Flask, render_template

# Create app
app = Flask(__name__)

# Define static routes
@app.route('/')
def index():
    print('Server request for home page...')
    return render_template('index.html')

@app.route('/api/app1')
def app1():
    return 'Application 1'

@app.route('/api/app2')
def app2():
    return 'Application 2'
