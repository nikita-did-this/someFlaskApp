from flask import Blueprint, current_app, render_template

from webapp.news.models import News
from webapp.weather import weather_by_city

blueprint=Blueprint('news', __name__)

@blueprint.route("/")
def index():
    page_title = "Новости Python"
    weather_data = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    news_list = News.query.order_by(News.published.desc()).all()
    return render_template('news/index.html', title=page_title, weather=weather_data, news=news_list)
