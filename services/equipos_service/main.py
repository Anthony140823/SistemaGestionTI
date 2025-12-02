from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from supabase import create_client, Client
import os
from datetime import date
import json

app = FastAPI(title="Equipos Service", version="1.0.0")

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# MODELOS PYDANTIC
# ============================================

class EquipoCreate(BaseModel):
    codigo_inventario: str
    categoria_id: int
    nombre: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    numero_serie: Optional[str] = None
    especificaciones: Optional[dict] = None
    proveedor_id: Optional[int] = None
    fecha_compra: Optional[date] = None
    costo_compra: Optional[float] = None
    fecha_garantia_fin: Optional[date] = None
    ubicacion_actual_id: Optional[int] = None
    estado_operativo: str = "operativo"
    estado_fisico: str = "bueno"
    asignado_a_id: Optional[int] = None
    notas: Optional[str] = None
    imagen_url: Optional[str] = None

class EquipoUpdate(BaseModel):
    nombre: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    especificaciones: Optional[dict] = None
    ubicacion_actual_id: Optional[int] = None
    estado_operativo: Optional[str] = None
    estado_fisico: Optional[str] = None
    asignado_a_id: Optional[int] = None
    notas: Optional[str] = None

class MovimientoCreate(BaseModel):
    equipo_id: int
    ubicacion_destino_id: int
    usuario_responsable_id: int
    motivo: str
    observaciones: Optional[str] = None

# ============================================
# ENDPOINTS
# ============================================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "equipos"}

@app.get("/equipos")
async def get_equipos(
    categoria: Optional[str] = None,
    estado: Optional[str] = None,
    ubicacion: Optional[int] = None
):
    """Obtener lista de equipos con filtros opcionales"""
    try:
        query = supabase.table("equipos").select(
            "*, categorias_equipos(nombre), ubicaciones(edificio, aula_oficina), proveedores(razon_social)"
        )
        
        if estado:
            query = query.eq("estado_operativo", estado)
        
        if ubicacion:
            query = query.eq("ubicacion_actual_id", ubicacion)
        
        response = query.order("fecha_registro", desc=True).execute()
        
        # Procesar especificaciones JSON
        equipos = []
        for equipo in response.data:
            if equipo.get('especificaciones') and isinstance(equipo['especificaciones'], str):
                try:
                    equipo['especificaciones'] = json.loads(equipo['especificaciones'])
                except:
                    pass
            equipos.append(equipo)
        
        return equipos
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/equipos/{equipo_id}")
async def get_equipo(equipo_id: int):
    """Obtener detalle de un equipo específico"""
    try:
        # Obtener equipo
        response = supabase.table("equipos").select(
            "*, categorias_equipos(nombre), ubicaciones(edificio, aula_oficina), proveedores(razon_social), usuarios(nombre_completo)"
        ).eq("id", equipo_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        
        equipo = response.data[0]
        
        # Procesar especificaciones
        if equipo.get('especificaciones') and isinstance(equipo['especificaciones'], str):
            try:
                equipo['especificaciones'] = json.loads(equipo['especificaciones'])
            except:
                pass
        
        # Obtener historial de movimientos
        movimientos_response = supabase.table("movimientos_equipos").select(
            "*, ubicaciones!movimientos_equipos_ubicacion_destino_id_fkey(edificio, aula_oficina), usuarios(nombre_completo)"
        ).eq("equipo_id", equipo_id).order("fecha_movimiento", desc=True).execute()
        
        equipo['historial_movimientos'] = movimientos_response.data
        
        return equipo
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/equipos")
async def create_equipo(equipo: EquipoCreate):
    """Crear nuevo equipo"""
    try:
        # Convertir especificaciones a JSON string si existe
        equipo_dict = equipo.model_dump()
        if equipo_dict.get('especificaciones'):
            equipo_dict['especificaciones'] = json.dumps(equipo_dict['especificaciones'])
        
        # Convertir fechas a string
        if equipo_dict.get('fecha_compra'):
            equipo_dict['fecha_compra'] = str(equipo_dict['fecha_compra'])
        if equipo_dict.get('fecha_garantia_fin'):
            equipo_dict['fecha_garantia_fin'] = str(equipo_dict['fecha_garantia_fin'])
        
        response = supabase.table("equipos").insert(equipo_dict).execute()
        
        return {"id": response.data[0]['id'], "message": "Equipo creado exitosamente"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/equipos/{equipo_id}")
async def update_equipo(equipo_id: int, equipo: EquipoUpdate):
    """Actualizar equipo existente"""
    try:
        # Preparar datos para actualizar (solo campos no nulos)
        update_data = {k: v for k, v in equipo.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        # Convertir especificaciones a JSON string si existe
        if 'especificaciones' in update_data:
            update_data['especificaciones'] = json.dumps(update_data['especificaciones'])
        
        response = supabase.table("equipos").update(update_data).eq("id", equipo_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        
        return {"message": "Equipo actualizado exitosamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/equipos/{equipo_id}")
async def delete_equipo(equipo_id: int):
    """Eliminar equipo"""
    try:
        response = supabase.table("equipos").delete().eq("id", equipo_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        
        return {"message": "Equipo eliminado exitosamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/movimientos")
async def create_movimiento(movimiento: MovimientoCreate):
    """Registrar movimiento de equipo"""
    try:
        # Obtener ubicación actual del equipo
        equipo_response = supabase.table("equipos").select("ubicacion_actual_id").eq("id", movimiento.equipo_id).execute()
        
        if not equipo_response.data:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        
        ubicacion_origen = equipo_response.data[0]['ubicacion_actual_id']
        
        # Crear movimiento
        movimiento_dict = movimiento.model_dump()
        movimiento_dict['ubicacion_origen_id'] = ubicacion_origen
        
        supabase.table("movimientos_equipos").insert(movimiento_dict).execute()
        
        # Actualizar ubicación del equipo
        supabase.table("equipos").update({
            "ubicacion_actual_id": movimiento.ubicacion_destino_id
        }).eq("id", movimiento.equipo_id).execute()
        
        return {"message": "Movimiento registrado exitosamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categorias")
async def get_categorias():
    """Obtener todas las categorías de equipos"""
    try:
        response = supabase.table("categorias_equipos").select("*").order("nombre").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ubicaciones")
async def get_ubicaciones():
    """Obtener todas las ubicaciones activas"""
    try:
        response = supabase.table("ubicaciones").select("*").eq("activo", True).order("edificio, aula_oficina").execute()
        
        # Agregar nombre completo
        ubicaciones = []
        for ubicacion in response.data:
            ubicacion['nombre_completo'] = f"{ubicacion['edificio']} - {ubicacion['aula_oficina']}"
            ubicaciones.append(ubicacion)
        
        return ubicaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
