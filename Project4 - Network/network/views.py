from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")


def new_post(request):

    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    data = json.loads(request.body)
    content = data.get("content", "")
    if not content:
        return JsonResponse({"error": "Content is required."}, status=400)  
    
    # Create post
    try:
        post = Post(
            user=request.user,
            content=content
        )
        post.save()
    except:
        return JsonResponse({"error": "Error creating post."}, status=500)  

    return JsonResponse({"message": "Post created successfully.", "post": post.serialize()}, status=201)


def posts(request):

    if request.method != "GET":
        return JsonResponse({"error": "Only GET request allowed."}, status=400)
    
    # get posts of followed people or all people depending on request
    if str(request.GET.get("following")).strip().lower() == "true":
        posts = Post.objects.filter(user__in=request.user.following.all())
    else:
        posts = Post.objects.all()
    posts = posts.order_by("-created")  # sort with most recent post first
    
    return JsonResponse([post.serialize() for post in posts], safe=False)



    
