import requests
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from bs4 import BeautifulSoup
from app import Article
from sqlalchemy import desc
import os
import bmemcached

cache = bmemcached.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','), os.environ.get('MEMCACHEDCLOUD_USERNAME'), os.environ.get('MEMCACHEDCLOUD_PASSWORD'))

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


def get_raw_site(url, **kwargs):
    headers = kwargs.get('headers', {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1)'
                                                   ' Gecko/20100101 Firefox/10.0.1', 'charset': 'utf-8'})
    query_params = kwargs.get('data', None)
    timeout = kwargs.get('timeout', 10)

    html = requests.get(url, headers=headers, data=query_params, timeout=timeout)
    html.encoding = 'utf=8'
    return BeautifulSoup(html.text, 'lxml')

def delete_all_and_leave_latest_100():
    articles_to_be_deleted = Article.query.order_by(desc(Article.id)).offset(100).all()
    for article in articles_to_be_deleted:
        db.session.delete(article)
    db.session.commit()

def add_latest_12_to_cache():
    all_articles = Article.query.order_by(desc(Article.id)).limit(12).all()
    cache.set('latest_12_items', all_articles, timeout=5 * 60)
    all_articles = cache.get('latest_12_items')
    print(all_articles)


def parse():
    detail_site_data = get_raw_site('http://businessinsider.de/?IR=C')
    if not detail_site_data:
        return
    delete_all_and_leave_latest_100()
    text_warpper = detail_site_data.body.find('div', class_='river')
    if text_warpper:
        articles = text_warpper.find_all('div')
        for article in articles:
            if article.find('div', class_='span6 first'):
                continue
            if not article.find('h2'):
                continue
            title = article.find('h2').getText()
            url = article.find('h2').find('a').get('href')
            picture_url = article.find('img').get('src')

            article = Article(url, title, picture_url)
            test_article = Article.query.filter(Article.title == title).all()
            if len(test_article) >= 1:
                continue
            db.session.add(article)
            db.session.commit()
    add_latest_12_to_cache()

parse()
