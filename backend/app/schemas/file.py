from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ArchivoOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    post_id: int
    nombre_original: str
    extension: str
    mime_type: Optional[str] = None
    tamano_bytes: int
    hash_sha256: Optional[str] = None
    descargas: int
    uploaded_at: datetime
