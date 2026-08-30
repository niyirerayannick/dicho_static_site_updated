from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import ContentCategory, ContentPost


def _filtered_posts(request, post_types):
    posts = ContentPost.objects.filter(is_published=True, post_type__in=post_types).select_related("category", "related_product")
    query = request.GET.get("q", "").strip()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query) | Q(related_product__name__icontains=query))
    return posts, query


def trainings(request):
    posts, query = _filtered_posts(request, [ContentPost.PostType.TRAINING])
    categories = ContentCategory.objects.filter(is_active=True, posts__post_type=ContentPost.PostType.TRAINING).distinct()
    selected_category = request.GET.get("category", "")
    if selected_category:
        posts = posts.filter(category__slug=selected_category)
    featured_post = posts.filter(is_featured=True).first()
    page_obj = Paginator(posts, 9).get_page(request.GET.get("page"))
    return render(request, "content/trainings.html", {"page_obj": page_obj, "posts": page_obj.object_list, "categories": categories, "query": query, "selected_category": selected_category, "featured_post": featured_post})


def training_detail(request, slug):
    post = get_object_or_404(ContentPost.objects.select_related("related_product", "category"), slug=slug, post_type=ContentPost.PostType.TRAINING, is_published=True)
    return render(request, "content/training_detail.html", {"post": post})


def press_room(request):
    posts, query = _filtered_posts(request, [ContentPost.PostType.NEWS, ContentPost.PostType.BLOG])
    selected_type = request.GET.get("type", "")
    if selected_type in (ContentPost.PostType.NEWS, ContentPost.PostType.BLOG):
        posts = posts.filter(post_type=selected_type)
    featured_post = posts.filter(is_featured=True).first()
    page_obj = Paginator(posts, 9).get_page(request.GET.get("page"))
    return render(request, "content/press_room.html", {"page_obj": page_obj, "posts": page_obj.object_list, "query": query, "selected_type": selected_type, "featured_post": featured_post})


def press_post_detail(request, slug):
    post = get_object_or_404(ContentPost.objects.select_related("related_product", "category"), slug=slug, post_type__in=[ContentPost.PostType.NEWS, ContentPost.PostType.BLOG], is_published=True)
    return render(request, "content/post_detail.html", {"post": post})

