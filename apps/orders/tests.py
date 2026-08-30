from urllib.parse import unquote

from django.test import TestCase
from django.urls import reverse

from apps.catalog.models import Category, Product
from apps.core.models import SiteSetting


class CheckoutWhatsAppFlowTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Wellness",
            slug="wellness",
            description="Wellness products",
        )
        self.product = Product.objects.create(
            category=self.category,
            name="ALVI Herbal Mix",
            slug="alvi-herbal-mix",
            short_description="Supports wellness",
            description="Wellness daily blend",
            size="250g",
            price="12000.00",
            stock_quantity=10,
        )
        SiteSetting.objects.create(
            company_name="DICHO Ltd",
            whatsapp_url="https://wa.me/250788428711",
        )

    def test_checkout_saves_order_and_success_page_has_whatsapp_cta(self):
        session = self.client.session
        session["dicho_cart"] = {str(self.product.pk): {"quantity": 2}}
        session.save()

        response = self.client.post(
            reverse("checkout"),
            {
                "full_name": "Alice Example",
                "email": "alice@example.com",
                "phone": "0788428711",
                "delivery_location": "Huye, Rwanda",
                "payment_method": "cash_on_delivery",
                "order_notes": "Please deliver before 5pm.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("order-success", response.url)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 8)

        order = self.client.session.get("dicho_cart")
        self.assertIsNone(order)

        success_response = self.client.get(response.url)
        content = success_response.content.decode("utf-8")
        self.assertContains(success_response, "Send Order on WhatsApp")
        self.assertIn("https://wa.me/250788428711", content)
        self.assertIn("ALVI Herbal Mix", content)
        self.assertIn("http://testserver/product/alvi-herbal-mix/", unquote(content))
