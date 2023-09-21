# US Hate Crimes App 

# Import dependencies
from flask import Flask

# Create app
app = Flask(__name__)

# Define static routes
@app.route('/')
def index():
    return (
        f'Available routes:<br/>'
        f'<ol>'
        f'<li><a href="/api/test1">/api/app1</a> - Application 1</li>'
        f'<li><a href="/api/test2">/api/app2</a> - Application 2</li>'
        f'</ol>'
    )

@app.route('/api/app1')
def app1():
    return 'Application 1'

@app.route('/api/app2')
def app2():
    return 'Application 2'
