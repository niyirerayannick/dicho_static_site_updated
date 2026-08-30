from django.contrib import admin
from django.utils.html import format_html

from .models import ContentCategory, ContentPost


@admin.register(ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("display_order", "name")


@admin.register(ContentPost)
class ContentPostAdmin(admin.ModelAdmin):
    list_display = ("title", "post_type", "category", "image_preview", "is_published", "is_featured", "published_at")
    list_filter = ("post_type", "is_published", "is_featured", "category")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = ("category", "related_product")
    ordering = ("-published_at",)

    @admin.display(description="Image")
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="48" height="48" style="object-fit:cover;border-radius:6px">', obj.featured_image.url)
        return "—"
