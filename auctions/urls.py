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
    path("watchlist/<str:user_username>", views.watchlist, name="watchlist"),
    path("watchlist/<int:user_id>/<int:listing_id>", views.watchlist_add, name="watchlist_add")
]
