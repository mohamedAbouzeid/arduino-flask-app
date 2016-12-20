import json
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask import Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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
    article = Article('google.com', 'This is a Dummy Title', 'http://www.presseportal.de/images/tt-de/3733-oeffentlichkeitsfahndungen.jpg')
    db.session.add(article)
    db.session.commit()
    return 'added'

@app.route('/api/article/list')
def get_data():
    all_articles = Article.query.all()
    articles = []
    for article in all_articles:
        articles.append({'url': article.url, 'title': article.title, 'picture_url': article.picture_url})
    return Response(json.dumps(articles), content_type='application/json')




if __name__ == '__main__':
    app.run()