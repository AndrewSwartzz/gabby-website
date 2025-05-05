import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
import flask_mail
from flask_mail import Mail
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)



