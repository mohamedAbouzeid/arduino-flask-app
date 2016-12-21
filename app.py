import json
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask import Response
from flask_cors import CORS
from werkzeug.contrib.cache import MemcachedCache
from config import MEMCACHEDCLOUD_SERVER, MEMCACHEDCLOUD_USERNAME, MEMCACHEDCLOUD_PASSWORD

cache = MemcachedCache([MEMCACHEDCLOUD_SERVER, MEMCACHEDCLOUD_USERNAME, MEMCACHEDCLOUD_PASSWORD])

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
app.config['DEBUG'] = os.environ.get('DEBUG', False)

db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(300))
    title = db.Column(db.String(300))
    picture_url = db.Column(db.String(300))

    def __init__(self, url, title, picture_url):
        self.url = url
        self.title = title
        self.picture_url = picture_url

    # def __repr__(self):
    #     return '<Title %r>' % self.title


@app.route('/addDummy')
def add_data():
    article = Article('http://www.google.com', 'This is a Dummy Title', 'http://www.presseportal.de/images/tt-de/'
                                                                        '3733-oeffentlichkeitsfahndungen.jpg')
    db.session.add(article)
    db.session.commit()
    return 'added Dummy entry'


@app.route('/api/article/list')
def get_data():
    all_articles = cache.get('latest_12_items')
    if all_articles is not None:
        articles = []
        for article in all_articles:
            articles.append({'link': article.url, 'title': article.title, 'image': article.picture_url,
                             'id': article.id})
        return Response(json.dumps(articles), content_type='application/json')


if __name__ == '__main__':
    app.run()
