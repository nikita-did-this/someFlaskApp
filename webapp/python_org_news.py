from bs4 import BeautifulSoup
from datetime import datetime
import requests
from webapp.model import db, News


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        return False


def get_python_news():
    html_link = get_html("https://www.python.org/blogs/")
    if html_link:
        soup = BeautifulSoup(html_link, "html.parser")
        all_news = soup.find("ul", class_='list-recent-posts').findAll('li')
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time')['datetime']
            try:
                published = datetime.strptime(published, "%Y-%m-%d")
            except ValueError:
                published = datetime.now()
            save_news(title, url, published)


def save_news(news_title, news_url, published_datetime):
    news_exists = News.query.filter(News.url == news_url).count()
    if not news_exists:
        news_obj = News(title=news_title, url=news_url, published=published_datetime)
        db.session.add(news_obj)
        db.session.commit()
