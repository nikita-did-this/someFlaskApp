from bs4 import BeautifulSoup
from datetime import datetime
from webapp.news.parsers.utils import get_html, save_news


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

