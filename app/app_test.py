# 1. Import Flask
from flask import Flask


# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def index():
    return "app\app_test"