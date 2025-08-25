from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- Chat Schemas ---

class ChatConversacionBase(BaseModel):
    pass # Usually created implicitly

class ChatConversacionCreate(ChatConversacionBase):
    inquilino_id: int
    participante_ids: List[int]

class ChatMensajeBase(BaseModel):
    contenido: str

class ChatMensajeCreate(ChatMensajeBase):
    conversacion_id: int
    remitente_usuario_id: int

# --- Foro Schemas ---

class ForoClaseBase(BaseModel):
    nombre_foro: str

class ForoClaseCreate(ForoClaseBase):
    clase_id: int
    inquilino_id: int

class ForoHiloBase(BaseModel):
    titulo: str

class ForoHiloCreate(ForoHiloBase):
    foro_id: int
    creado_por_usuario_id: int

class ForoPublicacionBase(BaseModel):
    contenido: str
    responde_a_id: Optional[int] = None

class ForoPublicacionCreate(ForoPublicacionBase):
    hilo_id: int
    usuario_id: int
