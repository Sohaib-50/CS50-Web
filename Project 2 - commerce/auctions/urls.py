from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("toggle_watching", views.toggle_watching, name="toggle_watching"),
    path("bid", views.bid, name="bid"),
    path("close_listing", views.close_listing, name="close_listing"),
]
