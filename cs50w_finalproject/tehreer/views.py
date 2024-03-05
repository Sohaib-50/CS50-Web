from typing import Dict, List

from django.contrib import messages
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ArticleForm, SigninForm, SignupForm
from .models import User, Article


def index(request):
    return render(request, 'tehreer/index.html', {
        "articles": Article.objects.all()
    })

def auth(request):
    auth_messages: List[str] = request.session.pop("auth_messages", [])
    focus_signup: bool = request.session.pop("focus_signup", "false").lower()
    signup_form_data: Dict[str, str] = request.session.pop("signup_form_data", {})
    signin_form_data: Dict[str, str] = request.session.pop("signin_form_data", {})

    return render(request, 'tehreer/auth.html', {
        "auth_messages": auth_messages,
        "focus_signup": True if focus_signup == 'true' else False,
        "signup_form": SignupForm(signup_form_data)
    })


def signup(request):
    signup_form = SignupForm(request.POST)

    # invalid input(s)
    if not signup_form.is_valid():

        for field, field_errors in signup_form.errors.items():
            for error in field_errors:
                request.session.setdefault("auth_messages", []).append(error)

        request.session["focus_signup"] = "true"

        signup_form_data: Dict[str, str] = signup_form.data.dict()
        signup_form_data.pop("password")
        signup_form_data.pop("password2")
        request.session["signup_form_data"] = signup_form_data

        return HttpResponseRedirect(reverse("tehreer:auth"))
    
    # Attempt to create new user
    try:
        user = User.objects.create_user(
            email=signup_form.cleaned_data['email'],
            username=signup_form.cleaned_data['email'],
            password=signup_form.cleaned_data['password'],
            first_name=signup_form.cleaned_data['first_name'],
            last_name=signup_form.cleaned_data['last_name'],
            bio=signup_form.cleaned_data.get('bio'),
            profile_picture=signup_form.cleaned_data.get('profile_picture')
        )
        user.save()
    except IntegrityError as e:
        print(e)

        request.session.setdefault("auth_messages", []).append("An account with this email already exists.")

        request.session["focus_signup"] = "true"

        signup_form_data: Dict[str, str] = signup_form.data.dict()
        signup_form_data.pop("password")
        signup_form_data.pop("password2")
        request.session["signup_form_data"] = signup_form_data

        return HttpResponseRedirect(reverse("tehreer:auth"))
    
    django_login(request, user)
    return HttpResponseRedirect(reverse("tehreer:index"))


def signin(request):

    # try to sign in
    email = request.POST.get("email", "").lower()
    password = request.POST.get("password")
    user: User | None = django_authenticate(request, username=email, password=password)
    print(email, password, user)

    # check sign in successful
    if user is not None:
        django_login(request, user)
        return HttpResponseRedirect(reverse("tehreer:index"))
    
    else:
        request.session.setdefault("auth_messages", []).append("Invalid email and/or password.")
        request.session["focus_signup"] = "false"
        request.session["signin_form_data"] = {"email": email}
        return HttpResponseRedirect(reverse("tehreer:auth"))


def signout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse("tehreer:index"))
    

@login_required
def write(request):

    if request.method == "GET":
        return render(request, 'tehreer/write.html', {
            "article_form": ArticleForm()
        })
    
    # POST request
    article_form = ArticleForm(request.POST)

    if article_form.is_valid():
        article = article_form.save(commit=False)
        article.author = request.user
        article.save()
        messages.info(request, 'Article published', extra_tags='toast')
        return redirect("tehreer:index")
    
    else:
        print("Invalid form")
        messages.info(request, 'Error: unable to publish, please check your content and try again', extra_tags='toast')
        return render(request, 'tehreer/write.html', {
            "article_form": article_form
        })




