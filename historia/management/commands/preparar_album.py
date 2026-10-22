import json
from pathlib import Path
from django.conf import settings
from django.core import serializers
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from historia.models import Alumno, FotoAlumno


class Command(BaseCommand):
    help = "Prepara el álbum local para GitHub o lo instala durante el despliegue."

    def add_arguments(self, parser):
        parser.add_argument("--instalar", action="store_true")

    def handle(self, *args, **options):
        folder = Path(settings.BASE_DIR) / "album_publicado"
        manifest = folder / "album.json"
        if options["instalar"]:
            if not manifest.exists():
                self.stdout.write("No hay álbum preparado; se conserva el existente.")
                return
            data = manifest.read_text(encoding="utf-8")
            records = json.loads(data)
            for record in records:
                for field in ("foto_instituto", "foto_actual", "imagen"):
                    name = record["fields"].get(field)
                    if not name:
                        continue
                    source = (folder / "fotos" / name).resolve()
                    if not source.is_relative_to((folder / "fotos").resolve()) or not source.is_file():
                        raise CommandError(f"Fotografía no disponible: {name}")
                    with source.open("rb") as uploaded:
                        if default_storage.exists(name):
                            default_storage.delete(name)
                        saved = default_storage.save(name, File(uploaded))
                    if saved != name:
                        raise CommandError(f"No se pudo instalar la fotografía: {name}")
            with transaction.atomic():
                for obj in serializers.deserialize("json", data):
                    obj.save()
            self.stdout.write(self.style.SUCCESS("Álbum instalado."))
        else:
            alumnos = list(Alumno.objects.all())
            fotos = list(FotoAlumno.objects.all())
            files = [photo for alumno in alumnos for photo in (alumno.foto_instituto, alumno.foto_actual) if photo]
            files += [foto.imagen for foto in fotos if foto.imagen]
            for photo in files:
                target = (folder / "fotos" / photo.name).resolve()
                if not target.is_relative_to((folder / "fotos").resolve()):
                    raise CommandError("Ruta de fotografía no válida.")
                target.parent.mkdir(parents=True, exist_ok=True)
                with photo.open("rb") as source, target.open("wb") as output:
                    for chunk in source.chunks():
                        output.write(chunk)
            folder.mkdir(parents=True, exist_ok=True)
            manifest.write_text(serializers.serialize("json", alumnos + fotos, indent=2), encoding="utf-8")
            self.stdout.write(self.style.SUCCESS("Álbum preparado en album_publicado. Incluye esta carpeta al actualizar GitHub."))
