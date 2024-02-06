from django.http import HttpResponse
from django.shortcuts import render
from .models import Article
from .forms import ArticleForm, SignUpForm
from django.utils.html import strip_tags, strip_spaces_between_tags

def index(request):
    return render(request, 'tehreer/index.html')

def auth(request):
    return render(request, 'tehreer/auth.html', {
        'signupform': SignUpForm()
    })