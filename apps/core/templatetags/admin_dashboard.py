from datetime import timedelta

from django import template
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.urls import reverse
from django.utils import timezone

from apps.catalog.models import Category, Product
from apps.contact.models import ContactMessage
from apps.newsletter.models import NewsletterSubscriber
from apps.orders.models import Order

try:
    from apps.content.models import ContentPost
except ImportError:  # pragma: no cover - keeps the dashboard safe if content is removed.
    ContentPost = None


register = template.Library()


@register.simple_tag
def admin_dashboard_data():
    """Return lightweight, real-time data for the staff-only admin index."""
    today = timezone.localdate()
    start_date = today - timedelta(days=6)
    status_counts = {value: 0 for value, _label in Order.Status.choices}
    status_counts.update(
        {
            entry["status"]: entry["count"]
            for entry in Order.objects.values("status").annotate(count=Count("id"))
        }
    )
    daily_counts = {
        entry["day"]: entry["count"]
        for entry in (
            Order.objects.filter(created_at__date__gte=start_date)
            .annotate(day=TruncDate("created_at"))
            .values("day")
            .annotate(count=Count("id"))
        )
    }
    dates = [start_date + timedelta(days=offset) for offset in range(7)]
    category_counts = list(
        Category.objects.annotate(product_total=Count("products"))
        .filter(product_total__gt=0)
        .order_by("-product_total", "name")
        .values_list("name", "product_total")[:8]
    )
    pending_orders = status_counts.get(Order.Status.PENDING, 0)
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    inactive_products = Product.objects.filter(is_active=False).count()
    low_stock_products = Product.objects.filter(stock_quantity__lte=5, is_active=True).count()
    unpublished_posts = ContentPost.objects.filter(is_published=False).count() if ContentPost else 0
    newsletter_subscribers = NewsletterSubscriber.objects.filter(is_active=True).count()

    alerts = []
    if pending_orders:
        alerts.append({"kind": "warning", "message": f"You have {pending_orders} pending order{'s' if pending_orders != 1 else ''} waiting for confirmation."})
    if unread_messages:
        alerts.append({"kind": "info", "message": f"You have {unread_messages} unread contact message{'s' if unread_messages != 1 else ''}."})
    if low_stock_products:
        alerts.append({"kind": "warning", "message": f"{low_stock_products} active product{'s' if low_stock_products != 1 else ''} ha{'ve' if low_stock_products != 1 else 's'} low stock."})
    if inactive_products:
        alerts.append({"kind": "neutral", "message": f"{inactive_products} product{'s' if inactive_products != 1 else ''} are inactive."})
    if unpublished_posts:
        alerts.append({"kind": "neutral", "message": f"{unpublished_posts} content post{'s' if unpublished_posts != 1 else ''} are not published."})
    if newsletter_subscribers:
        alerts.append({"kind": "success", "message": f"You have {newsletter_subscribers} active newsletter subscriber{'s' if newsletter_subscribers != 1 else ''}."})
    if not alerts:
        alerts.append({"kind": "success", "message": "All clear for now."})

    return {
        "kpis": [
            {"label": "Total Products", "value": Product.objects.count(), "helper": "All catalogue items", "icon": "bi-box-seam", "url": reverse("admin:catalog_product_changelist")},
            {"label": "Active Products", "value": Product.objects.filter(is_active=True).count(), "helper": "Visible in the shop", "icon": "bi-check-circle", "url": reverse("admin:catalog_product_changelist")},
            {"label": "Product Categories", "value": Category.objects.count(), "helper": "Organise your range", "icon": "bi-grid", "url": reverse("admin:catalog_category_changelist")},
            {"label": "Total Orders", "value": Order.objects.count(), "helper": "All customer orders", "icon": "bi-receipt", "url": reverse("admin:orders_order_changelist")},
            {"label": "Pending Orders", "value": pending_orders, "helper": "Awaiting confirmation", "icon": "bi-hourglass-split", "url": f"{reverse('admin:orders_order_changelist')}?status={Order.Status.PENDING}"},
            {"label": "Completed / Delivered", "value": status_counts.get(Order.Status.DELIVERED, 0), "helper": "Delivered to customers", "icon": "bi-truck", "url": f"{reverse('admin:orders_order_changelist')}?status={Order.Status.DELIVERED}"},
            {"label": "Total Revenue", "value": Order.objects.aggregate(total=Sum("total"))["total"] or 0, "helper": "Order value to date", "icon": "bi-cash-stack", "prefix": "RWF ", "url": reverse("admin:orders_order_changelist")},
            {"label": "Contact Messages", "value": ContactMessage.objects.count(), "helper": "Customer enquiries", "icon": "bi-envelope", "url": reverse("admin:contact_contactmessage_changelist")},
            {"label": "Newsletter Subscribers", "value": newsletter_subscribers, "helper": "Active email audience", "icon": "bi-people", "url": reverse("admin:newsletter_newslettersubscriber_changelist")},
        ],
        "recent_orders": Order.objects.order_by("-created_at")[:8],
        "recent_messages": ContactMessage.objects.order_by("-created_at")[:5],
        "alerts": alerts,
        "quick_actions": [
            {"label": "Add Product", "helper": "Create an ALVI item", "icon": "bi-plus-circle", "url": reverse("admin:catalog_product_add")},
            {"label": "View Orders", "helper": "Process customer orders", "icon": "bi-receipt", "url": reverse("admin:orders_order_changelist")},
            {"label": "Add Category", "helper": "Organise the catalogue", "icon": "bi-folder-plus", "url": reverse("admin:catalog_category_add")},
            {"label": "View Messages", "helper": "Review customer enquiries", "icon": "bi-envelope", "url": reverse("admin:contact_contactmessage_changelist")},
            *([{"label": "Add Press Post", "helper": "Publish training or news", "icon": "bi-pencil-square", "url": reverse("admin:content_contentpost_add")}] if ContentPost else []),
            {"label": "View Website", "helper": "Open the public site", "icon": "bi-globe2", "url": reverse("home")},
        ],
        "orders_by_status": {
            "labels": [label for _value, label in Order.Status.choices],
            "data": [status_counts[value] for value, _label in Order.Status.choices],
        },
        "orders_last_week": {
            "labels": [date.strftime("%a") for date in dates],
            "data": [daily_counts.get(date, 0) for date in dates],
        },
        "products_by_category": {
            "labels": [name for name, _count in category_counts],
            "data": [count for _name, count in category_counts],
        },
        "has_orders": any(status_counts.values()),
        "has_category_data": bool(category_counts),
    }
