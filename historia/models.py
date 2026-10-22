from django.db import models


class Alumno(models.Model):
    nombre = models.CharField("nombre y apellidos", max_length=200)
    foto_instituto = models.ImageField(
        "foto en el instituto", upload_to="alumnos/instituto/", blank=True
    )
    foto_actual = models.ImageField(
        "foto actual", upload_to="alumnos/actualidad/", blank=True
    )

    class Meta:
        ordering = ["nombre", "pk"]
        verbose_name = "compañero"
        verbose_name_plural = "compañeros"

    def __str__(self):
        return self.nombre


class FotoAlumno(models.Model):
    alumno = models.ForeignKey(Alumno, related_name="fotos", on_delete=models.CASCADE)
    imagen = models.ImageField("fotografía", upload_to="alumnos/galeria/")
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "pk"]
        verbose_name = "fotografía adicional"
        verbose_name_plural = "fotografías adicionales"
