from decimal import Decimal
from apps.catalog.models import Product


class Cart:
    session_key = "dicho_cart"
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(self.session_key, {})
    def add(self, product, quantity=1, override_quantity=False):
        key = str(product.id)
        if key not in self.cart: self.cart[key] = {"quantity": 0}
        self.cart[key]["quantity"] = quantity if override_quantity else self.cart[key]["quantity"] + quantity
        if self.cart[key]["quantity"] <= 0: self.cart.pop(key, None)
        self.save()
    def remove(self, product):
        self.cart.pop(str(product.id), None); self.save()
    def save(self): self.session.modified = True
    def clear(self): self.session.pop(self.session_key, None); self.session.modified = True
    def __iter__(self):
        products = Product.objects.filter(id__in=self.cart.keys(), is_active=True)
        for product in products:
            item = self.cart[str(product.id)].copy()
            item.update({"product": product, "total_price": product.price * item["quantity"]})
            yield item
    @property
    def count(self): return sum(item["quantity"] for item in self.cart.values())
    @property
    def subtotal(self): return sum((item["total_price"] for item in self), Decimal("0"))
