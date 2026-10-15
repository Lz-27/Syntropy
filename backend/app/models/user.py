from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    codigo_estudiante: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    nombre_completo: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    rol: Mapped[str] = mapped_column(String(20), default="estudiante")  # admin | estudiante
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    posts: Mapped[list["Post"]] = relationship(back_populates="autor", lazy="select")
    comentarios: Mapped[list["Comentario"]] = relationship(back_populates="usuario", lazy="select")
    auditoria_logs: Mapped[list["AuditoriaLog"]] = relationship(back_populates="usuario", lazy="select")
