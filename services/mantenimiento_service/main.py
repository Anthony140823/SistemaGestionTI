from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from supabase import create_client, Client
import os
from datetime import date, datetime, timedelta

app = FastAPI(title="Mantenimiento Service", version="1.0.0")

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# MODELOS PYDANTIC
# ============================================

class MantenimientoCreate(BaseModel):
    equipo_id: int
    tipo: str  # preventivo, correctivo
    fecha_programada: date
    proveedor_id: Optional[int] = None
    tecnico_responsable: Optional[str] = None
    diagnostico: Optional[str] = None
    observaciones: Optional[str] = None

class MantenimientoUpdate(BaseModel):
    fecha_realizada: Optional[date] = None
    estado: Optional[str] = None  # programado, en_proceso, completado, cancelado
    costo_total: Optional[float] = None
    diagnostico: Optional[str] = None
    solucion: Optional[str] = None
    observaciones: Optional[str] = None

class DetalleMantenimientoCreate(BaseModel):
    mantenimiento_id: int
    descripcion: str
    repuesto_usado: Optional[str] = None
    cantidad: Optional[int] = None
    costo_unitario: Optional[float] = None
    costo_total: Optional[float] = None

# ============================================
# ENDPOINTS
# ============================================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mantenimiento"}

@app.get("/mantenimientos")
async def get_mantenimientos(estado: Optional[str] = None, tipo: Optional[str] = None):
    """Obtener lista de mantenimientos"""
    try:
        query = supabase.table("mantenimientos").select(
            "*, equipos(codigo_inventario, nombre), proveedores(razon_social)"
        )
        
        if estado:
            query = query.eq("estado", estado)
        
        if tipo:
            query = query.eq("tipo", tipo)
        
        response = query.order("fecha_programada", desc=True).execute()
        return response.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mantenimientos/{mantenimiento_id}")
async def get_mantenimiento(mantenimiento_id: int):
    """Obtener detalle de un mantenimiento"""
    try:
        # Obtener mantenimiento
        response = supabase.table("mantenimientos").select(
            "*, equipos(codigo_inventario, nombre), proveedores(razon_social)"
        ).eq("id", mantenimiento_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
        
        mantenimiento = response.data[0]
        
        # Obtener detalles del mantenimiento
        detalles_response = supabase.table("detalle_mantenimientos").select("*").eq("mantenimiento_id", mantenimiento_id).execute()
        mantenimiento['detalles'] = detalles_response.data
        
        return mantenimiento
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mantenimientos")
async def create_mantenimiento(mantenimiento: MantenimientoCreate):
    """Crear nuevo mantenimiento"""
    try:
        mantenimiento_dict = mantenimiento.model_dump()
        
        # Convertir fecha a string
        if mantenimiento_dict.get('fecha_programada'):
            mantenimiento_dict['fecha_programada'] = str(mantenimiento_dict['fecha_programada'])
        
        mantenimiento_dict['estado'] = 'programado'
        
        response = supabase.table("mantenimientos").insert(mantenimiento_dict).execute()
        
        return {"id": response.data[0]['id'], "message": "Mantenimiento creado exitosamente"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/mantenimientos/{mantenimiento_id}")
async def update_mantenimiento(mantenimiento_id: int, mantenimiento: MantenimientoUpdate):
    """Actualizar mantenimiento"""
    try:
        update_data = {k: v for k, v in mantenimiento.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        # Convertir fecha a string
        if 'fecha_realizada' in update_data:
            update_data['fecha_realizada'] = str(update_data['fecha_realizada'])
        
        response = supabase.table("mantenimientos").update(update_data).eq("id", mantenimiento_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
        
        # Si se completó el mantenimiento, actualizar estado del equipo
        if update_data.get('estado') == 'completado':
            equipo_id = response.data[0]['equipo_id']
            supabase.table("equipos").update({"estado_operativo": "operativo"}).eq("id", equipo_id).execute()
        
        return {"message": "Mantenimiento actualizado exitosamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detalles")
async def create_detalle_mantenimiento(detalle: DetalleMantenimientoCreate):
    """Agregar detalle a un mantenimiento"""
    try:
        detalle_dict = detalle.model_dump()
        response = supabase.table("detalle_mantenimientos").insert(detalle_dict).execute()
        
        return {"id": response.data[0]['id'], "message": "Detalle agregado exitosamente"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/calendario")
async def get_calendario_mantenimientos():
    """Obtener calendario de mantenimientos programados"""
    try:
        print("Obteniendo calendario...")
        # Obtener todos los mantenimientos programados
        # Intentamos primero con la relación
        try:
            response = supabase.table("mantenimientos").select(
                "*, equipos(codigo_inventario, nombre)"
            ).eq("estado", "programado").order("fecha_programada").execute()
            print(f"Calendario obtenido: {len(response.data)} registros")
            return response.data
        except Exception as e_rel:
            print(f"Error con relación equipos: {e_rel}")
            # Fallback: sin relación
            response = supabase.table("mantenimientos").select("*").eq("estado", "programado").order("fecha_programada").execute()
            return response.data
    
    except Exception as e:
        print(f"ERROR CRITICO CALENDARIO: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/estadisticas")
async def get_estadisticas_mantenimientos():
    """Obtener estadísticas de mantenimientos"""
    try:
        # Total de mantenimientos por estado
        response = supabase.table("mantenimientos").select("estado").execute()
        mantenimientos = response.data
        
        estadisticas = {
            "total": len(mantenimientos),
            "programados": len([m for m in mantenimientos if m['estado'] == 'programado']),
            "en_proceso": len([m for m in mantenimientos if m['estado'] == 'en_proceso']),
            "completados": len([m for m in mantenimientos if m['estado'] == 'completado']),
            "cancelados": len([m for m in mantenimientos if m['estado'] == 'cancelado'])
        }
        
        # Costo total de mantenimientos
        response_costos = supabase.table("mantenimientos").select("costo_total").not_.is_("costo_total", "null").execute()
        costos = [m['costo_total'] for m in response_costos.data if m.get('costo_total')]
        estadisticas['costo_total'] = sum(costos) if costos else 0
        
        # Mantenimientos por tipo
        preventivos = len([m for m in mantenimientos if m.get('tipo') == 'preventivo'])
        correctivos = len([m for m in mantenimientos if m.get('tipo') == 'correctivo'])
        
        estadisticas['por_tipo'] = {
            "preventivo": preventivos,
            "correctivo": correctivos
        }
        
        return estadisticas
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
