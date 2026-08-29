from django.db import models
from apps.catalog.models import Product


class Order(models.Model):
    class PaymentMethod(models.TextChoices):
        MOBILE_MONEY = "mobile_money", "Mobile Money"; BANK_TRANSFER = "bank_transfer", "Bank Transfer"; CASH_ON_DELIVERY = "cash_on_delivery", "Cash on Delivery"
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"; CONFIRMED = "confirmed", "Confirmed"; PROCESSING = "processing", "Processing"; DELIVERED = "delivered", "Delivered"; CANCELLED = "cancelled", "Cancelled"
    order_number = models.CharField(max_length=30, unique=True, blank=True)
    full_name = models.CharField(max_length=150); email = models.EmailField(); phone = models.CharField(max_length=50)
    delivery_location = models.CharField(max_length=255); order_notes = models.TextField(blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2); delivery_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0); total = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices); status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True); updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["-created_at"]
    def __str__(self): return self.order_number or f"Order {self.pk}"
    def save(self, *args, **kwargs):
        if not self.order_number:
            last_id = (Order.objects.order_by("-id").values_list("id", flat=True).first() or 0) + 1
            self.order_number = f"DICHO-ORD-{last_id:05d}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    product_name = models.CharField(max_length=180); quantity = models.PositiveIntegerField(); unit_price = models.DecimalField(max_digits=12, decimal_places=2); line_total = models.DecimalField(max_digits=12, decimal_places=2)
    def __str__(self): return f"{self.quantity} × {self.product_name}"
