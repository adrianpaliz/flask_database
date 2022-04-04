from balance import app
from flask import jsonify
import sqlite3

from balance.models import ProcessData

instantiated_database_path = app.config["DATABASE_PATH"]
data_manager = ProcessData(instantiated_database_path)


@app.route("/api/v01/all")
def all():
    data = data_manager.recover_data()
    return jsonify(data)