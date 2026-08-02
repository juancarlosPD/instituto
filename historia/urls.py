from django.urls import path

from historia import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
]
