from typing import List, Dict
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User
from .forms import ArticleForm, SignupForm
from django.utils.html import strip_tags, strip_spaces_between_tags
from django.contrib.auth import authenticate as django_authenticate, login as django_login, logout as django_logout
from django.utils.http import urlencode
from django.urls import reverse


def index(request):
    return render(request, 'tehreer/index.html')

def auth(request):
    auth_messages: List[str] = request.session.pop("auth_messages", [])
    focus_signup: bool = request.session.pop("focus_signup", "false").lower()
    signup_form_data: Dict[str, str] = request.session.pop("signup_form_data", {})
    print(signup_form_data, "eee")

    return render(request, 'tehreer/auth.html', {
        "auth_messages": auth_messages,
        "focus_signup": True if focus_signup == 'true' else False,
        "signup_form": SignupForm(signup_form_data)
    })


def signup(request):
    signup_form = SignupForm(request.POST)
    print(signup_form.is_valid())

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
    # TODO
    pass


def signout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse("tehreer:index"))


















    # email: str = request.POST.get("email")
    # first_name: str  = request.POST.get("first_name")
    # last_name: str = request.POST.get("last_name")
    # password = request.POST.get("password")
    # password2 = request.POST.get("password2")

    # if password != password2:
    #     return HttpResponseRedirect(reverse("tehreer:auth") + "?" + urlencode({
    #         "auth_message": "Passwords don't match.",
    #         "focus_signup": True
    #     }))
    
    # if len(password) < 4:
    #     return HttpResponseRedirect(reverse("tehreer:auth") + "?" + urlencode({
    #         "auth_message": "Password must be atleast 4 characters long.",
    #         "focus_signup": True
    #     }))


def signin(request):
    pass
