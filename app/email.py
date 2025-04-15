from threading import Thread
from flask import render_template
from flask_mail import Message
from app import app, mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_redeem_email(form):
    send_email('Gabby Coupon Redemption Notice',
               sender=app.config['ADMINS'][0],
               recipients=[form.email.data],
               text_body=render_template('email/redeem.txt',
                                         code=form.code.raw_data[1], name=form.name.raw_data[1]),
               html_body=render_template('email/redeem.html',
                                         code=form.code.raw_data[1], name=form.name.raw_data[1]))