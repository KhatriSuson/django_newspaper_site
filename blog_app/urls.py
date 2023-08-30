from django.urls import path

from blog_app import views

app_name = "news_admin"
urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path(
        "post-detail/<int:pk>/",
        views.PostDetailView.as_view,
        name="post-detail",
    ),
    path("draft-list/", views.DraftListView.as_view(), name="draft-list"),
    path("post-publish/<int:pk>/", views.PostPublishView.as_view, name="post-publish"),
    path(
        "draft-detail/<int:pk>/", views.DraftDetailView.as_view(), name="draft-detail"
    ),
    path("post-create/", views.PostCreateView.as_view(), name="post-create"),
    path("post-update/<int:pk>/", views.PostUpdateView.as_view(), name="post-update"),
    path("post-delete/<int:pk>/", views.PostDeleteView.as_view(), name="post-delete"),
]
