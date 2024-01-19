import json

import requests
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Post, User


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
    content = data.get("content", "").strip()
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
    
    post = post.serialize()
    post.update({
        "current_user_likes": False,
        "current_user_owns": True,
    })
    return JsonResponse({"message": "Post created successfully.", "post": post}, status=201)


def posts(request, page_number=1):
    '''
    API route to get all posts, posts of a certain user, or posts of followed people of currently logged in user.
    '''

    if request.method != "GET":
        return JsonResponse({"error": "Only GET request allowed."}, status=400)
    
    # get posts of followed people, a certain user only, or all people depending on request
    if str(request.GET.get("following")).strip().lower() == "true":
        posts = Post.objects.filter(user__in=request.user.following.all())
    elif (username := request.GET.get("username")) is not None:
        try:
            user = User.objects.get(username__iexact=username.lower())  # case insensitive search
        except User.DoesNotExist:
            return JsonResponse({"error": "User with requested username not found"}, status=404)
        posts = Post.objects.filter(user=user)
    else:
        posts = Post.objects.all()
    posts = posts.order_by("-created")  # sort with most recent post first

    # paginate
    paginated_posts = Paginator(posts, per_page=10)
    try:
        page = paginated_posts.page(page_number)
    except:
        return JsonResponse({"error": f"Page {page_number} does not exist."}, status=404)
    posts = list(page.object_list)

    print(f"request.user inside posts view: {request.user}")
    for i, post in enumerate(posts):
        current_user_likes = None
        current_user_owns = None
        
        if request.user.is_authenticated:
            current_user_likes = request.user in post.likers.all()
            current_user_owns = request.user == post.user
            
        post = post.serialize()
        post.update({
            "current_user_likes": current_user_likes,
            "current_user_owns": current_user_owns,
        })
        posts[i] = post
    
    print(posts[0].keys())
    return JsonResponse({
        "posts": posts,
        "page_number": page_number,
        "total_pages": paginated_posts.num_pages,
    }, status=200)


def post(request, post_id):
    '''
    API route to update a post (like/unlike or edit).
    '''

    if request.method != "PATCH":
        return JsonResponse({"error": "Only PATCH request allowed."}, status=400)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post with requested ID not found"}, status=404)
    
    if not request.user.is_authenticated:
        return JsonResponse({"error": "A user must be signed in to use this route."}, status=403)
    
    data = json.loads(request.body)
    like = data.get("like")
    content = data.get("content")
    if (like is None and content is None) or (like is not None and content is not None):
        return JsonResponse({"error": "Must provide either like or content key but not both."}, status=400)
    
    if like is not None:
        if like == True:
            post.likers.add(request.user)
        else:
            post.likers.remove(request.user)
        return JsonResponse({"message": f"Successfully {'liked' if like else 'unliked'} post", "liked": like}, status=200)
    else:  # content is not None
        if request.user != post.user:
            return JsonResponse({"error": "Not owner, not allowed to edit."}, status=403)
        post.content = content
        post.save()
        return JsonResponse({"message": "Post content successfully edited."}, status=200)
    

def profile(request, username):
    '''
    API route to get information about a user.
    '''

    try:
        requested_user = User.objects.get(username__iexact=username.lower())  # case insensitive search
    except User.DoesNotExist:
        return JsonResponse({"error": "User with requested username not found"}, status=404)
    
    if request.method == "PUT":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "A user must be signed in to follow/unfollow."}, status=403)  # 403 means forbidden
        if request.user == requested_user:
            return JsonResponse({"error": "A user cannot follow/unfollow themselves."}, status=400)  # bad request
        
        data = json.loads(request.body)
        if (follow := data.get("follow")) is None:
            return JsonResponse({"error": "PUT request must contain 'follow' key."}, status=400)
        
        if follow == True:
            request.user.following.add(requested_user)
        else:
            request.user.following.remove(requested_user)
        return JsonResponse({"message": f"Successfully {'followed' if follow else 'unfollowed'}"}, status=200)

    else:  # request.method == "GET"
        requested_user_details = requested_user.serialize()

        # if any other user is signed in, find if they follow requested user or not
        if request.user.is_authenticated and (logged_in_user := request.user) != requested_user:
            requested_user_details.update(
                {"current_user_follows": requested_user.followers.filter(username=logged_in_user.username).exists()}
            )

        # add user's posts (using our posts API)
        print(f"request.user inside profile view: {request.user}")
        try:
            uri = request.build_absolute_uri(reverse("network:posts") + f"?username={requested_user.username}")
            headers = {k: v for k, v in request.headers.items()}  # copy headers from original request
            response = requests.get(uri, headers=headers)
            response.raise_for_status()
        except requests.RequestException:
            return JsonResponse({"error": "Error fetching posts."}, status=500)
        

        requested_user_details.update({"posts_page": response.json()})
            

        return JsonResponse(requested_user_details, status=200)
    