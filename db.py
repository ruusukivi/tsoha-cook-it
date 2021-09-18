from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app

# Replace hack done for Heroku due to a change in the sqlalchemy library
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
