from django.db import models


class SiteSetting(models.Model):
    company_name = models.CharField(max_length=100, default="DICHO Ltd")
    tagline = models.CharField(max_length=150, default="Natural • Quality • Trusted")
    phone = models.CharField(max_length=50, default="+250 788 123 456")
    email = models.EmailField(default="info@dicho.rw")
    whatsapp_number = models.CharField(max_length=30, default="250788123456")
    address = models.CharField(max_length=255, default="Kigali, Rwanda")
    working_hours = models.CharField(max_length=255, default="Mon - Sat: 8:00 AM - 6:00 PM")
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="site/", blank=True)
    favicon = models.ImageField(upload_to="site/", blank=True)

    def __str__(self): return self.company_name


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    image = models.ImageField(upload_to="testimonials/", blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ["display_order", "name"]
    def __str__(self): return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ["display_order", "question"]
    def __str__(self): return self.question
