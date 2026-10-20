from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Archivo(Base):
    __tablename__ = "archivos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int | None] = mapped_column(ForeignKey("posts.id"), nullable=True, index=True)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True, index=True)
    nombre_original: Mapped[str] = mapped_column(String(500))
    ruta: Mapped[str] = mapped_column(String(1000))
    extension: Mapped[str] = mapped_column(String(20))
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tamano_bytes: Mapped[int] = mapped_column(BigInteger, default=0)
    hash_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    descargas: Mapped[int] = mapped_column(Integer, default=0)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    post: Mapped[Optional["Post"]] = relationship(back_populates="archivos")
    usuario: Mapped[Optional["User"]] = relationship(lazy="select")
