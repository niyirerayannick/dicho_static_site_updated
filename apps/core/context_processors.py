from .models import SiteSetting


def site_context(request):
    from apps.cart.cart import Cart
    return {"site_setting": SiteSetting.objects.first(), "cart_count": Cart(request).count}
