from django.urls import path
from . import views

app_name = "tehreer"
urlpatterns = [
    path("", views.index, name="index"),
    path("auth/", views.auth, name="auth"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("write/", views.write, name="write"),
    # path("article/<int:article")


    # # Auth APIs
    # path("api/auth/signup", views.register, name="signup"),
    # path("api/auth/signin", views.register, name="signin"),
    # path("api/auth/signout", views.signout, name="signout"),
    
    # # Articles related APIs
    path("api/articles", views.articles_api, name="articles_api"),  # get all articles, or filtered by topic, a user, or all following users
    # path("api/search", views.articles, name="articles"),
    path("api/article/<int:article_id>", views.article_api, name="article_api"),
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