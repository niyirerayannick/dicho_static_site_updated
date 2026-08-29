from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="categories/", blank=True)
    asset_path = models.CharField(max_length=255, blank=True, help_text="Optional existing static image path")
    icon_class = models.CharField(max_length=80, blank=True, default="bi bi-leaf")
    is_active = models.BooleanField(default=True)
    show_in_hero = models.BooleanField(default=False)
    hero_title = models.CharField(max_length=180, blank=True)
    hero_subtitle = models.CharField(max_length=255, blank=True)
    hero_description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["display_order", "name"]
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse("category_detail", args=[self.slug])
    @property
    def product_count(self): return self.products.filter(is_active=True).count()


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.PROTECT)
    name = models.CharField(max_length=180)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    benefits = models.TextField(blank=True)
    ingredients = models.TextField(blank=True)
    usage_instruction = models.TextField(blank=True)
    size = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True)
    asset_path = models.CharField(max_length=255, blank=True, help_text="Optional existing static image path")
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["-created_at", "name"]
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse("product_detail", args=[self.slug])
    @property
    def in_stock(self): return self.stock_quantity > 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="additional_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ["display_order"]
    def __str__(self): return f"{self.product} image"
