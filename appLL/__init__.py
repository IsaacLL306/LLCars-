from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)



dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir  # Dirección de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)

from appLL import routes, models