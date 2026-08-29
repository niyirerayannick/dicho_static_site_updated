from django.contrib import admin
from .models import Order, OrderItem
class OrderItemInline(admin.TabularInline): model = OrderItem; extra = 0; readonly_fields = ("product_name", "quantity", "unit_price", "line_total")
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "full_name", "total", "payment_method", "status", "created_at")
    list_filter = ("status", "payment_method", "created_at"); search_fields = ("order_number", "full_name", "email", "phone")
    readonly_fields = ("order_number", "subtotal", "delivery_fee", "total", "created_at", "updated_at"); inlines = [OrderItemInline]
    @admin.action(description="Mark selected orders as Confirmed")
    def mark_confirmed(self, request, queryset): queryset.update(status=Order.Status.CONFIRMED)
    @admin.action(description="Mark selected orders as Processing")
    def mark_processing(self, request, queryset): queryset.update(status=Order.Status.PROCESSING)
    @admin.action(description="Mark selected orders as Delivered")
    def mark_delivered(self, request, queryset): queryset.update(status=Order.Status.DELIVERED)
    @admin.action(description="Mark selected orders as Cancelled")
    def mark_cancelled(self, request, queryset): queryset.update(status=Order.Status.CANCELLED)
    actions = ("mark_confirmed", "mark_processing", "mark_delivered", "mark_cancelled")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_name", "quantity", "unit_price", "line_total")
    list_filter = ("order__status",)
    search_fields = ("order__order_number", "product_name")
    readonly_fields = ("order", "product", "product_name", "quantity", "unit_price", "line_total")
