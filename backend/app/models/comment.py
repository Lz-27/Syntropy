from datetime import datetime, timezone
from sqlalchemy import Text, Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ReaccionComentario(Base):
    __tablename__ = "reacciones_comentarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    comentario_id: Mapped[int] = mapped_column(ForeignKey("comentarios.id", ondelete="CASCADE"), index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), index=True)
    tipo: Mapped[str] = mapped_column(String(50), index=True)  # aporte_valioso | duda | excelente_analisis
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    # Restricción: un usuario solo puede tener una reacción del mismo tipo o una única reacción por comentario
    __table_args__ = (
        UniqueConstraint("comentario_id", "usuario_id", name="uq_usuario_reaccion_comentario"),
    )

    comentario: Mapped["Comentario"] = relationship(back_populates="reacciones")
    usuario: Mapped["User"] = relationship()


class Comentario(Base):
    __tablename__ = "comentarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    padre_id: Mapped[int | None] = mapped_column(ForeignKey("comentarios.id"), nullable=True, index=True)
    contenido: Mapped[str] = mapped_column(Text)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    post: Mapped["Post"] = relationship(back_populates="comentarios")
    usuario: Mapped["User"] = relationship(back_populates="comentarios")
    padre: Mapped["Comentario | None"] = relationship(
        "Comentario",
        remote_side="Comentario.id",
        foreign_keys=[padre_id],
        back_populates="respuestas",
    )
    respuestas: Mapped[list["Comentario"]] = relationship(
        "Comentario",
        foreign_keys=[padre_id],
        back_populates="padre",
        lazy="select",
    )
    reacciones: Mapped[list["ReaccionComentario"]] = relationship(
        "ReaccionComentario",
        back_populates="comentario",
        cascade="all, delete-orphan",
        lazy="select",
    )

