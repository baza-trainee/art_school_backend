from sqladmin import ModelView

from src.posters.models import Poster


class PosterView(ModelView, model=Poster):
    column_list = [Poster.id, Poster.title, Poster.text, Poster.photo]
