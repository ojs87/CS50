from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("owen", views.owen, name="owen"),
    path("brian", views.brian, name="brian"),
    path("<str:name>", views.greet, name="greet")
]
