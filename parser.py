import requests
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)



def get_raw_site(url, **kwargs):
    headers = kwargs.get('headers', {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1)'
                                                   ' Gecko/20100101 Firefox/10.0.1'})
    query_params = kwargs.get('data', None)
    timeout = kwargs.get('timeout', 10)

    html = requests.get(url, headers=headers, data=query_params, timeout=timeout)
    return BeautifulSoup(html.text, 'lxml')

def parse():
    detail_site_data = get_raw_site('http://www.businessinsider.de/')
    if not detail_site_data:
        return
    text_warpper = detail_site_data.body.find('div', class_='river')
    if text_warpper:

        # image_urls = [text_warpper.find('img')]
        # paragraphs = text_warpper.find_all('p')
        # text = ''
        # for paragraph in paragraphs:
        #     text += paragraph.getText()
        # if image_urls:
        #     return {'text': text, 'image_urls': image_urls}
        # else:
        #     return {'text': text, 'image_urls': []}

