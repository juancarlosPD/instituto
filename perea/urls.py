from django.urls import include, path

urlpatterns = [
    path("", include("historia.urls")),
]
