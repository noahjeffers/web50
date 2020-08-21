from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:item_id>", views.item, name="item"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<int:item_id>/watch", views.watch,name="watch"),
    path("<int:item_id>/remove", views.remove,name="remove"),
    path("<int:item_id>/close", views.close,name="close"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.categories, name="category"),
    path("category/<int:category_id>", views.category, name="category"),
    path("error", views.error, name = "error"),
    path("create", views.create, name="create"),
    path("<int:item_id>/bid",views.bid,name="bid"),
    path("<int:item_id>/comment",views.comment,name="comment"),
    path("closed", views.closed, name="closed")
]
