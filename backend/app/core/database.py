from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings

# SQLite: connect_args solo aplica a SQLite
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,  # True para debug SQL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency — yields a DB session and closes it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def migrate_archivos_schema():
    from sqlalchemy import text
    with engine.connect() as conn:
        try:
            result = conn.execute(text("PRAGMA table_info(archivos)")).fetchall()
            if not result:
                return
            cols = {row[1]: row for row in result}
            needs_migration = "usuario_id" not in cols or (cols.get("post_id") and cols["post_id"][3] == 1)
            if needs_migration:
                conn.execute(text("PRAGMA foreign_keys=OFF;"))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS archivos_new (
                        id INTEGER PRIMARY KEY,
                        post_id INTEGER,
                        usuario_id INTEGER,
                        nombre_original VARCHAR(500) NOT NULL,
                        ruta VARCHAR(1000) NOT NULL,
                        extension VARCHAR(20) NOT NULL,
                        mime_type VARCHAR(100),
                        tamano_bytes BIGINT DEFAULT 0 NOT NULL,
                        hash_sha256 VARCHAR(64),
                        descargas INTEGER DEFAULT 0 NOT NULL,
                        uploaded_at DATETIME NOT NULL,
                        FOREIGN KEY(post_id) REFERENCES posts (id),
                        FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
                    );
                """))
                if "usuario_id" in cols:
                    conn.execute(text("""
                        INSERT INTO archivos_new (id, post_id, usuario_id, nombre_original, ruta, extension, mime_type, tamano_bytes, hash_sha256, descargas, uploaded_at)
                        SELECT id, post_id, usuario_id, nombre_original, ruta, extension, mime_type, tamano_bytes, hash_sha256, descargas, uploaded_at FROM archivos;
                    """))
                else:
                    conn.execute(text("""
                        INSERT INTO archivos_new (id, post_id, usuario_id, nombre_original, ruta, extension, mime_type, tamano_bytes, hash_sha256, descargas, uploaded_at)
                        SELECT id, post_id, NULL, nombre_original, ruta, extension, mime_type, tamano_bytes, hash_sha256, descargas, uploaded_at FROM archivos;
                    """))
                conn.execute(text("DROP TABLE archivos;"))
                conn.execute(text("ALTER TABLE archivos_new RENAME TO archivos;"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_archivos_id ON archivos (id);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_archivos_post_id ON archivos (post_id);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_archivos_usuario_id ON archivos (usuario_id);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_archivos_hash_sha256 ON archivos (hash_sha256);"))
                conn.execute(text("PRAGMA foreign_keys=ON;"))
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Notice: migration check: {e}")


def create_tables():
    """Crea todas las tablas definidas en los modelos ORM."""
    # Importar modelos para que SQLAlchemy los registre en Base.metadata
    from app.models import user, post, file, comment, audit  # noqa: F401
    Base.metadata.create_all(bind=engine)
    migrate_archivos_schema()
