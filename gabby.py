
from flask import render_template
import datetime
from random import randint
from app.forms import LoginForm
from app import app



@app.route("/")
@app.route('/home')

def home():

    date_str = '2024-05-06'
    date_format = "%Y-%m-%d"
    given_date = datetime.datetime.strptime(date_str, date_format).date()
    today = datetime.date.today()
    delta = today - given_date
    months1 = delta.days//30
    daysmonths1 = delta.days % 30

    date_str = '2024-09-06'
    date_format = "%Y-%m-%d"
    given_date = datetime.datetime.strptime(date_str, date_format).date()
    today = datetime.date.today()
    delta2 = today - given_date
    months2 = delta2.days//30
    daysmonths2 = delta2.days % 30

    return render_template('index.html', firstday=delta.days, dateday=delta2.days, months1=months1, months2=months2
                           ,daysmonths1=daysmonths1, daysmonths2=daysmonths2)

@app.route('/flirt')
def flirt():
    flirtlines = ['Girl are you my daily flintstones gummies, because i could eat you up every single day ahaha',
                  'Girl are you a subway employee, because id pay you 5 dollars to make me a foot long ahaha',
                  'Girl are you the dying dehydrated basil plant on my window sill, because all i wanna do is see you get wet']
    flirtline = flirtlines[randint(0,len(flirtlines)-1)]
    return render_template('pickupline.html', line=flirtline)


@app.route('/date', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        return render_template('success.html', choice=form.choice.data, other=form.otherrestaurant.data)
    return render_template('login.html', title = 'Sign In', form=form)


if __name__ == "__main__":
    app.run()
