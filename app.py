# 1. Import Flask
from flask import Flask

# 2. Create an app
app = Flask(__name__)

# 3. Define static routes
@app.route('/')
def index():
    return 'Default Page for App'

@app.route('/API/test')
def test():
    return 'This is a test API'