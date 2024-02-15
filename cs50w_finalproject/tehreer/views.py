from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Article
from .forms import ArticleForm
from django.utils.html import strip_tags, strip_spaces_between_tags
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlencode
from django.urls import reverse


def index(request):
    return render(request, 'tehreer/index.html')

def auth(request):
    auth_message = request.GET.get("auth_message")
    focus_signup = request.GET.get("focus_signup", "false").lower()

    return render(request, 'tehreer/auth.html', {
        "auth_message": auth_message,
        "focus_signup": True if focus_signup == 'true' else False,
    })


def signup(request):
    email: str = request.POST.get("email")
    first_name: str  = request.POST.get("first_name")
    last_name: str = request.POST.get("last_name")
    password = request.POST.get("password")
    password2 = request.POST.get("password2")

    if password != password2:
        return HttpResponseRedirect(reverse("tehreer:auth") + "?" + urlencode({
            "auth_message": "Passwords don't match.",
            "focus_signup": True
        }))
    
    if len(password) < 4:
        return HttpResponseRedirect(reverse("tehreer:auth") + "?" + urlencode({
            "auth_message": "Password must be atleast 4 characters long.",
            "focus_signup": True
        }))



# def signout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("index"))