from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import ListingForm
from .helpers import annotate_current_price
from .models import Bids, Comments, Listing, User


def index(request):
    listings = annotate_current_price(Listing.objects.filter(active=True))

    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": "Active Listings"
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    listing_details = Listing.objects.get(pk=listing_id)
    bids = Bids.objects.filter(listing=listing_details).order_by('-amount')
    comments = Comments.objects.filter(listing=listing_details).order_by('-timestamp')
    listing_details.current_price = bids[0].amount if bids else listing_details.starting_bid
    
    if not listing_details.active:
        winner = bids[0].bidder
        request.user.is_winner = True if request.user == winner else False

    # find watchlist status if there's someone signed in
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        if listing_details in user.watchlist.all():
            request.user.is_watching = True
        else:
            request.user.is_watching = False

    return render(request, "auctions/listing.html", {
        "listing_details": listing_details,
        "bids": bids,
        "comments": comments
    })


@login_required
def add_comment(request):
    content = request.POST['content']
    listing_id = request.POST['listing_id']
    current_listing = Listing.objects.get(pk=listing_id)
    commenter = User.objects.get(pk=request.user.id)

    # try to add comment
    try:
        comment = Comments(content=content, listing=current_listing, commenter=commenter)
        comment.save()
        messages.info(request, 'Comment added successfully')
    except IntegrityError:
        messages.info(request, 'Error adding comment')

    return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))
    
@login_required
def toggle_watching(request):
    listing_id = request.POST['listing_id']
    current_listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(pk=request.user.id)

    # toggle watching status
    try:
        if current_listing in user.watchlist.all():
            user.watchlist.remove(current_listing)
            # messages.info(request, 'Removed from watchlist')
        else:
            user.watchlist.add(current_listing)
            # messages.info(request, 'Added to watchlist')
    except IntegrityError:
        messages.info(request, 'Error adding comment')

    return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))


@login_required
def bid(request):
    amount = float(request.POST["amount"])
    selected_listing = Listing.objects.get(pk=request.POST['listing_id'])

    try:
        # if amount is less than current price, don't add bid
        current_price = selected_listing.bids.aggregate(Max('amount'))['amount__max']
        if current_price is None:
            current_price = selected_listing.starting_bid
        if amount <= current_price:
            messages.info(request, "Your bid must be greater than current price")
            return
        else:
            bid = Bids(bidder=request.user, listing=selected_listing, amount=amount)
            bid.save()
            messages.info(request, 'Bid added successfully')
    except IntegrityError:
        messages.info(request, 'Error adding bid')

    return HttpResponseRedirect(reverse("auctions:listing", args=(selected_listing.id,)))

@login_required
def close_listing(request):
    selected_listing = Listing.objects.get(pk=request.POST['listing_id'])
    selected_listing.active = False
    selected_listing.save()
    messages.info(request, 'Listing Closed Successfully')
    return HttpResponseRedirect(reverse("auctions:listing", args=(selected_listing.id,)))


@login_required
def watchlist(request):
    user = request.user
    watchlist = annotate_current_price(user.watchlist.all())

    return render(request, "auctions/index.html", {
        "listings": watchlist,
        "title": "Watchlist"
    })


def categories(request):
    categories = Listing.objects.values('category').distinct().exclude(category='')
    categories = [category['category'] for category in categories]
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


def category(request, category):
    category_listings = annotate_current_price(Listing.objects.filter(category=category, active=True))
    return render(request, "auctions/index.html", {
        "listings": category_listings,
        "title": f"Listings - Category: {category}"
    })

@login_required
def create_listing(requst):
    if requst.method == "GET":
        return render(requst, "auctions/create_listing.html", {
            "form": ListingForm()
        }
    )
    
    # if method POST
    form = ListingForm(requst.POST)
    if form.is_valid():
        listing = form.save(commit=False)
        listing.lister = requst.user
        listing.save()
        messages.info(requst, 'Listing created successfully')
        listing_id = listing.id
        return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))
    else:
        messages.info(requst, 'Error creating listing')
        return render(requst, "auctions/create_listing.html", {
            "form": form
        }
    )