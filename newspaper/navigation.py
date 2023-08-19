from newspaper.models import Category, Tag, Post 

def nav(request):
    categories = Category.objects.all()[:5]
    tags = Tag.objects.all()[:7]
    trending_posts = Post.objects.filter(status="active", published_at__isnull=False).order_by("-views_count")[:3]

    return {
        "categories": categories,
        "tags": tags,
        "trending_posts": trending_posts,
    }