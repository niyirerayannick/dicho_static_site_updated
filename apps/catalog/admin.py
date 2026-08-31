from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview", "is_active", "show_in_hero", "display_order", "updated_at")
    list_filter = ("is_active", "show_in_hero")
    search_fields = ("name", "description", "hero_title", "hero_subtitle", "hero_description")
    prepopulated_fields = {"slug": ("name",)}
    def image_preview(self, obj):
        return format_html('<img src="{}" width="45" height="45" style="object-fit:cover">', obj.image.url) if obj.image else "—"

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock_quantity", "image_preview", "is_active", "is_featured", "created_at")
    list_filter = ("category", "is_active", "is_featured", "is_best_seller", "is_new", "is_on_sale")
    search_fields = ("name", "short_description", "description", "ingredients", "benefits")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    def image_preview(self, obj):
        return format_html('<img src="{}" width="45" height="45" style="object-fit:cover">', obj.image.url) if obj.image else "—"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "alt_text", "display_order")
    list_filter = ("product__category",)
    search_fields = ("product__name", "alt_text")
