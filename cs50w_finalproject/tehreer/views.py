from django.shortcuts import render
from .models import Article
from .forms import ArticleForm
from django.utils.html import strip_tags, strip_spaces_between_tags

def index(request):
    articles = Article.objects.all().order_by("-created_at")
    for article in articles:
        display_body = strip_spaces_between_tags((article.body.html))[:100] + "..."
        article.display_body = display_body
        print(article.display_body)

    return render(request, "tehreer/index.html", {
        "articles": articles
    })

def new(request):

    if request.method == "GET":
        return render(request, "tehreer/new.html", {
            "form": ArticleForm()
        })
    
    else:  # POST request
        form = ArticleForm(request.POST)
        article = form.save()
        return render(request, "tehreer/article.html", {
            "article": article
        })
        


def article(request, article_id):
    return render(request, "tehreer/article.html", {
        "article": Article.objects.get(id=article_id)
    })
