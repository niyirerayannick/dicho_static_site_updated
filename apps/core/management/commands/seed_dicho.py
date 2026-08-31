from pathlib import Path
from shutil import copy2

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.text import slugify
from django.utils import timezone

from apps.catalog.models import Category, Product
from apps.content.models import ContentCategory, ContentPost
from apps.core.models import FAQ, SiteSetting, Testimonial


CATEGORIES = [
    ("Cosmetics & Personal Care", "Natural skincare, body care and personal hygiene essentials.", "categories/cosmetics.svg", "categories/cosmetics-personal-care.png", "bi bi-bag-heart"),
    ("Hair Care Products", "Shampoos, creams, oils and treatments for healthy strong hair.", "categories/hair.svg", "categories/hair-care-products.png", "bi bi-scissors"),
    ("Cooking & Edible Oils", "ALVI avocado oil for everyday cooking and nutrition.", "categories/edible-oils.svg", "categories/cooking-edible-oils.png", "bi bi-droplet"),
    ("Liquid Detergents & Home Care", "Effective cleaning products for home and commercial use.", "categories/detergents.svg", "categories/liquid-detergents-home-care.png", "bi bi-house-heart"),
    ("Aromatherapy & Essential Oils", "Pure essential oils for relaxation, wellness and formulations.", "categories/essential-oils.svg", "categories/aromatherapy-essential-oils.png", "bi bi-flower1"),
    ("Spices for Tea & Food", "Natural spices and herbs to enrich taste and aroma.", "categories/spices.svg", "categories/spices-tea-food.png", "bi bi-cup-hot"),
    ("Nuts & Dried Products", "Healthy nuts, seeds and dried fruits for energy and nutrition.", "categories/nuts.svg", "categories/nuts-dried-products.png", "bi bi-basket"),
    ("Fresh Agricultural Products", "Fresh, selected agricultural products including avocados.", "categories/fresh.svg", "categories/fresh-agricultural-products.png", "bi bi-leaf"),
]

HERO_CONTENT = {
    "Cosmetics & Personal Care": ("Natural Products", "Natural care for healthy, glowing skin", "Discover body lotions, aloe vera gel, herbal jelly, skin oils, and personal care products made for everyday use."),
    "Hair Care Products": ("Natural Products", "Nourish and protect your hair naturally", "Explore hair oils, creams, and jelly products designed to support healthy-looking hair and scalp care."),
    "Cooking & Edible Oils": ("Quality You Can Trust", "Pure ALVI avocado oil for everyday cooking and nutrition", "Choose ALVI avocado oil for cooking, roasting, frying, baking, drizzling, and dipping."),
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

LEGACY_SEED_SLUGS = ["dicho-aloe-vera-gel", "dicho-body-cream", "herbal-jelly", "glycerin", "hair-growth-oil", "hair-cream", "hair-jelly", "avocado-oil", "lavender-essential-oil", "lemongrass-essential-oil", "eucalyptus-essential-oil", "hand-soap", "multipurpose-liquid-detergent", "dishwashing-liquid", "spice-mix-for-tea", "mixed-nuts", "dried-raisins", "fresh-avocado"]

CONTENT_CATEGORIES = [
    ("Beauty & Personal Care", "Customer guidance for everyday beauty and personal care products."),
    ("Hair Care", "Simple guides for ALVI hair and scalp care products."),
    ("Home Care", "Guidance for everyday household cleaning products."),
    ("Food & Nutrition", "Kitchen guidance for selected ALVI food products."),
    ("Product Education", "Articles about ALVI products and everyday customer care."),
    ("Company News", "Updates from DICHO Ltd and the ALVI product brand."),
]

CONTENT_POSTS = [
    ("training", "Beauty & Personal Care", "How to Use ALVI Aloe Vera Hydrating Gel", "A simple guide for using ALVI Aloe Vera Hydrating Gel as part of daily personal care.", "Apply the gel to clean skin, avoiding the eye area. Use a suitable amount as part of your everyday care routine. Check the product label before use and store the product properly after use.", "alvi-aloe-vera-hydrating-gel", "products/alvi-aloe-vera-hydrating-gel.jpeg", True),
    ("training", "Beauty & Personal Care", "How to Use ALVI Herbal Jelly", "Learn how ALVI Herbal Jelly can be used for daily skin care and moisturizing.", "Apply a small amount to clean skin, focusing on dry areas. Use as needed for everyday skin care and always follow the product label instructions.", "alvi-herbal-jelly", "products/alvi-herbal-jelly.jpeg", False),
    ("training", "Beauty & Personal Care", "How to Use ALVI Body Lotion – Avocado Oil & Aloe Vera", "A customer guide for using ALVI Body Lotion for everyday skin care.", "Apply the lotion after bathing or whenever skin feels dry. Use it as part of a daily routine to help keep skin moisturized, following the product label instructions.", "alvi-body-lotion-avocado-oil-aloe-vera", "products/alvi-body-lotion.jpeg", False),
    ("training", "Hair Care", "How to Use ALVI Avocado Hair Growing Oil", "A simple guide for applying ALVI Avocado Hair Growing Oil as part of a hair and scalp care routine.", "Apply a small amount to the scalp or hair and massage gently. Use regularly as part of your routine, avoid overuse, and follow the product label instructions.", "alvi-avocado-hair-growing-oil", "products/alvi-avocado-hair-growing-oil.jpeg", False),
    ("training", "Food & Nutrition", "How to Use ALVI Extra Virgin Avocado Oil", "Learn common kitchen uses for ALVI Extra Virgin Avocado Oil.", "Use avocado oil for cooking, dressing, drizzling, roasting, frying, or baking as appropriate for your recipe. Store it safely in the kitchen and follow the product label instructions.", "alvi-extra-virgin-avocado-oil-cold-pressed", "products/alvi-extra-virgin-avocado-oil.jpeg", False),
    ("training", "Home Care", "How to Use ALVI Multipurpose Liquid Detergent", "A simple home-care guide for using ALVI Multipurpose Liquid Detergent.", "Use the correct quantity for the cleaning task and follow the label safety instructions. Keep the product away from children and store it properly after use.", "alvi-multipurpose-liquid-detergent-1l", "products/alvi-multipurpose-liquid-detergent-1l.jpeg", False),
    ("blog", "Product Education", "Why Natural Ingredients Matter in Everyday Care", "DICHO Ltd shares why natural ingredients are important in ALVI product development.", "Everyday care starts with understanding customer needs and handling products with care. DICHO Ltd draws inspiration from plant-based ingredients while focusing on quality handling and safe everyday product use. Customers should always select products that fit their needs and follow the product label.", None, "products/alvi-body-lotion.jpeg", True),
    ("blog", "Product Education", "From Natural Sources to ALVI Products", "A look at avocado, aloe vera, calendula, and other natural inspirations behind ALVI products.", "Avocado, aloe vera, and calendula are natural inspirations behind selected ALVI products. DICHO Ltd values natural sourcing and quality handling as ingredients move toward finished products for everyday care. This does not imply ownership of farms or plantations.", None, "products/fresh-avocado.svg", False),
    ("blog", "Product Education", "Choosing the Right ALVI Product for Your Daily Routine", "A simple guide to help customers choose ALVI products by need.", "Consider your everyday need when selecting ALVI products: beauty care, hair care, home care, ALVI avocado oil, nuts, or dried products. Review the product label and description, then contact DICHO Ltd if you need additional customer guidance.", None, "products/alvi-aloe-vera-hydrating-gel.jpeg", False),
    ("news", "Company News", "DICHO Ltd Introduces ALVI Natural Products Online", "DICHO Ltd is making ALVI products easier to discover and order through its online platform.", "The DICHO Ltd website brings ALVI product categories, customer ordering, and WhatsApp support together in one place. Customers can explore products, add items to the cart, and contact the team for guidance.", None, "products/alvi-extra-virgin-avocado-oil.jpeg", True),
    ("news", "Company News", "DICHO Ltd Expands Product Visibility Through Digital Platform", "The new website supports product visibility, customer communication, and online ordering.", "The digital platform helps customers discover ALVI products, communicate with DICHO Ltd, and place orders online. It supports product visibility and convenient customer access as the business grows.", None, "products/alvi-multipurpose-liquid-detergent-1l.jpeg", False),
]


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


def ensure_content_image(command, source_relative_path, filename):
    """Copy a repository image to the editable content media directory."""
    source = Path(settings.BASE_DIR) / "images" / source_relative_path
    destination = Path(settings.MEDIA_ROOT) / "content" / filename
    if not source.is_file():
        command.stdout.write(command.style.WARNING(f"Content image source missing: {source}"))
        return ""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists() or source.stat().st_mtime_ns > destination.stat().st_mtime_ns:
        copy2(source, destination)
    return f"content/{filename}"


class Command(BaseCommand):
    help = "Create or update DICHO and ALVI product data without duplicating records."

    def handle(self, *args, **options):
        social_defaults = {"facebook_url": "https://www.facebook.com/reel/1756488252150114/?app=fbl", "instagram_url": "https://www.instagram.com/alvi001270?igsi=MWQzOWljem52dzJmZw==", "tiktok_url": "https://vm.tiktok.com/ZS9BMxLMNBPSc-LSU9C/", "youtube_url": "", "x_url": "", "linkedin_url": ""}
        site, _ = SiteSetting.objects.get_or_create(company_name="DICHO Ltd", defaults={"tagline": "Home of ALVI Natural Products", "phone": "0788428711 / 0783285278", "email": "info@dicho.rw", "whatsapp_number": "0788428711", "whatsapp_url": "https://wa.me/250788428711", "address": "Huye, Rwanda", "working_hours": "Mon - Sat: 8:00 AM - 6:00 PM", **social_defaults})
        SiteSetting.objects.filter(pk=site.pk).update(phone="0788428711 / 0783285278", whatsapp_number="0788428711", whatsapp_url="https://wa.me/250788428711", address="Huye, Rwanda", **social_defaults)
        site.refresh_from_db(fields=["phone", "whatsapp_number", "whatsapp_url", "address", *social_defaults.keys()])
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
        Product.objects.filter(Q(name__icontains="olive") | Q(name__icontains="sunflower")).update(is_active=False, is_featured=False, is_best_seller=False, is_new=False)
        for index, data in enumerate(REAL_PRODUCTS):
            product_image = data["image"] if ensure_media_file(self, data["image"]) else ""
            defaults = {"name": data["name"], "category": categories[data["category"]], "short_description": data["short_description"], "description": data["description"], "benefits": data["benefits"], "ingredients": data["ingredients"], "usage_instruction": data["usage"], "size": data["size"], "price": data["price"], "old_price": None, "image": product_image, "asset_path": "", "is_active": True, "is_featured": True, "is_new": index < 7, "is_best_seller": index in (3, 6, 10), "is_on_sale": False}
            product, created = Product.objects.update_or_create(slug=slugify(data["name"]), defaults=defaults)
            if created:
                product.stock_quantity = 50; product.save(update_fields=["stock_quantity"])
        content_categories = {}
        for order, (name, description) in enumerate(CONTENT_CATEGORIES, 1):
            category, _ = ContentCategory.objects.update_or_create(slug=slugify(name), defaults={"name": name, "description": description, "display_order": order, "is_active": True})
            content_categories[name] = category
        for order, (post_type, category_name, title, excerpt, content, product_slug, image_source, is_featured) in enumerate(CONTENT_POSTS, 1):
            slug = slugify(title)
            image_name = f"{slug}{Path(image_source).suffix}"
            image_path = ensure_content_image(self, image_source, image_name)
            related_product = Product.objects.filter(slug=product_slug).first() if product_slug else None
            ContentPost.objects.update_or_create(slug=slug, defaults={"post_type": post_type, "title": title, "category": content_categories[category_name], "excerpt": excerpt, "content": content, "featured_image": image_path, "related_product": related_product, "author_name": "DICHO Ltd", "is_featured": is_featured, "is_published": True, "published_at": timezone.now(), "meta_title": f"{title} | DICHO Ltd", "meta_description": excerpt})
        for order, (question, answer) in enumerate([("How can I place an order?", "Use the shop page, cart and checkout, or contact us on WhatsApp."), ("Do you offer delivery across Rwanda?", "Delivery details are confirmed by the DICHO team after checkout."), ("How can I become a distributor?", "Send a wholesale or partnership inquiry through the contact form.")], 1): FAQ.objects.get_or_create(question=question, defaults={"answer": answer, "display_order": order})
        for order, (name, location, message) in enumerate([("Aline M.", "Kigali", "Natural products I can trust for my family."), ("David K.", "Rwanda", "Reliable quality and friendly customer service.")], 1): Testimonial.objects.get_or_create(name=name, defaults={"location": location, "message": message, "display_order": order})
        self.stdout.write(self.style.SUCCESS("DICHO and ALVI seed data is ready."))
