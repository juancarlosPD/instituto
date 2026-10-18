from django.test import TestCase

from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

from .models import Alumno


class AlbumTests(TestCase):
    def test_empty_album_and_pending_photos(self):
        self.assertContains(self.client.get(reverse("inicio")), "Pronto empezaremos")
        Alumno.objects.create(nombre="Ana García")
        response = self.client.get(reverse("inicio"))
        self.assertContains(response, "Ana García")
        self.assertContains(response, "Fotografía pendiente", count=2)

    def test_admin_uploads_both_photos_and_home_displays_them(self):
        user = get_user_model().objects.create_superuser(
            username="administrador", password="solo-para-pruebas"
        )
        self.client.force_login(user)
        buffer = BytesIO()
        Image.new("RGB", (30, 40), "green").save(buffer, format="PNG")
        with override_settings(STORAGES={
            "default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
            "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
        }):
            with override_settings():
                response = self.client.post(reverse("admin:historia_alumno_add"), {
                    "nombre": "Ana García",
                    "foto_instituto": SimpleUploadedFile("antes.png", buffer.getvalue(), content_type="image/png"),
                    "foto_actual": SimpleUploadedFile("ahora.png", buffer.getvalue(), content_type="image/png"),
                    "_save": "Guardar",
                })
                self.assertEqual(response.status_code, 302)
                alumno = Alumno.objects.get()
                self.assertTrue(alumno.foto_instituto.storage.exists(alumno.foto_instituto.name))
                self.assertTrue(alumno.foto_actual.storage.exists(alumno.foto_actual.name))
                self.client.logout()
                response = self.client.get(reverse("inicio"))
                for epoca in ("instituto", "actualidad"):
                    url = reverse("foto_alumno", args=[alumno.pk, epoca])
                    self.assertContains(response, url)
                    foto_response = self.client.get(url)
                    self.assertEqual(foto_response.status_code, 200)
                    self.assertEqual(b"".join(foto_response.streaming_content), buffer.getvalue())
                self.assertNotContains(response, "Fotografía pendiente")

    def test_missing_photo_returns_404(self):
        alumno = Alumno.objects.create(nombre="Ana García")
        self.assertEqual(self.client.get(reverse("foto_alumno", args=[alumno.pk, "instituto"])).status_code, 404)

# Create your tests here.
