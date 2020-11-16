from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("createnewpage.html", views.newpage, name="newpage"),
    path("wiki/<str:name>/edit", views.editpage, name="editpage"),
    path("wiki/", views.randompage, name="randompage")
]
