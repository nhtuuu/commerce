from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User, Listing, Watchlist, Bid, Comment, Cat
import locale
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from decimal import Decimal
from .forms import CreateForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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

def create(request):
    form = CreateForm()
    return render(request, "auctions/create.html", {
        "form": form
    })

def listing(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return render(request, "auctions/index.html", {
                "listings": Listing.objects.all()
            })
                          

def listing_detail(request, listing_id):
    form = CommentForm()
    listing = Listing.objects.get(pk=listing_id)
    highest_bid = Bid.objects.filter(item=listing).aggregate(max_bid=Max("amount"), max_bidder=Max("bidder"))
    winner_id = highest_bid["max_bidder"]
    user_id = request.user.id
    legit_owner = request.user == listing.user
    if user_id is not None and winner_id is not None:
        winner = User.objects.get(id=winner_id)
        user = User.objects.get(id=user_id)
        is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
        return render(request, "auctions/detail.html", {
            "comments": Comment.objects.filter(item=listing),
            "all_bid": Bid.objects.filter(item=listing),
            "listing": listing,
            "is_watchlisted": is_watchlisted,
            "legit_owner": legit_owner,
            "winner": winner,
            "winner_id": winner_id,
            "form": form
        })
    elif user_id is not None and winner_id is None:
        user = User.objects.get(id=user_id)
        is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
        return render(request, "auctions/detail.html", {
            "comments": Comment.objects.filter(item=listing),
            "all_bid": Bid.objects.filter(item=listing),
            "listing": listing,
            "is_watchlisted": is_watchlisted,
            "legit_owner": legit_owner,
            "form": form
        })
    else:
        winner = User.objects.get(id=winner_id)
        return render(request, "auctions/detail.html", {
            "comments": Comment.objects.filter(item=listing),
            "all_bid": Bid.objects.filter(item=listing),
            "listing": listing,
            "form": form,
            "legit_owner": legit_owner,
            "winner": winner,
            "winner_id": winner_id
        })

def watchlist(request, user_username):
    user = get_object_or_404(User, username = user_username)
    watchlist = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def watchlist_add(request, listing_id):
    form = CommentForm()
    listing = Listing.objects.get(pk=listing_id)
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    legit_owner = request.user == listing.user
    highest_bid = Bid.objects.filter(item=listing).aggregate(max_bid=Max("amount"), max_bidder=Max("bidder"))
    winner_id = highest_bid["max_bidder"]
    watchlist_add = Watchlist(item=listing, user = user)
    watchlist_add.save()
    is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
    if user_id is not None and winner_id is not None:
        winner = User.objects.get(id=winner_id)
        return render(request, "auctions/detail.html", {
            "comments": Comment.objects.filter(item=listing),
            "all_bid": Bid.objects.filter(item=listing),
            "listing": listing,
            "is_watchlisted": is_watchlisted,
            "legit_owner": legit_owner,
            "winner": winner,
            "form": form
        })
    else:
        return render(request, "auctions/detail.html", {
            "comments": Comment.objects.filter(item=listing),
            "all_bid": Bid.objects.filter(item=listing),
            "listing": listing,
            "is_watchlisted": is_watchlisted,
            "legit_owner": legit_owner,
            "form": form
        })

def watchlist_remove(request, listing_id):
    form = CommentForm()
    user_id = request.user.id
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(id=user_id)
    legit_owner = request.user == listing.user
    highest_bid = Bid.objects.filter(item=listing).aggregate(max_bid=Max("amount"), max_bidder=Max("bidder"))
    winner_id = highest_bid["max_bidder"]
    watchlist_item = Watchlist.objects.filter(item=listing, user=user)
    watchlist_item.delete()
    is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
    if user_id is not None and winner_id is not None:
        winner = User.objects.get(id=winner_id)
        return render(request, "auctions/detail.html", {
            "comments": Comment.objects.filter(item=listing),
            "all_bid": Bid.objects.filter(item=listing),
            "listing": listing,
            "is_watchlisted": is_watchlisted,
            "legit_owner": legit_owner,
            "winner": winner,
            "form": form
        })
    else:
        return render(request, "auctions/detail.html", {
            "comments": Comment.objects.filter(item=listing),
            "all_bid": Bid.objects.filter(item=listing),
            "listing": listing,
            "is_watchlisted": is_watchlisted,
            "legit_owner": legit_owner,
            "form": form
        })

def bid(request, user_id, listing_id):
    form = CommentForm()
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(id=user_id)
    legit_owner = request.user == listing.user
    highest_bid = Bid.objects.filter(item=listing).aggregate(max_bid=Max("amount"), max_bidder=Max("bidder"))
    winner_id = highest_bid["max_bidder"]
    amount = request.POST.get("amount")
    highest_bid = Bid.objects.filter(item=listing).aggregate(Max("amount"))["amount__max"]
    if winner_id is not None:
        winner = User.objects.get(id=winner_id)
        if amount == "":
            is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
            return render(request, "auctions/detail.html", {
                "comments": Comment.objects.filter(item=listing),
                "all_bid": Bid.objects.filter(item=listing),
                "listing": listing,
                "is_watchlisted": is_watchlisted,
                "amount": amount,
                "legit_owner": legit_owner,
                "winner": winner,
                "form": form
            })
        else:
            if highest_bid is None and Decimal(amount) > listing.price:
                add_bid = Bid(item=listing, bidder=user, amount=amount)
                add_bid.save()
                is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
                return render(request, "auctions/detail.html", {
                    "comments": Comment.objects.filter(item=listing),
                    "all_bid": Bid.objects.filter(item=listing),
                    "listing": listing,
                    "is_watchlisted": is_watchlisted,
                    "legit_owner": legit_owner,
                    "winner": winner,
                    "form": form
                })
            elif highest_bid is None and Decimal(amount) < listing.price:
                lower_than_price = highest_bid is None and Decimal(amount) < listing.price
                is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
                return render(request, "auctions/detail.html", {
                    "comments": Comment.objects.filter(item=listing),
                    "all_bid": Bid.objects.filter(item=listing),
                    "listing": listing,
                    "is_watchlisted": is_watchlisted,
                    "lower_than_price": lower_than_price,
                    "legit_owner": legit_owner,
                    "winner": winner,
                    "form": form
                })
            elif highest_bid is not None and Decimal(amount) > highest_bid and Decimal(amount) > listing.price:
                add_bid = Bid(item=listing, bidder=user, amount=amount)
                add_bid.save()
                is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
                return render(request, "auctions/detail.html", {
                    "comments": Comment.objects.filter(item=listing),
                    "all_bid": Bid.objects.filter(item=listing),
                    "listing": listing,
                    "is_watchlisted": is_watchlisted,
                    "legit_owner": legit_owner,
                    "winner": winner,
                    "form": form
                })
            elif highest_bid is not None and Decimal(amount) < listing.price:
                lower_than_price = highest_bid is not None and Decimal(amount) < listing.price
                is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
                return render(request, "auctions/detail.html", {
                    "comments": Comment.objects.filter(item=listing),
                    "all_bid": Bid.objects.filter(item=listing),
                    "listing": listing,
                    "is_watchlisted": is_watchlisted,
                    "lower_than_price": lower_than_price,
                    "legit_owner": legit_owner,
                    "winner": winner,
                    "form": form
                })
            else:
                error = Decimal(amount) < highest_bid
                is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
                return render(request, "auctions/detail.html", {
                    "comments": Comment.objects.filter(item=listing),
                    "all_bid": Bid.objects.filter(item=listing),
                    "listing": listing,
                    "is_watchlisted": is_watchlisted,
                    "error": error,
                    "legit_owner": legit_owner,
                    "winner": winner,
                    "form": form
                })
    else:
        if amount == "":
            is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
            return render(request, "auctions/detail.html", {
                "comments": Comment.objects.filter(item=listing),
                "all_bid": Bid.objects.filter(item=listing),
                "listing": listing,
                "is_watchlisted": is_watchlisted,
                "amount": amount,
                "legit_owner": legit_owner,
                "form": form
            })
        else:
            if highest_bid is None and Decimal(amount) > listing.price:
                add_bid = Bid(item=listing, bidder=user, amount=amount)
                add_bid.save()
                is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
                return render(request, "auctions/detail.html", {
                    "comments": Comment.objects.filter(item=listing),
                    "all_bid": Bid.objects.filter(item=listing),
                    "listing": listing,
                    "is_watchlisted": is_watchlisted,
                    "legit_owner": legit_owner,
                    "form": form
                })
            elif highest_bid is None and Decimal(amount) <= listing.price:
                lower_than_price = highest_bid is None and Decimal(amount) <= listing.price
                is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
                return render(request, "auctions/detail.html", {
                    "comments": Comment.objects.filter(item=listing),
                    "all_bid": Bid.objects.filter(item=listing),
                    "listing": listing,
                    "is_watchlisted": is_watchlisted,
                    "lower_than_price": lower_than_price,
                    "legit_owner": legit_owner,
                    "form": form
                })
            elif highest_bid is not None and Decimal(amount) > highest_bid and Decimal(amount) > listing.price:
                add_bid = Bid(item=listing, bidder=user, amount=amount)
                add_bid.save()
                is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
                return render(request, "auctions/detail.html", {
                    "comments": Comment.objects.filter(item=listing),
                    "all_bid": Bid.objects.filter(item=listing),
                    "listing": listing,
                    "is_watchlisted": is_watchlisted,
                    "legit_owner": legit_owner,
                    "form": form
                })
            elif highest_bid is not None and Decimal(amount) < listing.price:
                lower_than_price = highest_bid is not None and Decimal(amount) < listing.price
                is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
                return render(request, "auctions/detail.html", {
                    "comments": Comment.objects.filter(item=listing),
                    "all_bid": Bid.objects.filter(item=listing),
                    "listing": listing,
                    "is_watchlisted": is_watchlisted,
                    "lower_than_price": lower_than_price,
                    "legit_owner": legit_owner,
                    "form": form
                })
            else:
                error = Decimal(amount) < highest_bid
                is_watchlisted = Watchlist.objects.filter(item=listing, user=user).exists()
                return render(request, "auctions/detail.html", {
                    "comments": Comment.objects.filter(item=listing),
                    "all_bid": Bid.objects.filter(item=listing),
                    "listing": listing,
                    "is_watchlisted": is_watchlisted,
                    "error": error,
                    "legit_owner": legit_owner,
                    "form": form
                })
        
def close(request, listing_id):
    form = CommentForm()
    listing = Listing.objects.get(pk=listing_id)
    legit_owner = request.user == listing.user
    highest_bid = Bid.objects.filter(item=listing).aggregate(max_bid=Max("amount"), max_bidder=Max("bidder"))
    winner_id = highest_bid["max_bidder"]
    if winner_id is not None:
        winner = User.objects.get(id=winner_id)
        if winner:
            listing.winner = winner
            listing.active = False
            listing.save()
            return render(request, "auctions/detail.html", {
                "comments": Comment.objects.filter(item=listing),
                "winner": winner,
                "listing": listing,
                "winner_id": winner_id,
                "form": form
            })
    else:
        listing.active = False
        listing.save()
        return render(request, "auctions/detail.html", {
                "comments": Comment.objects.filter(item=listing),
                "listing": listing,
                "winner_id": winner_id,
                "form": form
            })
    
def comment(request, listing_id):
    form = CommentForm()
    listing = Listing.objects.get(pk=listing_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            add_comment = form.save(commit=False)
            add_comment.commenters = request.user
            add_comment.item = listing
            add_comment.save()
            form = CommentForm()
            return render(request, "auctions/detail.html", {
            "comments": Comment.objects.filter(item=listing),
            "listing": listing,
            "form": form
        }) 

def categories(request):
    return render(request, "auctions/categories.html", {
        "category": Cat.objects.all()
    })

def listing_category(request, listing_category):
    listing = Listing.objects.filter(category=listing_category)
    return render(request, "auctions/cat_detail.html", {
        "listing_category": listing_category,
        "listing": listing
    })
