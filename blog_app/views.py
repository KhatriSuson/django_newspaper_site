from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from blog_app.forms import PostForm
from newspaper.models import Post

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy

# from typing import Any
# from django.db import models
# from django.db.models.query import QuerySet
# from django.shortcuts import render
# from django.urls import reverse_lazy
# from blog_app.models import Post
# from blog_app import PostForm

# from django.utils import timezone
# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import get_object_or_404
# from django.views.generic import ListView, DetailView,CreateView,UpdateView


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "news_admin/post_create.html"
    form_class = PostForm
    # success_url = reverse_lazy("news_admin:draft-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("news_admin:draft-detail", kwargs={"pk": self.object.pk})


class PostListView(ListView):
    model = Post
    template_name = "news_admin/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.filter(published_at__isnull=False).order_by(
            "published_at"
        )
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name = "news_admin/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=False)
        return queryset





class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "news_admin/post_list.html"
    content_objects_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.filter(published_at__isnull=True).order_by("created_at")
        return queryset


# @login_required
# def draft_list(request):
#     posts = Post.objects.filter(published_at__isnull=True).order_by("created_at")
#     return render(request, "post_list.html", {"posts":posts},)


class DraftDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "news_admin/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=True)
        return queryset


# from django.contrib.auth.decorators import login_required
# @login_required
# def draft_detail(request,pk):

#     post = get_object_or_404(Post, pk=pk, published_at__isnull=True)
#     return render(request, "post_details.html", {"post":post},)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "news_admin/post_create.html"
    form_class = PostForm

    def get_success_url(self):
        post = self.get_object()
        if post.published_at:
            return reverse_lazy("news_admin:post-detail", kwargs={"pk": post.pk})
        else:
            return reverse_lazy("news_admin:draft-detail", kwargs={"pk": post.pk})





class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("news_admin:post-list")


class PostPublishView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.published_at = timezone.now()
        post.save()
        return redirect("news_admin:post-detail", pk=pk)


class PostUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
        return render(
            request,
            "news_admin:post_create.html",
            {"form": form},
        )

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            if post.published_at:
                return redirect("news_admin:post-detail", pk=post.pk)
            else:
                return redirect("news_admin:draft-detail", pk=post.pk)
        return render(
            request,
            "news_admin:post_create.html",
            {"form": form},
        )
