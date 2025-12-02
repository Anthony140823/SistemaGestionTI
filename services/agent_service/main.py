from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
import os
from datetime import date, datetime, timedelta
from typing import List, Dict

app = FastAPI(title="Agent Service", version="1.0.0")

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configuración de agentes
AGENT_RUN_INTERVAL_HOURS = int(os.getenv("AGENT_RUN_INTERVAL_HOURS", "24"))
AGENT_MAINTENANCE_CHECK_DAYS = int(os.getenv("AGENT_MAINTENANCE_CHECK_DAYS", "7"))

# ============================================
# FUNCIONES DE AGENTES
# ============================================

async def agent_verificar_mantenimientos_pendientes():
    """Agente que verifica mantenimientos próximos a vencer"""
    try:
        hoy = date.today()
        fecha_limite = hoy + timedelta(days=AGENT_MAINTENANCE_CHECK_DAYS)
        
        # Buscar mantenimientos programados próximos
        response = supabase.table("mantenimientos").select(
            "*, equipos(codigo_inventario, nombre)"
        ).eq("estado", "programado").gte("fecha_programada", str(hoy)).lte("fecha_programada", str(fecha_limite)).execute()
        
        notificaciones_creadas = 0
        
        for mant in response.data:
            # Verificar si ya existe notificación para este mantenimiento
            notif_existente = supabase.table("notificaciones").select("id").eq("mantenimiento_relacionado_id", mant['id']).eq("leida", False).execute()
            
            if not notif_existente.data:
                # Crear notificación
                equipo_nombre = mant['equipos']['nombre'] if mant.get('equipos') else 'Equipo desconocido'
                fecha_prog = mant['fecha_programada']
                
                notificacion = {
                    "tipo": "mantenimiento",
                    "titulo": "Mantenimiento Programado Próximo",
                    "mensaje": f"El equipo '{equipo_nombre}' tiene un mantenimiento {mant['tipo']} programado para el {fecha_prog}",
                    "prioridad": "media",
                    "mantenimiento_relacionado_id": mant['id'],
                    "equipo_relacionado_id": mant['equipo_id']
                }
                
                supabase.table("notificaciones").insert(notificacion).execute()
                notificaciones_creadas += 1
        
        return {
            "agente": "verificar_mantenimientos_pendientes",
            "ejecutado": True,
            "notificaciones_creadas": notificaciones_creadas
        }
    
    except Exception as e:
        return {
            "agente": "verificar_mantenimientos_pendientes",
            "ejecutado": False,
            "error": str(e)
        }

async def agent_verificar_garantias():
    """Agente que verifica garantías próximas a vencer"""
    try:
        hoy = date.today()
        fecha_limite = hoy + timedelta(days=30)
        
        # Buscar equipos con garantía próxima a vencer
        response = supabase.table("equipos").select("id, codigo_inventario, nombre, fecha_garantia_fin").not_.is_("fecha_garantia_fin", "null").gte("fecha_garantia_fin", str(hoy)).lte("fecha_garantia_fin", str(fecha_limite)).execute()
        
        notificaciones_creadas = 0
        
        for equipo in response.data:
            # Verificar si ya existe notificación
            notif_existente = supabase.table("notificaciones").select("id").eq("equipo_relacionado_id", equipo['id']).eq("tipo", "garantia").eq("leida", False).execute()
            
            if not notif_existente.data:
                fecha_fin = equipo['fecha_garantia_fin']
                dias_restantes = (datetime.strptime(fecha_fin, '%Y-%m-%d').date() - hoy).days
                
                notificacion = {
                    "tipo": "garantia",
                    "titulo": "Garantía Próxima a Vencer",
                    "mensaje": f"La garantía del equipo '{equipo['nombre']}' ({equipo['codigo_inventario']}) vence en {dias_restantes} días (fecha: {fecha_fin})",
                    "prioridad": "alta",
                    "equipo_relacionado_id": equipo['id']
                }
                
                supabase.table("notificaciones").insert(notificacion).execute()
                notificaciones_creadas += 1
        
        return {
            "agente": "verificar_garantias",
            "ejecutado": True,
            "notificaciones_creadas": notificaciones_creadas
        }
    
    except Exception as e:
        return {
            "agente": "verificar_garantias",
            "ejecutado": False,
            "error": str(e)
        }

async def agent_verificar_equipos_obsoletos():
    """Agente que identifica equipos obsoletos (más de 5 años)"""
    try:
        hoy = date.today()
        fecha_limite = hoy - timedelta(days=5*365)  # 5 años atrás
        
        # Buscar equipos antiguos
        response = supabase.table("equipos").select("id, codigo_inventario, nombre, fecha_compra, estado_operativo").not_.is_("fecha_compra", "null").lte("fecha_compra", str(fecha_limite)).execute()
        
        notificaciones_creadas = 0
        
        for equipo in response.data:
            # Solo notificar si el equipo está operativo (podría necesitar reemplazo)
            if equipo.get('estado_operativo') == 'operativo':
                # Verificar si ya existe notificación
                notif_existente = supabase.table("notificaciones").select("id").eq("equipo_relacionado_id", equipo['id']).eq("tipo", "obsolescencia").eq("leida", False).execute()
                
                if not notif_existente.data:
                    fecha_compra = equipo['fecha_compra']
                    antiguedad_anios = (hoy - datetime.strptime(fecha_compra, '%Y-%m-%d').date()).days / 365
                    
                    notificacion = {
                        "tipo": "obsolescencia",
                        "titulo": "Equipo Obsoleto Detectado",
                        "mensaje": f"El equipo '{equipo['nombre']}' ({equipo['codigo_inventario']}) tiene {int(antiguedad_anios)} años de antigüedad. Considere su reemplazo.",
                        "prioridad": "media",
                        "equipo_relacionado_id": equipo['id']
                    }
                    
                    supabase.table("notificaciones").insert(notificacion).execute()
                    notificaciones_creadas += 1
        
        return {
            "agente": "verificar_equipos_obsoletos",
            "ejecutado": True,
            "notificaciones_creadas": notificaciones_creadas
        }
    
    except Exception as e:
        return {
            "agente": "verificar_equipos_obsoletos",
            "ejecutado": False,
            "error": str(e)
        }

async def agent_verificar_mantenimientos_atrasados():
    """Agente que detecta mantenimientos atrasados"""
    try:
        hoy = date.today()
        
        # Buscar mantenimientos programados con fecha pasada
        response = supabase.table("mantenimientos").select(
            "*, equipos(codigo_inventario, nombre)"
        ).eq("estado", "programado").lt("fecha_programada", str(hoy)).execute()
        
        notificaciones_creadas = 0
        
        for mant in response.data:
            # Verificar si ya existe notificación
            notif_existente = supabase.table("notificaciones").select("id").eq("mantenimiento_relacionado_id", mant['id']).eq("tipo", "mantenimiento_atrasado").eq("leida", False).execute()
            
            if not notif_existente.data:
                equipo_nombre = mant['equipos']['nombre'] if mant.get('equipos') else 'Equipo desconocido'
                fecha_prog = mant['fecha_programada']
                dias_atraso = (hoy - datetime.strptime(fecha_prog, '%Y-%m-%d').date()).days
                
                notificacion = {
                    "tipo": "mantenimiento_atrasado",
                    "titulo": "Mantenimiento Atrasado",
                    "mensaje": f"El mantenimiento {mant['tipo']} del equipo '{equipo_nombre}' está atrasado {dias_atraso} días (programado: {fecha_prog})",
                    "prioridad": "alta",
                    "mantenimiento_relacionado_id": mant['id'],
                    "equipo_relacionado_id": mant['equipo_id']
                }
                
                supabase.table("notificaciones").insert(notificacion).execute()
                notificaciones_creadas += 1
        
        return {
            "agente": "verificar_mantenimientos_atrasados",
            "ejecutado": True,
            "notificaciones_creadas": notificaciones_creadas
        }
    
    except Exception as e:
        return {
            "agente": "verificar_mantenimientos_atrasados",
            "ejecutado": False,
            "error": str(e)
        }

# ============================================
# ENDPOINTS
# ============================================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "agents"}

@app.post("/run-all-agents")
async def run_all_agents():
    """Ejecutar todos los agentes inteligentes"""
    try:
        resultados = []
        
        # Ejecutar cada agente
        resultados.append(await agent_verificar_mantenimientos_pendientes())
        resultados.append(await agent_verificar_garantias())
        resultados.append(await agent_verificar_equipos_obsoletos())
        resultados.append(await agent_verificar_mantenimientos_atrasados())
        
        total_notificaciones = sum([r.get('notificaciones_creadas', 0) for r in resultados])
        
        return {
            "mensaje": "Agentes ejecutados correctamente",
            "total_notificaciones_creadas": total_notificaciones,
            "resultados": resultados
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notificaciones")
async def get_notificaciones(leida: str = "false"):
    """Obtener notificaciones"""
    try:
        leida_bool = leida.lower() == "true"
        
        response = supabase.table("notificaciones").select(
            "*, equipos(codigo_inventario, nombre)"
        ).eq("leida", leida_bool).order("fecha_creacion", desc=True).limit(50).execute()
        
        return response.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/notificaciones/{notificacion_id}/marcar-leida")
async def marcar_notificacion_leida(notificacion_id: int):
    """Marcar notificación como leída"""
    try:
        response = supabase.table("notificaciones").update({
            "leida": True,
            "fecha_leida": datetime.now().isoformat()
        }).eq("id", notificacion_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        return {"message": "Notificación marcada como leída"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/notificaciones/{notificacion_id}")
async def delete_notificacion(notificacion_id: int):
    """Eliminar notificación"""
    try:
        response = supabase.table("notificaciones").delete().eq("id", notificacion_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        return {"message": "Notificación eliminada"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
