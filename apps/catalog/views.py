from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Category, Product


def _product_list(request, template="catalog/shop.html", category=None):
    products = Product.objects.filter(is_active=True).select_related("category")
    if category: products = products.filter(category=category)
    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(category__name__icontains=query) | Q(description__icontains=query))
    selected_category = request.GET.get("category", "")
    if selected_category and not category: products = products.filter(category__slug=selected_category)
    ordering = request.GET.get("sort", "")
    products = products.order_by({"price_asc": "price", "price_desc": "-price", "newest": "-created_at"}.get(ordering, "-created_at"))
    page_obj = Paginator(products, 12).get_page(request.GET.get("page"))
    return render(request, template, {"page_obj": page_obj, "products": page_obj.object_list,
        "categories": Category.objects.filter(is_active=True), "query": query, "selected_category": selected_category,
        "selected_sort": ordering, "current_category": category})


def shop(request): return _product_list(request)
def search(request): return _product_list(request, "catalog/search.html")
def categories(request): return render(request, "catalog/categories.html", {"categories": Category.objects.filter(is_active=True)})
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    return _product_list(request, "catalog/category_detail.html", category)
def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    return render(request, "catalog/product_detail.html", {"product": product, "related_products": related_products})
