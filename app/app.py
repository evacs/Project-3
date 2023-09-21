# 1. Import Flask
from flask import Flask

# 2. Create an app
app = Flask(__name__)

# 3. Define static routes
@app.route('/')
def index():
    print('Server request for home page...')
    return (
        f'Available routes:<br/>'
        f'<ol>'
        f'<li><a href="/api/test1">/api/test1</a> - Test 1</li>'
        f'<li><a href="/api/test2">/api/test2</a> - Test 2</li>'
        f'</ol>'
    )

@app.route('/api/test1')
def test1():

    return 'Test 1'

@app.route('/api/test2')
def test2():

    return 'Test 2'