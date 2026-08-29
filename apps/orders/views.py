from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from apps.cart.cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem

def checkout(request):
    cart = Cart(request); items = list(cart)
    if not items:
        messages.info(request, "Your cart is empty. Add a product before checking out."); return redirect("shop")
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False); order.subtotal = cart.subtotal; order.delivery_fee = 0; order.total = order.subtotal; order.save()
                for item in items:
                    product = item["product"]
                    OrderItem.objects.create(order=order, product=product, product_name=product.name, quantity=item["quantity"], unit_price=product.price, line_total=item["total_price"])
                    if product.stock_quantity >= item["quantity"]:
                        product.stock_quantity -= item["quantity"]; product.save(update_fields=["stock_quantity"])
                cart.clear()
            return redirect("order_success", order_number=order.order_number)
    else: form = CheckoutForm()
    return render(request, "orders/checkout.html", {"form": form, "cart_items": items, "subtotal": cart.subtotal})

def order_success(request, order_number):
    return render(request, "orders/order_success.html", {"order": get_object_or_404(Order, order_number=order_number)})
