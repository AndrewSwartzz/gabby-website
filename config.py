import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "GabbyCat"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587  # For TLS
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'andrew.swartz.cs205@gmail.com'  # Your Gmail address
    MAIL_PASSWORD = 'iaqb jhoy chvi nbqo'  # NOT your regular password (see below)
    MAIL_DEFAULT_SENDER = 'andrew.swartz.cs205@gmail.com'
    ADMINS = ["andrew.swartz.cs205@gmail.com"]