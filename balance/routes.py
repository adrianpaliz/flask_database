from balance import app
from flask import render_template, flash, request, redirect, url_for
from balance.models import ProcessData
import sqlite3
from balance.forms import MovementsForm
from datetime import date, time

database_path = app.config['DATABASE_PATH']
# instantiated_database_path
data_manager = ProcessData(database_path)

@app.route("/")
def home():
    
    try:
        data = data_manager.recover_data()
        return render_template("movements.html", movements=data)
    except sqlite3.Error as error:
        flash("Database error.")
        return render_template("movements.html", movements=[])

@app.route("/new", methods=["GET", "POST"])
def new():
    instantiated_form = MovementsForm()
    if request.method == "GET":
        return render_template("new.html", jinja_form=instantiated_form)
    else:
        if instantiated_form.validate():
            day = str(instantiated_form.day.data)
            hour = str(instantiated_form.hour.data)
            concept = instantiated_form.concept.data
            income = int(instantiated_form.income.data)
            amount = instantiated_form.amount.data

            try:
                data_manager.edit_data((day, hour, concept, income, amount))
                return redirect(url_for("home"))
            except sqlite3.Error as error:
                flash("Database error.")
                return render_template ("new.html", jinja_form = instantiated_form)
            
        else:
            return render_template ("new.html", jinja_form = instantiated_form)

@app.route("/edit/<int:variable_id>", methods=["GET", "POST"])
def edit(variable_id):
    if request.method == 'GET':       

        try:
            movements = data_manager.consult_id(variable_id)
            if len(movements) == 0:
                flash(f"There is not {variable_id} movement")
                return redirect(url_for("home"))

            movement = movements[0]
            movement['day'] = date.fromisoformat(movement['day'])
            movement['hour'] = time.fromisoformat(movement['hour'])
            instantiated_form = MovementsForm(data=movement)
            return render_template("edit.html", jinja_form = instantiated_form, jinja_id = variable_id)


            
        except sqlite3.Error as error:
            flash("Database error.")
            instantiated_form = MovementsForm()
            return render_template("edit.html", jinja_form = instantiated_form, jinja_id = variable_id)

    else:
        instantiated_form = MovementsForm()
        if instantiated_form.validate():
            
            params = (str(instantiated_form.day.data), str(instantiated_form.hour.data), instantiated_form.concept.data, instantiated_form.income.data, instantiated_form.amount.data, variable_id)
            
            try:
                data_manager.update_data(params)
                return redirect(url_for("home"))
            except sqlite3.Error as error:
                flash("Database error.")
                return render_template("edit.html", jinja_form = instantiated_form, jinja_id = variable_id)
        else:
            return render_template("edit.html", jinja_form = instantiated_form, jinja_id = variable_id)
