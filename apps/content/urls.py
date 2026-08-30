from django.urls import path

from . import views


urlpatterns = [
    path("trainings/", views.trainings, name="trainings"),
    path("trainings/<slug:slug>/", views.training_detail, name="training_detail"),
    path("press-room/", views.press_room, name="press_room"),
    path("press-room/<slug:slug>/", views.press_post_detail, name="press_post_detail"),
]

