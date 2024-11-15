from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name='register'),
    path("profile/", views.profile, name="profile"),
    path("", views.PostListView.as_view(), name="posts"),
    path("posts/<int:pk>", views.PostDetailView.as_view(), name="post"),
    path("userposts/", views.UserPostListView.as_view(), name="userposts"),
    path("usercomments/", views.UserCommentListView.as_view(), name="usercomments"),
    path("comments/<int:pk>/update", views.CommentUpdateView.as_view(), name="comments_update"),
    path("comments/<int:pk>/delete", views.CommentDeleteView.as_view(), name="comments_delete"),
    path("posts/create", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/update", views.PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/delete", views.PostDeleteView.as_view(), name="post_delete"),
]
