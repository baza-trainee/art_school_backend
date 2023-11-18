from sqladmin import ModelView

from src.news.models import News


class NewsView(ModelView, model=News):
    column_list = [News.id, News.title, News.text, News.photo]
