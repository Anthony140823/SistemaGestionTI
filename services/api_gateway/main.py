from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os
from typing import Optional

app = FastAPI(
    title="API Gateway - Sistema de Gestión TI",
    description="Gateway central para todos los microservicios",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs de los microservicios
EQUIPOS_SERVICE_URL = os.getenv("EQUIPOS_SERVICE_URL", "http://equipos-service:8001")
PROVEEDORES_SERVICE_URL = os.getenv("PROVEEDORES_SERVICE_URL", "http://proveedores-service:8002")
MANTENIMIENTO_SERVICE_URL = os.getenv("MANTENIMIENTO_SERVICE_URL", "http://mantenimiento-service:8003")
REPORTES_SERVICE_URL = os.getenv("REPORTES_SERVICE_URL", "http://reportes-service:8004")
AGENT_SERVICE_URL = os.getenv("AGENT_SERVICE_URL", "http://agent-service:8005")

# Cliente HTTP para hacer peticiones a microservicios
http_client = httpx.AsyncClient(timeout=30.0)

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint con información del API"""
    return {
        "message": "API Gateway - Sistema de Gestión de Equipos TI",
        "version": "1.0.0",
        "docs": "/docs",
        "services": {
            "equipos": f"{EQUIPOS_SERVICE_URL}",
            "proveedores": f"{PROVEEDORES_SERVICE_URL}",
            "mantenimiento": f"{MANTENIMIENTO_SERVICE_URL}",
            "reportes": f"{REPORTES_SERVICE_URL}",
            "agents": f"{AGENT_SERVICE_URL}"
        }
    }

# ============================================
# PROXY FUNCTIONS
# ============================================

async def proxy_request(service_url: str, path: str, method: str = "GET", **kwargs):
    """Función genérica para hacer proxy de peticiones a microservicios"""
    url = f"{service_url}{path}"
    
    try:
        if method == "GET":
            response = await http_client.get(url, **kwargs)
        elif method == "POST":
            response = await http_client.post(url, **kwargs)
        elif method == "PUT":
            response = await http_client.put(url, **kwargs)
        elif method == "DELETE":
            response = await http_client.delete(url, **kwargs)
        else:
            raise HTTPException(status_code=405, detail="Method not allowed")
        
        response.raise_for_status()
        return response.json()
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# ============================================
# EQUIPOS ENDPOINTS
# ============================================

@app.get("/api/equipos")
async def get_equipos(categoria: Optional[str] = None, estado: Optional[str] = None, ubicacion: Optional[int] = None):
    """Obtener lista de equipos"""
    params = {}
    if categoria:
        params["categoria"] = categoria
    if estado:
        params["estado"] = estado
    if ubicacion:
        params["ubicacion"] = ubicacion
    
    return await proxy_request(EQUIPOS_SERVICE_URL, "/equipos", params=params)

@app.get("/api/equipos/{equipo_id}")
async def get_equipo(equipo_id: int):
    """Obtener detalle de un equipo"""
    return await proxy_request(EQUIPOS_SERVICE_URL, f"/equipos/{equipo_id}")

@app.post("/api/equipos")
async def create_equipo(request: Request):
    """Crear nuevo equipo"""
    data = await request.json()
    return await proxy_request(EQUIPOS_SERVICE_URL, "/equipos", method="POST", json=data)

@app.put("/api/equipos/{equipo_id}")
async def update_equipo(equipo_id: int, request: Request):
    """Actualizar equipo"""
    data = await request.json()
    return await proxy_request(EQUIPOS_SERVICE_URL, f"/equipos/{equipo_id}", method="PUT", json=data)

@app.delete("/api/equipos/{equipo_id}")
async def delete_equipo(equipo_id: int):
    """Eliminar equipo"""
    return await proxy_request(EQUIPOS_SERVICE_URL, f"/equipos/{equipo_id}", method="DELETE")

@app.get("/api/categorias")
async def get_categorias():
    """Obtener categorías de equipos"""
    return await proxy_request(EQUIPOS_SERVICE_URL, "/categorias")

@app.get("/api/ubicaciones")
async def get_ubicaciones():
    """Obtener ubicaciones"""
    return await proxy_request(EQUIPOS_SERVICE_URL, "/ubicaciones")

@app.post("/api/movimientos")
async def create_movimiento(request: Request):
    """Registrar movimiento de equipo"""
    data = await request.json()
    return await proxy_request(EQUIPOS_SERVICE_URL, "/movimientos", method="POST", json=data)

# ============================================
# PROVEEDORES ENDPOINTS
# ============================================

@app.get("/api/proveedores")
async def get_proveedores(activo: Optional[bool] = None):
    """Obtener lista de proveedores"""
    params = {}
    if activo is not None:
        params["activo"] = activo
    return await proxy_request(PROVEEDORES_SERVICE_URL, "/proveedores", params=params)

@app.get("/api/proveedores/{proveedor_id}")
async def get_proveedor(proveedor_id: int):
    """Obtener detalle de un proveedor"""
    return await proxy_request(PROVEEDORES_SERVICE_URL, f"/proveedores/{proveedor_id}")

@app.post("/api/proveedores")
async def create_proveedor(request: Request):
    """Crear nuevo proveedor"""
    data = await request.json()
    return await proxy_request(PROVEEDORES_SERVICE_URL, "/proveedores", method="POST", json=data)

@app.put("/api/proveedores/{proveedor_id}")
async def update_proveedor(proveedor_id: int, request: Request):
    """Actualizar proveedor"""
    data = await request.json()
    return await proxy_request(PROVEEDORES_SERVICE_URL, f"/proveedores/{proveedor_id}", method="PUT", json=data)

@app.delete("/api/proveedores/{proveedor_id}")
async def delete_proveedor(proveedor_id: int):
    """Eliminar proveedor"""
    return await proxy_request(PROVEEDORES_SERVICE_URL, f"/proveedores/{proveedor_id}", method="DELETE")

@app.get("/api/contratos")
async def get_contratos():
    """Obtener contratos"""
    return await proxy_request(PROVEEDORES_SERVICE_URL, "/contratos")

@app.post("/api/contratos")
async def create_contrato(request: Request):
    """Crear nuevo contrato"""
    data = await request.json()
    return await proxy_request(PROVEEDORES_SERVICE_URL, "/contratos", method="POST", json=data)

# ============================================
# MANTENIMIENTOS ENDPOINTS
# ============================================

@app.get("/api/mantenimientos")
async def get_mantenimientos(estado: Optional[str] = None, tipo: Optional[str] = None):
    """Obtener lista de mantenimientos"""
    params = {}
    if estado:
        params["estado"] = estado
    if tipo:
        params["tipo"] = tipo
    return await proxy_request(MANTENIMIENTO_SERVICE_URL, "/mantenimientos", params=params)

@app.get("/api/mantenimientos/calendario")
async def get_calendario_mantenimientos():
    """Obtener calendario de mantenimientos"""
    return await proxy_request(MANTENIMIENTO_SERVICE_URL, "/calendario")

@app.get("/api/mantenimientos/estadisticas")
async def get_estadisticas_mantenimientos():
    """Obtener estadísticas de mantenimientos"""
    return await proxy_request(MANTENIMIENTO_SERVICE_URL, "/estadisticas")

@app.get("/api/mantenimientos/{mantenimiento_id}")
async def get_mantenimiento(mantenimiento_id: int):
    """Obtener detalle de un mantenimiento"""
    return await proxy_request(MANTENIMIENTO_SERVICE_URL, f"/mantenimientos/{mantenimiento_id}")

@app.post("/api/mantenimientos")
async def create_mantenimiento(request: Request):
    """Crear nuevo mantenimiento"""
    data = await request.json()
    return await proxy_request(MANTENIMIENTO_SERVICE_URL, "/mantenimientos", method="POST", json=data)

@app.put("/api/mantenimientos/{mantenimiento_id}")
async def update_mantenimiento(mantenimiento_id: int, request: Request):
    """Actualizar mantenimiento"""
    data = await request.json()
    return await proxy_request(MANTENIMIENTO_SERVICE_URL, f"/mantenimientos/{mantenimiento_id}", method="PUT", json=data)

# ============================================
# REPORTES ENDPOINTS
# ============================================

@app.get("/api/reportes/dashboard")
async def get_dashboard():
    """Obtener datos del dashboard principal"""
    return await proxy_request(REPORTES_SERVICE_URL, "/dashboard")

@app.get("/api/reportes/equipos-por-ubicacion")
async def get_equipos_por_ubicacion():
    """Obtener reporte de equipos por ubicación"""
    return await proxy_request(REPORTES_SERVICE_URL, "/equipos-por-ubicacion")

@app.get("/api/reportes/equipos-por-estado")
async def get_equipos_por_estado():
    """Obtener reporte de equipos por estado"""
    return await proxy_request(REPORTES_SERVICE_URL, "/equipos-por-estado")

@app.get("/api/reportes/costos-mantenimiento")
async def get_costos_mantenimiento():
    """Obtener reporte de costos de mantenimiento"""
    return await proxy_request(REPORTES_SERVICE_URL, "/costos-mantenimiento")

@app.get("/api/reportes/antiguedad-equipos")
async def get_antiguedad_equipos():
    """Obtener reporte de antigüedad de equipos"""
    return await proxy_request(REPORTES_SERVICE_URL, "/antiguedad-equipos")

# ============================================
# AGENTS ENDPOINTS
# ============================================

@app.post("/api/agents/run-all-agents")
async def run_all_agents():
    """Ejecutar todos los agentes inteligentes"""
    return await proxy_request(AGENT_SERVICE_URL, "/run-all-agents", method="POST")

@app.get("/api/agents/notificaciones")
async def get_notificaciones(leida: Optional[bool] = None):
    """Obtener notificaciones"""
    params = {}
    if leida is not None:
        params["leida"] = str(leida).lower()
    return await proxy_request(AGENT_SERVICE_URL, "/notificaciones", params=params)

@app.put("/api/agents/notificaciones/{notificacion_id}/marcar-leida")
async def marcar_notificacion_leida(notificacion_id: int):
    """Marcar notificación como leída"""
    return await proxy_request(AGENT_SERVICE_URL, f"/notificaciones/{notificacion_id}/marcar-leida", method="PUT")

# ============================================
# ERROR HANDLERS
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# ============================================
# STARTUP/SHUTDOWN EVENTS
# ============================================

@app.on_event("startup")
async def startup_event():
    print("🚀 API Gateway iniciado correctamente")
    print(f"📍 Equipos Service: {EQUIPOS_SERVICE_URL}")
    print(f"📍 Proveedores Service: {PROVEEDORES_SERVICE_URL}")
    print(f"📍 Mantenimiento Service: {MANTENIMIENTO_SERVICE_URL}")
    print(f"📍 Reportes Service: {REPORTES_SERVICE_URL}")
    print(f"📍 Agent Service: {AGENT_SERVICE_URL}")

@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()
    print("👋 API Gateway detenido")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
