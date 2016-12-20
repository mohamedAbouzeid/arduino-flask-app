import requests
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
print(os.environ['DATABASE_URL'])
db = SQLAlchemy(app)

@app.route('/')
def get_data():
    print(requests.get('https://randomuser.me/api/').content)
    return requests.get('https://randomuser.me/api/').content



if __name__ == '__main__':
    app.run()