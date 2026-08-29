from django.urls import path
from . import views

urlpatterns = [
    path("shop/", views.shop, name="shop"), path("categories/", views.categories, name="categories"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"), path("search/", views.search, name="search"),
]
