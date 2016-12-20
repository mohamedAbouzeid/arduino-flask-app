import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
print(os.environ['DATABASE_URL'])
db = SQLAlchemy(app)