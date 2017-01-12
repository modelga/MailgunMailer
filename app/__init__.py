# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.debug = True
bcrypt = Bcrypt(app)

from app.controllers import *
