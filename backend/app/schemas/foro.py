from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum
from datetime import datetime
from typing import Optional
from fastapi import UploadFile


class Rama(str, Enum):
    """Ramas disponibles"""
    CAMINANTES = "Caminantes"
    ROVERS = "Rovers"
    DIRIGENTE_JOVEN = "Dirigente Joven"
    DIRIGENTE = "Dirigente"


class ForoParticipantBase(BaseModel):
    """Schema base de participante"""
    full_name: str = Field(..., min_length=3, max_length=255, description="Nombre completo")
    nis: str = Field(..., min_length=5, max_length=50, description="Número de Identificación Scout")
    email: EmailStr = Field(..., description="Email del participante")
    rama: Rama = Field(..., description="Rama scout")
    notes: Optional[str] = Field(None, max_length=1000, description="Notas adicionales")
    
    @validator('full_name')
    def name_must_have_spaces(cls, v):
        """Validar que el nombre tenga al menos nombre y apellido"""
        if v.count(' ') < 1:
            raise ValueError('El nombre debe incluir al menos nombre y apellido')
        return v
    
    class Config:
        use_enum_values = True


class ForoParticipantCreate(ForoParticipantBase):
    """Schema para crear participante"""
    pass


class ForoParticipantUpdate(BaseModel):
    """Schema para actualizar participante"""
    full_name: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    rama: Optional[Rama] = None
    notes: Optional[str] = Field(None, max_length=1000)
    is_confirmed: Optional[bool] = None
    
    class Config:
        use_enum_values = True


class ForoParticipantResponse(ForoParticipantBase):
    """Schema de respuesta para participante"""
    id: int
    registration_date: datetime
    updated_date: datetime
    is_confirmed: bool
    medical_filename: Optional[str] = None
    grow_together_filename: Optional[str] = None
    safe_from_harm_filename: Optional[str] = None
    
    class Config:
        from_attributes = True


class ForoParticipantDetail(ForoParticipantResponse):
    """Schema detallado de participante con información de archivos"""
    has_medical_file: bool = Field(default=False)
    has_grow_together_cert: bool = Field(default=False)
    has_safe_from_harm_cert: bool = Field(default=False)


class ForoImportResult(BaseModel):
    """Resultado de importación XLSX"""
    total_records: int
    successful_records: int
    failed_records: int
    import_id: Optional[int] = None
    errors: Optional[list] = None
    message: str


class ForoImportLogResponse(BaseModel):
    """Response para log de importación"""
    id: int
    filename: str
    uploaded_by: str
    total_records: int
    successful_records: int
    failed_records: int
    upload_date: datetime
    errors: Optional[str] = None
    
    class Config:
        from_attributes = True


class ForoStatistics(BaseModel):
    """Estadísticas del Foro"""
    total_participants: int
    confirmed_participants: int
    by_rama: dict  # {rama: count}
    registration_rate: float  # porcentaje de confirmación


class ParticipantXLSXRow(BaseModel):
    """Estructura esperada de fila en XLSX"""
    full_name: str
    nis: str
    email: str
    rama: str
    notes: Optional[str] = None
