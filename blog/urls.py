# created by me
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="blog"),
    path("blogpost/<int:id>", views.blogpost,name="blogHome"),
]

