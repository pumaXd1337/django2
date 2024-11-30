from django.shortcuts import render, get_object_or_404
from django.db.models.manager import BaseManager
from .models import Category, Post
from datetime import datetime, timezone


# Create your views here.
def index(request):

    posts = _filter_posts(Post.objects.select_related(
        'category', 'author', 'location'
    ))[:5]

    return render(request, 'blog/index.html',
                  {'post_list': posts})


def post_detail(request, post_id):

    now = datetime.now(timezone.utc)
    post_obj = get_object_or_404(
        Post,
        pk=post_id,
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    )

    return render(request, 'blog/detail.html',
                  {'post': post_obj})


def category_posts(request, category_slug):

    category_obj = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = _filter_posts(category_obj.posts.select_related(
        'category', 'author', 'location'
    ), category_filtered=True)

    return render(request, 'blog/category.html',
                  {
                      'post_list': posts,
                      'category': category_obj
                  })


def _filter_posts(posts: BaseManager[Post],
                  category_filtered=False) -> BaseManager[Post]:

    now = datetime.now(timezone.utc)

    if category_filtered:
        return posts.filter(
            pub_date__lte=now,
            is_published=True
        )
    else:
        return posts.filter(
            pub_date__lte=now,
            is_published=True,
            category__is_published=True
        )
