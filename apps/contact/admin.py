from django.contrib import admin
from .models import ContactMessage
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "subject", "is_read", "created_at"); list_filter = ("is_read", "created_at"); search_fields = ("full_name", "email", "phone", "subject", "message"); readonly_fields = ("created_at",)
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + (("message",) if obj else ())
