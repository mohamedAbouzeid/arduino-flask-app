import requests
import os
import json
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    title = db.Column(db.String(100))
    picture_url = db.Column(db.String(200))

    def __init__(self, url, title, picture_url):
        self.url = url
        self.title = title
        self.picture_url = picture_url

    # def __repr__(self):
    #     return '<Title %r>' % self.title

@app.route('/')
def add_data():
    article = Article('google.com', 'hamada', 'google-image.com')
    db.session.add(article)
    db.session.commit()
    return 'added'

@app.route('/api/article/list')
def get_data():
    all_articles = Article.query.all()
    articles = []
    for article in all_articles:
        articles.append({'url': article.url, 'title': article.title, 'picture_url': article.picture_url})
    return json.dumps(articles)



if __name__ == '__main__':
    app.run()