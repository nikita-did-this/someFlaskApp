from bs4 import BeautifulSoup
from datetime import datetime
import locale
import platform
from webapp.db import db
from webapp.news.models import News

from webapp.news.parsers.utils import get_html, save_news

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')

def get_news_content():
        news_without_text = News.query.filter(News.text.is_(None)).all()
        for news in news_without_text:
            html = get_html(news.url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                try:
                    article = soup.find('div', class_='tm-article-body').decode_contents()
                except AttributeError:
                    continue
                if article:
                    news.text = article
                    db.session.add(news)
                    db.session.commit()

def get_news_snippets():
    html_link = get_html("https://habr.com/ru/search/?target_type=posts&q=python&order_by=date")
    if html_link:
        soup = BeautifulSoup(html_link, "html.parser")
        all_news = soup.find("div", class_='tm-articles-list').\
            findAll('article', class_='tm-articles-list__item')
        for news in all_news:
            title = news.find('a', class_='tm-article-snippet__title-link').find('span').text
            url = "https://habr.com" + \
                  news.find('a', class_="tm-article-snippet__title-link")['href']
            published = news.find('span', class_='tm-article-snippet__datetime-published')\
                .find('time')['title']
            published = parse_habr_date(published)
            save_news(title, url, published)

def parse_habr_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d, %H:%M')
    except ValueError:
        return datetime.now()
