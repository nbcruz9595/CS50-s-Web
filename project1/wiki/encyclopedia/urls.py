from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("message", views.message, name="message"),
    path("newentry/", views.newentry, name="newentry"),
    path("edit/<str:entry>",views.edit_entry, name="edit_entry"),
    path("random_page",views.random_page, name="random_page"),
]
