from flask import Flask, request, render_template
import datetime


app = Flask(__name__)


@app.route("/")

def home():

    date_str = '2024-05-06'
    date_format = "%Y-%m-%d"
    given_date = datetime.datetime.strptime(date_str, date_format).date()
    today = datetime.date.today()
    delta = today - given_date

    date_str = '2024-09-06'
    date_format = "%Y-%m-%d"
    given_date = datetime.datetime.strptime(date_str, date_format).date()
    today = datetime.date.today()
    delta2 = today - given_date

    return render_template('index.html', firstday=delta.days, dateday=delta2.days)

if __name__ == "__main__":
    app.run()
