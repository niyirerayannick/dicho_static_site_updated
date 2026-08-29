from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from apps.catalog.models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart.html", {"cart": cart, "cart_items": list(cart), "subtotal": cart.subtotal})

@require_POST
def add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    quantity = max(1, int(request.POST.get("quantity", 1)))
    Cart(request).add(product, min(quantity, product.stock_quantity) if product.stock_quantity else quantity)
    messages.success(request, f"{product.name} was added to your cart.")
    return redirect(request.POST.get("next") or "cart_detail")

@require_POST
def update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Cart(request).add(product, max(0, int(request.POST.get("quantity", 1))), override_quantity=True)
    messages.success(request, "Cart updated.")
    return redirect("cart_detail")

@require_POST
def remove(request, product_id):
    Cart(request).remove(get_object_or_404(Product, pk=product_id))
    messages.success(request, "Item removed from your cart.")
    return redirect("cart_detail")
