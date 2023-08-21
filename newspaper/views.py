import datetime
from typing import Any, Dict
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View, DetailView
from newspaper.models import Post, Category, Tag
from django.utils import timezone
from django.contrib import messages 
from newspaper.forms import ContactForm, CommentForm


# Create your views here.

class HomeView(ListView):
    model = Post
    template_name = "aznews/home.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.filter(status="active", published_at__isnull=False)[:5]
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_post"] = Post.objects.filter(published_at__isnull=False, status="active").order_by("-published_at", "-views_count").first()
        context["featured_post"] = Post.objects.filter(published_at__isnull=False, status="active").order_by("-published_at", "-views_count")[1:4]
        one_week_ago = timezone.now() -datetime.timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(published_at__isnull=False, status="active", published_at__gte=one_week_ago).order_by("-published_at", "-views_count")[:7]
        context["recent_posts"] = Post.objects.filter(published_at__isnull=False, status="active").order_by("-published_at")[:7]
        return context 
    
    
class AbooutView(TemplateView):
    template_name = "aznews/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

from newspaper.forms import ContactForm
class ContactView(View):
    template_name = "aznews/contact.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your query was successfully submitted.")
            return redirect("contact")
        else:
            messages.error(request, "Cannot sumbit your query. Something went wrong.")
            return render(request, self.template_name, {"form":form},)



class PostListView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        queryset = Post.objects.filter(status="active", published_at__isnull=False)
        return queryset
    
class PostByCategoryView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        queryset = Post.objects.filter(status="active", published_at__isnull=False, category__id=self.kwargs["category_id"],),
        return queryset
    

class PostByTagView(ListView):
    model = Post
    template_name = "aznews/list/list.html"
    context_object_name = "posts"
    paginate_by = 1

    def get_queryset(self):
        queryset = Post.objects.filter(
            status="active", published_at__isnull=False, tag__id=self.kwarg["tag_id"],
        )
        return queryset
    



class PostDetailView(DetailView):
    
    model = Post 
    template_name = "aznews/detail/detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_post = self.get_object()

        context["previous_post"] = (Post.objects.filter(published_at__isnull=False, status="active", id__lt=current_post.id).order_by("-id").first()) # "-id" = descendign order sorting

        context["next_post"] = (Post.objects.filter(published_at__isnull=False, status="active", id__gt=current_post.id).order_by("id").first())
        return context


class CommentView(View):
    def post(self, request):
        form = CommentForm(request.POST)
        post_id = request.POST["post"]
        if form.is_valid():
            form.save()
            return redirect("post-detail", post_id)

            post = Post.objects.get(pk=post_id)
            return render(request, "aznews/detail/detail.html", {"post":post, "form":form},)

from django.core.paginator import Paginator, PageNotAnInteger
from django.db.models import Q

class PostSearchView(View):
    template_name = "aznews/list/list.html"

    def get(self, request, *args, **kwargs):
        query = request.GET["query"]
        post_list = Post.objects.filter((Q(title__icontains=query) | Q(content__icontains=query)) & Q(status="active") & Q(published_at__isnull=False)).order_by("-published_at")


        # pagination start

        page = request.GET.get("page", 1)
        paginate_by = 3
        paginator = Paginator(post_list, paginate_by)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)

            # paginaton end 

        return render(request, self.template_name, {"page_obj": posts, "query": query},)