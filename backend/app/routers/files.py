import os
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, status, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.audit import AuditoriaLog
from app.schemas.file import ArchivoOut
from app.services.file_service import FileService

router = APIRouter(tags=["files"])


def _log(db: Session, accion: str, usuario_id=None, entidad_id=None, ip=None, detalle=None):
    db.add(
        AuditoriaLog(
            accion=accion,
            usuario_id=usuario_id,
            entidad="archivo",
            entidad_id=entidad_id,
            ip=ip,
            detalle=detalle,
        )
    )
    db.commit()


@router.post("/posts/{post_id}/files", response_model=List[ArchivoOut], status_code=status.HTTP_201_CREATED)
async def upload_files_to_post(
    post_id: int,
    request: Request,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Sube uno o múltiples archivos a una publicación existente con validación SHA-256."""
    service = FileService(db)
    archivos = await service.save_post_files(post_id, files, current_user)
    ip = request.client.host if request.client else None
    for a in archivos:
        _log(
            db,
            "upload_file",
            usuario_id=current_user.id,
            entidad_id=a.id,
            ip=ip,
            detalle=f"{a.nombre_original} ({a.tamano_bytes} bytes, hash: {a.hash_sha256[:8]}...)",
        )
    return archivos


@router.get("/files/{file_id}", response_model=ArchivoOut)
def get_file_metadata(file_id: int, db: Session = Depends(get_db)):
    """Obtiene los metadatos de un archivo (nombre, tamaño, tipo, hash SHA-256)."""
    service = FileService(db)
    return service.get_file_record(file_id)


@router.get("/files/{file_id}/preview")
def preview_file(file_id: int, db: Session = Depends(get_db)):
    """Transmite el archivo para previsualización directa en el navegador (Content-Disposition: inline)."""
    service = FileService(db)
    archivo = service.get_file_record(file_id)
    if not os.path.exists(archivo.ruta):
        return FileResponse(path="", status_code=status.HTTP_404_NOT_FOUND)

    headers = {"Content-Disposition": f'inline; filename="{archivo.nombre_original}"'}
    return FileResponse(
        path=archivo.ruta,
        media_type=archivo.mime_type or "application/octet-stream",
        headers=headers,
    )


@router.get("/files/{file_id}/download")
def download_file(file_id: int, request: Request, db: Session = Depends(get_db)):
    """Descarga el archivo adjunto (Content-Disposition: attachment) e incrementa el contador de descargas."""
    service = FileService(db)
    archivo = service.register_download(file_id)
    ip = request.client.host if request.client else None
    _log(db, "download_file", entidad_id=archivo.id, ip=ip, detalle=archivo.nombre_original)

    return FileResponse(
        path=archivo.ruta,
        media_type=archivo.mime_type or "application/octet-stream",
        filename=archivo.nombre_original,
    )


@router.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Elimina un archivo adjunto (solo el autor de la publicación o admin)."""
    service = FileService(db)
    service.delete_file(file_id, current_user)
    ip = request.client.host if request.client else None
    _log(db, "delete_file", usuario_id=current_user.id, entidad_id=file_id, ip=ip)
    return None
