from flask import Flask, render_template

from webapp.model import db, News
from webapp.python_org_news import get_python_news
from webapp.weather import weather_by_city


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        page_title = "Новости Python"
        weather_data = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', title=page_title, weather=weather_data, news=news_list)

    return app
