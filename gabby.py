
from flask import render_template, flash
import datetime
from random import randint

from flask_wtf import form

from app.email import send_email, send_redeem_email
from app.forms import LoginForm, RedeemForm
from app import app

from datetime import datetime as dt


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

    target_date = dt(2004, 4, 7)
    days_since = (dt.now() - target_date).days
    age = (days_since//365)-1

    if today.day == 15 and today.month == 4:
        return render_template('birthday.html', firstday=delta.days, dateday=delta2.days, months1=months1, months2=months2
                               , daysmonths1=daysmonths1, daysmonths2=daysmonths2, days_since=days_since, age=age)

    else:
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

@app.route('/coupons', methods=['GET', 'POST'])
def coupons():
    coupons = [
        {"title": "Breakfast in Bed", "code": "LOVE123", "valid": True},
        {"title": "5 Minute Makeout", "code": "KIS456", "valid": True},
        {"title": "1 Free Raspberry", "code": "RAS343", "valid": True},
        {"title": "Full Expense Panera Trip", "code": "PAN346", "valid": True},
        {"title": "Back Massage", "code": "BAK983", "valid": True},
        {"title": "10 No Resistance Ass Slaps", "code": "ASS069", "valid": True},
        {"title": "Piggy Back Ride to any Valid Location", "code": "PIG287", "valid": True}
    ]
    form = RedeemForm()
    if form.validate_on_submit():
        send_redeem_email(form)
        flash('Redeemed ' + form.name.raw_data[1] + ' Coupon!')
        return render_template('coupons.html', title="Coupons",coupons=coupons, form=form)
    return render_template('coupons.html', title="Coupons",coupons=coupons,form=form)

@app.route('/reasons')
def reasons():
    return render_template('love_reasons.html', title="LoveReasons")


if __name__ == "__main__":
    app.run()
