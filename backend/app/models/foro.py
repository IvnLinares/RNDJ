from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Enum as SQLEnum, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class Rama(str, enum.Enum):
    """Ramas disponibles"""
    CAMINANTES = "Caminantes"  # 15-18 años
    ROVERS = "Rovers"          # 18-22 años
    DIRIGENTE_JOVEN = "Dirigente Joven"  # 22-25 años
    DIRIGENTE = "Dirigente"    # 25+ años


class ForoParticipant(Base):
    """Participante en el 5to Foro Nacional de Jóvenes"""
    __tablename__ = "foro_participants"

    id = Column(Integer, primary_key=True, index=True)
    
    # Información básica
    full_name = Column(String(255), nullable=False, index=True)
    nis = Column(String(50), nullable=False, unique=True, index=True)  # Número de Identificación Scout
    email = Column(String(255), nullable=False, index=True)
    rama = Column(SQLEnum(Rama), nullable=False)  # Rama Scout
    
    # Archivos adjuntos
    medical_file = Column(LargeBinary, nullable=True)  # Ficha médica (PDF)
    medical_filename = Column(String(255), nullable=True)
    
    grow_together_cert = Column(LargeBinary, nullable=True)  # Certificado Ley Crecer Juntos (PDF)
    grow_together_filename = Column(String(255), nullable=True)
    
    safe_from_harm_cert = Column(LargeBinary, nullable=True)  # Certificado Safe from Harm (PDF)
    safe_from_harm_filename = Column(String(255), nullable=True)
    
    # Notas
    notes = Column(Text, nullable=True)
    
    # Control
    registration_date = Column(DateTime, default=datetime.utcnow, index=True)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_confirmed = Column(Boolean, default=False)  # Si el participante confirmó asistencia
    
    def __repr__(self):
        return f"<ForoParticipant(id={self.id}, name={self.full_name}, rama={self.rama})>"


class ForoImportLog(Base):
    """Log de importaciones XLSX para auditoría"""
    __tablename__ = "foro_import_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    uploaded_by = Column(String(255), nullable=False)
    total_records = Column(Integer, default=0)
    successful_records = Column(Integer, default=0)
    failed_records = Column(Integer, default=0)
    errors = Column(Text, nullable=True)  # JSON de errores detallados
    upload_date = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<ForoImportLog(id={self.id}, filename={self.filename}, successful={self.successful_records})>"
