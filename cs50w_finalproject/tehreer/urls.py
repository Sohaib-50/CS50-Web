from django.urls import path
from . import views

app_name = "tehreer"
urlpatterns = [
    path("", views.index, name="index")
]