import requests
from webapp.db import db
from webapp.news.models import News


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64;rv: 106.0) Gecko / 20100101Firefox / 106.0'}
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False


def save_news(news_title, news_url, published_datetime):
    news_exists = News.query.filter(News.url == news_url).count()
    if not news_exists:
        news_obj = News(title=news_title, url=news_url, published=published_datetime)
        db.session.add(news_obj)
        db.session.commit()
