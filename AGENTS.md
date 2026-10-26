
# Reglas de trabajo del proyecto instituto

## 1. Organización de archivos

- Mantener limpia la raíz del proyecto Django.
- No crear scripts auxiliares de restauración en la raíz.
- No guardar PNG, JPG, WEBP ni imágenes de prueba en la raíz.
- Conservar manage.py en su ubicación original.
- No crear carpetas innecesarias.

## 2. Restauraciones fotográficas

- Guardar las nuevas imágenes de trabajo en:
  archivo_restauraciones/nuevas/
- Si es necesario crear scripts auxiliares, guardarlos en:
  archivo_restauraciones/nuevas/scripts/
- Crear estas subcarpetas únicamente cuando sean necesarias.
- No ejecutar los scripts antiguos archivados sin revisar sus rutas.
- No sobrescribir restauraciones existentes sin autorización.
- En retratos, conservar exactamente los rasgos faciales, proporciones, mirada, expresión y pose originales. No inventar detalles faciales.

## 3. Archivos protegidos

No modificar, mover ni eliminar sin autorización expresa:

- media/
- album_publicado/
- db.sqlite3
- Configuración de Django y Railway

## 4. Seguridad

- Antes de modificar archivos, identificar los afectados.
- Preferir cambios mínimos y reversibles.
- No realizar git push, despliegues o migraciones sin autorización.
- No eliminar fotografías ni scripts sin permiso.
- Comprobar el funcionamiento de Django después de modificaciones relevantes.
