from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask("shell_hacker_game")
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from shell_hacker_game import routes