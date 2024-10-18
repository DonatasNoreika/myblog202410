
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="posts"),
    path("posts/<int:pk>", views.PostDetailView.as_view(), name="post"),
    path("userposts/", views.UserPostListView.as_view(), name="userposts"),
]
