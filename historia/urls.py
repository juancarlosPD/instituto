from django.urls import path

from historia import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("fotos/<int:pk>/<str:epoca>/", views.foto_alumno, name="foto_alumno"),
]
