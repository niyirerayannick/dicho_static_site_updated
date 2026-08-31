from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("natural-sources/", views.natural_sources, name="natural_sources"),
    path("natural-sources/<slug:slug>/", views.natural_source_detail, name="natural_source_detail"),
]
