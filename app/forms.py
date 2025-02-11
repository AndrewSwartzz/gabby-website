from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import RadioField


class LoginForm(FlaskForm):
    choice = RadioField('Restaurant', choices=[('Moosewood', 'Moosewood'), ('MIX', 'MIX'), ('Monks', 'Monks')])
    otherrestaurant = StringField('Other Choice')
    submit = SubmitField('Submit')