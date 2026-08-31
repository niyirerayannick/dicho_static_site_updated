from django.contrib import admin
from .models import FAQ, SiteSetting, Testimonial

admin.site.site_header = "DICHO Admin"
admin.site.site_title = "DICHO Admin Portal"
admin.site.index_title = "Dashboard"


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("company_name", "phone", "email", "facebook_url", "instagram_url", "tiktok_url")
    fieldsets = (
        ("Company details", {"fields": ("company_name", "tagline", "phone", "email", "whatsapp_number", "whatsapp_url", "address", "working_hours", "logo", "favicon")}),
        ("Social media", {"fields": ("facebook_url", "instagram_url", "tiktok_url", "youtube_url", "x_url", "linkedin_url")}),
    )
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "rating", "is_active", "display_order")
    list_filter = ("is_active", "rating")
    search_fields = ("name", "location", "message")
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("question", "answer")
