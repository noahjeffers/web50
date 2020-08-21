from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max,Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import locale
from django import forms
from django.contrib.auth.decorators import login_required
import datetime

from .models import User, Listing, Comments, Bids, Category

class CreateForm(forms.Form):
    title = forms.CharField(label = "Title")
    description = forms.CharField(widget=forms.Textarea(attrs={'cols': 20, 'rows': 5}))
    imageLink = forms.CharField(label = "Link to image", required = False)
    openingBid = forms.CharField(label="Opening Bid")

    



def index(request):

    active_listings = Listing.objects.filter(active=True)

    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "bids": Bids.objects.all()
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def item(request, item_id):
    item = Listing.objects.get(pk=item_id)
    comment = Comments.objects.filter(listingID=item)
    return render(request, "auctions/item.html",{
        "item": item,
        "watching": item.watched.all(),
        "comments": comment
    })

@login_required
def watchlist(request):
    userid = request.user
    user = User.objects.get(pk=userid.id)
    return render(request,"auctions/watchlist.html",{
        "watchlist": user.watching.all()
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def category(request,category_id):
    category = Category.objects.get(pk=category_id)
    active_listings = Listing.objects.filter(active=True)
    return render(request, "auctions/category.html", {
        "listings": active_listings.filter(category=int(category_id)),
        "category": category
    })

@login_required
def watch(request,item_id):
    user = request.user
    item = Listing.objects.get(pk=item_id)

    item.watched.add(user)
    return redirect('/'+str(item_id))


def remove(request,item_id):
    user = request.user
    item = Listing.objects.get(pk=item_id)
    item.watched.remove(user)
    return redirect('/'+str(item_id))

def close(request,item_id):
    item = Listing.objects.get(pk=item_id)
    item.active = False
    item.save()
    return render(request, "auctions/error.html",{
        "error":item.active
    })
    return redirect('/'+str(item_id))

def error(request):
    pass

@login_required
def create(request):
    if request.method == "POST":
        user = request.user
        category = Category.objects.get(pk=request.POST["category"])
        newListing = Listing(title=request.POST["title"], description=request.POST['description'],
            imageLink=request.POST["imageLink"],uploadDate=datetime.datetime.now(),listedBy=request.user  ,category= category)     
        newListing.save()
        newBid =Bids(listingID=newListing,userID=user,amount=request.POST['openingBid'])
        newBid.save()
        newListing.currentbid=newBid
        newListing.save()

        return redirect('/'+str(newListing.id))
    return render(request, "auctions/create.html",{
        "categories": Category.objects.all(),
        "createForm":CreateForm()
    })

@login_required
def bid(request,item_id):
    user = request.user
    item = Listing.objects.get(pk=item_id)
    pendingBid = int(request.POST["amount"])
    if pendingBid > item.currentbid.amount:
        newBid =Bids(listingID=item,userID=user,amount=pendingBid)
        newBid.save()
        item.currentbid=newBid
        item.save()
        return redirect('/'+str(item.id))
    else:
        return render(request, "auctions/error.html",{
            "error": "Your bid must be larger than the current bid"
        })

def closed(request):
    inactive_listings = Listing.objects.filter(active=False)

    return render(request, "auctions/index.html", {
        "listings": inactive_listings,
        "bids": Bids.objects.all()
    })

@login_required
def comment(request, item_id):
    user = request.user
    item = Listing.objects.get(pk=item_id)
    newComment = Comments(listingID=item,content=request.POST['content'], userID=user)
    newComment.save()
    return redirect('/'+str(item.id))
