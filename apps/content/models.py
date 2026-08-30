from django.db import models
from django.urls import reverse

from apps.catalog.models import Product


class ContentCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("display_order", "name")
        verbose_name_plural = "content categories"

    def __str__(self):
        return self.name


class ContentPost(models.Model):
    class PostType(models.TextChoices):
        TRAINING = "training", "Training"
        NEWS = "news", "News"
        BLOG = "blog", "Blog"

    post_type = models.CharField(max_length=12, choices=PostType.choices)
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ContentCategory, on_delete=models.PROTECT, related_name="posts")
    excerpt = models.TextField()
    content = models.TextField()
    featured_image = models.ImageField(upload_to="content/", blank=True)
    related_product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name="content_posts", blank=True, null=True)
    author_name = models.CharField(max_length=120, default="DICHO Ltd")
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=320, blank=True)

    class Meta:
        ordering = ("-published_at", "-created_at")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.post_type == self.PostType.TRAINING:
            return reverse("training_detail", args=[self.slug])
        return reverse("press_post_detail", args=[self.slug])

