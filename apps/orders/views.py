from urllib.parse import quote

from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from apps.cart.cart import Cart
from apps.core.models import SiteSetting
from .forms import CheckoutForm
from .models import Order, OrderItem

WHATSAPP_DEFAULT_URL = "https://wa.me/250788428711"


def build_order_whatsapp_message(order, request=None):
    item_lines = []
    for item in order.items.all():
        product_link = ""
        if item.product:
            product_url = item.product.get_absolute_url()
            product_link = request.build_absolute_uri(product_url) if request else product_url
        item_lines.append(
            f"- {item.product_name} x{item.quantity} = RWF {item.line_total:.2f}"
            + (f"\n  Product link: {product_link}" if product_link else "")
        )

    message = (
        "Hello DICHO Ltd, I would like to place my order.\n\n"
        f"Order Number: {order.order_number}\n"
        f"Customer Name: {order.full_name}\n"
        f"Phone: {order.phone}\n"
        f"Delivery Location: {order.delivery_location}\n"
        f"Payment Method: {order.get_payment_method_display()}\n"
        f"Order Notes: {order.order_notes or 'None'}\n\n"
        "Products:\n"
        + "\n".join(item_lines)
        + f"\n\nTotal: RWF {order.total:.2f}\n"
    )
    return message


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
    order = get_object_or_404(Order, order_number=order_number)
    site_setting = SiteSetting.objects.first()
    whatsapp_base = getattr(site_setting, "whatsapp_url", "") or WHATSAPP_DEFAULT_URL
    whatsapp_url = f"{whatsapp_base}?text={quote(build_order_whatsapp_message(order, request))}"
    return render(request, "orders/order_success.html", {"order": order, "whatsapp_url": whatsapp_url})
