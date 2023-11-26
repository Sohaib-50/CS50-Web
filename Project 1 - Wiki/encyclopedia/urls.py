from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("random_page", views.random_page, name="random_page"),
    path("edit/<str:title>", views.edit, name="edit")
]
