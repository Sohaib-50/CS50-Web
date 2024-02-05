from django.urls import path
from . import views

app_name = "tehreer"
urlpatterns = [
    path("", views.index, name="index"),
    path("article", views.article, name="article")

    # # Auth APIs
    # path("api/auth/signup", views.register, name="signup"),
    # path("api/auth/signin", views.register, name="signin"),
    # path("api/auth/signout", views.signout, name="signout"),
    
    # # Articles related APIs
    # path("api/articles", views.articles, name="articles"),  # get all articles, or filtered by topic, a user, or all following users
    # path("api/search", views.articles, name="articles"),
    # path("api/article/<int:article_id>", views.article, name="article"),
    # path("api/article/<int:article_id>/edit", views.edit_article, name="edit_article"),
    # path("api/post_article", views.post_article, name="post_article"),

    # # APIs for other activities
    # path("api/post_comment", views.post_comment, name="post_comment"),
    # path("api/edit_comment", views.post_comment, name="post_comment"),
    # path("api/like_post", views.like_post, name="like_post"),
    # path("api/follow_user", views.follow_user, name="follow_user"),

    # # User related APIs
    # path("api/user/<int:user_id>", views.user, name="user"),
    # path("api/activity_log", views.activity_log, name="activity_log")
]