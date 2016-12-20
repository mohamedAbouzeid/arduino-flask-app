import requests
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
print(os.environ['DATABASE_URL'])
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    title = db.Column(db.String(100))
    picture_url =  db.Column(db.String(200))

    def __init__(self, url, title, picture_url):
        self.url = url
        self.title = title
        self.picture_url = picture_url

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def get_data():
    article = Article('google.com', 'john.doe@example.com', 'google-image.com')
    db.session.add(article)
    db.session.commit()
    print(requests.get('https://randomuser.me/api/').content)
    return requests.get('https://randomuser.me/api/').content

@app.route('/app/list')
def get_data():
    all_users = Article.query.all()
    print(all_users)
    return all_users



if __name__ == '__main__':
    app.run()