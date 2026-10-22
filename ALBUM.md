# Publicar las fotos desde el ordenador

1. Añade compañeros y fotografías desde la administración local.
2. Abre `Preparar album para GitHub.bat` y espera el mensaje de éxito.
3. Incluye `album_publicado`, junto con los cambios del proyecto, al actualizar GitHub.
4. El despliegue de Railway instala los nombres y las fotos automáticamente.

La carpeta preparada contiene solo datos del álbum y fotografías; no incluye usuarios ni contraseñas. Las fotos estarán en el repositorio: utiliza un repositorio privado si no quieres que se puedan consultar en GitHub.

El álbum local es la referencia para los registros publicados. Los cambios hechos en Railway sobre esos registros se reemplazan al desplegar. Los registros que solo existen en Railway no se eliminan automáticamente.

No subas `db.sqlite3`, `media`, `.env` ni el entorno virtual. Si no has preparado un álbum, el despliegue conserva el existente.
