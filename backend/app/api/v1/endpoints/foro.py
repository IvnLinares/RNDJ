from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import openpyxl
from io import BytesIO
import json
from datetime import datetime

from app.database import get_db
from app.models.foro import ForoParticipant, ForoImportLog, Rama
from app.schemas.foro import (
    ForoParticipantCreate,
    ForoParticipantResponse,
    ForoParticipantUpdate,
    ForoParticipantDetail,
    ForoImportResult,
    ForoImportLogResponse,
    ForoStatistics,
)
from app.api.v1.endpoints.users import get_current_user_from_token

router = APIRouter()


# =====================
# CRUD - Participantes
# =====================

@router.post("/participants", response_model=ForoParticipantResponse, tags=["Foro Nacional"])
async def create_participant(
    participant: ForoParticipantCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Crear un nuevo participante en el Foro Nacional.
    
    Solo usuarios autenticados pueden crear registros.
    """
    # Verificar si el NIS ya existe
    stmt_nis = select(ForoParticipant).where(ForoParticipant.nis == participant.nis)
    result_nis = await db.execute(stmt_nis)
    existing_nis = result_nis.scalars().first()
    if existing_nis:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un participante con el NIS {participant.nis}"
        )
    
    # Verificar si el email ya existe
    stmt_email = select(ForoParticipant).where(ForoParticipant.email == participant.email)
    result_email = await db.execute(stmt_email)
    existing_email = result_email.scalars().first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un participante con el email {participant.email}"
        )
    
    db_participant = ForoParticipant(**participant.dict())
    db.add(db_participant)
    await db.commit()
    await db.refresh(db_participant)
    
    return db_participant


@router.get("/participants", response_model=List[ForoParticipantResponse], tags=["Foro Nacional"])
async def list_participants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    rama: Optional[str] = None,
    is_confirmed: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Listar todos los participantes del Foro Nacional.
    
    Soporta filtrado por rama y confirmación.
    """
    stmt = select(ForoParticipant)
    
    if rama:
        stmt = stmt.where(ForoParticipant.rama == rama)
    
    if is_confirmed is not None:
        stmt = stmt.where(ForoParticipant.is_confirmed == is_confirmed)
    
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/participants/{participant_id}", response_model=ForoParticipantDetail, tags=["Foro Nacional"])
async def get_participant(
    participant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Obtener detalles de un participante específico.
    """
    stmt = select(ForoParticipant).where(ForoParticipant.id == participant_id)
    result = await db.execute(stmt)
    db_participant = result.scalars().first()
    
    if not db_participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participante {participant_id} no encontrado"
        )
    
    # Agregar información sobre archivos
    response_data = ForoParticipantResponse.from_orm(db_participant).dict()
    response_data['has_medical_file'] = db_participant.medical_file is not None
    response_data['has_grow_together_cert'] = db_participant.grow_together_cert is not None
    response_data['has_safe_from_harm_cert'] = db_participant.safe_from_harm_cert is not None
    
    return response_data


@router.put("/participants/{participant_id}", response_model=ForoParticipantResponse, tags=["Foro Nacional"])
async def update_participant(
    participant_id: int,
    participant_update: ForoParticipantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Actualizar información de un participante.
    """
    stmt = select(ForoParticipant).where(ForoParticipant.id == participant_id)
    result = await db.execute(stmt)
    db_participant = result.scalars().first()
    
    if not db_participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participante {participant_id} no encontrado"
        )
    
    # Si se está actualizando el email, verificar que no esté duplicado
    if participant_update.email and participant_update.email != db_participant.email:
        stmt_email = select(ForoParticipant).where(
            ForoParticipant.email == participant_update.email
        )
        result_email = await db.execute(stmt_email)
        existing_email = result_email.scalars().first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un participante con el email {participant_update.email}"
            )
    
    update_data = participant_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_participant, field, value)
    
    db.add(db_participant)
    await db.commit()
    await db.refresh(db_participant)
    
    return db_participant


@router.delete("/participants/{participant_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Foro Nacional"])
async def delete_participant(
    participant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Eliminar un participante (solo con permisos de admin).
    """
    stmt = select(ForoParticipant).where(ForoParticipant.id == participant_id)
    result = await db.execute(stmt)
    db_participant = result.scalars().first()
    
    if not db_participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participante {participant_id} no encontrado"
        )
    
    db.delete(db_participant)
    await db.commit()
    return None


# =======================
# Gestión de Archivos
# =======================

@router.post("/participants/{participant_id}/medical-file", status_code=status.HTTP_200_OK, tags=["Foro Nacional"])
async def upload_medical_file(
    participant_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Cargar ficha médica (PDF) para un participante.
    """
    if file.content_type not in ['application/pdf']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se aceptan archivos PDF"
        )
    
    stmt = select(ForoParticipant).where(ForoParticipant.id == participant_id)
    result = await db.execute(stmt)
    db_participant = result.scalars().first()
    
    if not db_participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participante {participant_id} no encontrado"
        )
    
    file_content = await file.read()
    db_participant.medical_file = file_content
    db_participant.medical_filename = file.filename
    
    db.add(db_participant)
    await db.commit()
    
    return {"message": "Ficha médica cargada exitosamente", "filename": file.filename}


@router.post("/participants/{participant_id}/grow-together-cert", status_code=status.HTTP_200_OK, tags=["Foro Nacional"])
async def upload_grow_together_cert(
    participant_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Cargar certificado Ley Crecer Juntos (PDF) para un participante.
    """
    if file.content_type not in ['application/pdf']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se aceptan archivos PDF"
        )
    
    stmt = select(ForoParticipant).where(ForoParticipant.id == participant_id)
    result = await db.execute(stmt)
    db_participant = result.scalars().first()
    
    if not db_participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participante {participant_id} no encontrado"
        )
    
    file_content = await file.read()
    db_participant.grow_together_cert = file_content
    db_participant.grow_together_filename = file.filename
    
    db.add(db_participant)
    await db.commit()
    
    return {"message": "Certificado Ley Crecer Juntos cargado exitosamente", "filename": file.filename}


@router.post("/participants/{participant_id}/safe-from-harm-cert", status_code=status.HTTP_200_OK, tags=["Foro Nacional"])
async def upload_safe_from_harm_cert(
    participant_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Cargar certificado Safe from Harm (PDF) para un participante.
    """
    if file.content_type not in ['application/pdf']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se aceptan archivos PDF"
        )
    
    stmt = select(ForoParticipant).where(ForoParticipant.id == participant_id)
    result = await db.execute(stmt)
    db_participant = result.scalars().first()
    
    if not db_participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participante {participant_id} no encontrado"
        )
    
    file_content = await file.read()
    db_participant.safe_from_harm_cert = file_content
    db_participant.safe_from_harm_filename = file.filename
    
    db.add(db_participant)
    await db.commit()
    
    return {"message": "Certificado Safe from Harm cargado exitosamente", "filename": file.filename}


@router.get("/participants/{participant_id}/medical-file", tags=["Foro Nacional"])
async def download_medical_file(
    participant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Descargar ficha médica de un participante.
    """
    stmt = select(ForoParticipant).where(ForoParticipant.id == participant_id)
    result = await db.execute(stmt)
    db_participant = result.scalars().first()
    
    if not db_participant or not db_participant.medical_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Archivo no encontrado"
        )
    
    return {
        "filename": db_participant.medical_filename,
        "content_type": "application/pdf"
    }


# ================
# Importar XLSX
# ================

@router.post("/import-xlsx", response_model=ForoImportResult, tags=["Foro Nacional"])
async def import_from_xlsx(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Importar participantes desde archivo XLSX.
    
    El archivo debe tener las siguientes columnas:
    - full_name: Nombre completo
    - nis: Número de Identificación Scout
    - email: Email
    - rama: Rama (Caminantes, Rovers, Dirigente Joven, Dirigente)
    - notes: (Opcional) Notas adicionales
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se aceptan archivos Excel (.xlsx, .xls)"
        )
    
    try:
        # Leer archivo
        content = await file.read()
        workbook = openpyxl.load_workbook(BytesIO(content))
        worksheet = workbook.active
        
        total_records = 0
        successful_records = 0
        failed_records = 0
        errors = []
        
        # Procesar filas
        for row_idx, row in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
            if not row or all(cell is None for cell in row):
                continue
            
            total_records += 1
            
            try:
                full_name = row[0]
                nis = row[1]
                email = row[2]
                rama = row[3]
                notes = row[4] if len(row) > 4 else None
                
                # Validaciones básicas
                if not full_name or not nis or not email:
                    failed_records += 1
                    errors.append({
                        "row": row_idx,
                        "error": "Campos requeridos faltantes (nombre, NIS, email)"
                    })
                    continue
                
                # Validar rama
                try:
                    valid_ramas = [r.value for r in Rama]
                    if str(rama).strip() not in valid_ramas:
                        failed_records += 1
                        errors.append({
                            "row": row_idx,
                            "error": f"Rama inválida: {rama}. Válidas: {', '.join(valid_ramas)}"
                        })
                        continue
                except:
                    pass
                
                # Verificar duplicados (async)
                nis_str = str(nis).strip()
                stmt_nis = select(ForoParticipant).where(ForoParticipant.nis == nis_str)
                result_nis = await db.execute(stmt_nis)
                existing_nis = result_nis.scalars().first()
                
                if existing_nis:
                    failed_records += 1
                    errors.append({
                        "row": row_idx,
                        "error": f"NIS duplicado: {nis}"
                    })
                    continue
                
                email_str = str(email).strip()
                stmt_email = select(ForoParticipant).where(ForoParticipant.email == email_str)
                result_email = await db.execute(stmt_email)
                existing_email = result_email.scalars().first()
                
                if existing_email:
                    failed_records += 1
                    errors.append({
                        "row": row_idx,
                        "error": f"Email duplicado: {email}"
                    })
                    continue
                
                # Crear participante
                new_participant = ForoParticipant(
                    full_name=str(full_name).strip(),
                    nis=nis_str,
                    email=email_str,
                    rama=str(rama).strip(),
                    notes=str(notes).strip() if notes else None
                )
                
                db.add(new_participant)
                successful_records += 1
                
            except Exception as e:
                failed_records += 1
                errors.append({
                    "row": row_idx,
                    "error": str(e)
                })
        
        # Commit de todos los registros
        await db.commit()
        
        # Crear log
        import_log = ForoImportLog(
            filename=file.filename,
            uploaded_by=current_user.username,
            total_records=total_records,
            successful_records=successful_records,
            failed_records=failed_records,
            errors=json.dumps(errors) if errors else None
        )
        db.add(import_log)
        await db.commit()
        await db.refresh(import_log)  # Actualizar para obtener el ID generado
        
        return ForoImportResult(
            total_records=total_records,
            successful_records=successful_records,
            failed_records=failed_records,
            import_id=import_log.id,
            errors=errors if errors else None,
            message=f"Importación completada: {successful_records}/{total_records} registros exitosos"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar archivo: {str(e)}"
        )


# ==============
# Estadísticas
# ==============

@router.get("/statistics", response_model=ForoStatistics, tags=["Foro Nacional"])
async def get_statistics(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Obtener estadísticas del Foro Nacional.
    """
    # Total de participantes
    stmt_total = select(func.count(ForoParticipant.id))
    result_total = await db.execute(stmt_total)
    total = result_total.scalar() or 0
    
    # Participantes confirmados
    stmt_confirmed = select(func.count(ForoParticipant.id)).where(ForoParticipant.is_confirmed == True)
    result_confirmed = await db.execute(stmt_confirmed)
    confirmed = result_confirmed.scalar() or 0
    
    # Contar por rama
    stmt_by_rama = select(ForoParticipant.rama, func.count(ForoParticipant.id)).group_by(ForoParticipant.rama)
    result_by_rama = await db.execute(stmt_by_rama)
    by_rama = {rama: count for rama, count in result_by_rama.all()}
    
    registration_rate = (confirmed / total * 100) if total > 0 else 0
    
    return ForoStatistics(
        total_participants=total,
        confirmed_participants=confirmed,
        by_rama=by_rama,
        registration_rate=registration_rate
    )


@router.get("/import-logs", response_model=List[ForoImportLogResponse], tags=["Foro Nacional"])
async def get_import_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user_from_token)
):
    """
    Obtener historial de importaciones XLSX.
    """
    stmt = select(ForoImportLog).order_by(ForoImportLog.upload_date.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
