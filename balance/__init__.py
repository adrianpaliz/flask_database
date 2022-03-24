from flask import Flask

app = Flask(__name__)
app.config['DATABASE_PATH'] = "database path"
app.config['SECRET_KEY'] = 'here your key'

from balance import routes
from balance import api_routes