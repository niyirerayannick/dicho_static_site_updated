from django.http import Http404
from django.shortcuts import render
from apps.catalog.models import Category, Product


NATURAL_SOURCES = {
    "avocado-farms": {
        "title": "Avocado Farms",
        "image": "home/avocado-farm.png",
        "fallback_image": "products/fresh-avocado.svg",
        "image_alt": "Avocado farm source for ALVI products",
        "card_description": "Carefully selected avocado sources used to support ALVI avocado oil and natural care products.",
        "description": "Avocado is one of the natural sources connected to ALVI avocado oil and selected personal care products. DICHO Ltd values quality sourcing and careful handling from natural ingredients to finished ALVI products.",
        "info_cards": [
            ("Natural Source", "Avocado is used as an inspiration and ingredient source for ALVI avocado oil and selected care products."),
            ("ALVI Product Link", "Connected to ALVI Extra Virgin Avocado Oil and avocado-based personal care products."),
            ("Quality Focus", "DICHO Ltd focuses on safe handling, packaging, and customer trust."),
        ],
    },
    "aloe-vera-field": {
        "title": "Aloe Vera Field",
        "image": "home/aloe-vera-field.png",
        "fallback_image": "products/alvi-aloe-vera-hydrating-gel.jpeg",
        "image_alt": "Aloe vera field source for ALVI products",
        "card_description": "Aloe vera fields connected to ALVI personal care inspiration and product development.",
        "description": "Aloe vera is connected to ALVI personal care products and natural product inspiration. DICHO Ltd uses natural-source storytelling to help customers understand the background of ALVI products.",
        "info_cards": [
            ("Natural Inspiration", "Aloe vera supports ALVI personal care product development and customer education."),
            ("ALVI Product Link", "Connected to ALVI Aloe Vera Hydrating Gel and selected beauty care products."),
            ("Customer Guidance", "Customers are encouraged to follow product label instructions for safe use."),
        ],
    },
    "calendula-field": {
        "title": "Calendula Field",
        "image": "home/calendula-field.png",
        "fallback_image": "products/alvi-calendula-oil.jpeg",
        "image_alt": "Calendula field source for ALVI products",
        "card_description": "Calendula-inspired natural sources used in selected ALVI skin care products.",
        "description": "Calendula is one of the natural inspirations behind selected ALVI skin care products. DICHO Ltd continues to improve product quality, labels, packaging, and customer education.",
        "info_cards": [
            ("Natural Inspiration", "Calendula is used as a natural inspiration for selected ALVI skin care products."),
            ("ALVI Product Link", "Connected to ALVI Calendula Oil and selected skin care products."),
            ("Brand Quality", "DICHO Ltd focuses on clear product presentation and quality handling."),
        ],
    },
}


def home(request):
    return render(request, "pages/home.html", {
        "hero_categories": Category.objects.filter(is_active=True, show_in_hero=True).order_by("display_order")[:4],
        "categories": Category.objects.filter(is_active=True)[:8],
        "featured_products": Product.objects.filter(is_active=True, is_featured=True)[:8],
    })


def about(request): return render(request, "pages/about.html")


def natural_sources(request):
    return render(request, "pages/natural_sources.html", {"sources": NATURAL_SOURCES.items()})


def natural_source_detail(request, slug):
    source = NATURAL_SOURCES.get(slug)
    if source is None:
        raise Http404("Natural source not found")
    return render(request, "pages/natural_source_detail.html", {"source": source})
