from django.shortcuts import render
from apps.catalog.models import Category, Product


def home(request):
    return render(request, "pages/home.html", {
        "hero_categories": Category.objects.filter(is_active=True, show_in_hero=True).order_by("display_order")[:4],
        "categories": Category.objects.filter(is_active=True)[:8],
        "featured_products": Product.objects.filter(is_active=True, is_featured=True)[:8],
    })


def about(request): return render(request, "pages/about.html")
