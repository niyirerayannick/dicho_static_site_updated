from django.contrib import admin
from .models import FAQ, SiteSetting, Testimonial

admin.site.register(SiteSetting)
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
