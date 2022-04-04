from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, FloatField, SubmitField, TimeField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from datetime import date

def less_than_or_equal_to_today(jinja_form, field):
    today = date.today()
    if field.data > today:
        raise ValidationError("The date must not be later than today")

class MovementsForm(FlaskForm):
    day = DateField ("Date", validators=[DataRequired (message="Please insert a date"),less_than_or_equal_to_today])
    hour = TimeField ("Time", validators=[DataRequired()])
    concept = StringField ("Concept", validators=[DataRequired(), Length(min=5)])
    income = SelectField ("Type", validators=[DataRequired()], choices=[(0, "Expense"), (1, "Income")])
    amount = FloatField ("Amount", validators=[DataRequired(), NumberRange(message="Must be a positive", min=0.01)])
    submit = SubmitField ("Submit")