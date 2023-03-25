from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing", views.listing, name="listing"),
    path("listing/<int:listing_id>", views.listing_detail, name="listing_detail"),
    path("watchlist/<str:user_username>/", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist/remove/<int:listing_id>", views.watchlist_remove, name="watchlist_remove"),
    path("listing/<int:user_id>/<int:listing_id>/bid", views.bid, name="bid"),
    path("listing/<int:listing_id>/close", views.close, name="close"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:listing_category>", views.listing_category, name="listing_category")
]
