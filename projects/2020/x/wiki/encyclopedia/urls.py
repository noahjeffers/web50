from django.urls import path

from . import views


app_name="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/new", views.new, name="new"),
    path("wiki/error",views.error, name="error"),
    path("search", views.search, name="search"),
    path("wiki/search", views.search, name = "search"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("wiki/<str:title>",views.page, name="page"),
    path("random", views.random, name = "random")
]
