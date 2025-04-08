from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import RadioField
from wtforms.validators import Email


class LoginForm(FlaskForm):
    choice = RadioField('Restaurant', choices=[('Moosewood', 'Moosewood'), ('MIX', 'MIX'), ('Monks', 'Monks')])
    otherrestaurant = StringField('Other Choice')
    submit = SubmitField('Submit')

class RedeemForm(FlaskForm):
    email = StringField('Email')
    name = ""
    code = ""
    submit = SubmitField('Redeem')