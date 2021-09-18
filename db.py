from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

# Replace hack done for Heroku due to a change in the sqlalchemy library
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql:///", 1)
db = SQLAlchemy(app)
