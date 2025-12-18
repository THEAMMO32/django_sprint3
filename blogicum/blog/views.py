from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


POSTS_LIMIT = 5


def _published_posts_queryset():
    return (
        Post.objects.select_related('category', 'location', 'author')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__isnull=False,
            category__is_published=True,
        )
        .order_by('-pub_date')
    )


def index(request):
    posts = _published_posts_queryset()[:POSTS_LIMIT]
    return render(request, 'blog/index.html', {'posts': posts})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    posts = (
        _published_posts_queryset()
        .filter(category=category)
    )
    return render(
        request,
        'blog/category.html',
        {'category': category, 'posts': posts},
    )


def post_detail(request, post_id):
    post = get_object_or_404(
        _published_posts_queryset(),
        pk=post_id,
    )
    return render(request, 'blog/detail.html', {'post': post})
