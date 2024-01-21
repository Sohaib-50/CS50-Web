from django.urls import path
from . import views

app_name = "tehreer"
urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("article/<int:article_id>", views.article, name="article")
]