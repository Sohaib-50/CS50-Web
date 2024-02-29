from typing import List, Dict
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import User
from .forms import ArticleForm, SignupForm, SigninForm
from django.utils import html
from django.contrib.auth import authenticate as django_authenticate, login as django_login, logout as django_logout
from django.utils.http import urlencode
from django.urls import reverse


def index(request):
    return render(request, 'tehreer/index.html')

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
    

def write(request):

    if request.method == "GET":
        return render(request, 'tehreer/write.html', {
            "article_form": ArticleForm()
        })
    
    
    # Else If POST request
    print("pst", request.POST)
    article_form = ArticleForm(request.POST)
    if article_form.is_valid():
        content_text = html.strip_tags(eval(article_form.cleaned_data['content'])['html'])
        print(f"Content: {content_text}", type(content_text))
    else:
        print("dirty")
    # print(article_form.is_valid())
    # print(article_form.data.get("content", None))
    return render(request, 'tehreer/write.html', {
            "article_form": article_form
        })




