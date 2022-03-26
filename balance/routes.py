from balance import app
from flask import render_template, flash, request, redirect, url_for
from balance.models import ProcessData
import sqlite3
from balance.forms import MovementsForm
from datetime import date, time


instantiated_database_path = app.config["DATABASE_PATH"]
data_manager = ProcessData(instantiated_database_path)


@app.route("/")
def home():
    data = data_manager.recover_data()
    return render_template("movements.html", movements=data)


@app.route("/new", methods=["GET", "POST"])
def new():
    instantiated_form = MovementsForm()
    if request.method == "GET":
        return render_template("new.html", jinja_form=instantiated_form)
    else:
        if instantiated_form.validate():
            pass


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    pass
