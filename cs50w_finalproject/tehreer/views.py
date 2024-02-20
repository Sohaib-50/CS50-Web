from typing import List
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User
from .forms import ArticleForm, SignupForm
from django.utils.html import strip_tags, strip_spaces_between_tags
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlencode
from django.urls import reverse


def index(request):
    return render(request, 'tehreer/index.html')

def auth(request):
    auth_messages: List[str] = request.session.pop("auth_messages", [])
    focus_signup: bool = request.session.pop("focus_signup", "false").lower()
    signup_form: SignupForm = request.session.pop("signup_form", SignupForm())

    # debugging
    focus_signup = 'true'
    # auth_messages = ["Poor email sick dubste Poor email", "sick dubstep","Poor email", "sick dubstep", "Poor email", "sick dubstep","Poor email", "sick dubstep","Poor email", "sick dubstep"]
    auth_messages = ["Enter a valid email address.", "Passwords do not match."]


    return render(request, 'tehreer/auth.html', {
        "auth_messages": auth_messages,
        "focus_signup": True if focus_signup == 'true' else False,
        "signup_form": signup_form
    })


def signup(request):
    signup_form = SignupForm(request.POST)
    print(signup_form.is_valid())

    if not signup_form.is_valid():

        # add error messages to auth_messages list in session for passing to auth view and displaying on frontend
        for field, field_errors in signup_form.errors.items():
            for error in field_errors:
                request.session.setdefault("auth_messages", []).append(error)
        request.session["focus_signup"] = "true"
        request.session["signup_form"] = signup_form
        return HttpResponseRedirect(reverse("tehreer:auth"))
    
    else:
        request.session.setdefault("auth_messages", []).append("Successfully signed up!")
        request.session["focus_signup"] = "true"
        return HttpResponseRedirect(reverse("tehreer:auth"))



















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

# def signout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse("index"))