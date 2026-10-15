from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.file import Archivo


class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, file_id: int) -> Optional[Archivo]:
        return self.db.query(Archivo).filter(Archivo.id == file_id).first()

    def get_by_hash(self, post_id: int, hash_sha256: str) -> Optional[Archivo]:
        return (
            self.db.query(Archivo)
            .filter(Archivo.post_id == post_id, Archivo.hash_sha256 == hash_sha256)
            .first()
        )

    def list_by_post(self, post_id: int) -> List[Archivo]:
        return (
            self.db.query(Archivo)
            .filter(Archivo.post_id == post_id)
            .order_by(Archivo.uploaded_at.desc())
            .all()
        )

    def list_all(self, limit: int = 100) -> List[Archivo]:
        return (
            self.db.query(Archivo)
            .order_by(Archivo.uploaded_at.desc())
            .limit(limit)
            .all()
        )

    def create(
        self,
        post_id: int,
        nombre_original: str,
        ruta: str,
        extension: str,
        tamano_bytes: int,
        hash_sha256: str,
        mime_type: Optional[str] = None,
    ) -> Archivo:
        archivo = Archivo(
            post_id=post_id,
            nombre_original=nombre_original,
            ruta=ruta,
            extension=extension,
            mime_type=mime_type,
            tamano_bytes=tamano_bytes,
            hash_sha256=hash_sha256,
        )
        self.db.add(archivo)
        self.db.commit()
        self.db.refresh(archivo)
        return archivo

    def increment_downloads(self, file_id: int) -> None:
        self.db.query(Archivo).filter(Archivo.id == file_id).update(
            {Archivo.descargas: Archivo.descargas + 1}, synchronize_session=False
        )
        self.db.commit()

    def delete(self, archivo: Archivo) -> None:
        self.db.delete(archivo)
        self.db.commit()
