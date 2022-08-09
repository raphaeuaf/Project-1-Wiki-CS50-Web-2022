from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("editpage", views.editpage, name="editpage"),
    path("randompage", views.randompage, name="randompage"),
    path("<str:title>", views.retrieve, name="retrieve")
]
