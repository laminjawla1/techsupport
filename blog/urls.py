from django.urls import path
from .views import (PostListView, PostDetailView, UserPostListView, index, 
                    RequestAuthorshipView, PostByCategoryView, like_post, CommentView, CommentUpdateViewView)

urlpatterns = [
    # path("", PostListView.as_view(), name="blog_home"),
    path("", index, name="blog_home"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<str:username>/posts", UserPostListView.as_view(), name="user_posts"),
    path("post/<int:pk>/comment", CommentView.as_view(), name="add_comment"),
    path("post/comment/<int:pk>/<int:post_id>/edit", CommentUpdateViewView.as_view(), name="edit_comment"),
    path("posts/<str:category>/", PostByCategoryView.as_view(), name="category_posts"),
    path("authorship/request/", RequestAuthorshipView.as_view(), name="request_authorship"),
    path('like/<int:pk>/', like_post, name='like_post'),
]