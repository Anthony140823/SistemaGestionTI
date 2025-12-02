from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from supabase import create_client, Client
import os
from datetime import date

app = FastAPI(title="Proveedores Service", version="1.0.0")

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# MODELOS PYDANTIC
# ============================================

class ProveedorCreate(BaseModel):
    ruc: str
    razon_social: str
    nombre_comercial: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_telefono: Optional[str] = None
    contacto_email: Optional[str] = None
    sitio_web: Optional[str] = None
    calificacion: Optional[float] = None
    notas: Optional[str] = None

class ProveedorUpdate(BaseModel):
    razon_social: Optional[str] = None
    nombre_comercial: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    contacto_nombre: Optional[str] = None
    contacto_telefono: Optional[str] = None
    contacto_email: Optional[str] = None
    sitio_web: Optional[str] = None
    calificacion: Optional[float] = None
    activo: Optional[bool] = None
    notas: Optional[str] = None

class ContratoCreate(BaseModel):
    proveedor_id: int
    numero_contrato: str
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    monto_total: Optional[float] = None
    estado: str = "vigente"
    notas: Optional[str] = None

# ============================================
# ENDPOINTS - PROVEEDORES
# ============================================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "proveedores"}

@app.get("/proveedores")
async def get_proveedores(activo: Optional[bool] = None):
    """Obtener lista de proveedores"""
    try:
        query = supabase.table("proveedores").select("*")
        
        if activo is not None:
            query = query.eq("activo", activo)
        
        response = query.order("razon_social").execute()
        return response.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/proveedores/{proveedor_id}")
async def get_proveedor(proveedor_id: int):
    """Obtener detalle de un proveedor"""
    try:
        # Obtener proveedor
        response = supabase.table("proveedores").select("*").eq("id", proveedor_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        
        proveedor = response.data[0]
        
        # Obtener contratos del proveedor
        contratos_response = supabase.table("contratos").select("*").eq("proveedor_id", proveedor_id).order("fecha_inicio", desc=True).execute()
        proveedor['contratos'] = contratos_response.data
        
        # Obtener equipos comprados a este proveedor
        equipos_response = supabase.table("equipos").select("id, codigo_inventario, nombre, fecha_compra, costo_compra").eq("proveedor_id", proveedor_id).execute()
        proveedor['equipos_comprados'] = equipos_response.data
        
        return proveedor
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/proveedores")
async def create_proveedor(proveedor: ProveedorCreate):
    """Crear nuevo proveedor"""
    try:
        proveedor_dict = proveedor.model_dump()
        response = supabase.table("proveedores").insert(proveedor_dict).execute()
        
        return {"id": response.data[0]['id'], "message": "Proveedor creado exitosamente"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/proveedores/{proveedor_id}")
async def update_proveedor(proveedor_id: int, proveedor: ProveedorUpdate):
    """Actualizar proveedor"""
    try:
        update_data = {k: v for k, v in proveedor.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        response = supabase.table("proveedores").update(update_data).eq("id", proveedor_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        
        return {"message": "Proveedor actualizado exitosamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/proveedores/{proveedor_id}")
async def delete_proveedor(proveedor_id: int):
    """Eliminar proveedor (marcar como inactivo)"""
    try:
        response = supabase.table("proveedores").update({"activo": False}).eq("id", proveedor_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        
        return {"message": "Proveedor desactivado exitosamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============================================
# ENDPOINTS - CONTRATOS
# ============================================

@app.get("/contratos")
async def get_contratos(proveedor_id: Optional[int] = None, estado: Optional[str] = None):
    """Obtener lista de contratos"""
    try:
        query = supabase.table("contratos").select("*, proveedores(razon_social)")
        
        if proveedor_id:
            query = query.eq("proveedor_id", proveedor_id)
        
        if estado:
            query = query.eq("estado", estado)
        
        response = query.order("fecha_inicio", desc=True).execute()
        return response.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contratos/{contrato_id}")
async def get_contrato(contrato_id: int):
    """Obtener detalle de un contrato"""
    try:
        response = supabase.table("contratos").select("*, proveedores(*)").eq("id", contrato_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Contrato no encontrado")
        
        return response.data[0]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/contratos")
async def create_contrato(contrato: ContratoCreate):
    """Crear nuevo contrato"""
    try:
        contrato_dict = contrato.model_dump()
        
        # Convertir fechas a string
        if contrato_dict.get('fecha_inicio'):
            contrato_dict['fecha_inicio'] = str(contrato_dict['fecha_inicio'])
        if contrato_dict.get('fecha_fin'):
            contrato_dict['fecha_fin'] = str(contrato_dict['fecha_fin'])
        
        response = supabase.table("contratos").insert(contrato_dict).execute()
        
        return {"id": response.data[0]['id'], "message": "Contrato creado exitosamente"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/contratos/{contrato_id}")
async def update_contrato(contrato_id: int, estado: str):
    """Actualizar estado de contrato"""
    try:
        response = supabase.table("contratos").update({"estado": estado}).eq("id", contrato_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Contrato no encontrado")
        
        return {"message": "Contrato actualizado exitosamente"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
