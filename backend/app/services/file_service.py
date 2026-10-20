import os
import uuid
import hashlib
import mimetypes
from typing import List, Optional
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from PIL import Image

from app.core.config import settings
from app.models.file import Archivo
from app.models.post import Post
from app.models.user import User
from app.repositories.file_repo import FileRepository
from app.repositories.post_repo import PostRepository


class FileService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = FileRepository(db)
        self.post_repo = PostRepository(db)

    async def save_post_files(
        self,
        post_id: int,
        files: List[UploadFile],
        current_user: User,
    ) -> List[Archivo]:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Publicación no encontrada",
            )

        # Autorización: creador del post o admin
        if post.autor_id != current_user.id and current_user.rol != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para subir archivos a esta publicación",
            )

        saved_records = []
        post_dir = os.path.join(settings.UPLOAD_DIR, str(post_id))
        os.makedirs(post_dir, exist_ok=True)

        for upload in files:
            original_filename = upload.filename or "archivo_desconocido"
            ext = os.path.splitext(original_filename)[1].lower().replace(".", "")

            # 1. Validar extensión permitida
            if ext not in settings.allowed_extensions_set:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Extensión .{ext} no permitida. Formatos válidos: {settings.ALLOWED_EXTENSIONS}",
                )

            # 2. Leer chunks, calcular SHA-256 y validar tamaño
            sha256_hash = hashlib.sha256()
            total_size = 0
            chunks = []

            while True:
                chunk = await upload.read(8192) # 8KB
                if not chunk:
                    break
                total_size += len(chunk)
                if total_size > settings.max_file_bytes:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"El archivo '{original_filename}' supera el límite permitido de {settings.MAX_FILE_MB}MB",
                    )
                sha256_hash.update(chunk)
                chunks.append(chunk)

            file_hash = sha256_hash.hexdigest()

            # 3. Validar no-duplicado en la misma publicación
            existing = self.repo.get_by_hash(post_id, file_hash)
            if existing:
                # Si ya existe exactamente el mismo archivo en el post, lo retornamos o ignoramos duplicado
                saved_records.append(existing)
                continue

            # 4. Guardar archivo en disco
            safe_id = uuid.uuid4().hex[:12]
            stored_filename = f"{safe_id}_{original_filename.replace(' ', '_')}"
            stored_path = os.path.join(post_dir, stored_filename)

            with open(stored_path, "wb") as f:
                for c in chunks:
                    f.write(c)

            # 5. Detección MIME
            detected_mime = upload.content_type
            if not detected_mime or detected_mime == "application/octet-stream":
                guess, _ = mimetypes.guess_type(original_filename)
                detected_mime = guess or "application/octet-stream"

            # 6. Generar thumbnail si es imagen compatible
            if ext in ("png", "jpg", "jpeg", "webp"):
                try:
                    thumb_path = os.path.join(post_dir, f"thumb_{stored_filename}")
                    with Image.open(stored_path) as img:
                        img.thumbnail((400, 400))
                        img.save(thumb_path)
                except Exception:
                    pass # Thumbnail opcional si Pillow encuentra formato especial

            # 7. Insertar en base de datos
            archivo = self.repo.create(
                post_id=post_id,
                usuario_id=current_user.id,
                nombre_original=original_filename,
                ruta=stored_path,
                extension=ext,
                tamano_bytes=total_size,
                hash_sha256=file_hash,
                mime_type=detected_mime,
            )
            saved_records.append(archivo)

        return saved_records

    async def save_inline_file(
        self,
        upload: UploadFile,
        current_user: User,
    ) -> Archivo:
        original_filename = upload.filename or "archivo_adjunto"
        ext = os.path.splitext(original_filename)[1].lower().replace(".", "")

        # 1. Validar extensión permitida
        if ext not in settings.allowed_extensions_set:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Extensión .{ext} no permitida. Formatos válidos: {settings.ALLOWED_EXTENSIONS}",
            )

        # 2. Leer chunks, calcular SHA-256 y validar tamaño
        sha256_hash = hashlib.sha256()
        total_size = 0
        chunks = []

        while True:
            chunk = await upload.read(8192)
            if not chunk:
                break
            total_size += len(chunk)
            if total_size > settings.max_file_bytes:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"El archivo '{original_filename}' supera el límite permitido de {settings.MAX_FILE_MB}MB",
                )
            sha256_hash.update(chunk)
            chunks.append(chunk)

        file_hash = sha256_hash.hexdigest()

        # 3. Guardar archivo en disco
        media_dir = os.path.join(settings.UPLOAD_DIR, "inline", str(current_user.id))
        os.makedirs(media_dir, exist_ok=True)

        safe_id = uuid.uuid4().hex[:12]
        clean_name = "".join(c for c in original_filename if c.isalnum() or c in "._- ")
        stored_filename = f"{safe_id}_{clean_name.replace(' ', '_')}"
        stored_path = os.path.join(media_dir, stored_filename)

        with open(stored_path, "wb") as f:
            for c in chunks:
                f.write(c)

        # 4. Detección MIME
        detected_mime = upload.content_type
        if not detected_mime or detected_mime == "application/octet-stream":
            guess, _ = mimetypes.guess_type(original_filename)
            detected_mime = guess or "application/octet-stream"

        # 5. Insertar registro en BD
        archivo = self.repo.create(
            post_id=None,
            usuario_id=current_user.id,
            nombre_original=original_filename,
            ruta=stored_path,
            extension=ext,
            tamano_bytes=total_size,
            hash_sha256=file_hash,
            mime_type=detected_mime,
        )
        return archivo

    def associate_files_to_post(
        self,
        post_id: int,
        file_ids: List[int],
        current_user: User,
    ) -> None:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Publicación no encontrada",
            )
        if post.autor_id != current_user.id and current_user.rol != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para asociar archivos a esta publicación",
            )
        self.repo.associate_files_to_post(file_ids, post_id)

    def get_file_record(self, file_id: int) -> Archivo:
        archivo = self.repo.get_by_id(file_id)
        if not archivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Archivo no encontrado",
            )
        return archivo

    def register_download(self, file_id: int) -> Archivo:
        archivo = self.get_file_record(file_id)
        if not os.path.exists(archivo.ruta):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El archivo físico no se encuentra en el servidor",
            )
        self.repo.increment_downloads(file_id)
        archivo.descargas += 1
        return archivo

    def delete_file(self, file_id: int, current_user: User) -> None:
        archivo = self.get_file_record(file_id)
        post = self.post_repo.get_by_id(archivo.post_id) if archivo.post_id else None

        is_owner = (archivo.usuario_id == current_user.id) or (post and post.autor_id == current_user.id)
        if current_user.rol != "admin" and not is_owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar este archivo",
            )

        # Borrar físico si existe
        if os.path.exists(archivo.ruta):
            try:
                os.remove(archivo.ruta)
            except OSError:
                pass

        self.repo.delete(archivo)
