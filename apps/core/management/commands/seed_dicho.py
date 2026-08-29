from pathlib import Path
from shutil import copy2

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.catalog.models import Category, Product
from apps.core.models import FAQ, SiteSetting, Testimonial


CATEGORIES = [
    ("Cosmetics & Personal Care", "Natural skincare, body care and personal hygiene essentials.", "categories/cosmetics.svg", "categories/cosmetics-personal-care.png", "bi bi-bag-heart"),
    ("Hair Care Products", "Shampoos, creams, oils and treatments for healthy strong hair.", "categories/hair.svg", "categories/hair-care-products.png", "bi bi-scissors"),
    ("Cooking & Edible Oils", "Pure, healthy oils for cooking, dressing and everyday meals.", "categories/edible-oils.svg", "categories/cooking-edible-oils.png", "bi bi-droplet"),
    ("Liquid Detergents & Home Care", "Effective cleaning products for home and commercial use.", "categories/detergents.svg", "categories/liquid-detergents-home-care.png", "bi bi-house-heart"),
    ("Aromatherapy & Essential Oils", "Pure essential oils for relaxation, wellness and formulations.", "categories/essential-oils.svg", "categories/aromatherapy-essential-oils.png", "bi bi-flower1"),
    ("Spices for Tea & Food", "Natural spices and herbs to enrich taste and aroma.", "categories/spices.svg", "categories/spices-tea-food.png", "bi bi-cup-hot"),
    ("Nuts & Dried Products", "Healthy nuts, seeds and dried fruits for energy and nutrition.", "categories/nuts.svg", "categories/nuts-dried-products.png", "bi bi-basket"),
    ("Fresh Agricultural Products", "Fresh, selected agricultural products including avocados.", "categories/fresh.svg", "categories/fresh-agricultural-products.png", "bi bi-leaf"),
]

HERO_CONTENT = {
    "Cosmetics & Personal Care": ("Natural Products", "Natural care for healthy, glowing skin", "Discover body lotions, aloe vera gel, herbal jelly, skin oils, and personal care products made for everyday use."),
    "Hair Care Products": ("Natural Products", "Nourish and protect your hair naturally", "Explore hair oils, creams, and jelly products designed to support healthy-looking hair and scalp care."),
    "Cooking & Edible Oils": ("Quality You Can Trust", "Pure oils for everyday cooking and nutrition", "Choose quality avocado oil, olive oil, sunflower oil, and other natural edible oils for your kitchen."),
    "Liquid Detergents & Home Care": ("Quality You Can Trust", "Clean, fresh, and trusted home care", "Find multipurpose liquid detergents and home care products suitable for households and commercial use."),
}

# Placeholder prices supplied in the project brief; replace when a live price list is available.
REAL_PRODUCTS = [
    {"name": "ALVI Castor Oil", "category": "Cosmetics & Personal Care", "size": "Size not clearly visible", "price": 8000, "image": "products/alvi-castor-oil.jpeg", "short_description": "Skin care oil infused with Vitamin A for skin.", "description": "ALVI Castor Oil is a skin care oil. The label states that it is infused with Vitamin A for skin.", "benefits": "Infused with Vitamin A for Skin.", "ingredients": "See product label for details.", "usage": "Apply externally according to the product label."},
    {"name": "ALVI Calendula Oil", "category": "Cosmetics & Personal Care", "size": "Size not clearly visible", "price": 8000, "image": "products/alvi-calendula-oil.jpeg", "short_description": "Skin care oil infused with Vitamin A for skin.", "description": "ALVI Calendula Oil is a skin care oil. The label states that it is infused with Vitamin A for skin.", "benefits": "Infused with Vitamin A for Skin.", "ingredients": "See product label for details.", "usage": "Apply externally according to the product label."},
    {"name": "ALVI Aloe Vera Hydrating Gel", "category": "Cosmetics & Personal Care", "size": "Size not clearly visible", "price": 8000, "image": "products/alvi-aloe-vera-hydrating-gel.jpeg", "short_description": "Hydrating aloe vera gel with Vitamin C.", "description": "ALVI Aloe Vera Hydrating Gel is a hydrating skin care gel. The label states that it is made with Vitamin C.", "benefits": "With Vitamin C.", "ingredients": "See product label for details.", "usage": "Apply externally according to the product label."},
    {"name": "ALVI Herbal Jelly", "category": "Cosmetics & Personal Care", "size": "230 g", "price": 3000, "image": "products/alvi-herbal-jelly.jpeg", "short_description": "Herbal jelly with calendula oil and avocado oil.", "description": "ALVI Herbal Jelly contains calendula oil (3%) and avocado oil. The label mentions deep moisturizing and skin protection.", "benefits": "With calendula oil (3%) and avocado oil. Label mentions deep moisturizing and skin protection.", "ingredients": "Calendula oil (3%) and avocado oil; see product label for details.", "usage": "Apply externally according to the product label."},
    {"name": "ALVI Body Lotion – Avocado Oil & Aloe Vera", "category": "Cosmetics & Personal Care", "size": "500 ml", "price": 5000, "image": "products/alvi-body-lotion.jpeg", "short_description": "Body lotion with avocado oil and aloe vera.", "description": "ALVI Body Lotion with avocado oil and aloe vera nourishes and softens the skin.", "benefits": "Nourishes and softens the skin.", "ingredients": "See product label for details.", "usage": "Apply externally according to the product label."},
    {"name": "ALVI Avocado Hair Growing Oil", "category": "Hair Care Products", "size": "50 ml", "price": 6000, "image": "products/alvi-avocado-hair-growing-oil.jpeg", "short_description": "Hair-growing oil with avocado oil and natural herbs.", "description": "ALVI Avocado Hair Growing Oil is a hair care oil with avocado oil and natural herbs, as stated on the label.", "benefits": "Hair-growing oil with avocado oil and natural herbs.", "ingredients": "See product label for details.", "usage": "Use according to the product label."},
    {"name": "ALVI Extra Virgin Avocado Oil – Cold Pressed", "category": "Cooking & Edible Oils", "size": "500 ml", "price": 15000, "image": "products/alvi-extra-virgin-avocado-oil.jpeg", "short_description": "Cold pressed extra virgin avocado oil for cooking.", "description": "Cold pressed avocado oil suitable for cooking, roasting, frying, baking, drizzling, and dipping.", "benefits": "Suitable for cooking, roasting, frying, baking, drizzling, and dipping.", "ingredients": "See product label for details.", "usage": "Use as a cooking oil according to the product label."},
    {"name": "ALVI Multipurpose Liquid Detergent 1L", "category": "Liquid Detergents & Home Care", "size": "1L", "price": 4000, "image": "products/alvi-multipurpose-liquid-detergent-1l.jpeg", "short_description": "Multipurpose liquid detergent for cleaning and home care.", "description": "ALVI Multipurpose Liquid Detergent for cleaning and home care.", "benefits": "Multipurpose liquid detergent for cleaning and home care.", "ingredients": "See product label for details.", "usage": "Use according to the product label."},
    {"name": "ALVI Multipurpose Liquid Detergent 5L", "category": "Liquid Detergents & Home Care", "size": "5L", "price": 12000, "image": "products/alvi-multipurpose-liquid-detergent-5l.jpeg", "short_description": "Multipurpose liquid detergent for household and commercial cleaning.", "description": "ALVI Multipurpose Liquid Detergent for household and commercial cleaning.", "benefits": "Multipurpose liquid detergent for household and commercial cleaning.", "ingredients": "See product label for details.", "usage": "Use according to the product label."},
    {"name": "ALVI Multipurpose Liquid Detergent 20L", "category": "Liquid Detergents & Home Care", "size": "20L", "price": 35000, "image": "products/alvi-multipurpose-liquid-detergent-20l.jpeg", "short_description": "Large-size multipurpose liquid detergent for bulk cleaning.", "description": "Large-size ALVI Multipurpose Liquid Detergent for commercial and bulk cleaning use.", "benefits": "Large-size multipurpose liquid detergent for commercial and bulk cleaning use.", "ingredients": "See product label for details.", "usage": "Use according to the product label."},
    {"name": "DICHO Grape / Raisins", "category": "Nuts & Dried Products", "size": "250 g", "price": 4000, "image": "products/dicho-grape-raisins.jpeg", "short_description": "Packaged dried grapes / raisins.", "description": "DICHO packaged dried grapes / raisins. The product label displays Grape.", "benefits": "Packaged dried grapes / raisins.", "ingredients": "See product label for details.", "usage": "Enjoy as desired."},
    {"name": "DICHO Cashew Nut", "category": "Nuts & Dried Products", "size": "250 g", "price": 5000, "image": "products/dicho-cashew-nut.png", "short_description": "Packaged cashew nuts.", "description": "DICHO packaged cashew nuts.", "benefits": "Packaged cashew nuts.", "ingredients": "See product label for details.", "usage": "Enjoy as desired."},
    {"name": "DICHO Hibiscus Dried Flower", "category": "Nuts & Dried Products", "size": "125 g", "price": 3000, "image": "products/dicho-hibiscus-dried-flower.jpeg", "short_description": "Packaged dried hibiscus flower.", "description": "DICHO packaged dried hibiscus flower.", "benefits": "Packaged dried hibiscus flower.", "ingredients": "See product label for details.", "usage": "Use according to the product label."},
]

LEGACY_SEED_SLUGS = ["dicho-aloe-vera-gel", "dicho-body-cream", "herbal-jelly", "glycerin", "hair-growth-oil", "hair-cream", "hair-jelly", "avocado-oil", "olive-oil-extra-virgin", "sunflower-oil", "lavender-essential-oil", "lemongrass-essential-oil", "eucalyptus-essential-oil", "hand-soap", "multipurpose-liquid-detergent", "dishwashing-liquid", "spice-mix-for-tea", "mixed-nuts", "dried-raisins", "fresh-avocado"]


def ensure_media_file(command, relative_path):
    """Copy a repository image into MEDIA_ROOT without overwriting newer media."""
    source = Path(settings.BASE_DIR) / "images" / relative_path
    destination = Path(settings.MEDIA_ROOT) / relative_path
    if not source.is_file():
        command.stdout.write(command.style.WARNING(f"Image source missing: {source}"))
        return destination.is_file()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists() or source.stat().st_mtime_ns > destination.stat().st_mtime_ns:
        copy2(source, destination)
        command.stdout.write(f"Copied media image: {relative_path}")
    return True


class Command(BaseCommand):
    help = "Create or update DICHO and ALVI product data without duplicating records."

    def handle(self, *args, **options):
        site, _ = SiteSetting.objects.get_or_create(company_name="DICHO Ltd", defaults={"tagline": "Home of ALVI Natural Products", "phone": "+250 788 428 711", "email": "info@dicho.rw", "whatsapp_number": "+250 788 428 711", "whatsapp_url": "https://wa.me/250788428711", "address": "Kigali, Rwanda", "working_hours": "Mon - Sat: 8:00 AM - 6:00 PM"})
        SiteSetting.objects.filter(pk=site.pk).update(phone="+250 788 428 711", whatsapp_number="+250 788 428 711", whatsapp_url="https://wa.me/250788428711")
        site.refresh_from_db(fields=["phone", "whatsapp_number", "whatsapp_url"])
        logo_available = ensure_media_file(self, "logo/dicho-logo.jpeg")
        if logo_available and (not site.logo or not site.logo.storage.exists(site.logo.name)):
            site.logo.name = "site/dicho-logo.jpeg"; site.save(update_fields=["logo"])
        categories = {}
        for order, (name, description, asset_path, image, icon_class) in enumerate(CATEGORIES, 1):
            hero_title, hero_subtitle, hero_description = HERO_CONTENT.get(name, ("", "", ""))
            category_image = image if ensure_media_file(self, image) else ""
            category, _ = Category.objects.update_or_create(slug=slugify(name), defaults={"name": name, "description": description, "asset_path": asset_path, "image": category_image, "icon_class": icon_class, "is_active": True, "show_in_hero": name in HERO_CONTENT, "hero_title": hero_title, "hero_subtitle": hero_subtitle, "hero_description": hero_description, "display_order": order})
            categories[name] = category
        Product.objects.filter(slug__in=LEGACY_SEED_SLUGS).update(is_active=False, is_featured=False, is_best_seller=False, is_new=False)
        for index, data in enumerate(REAL_PRODUCTS):
            product_image = data["image"] if ensure_media_file(self, data["image"]) else ""
            defaults = {"name": data["name"], "category": categories[data["category"]], "short_description": data["short_description"], "description": data["description"], "benefits": data["benefits"], "ingredients": data["ingredients"], "usage_instruction": data["usage"], "size": data["size"], "price": data["price"], "old_price": None, "image": product_image, "asset_path": "", "is_active": True, "is_featured": True, "is_new": index < 7, "is_best_seller": index in (3, 6, 10), "is_on_sale": False}
            product, created = Product.objects.update_or_create(slug=slugify(data["name"]), defaults=defaults)
            if created:
                product.stock_quantity = 50; product.save(update_fields=["stock_quantity"])
        for order, (question, answer) in enumerate([("How can I place an order?", "Use the shop page, cart and checkout, or contact us on WhatsApp."), ("Do you offer delivery across Rwanda?", "Delivery details are confirmed by the DICHO team after checkout."), ("How can I become a distributor?", "Send a wholesale or partnership inquiry through the contact form.")], 1): FAQ.objects.get_or_create(question=question, defaults={"answer": answer, "display_order": order})
        for order, (name, location, message) in enumerate([("Aline M.", "Kigali", "Natural products I can trust for my family."), ("David K.", "Rwanda", "Reliable quality and friendly customer service.")], 1): Testimonial.objects.get_or_create(name=name, defaults={"location": location, "message": message, "display_order": order})
        self.stdout.write(self.style.SUCCESS("DICHO and ALVI seed data is ready."))
