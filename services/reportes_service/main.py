from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
import os
from datetime import date, datetime, timedelta
from typing import Dict, List

app = FastAPI(title="Reportes Service", version="1.0.0")

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# ENDPOINTS
# ============================================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "reportes"}

@app.get("/dashboard")
async def get_dashboard():
    """Obtener datos del dashboard principal"""
    try:
        # Total de equipos
        equipos_response = supabase.table("equipos").select("id, estado_operativo, costo_compra").execute()
        equipos = equipos_response.data
        
        total_equipos = len(equipos)
        equipos_operativos = len([e for e in equipos if e.get('estado_operativo') == 'operativo'])
        equipos_reparacion = len([e for e in equipos if e.get('estado_operativo') == 'en_reparacion'])
        
        # Calcular tasa de disponibilidad
        tasa_disponibilidad = round((equipos_operativos / total_equipos * 100), 2) if total_equipos > 0 else 0
        
        # Valor del inventario
        valor_inventario = sum([e.get('costo_compra', 0) or 0 for e in equipos])
        
        # Mantenimientos del mes actual
        hoy = date.today()
        primer_dia_mes = hoy.replace(day=1)
        
        mantenimientos_response = supabase.table("mantenimientos").select("id, costo_total").gte("fecha_programada", str(primer_dia_mes)).lte("fecha_programada", str(hoy)).execute()
        mantenimientos = mantenimientos_response.data
        
        mantenimientos_mes = len(mantenimientos)
        costo_mantenimiento_mes = sum([m.get('costo_total', 0) or 0 for m in mantenimientos])
        
        return {
            "total_equipos": total_equipos,
            "equipos_operativos": equipos_operativos,
            "equipos_reparacion": equipos_reparacion,
            "tasa_disponibilidad": tasa_disponibilidad,
            "valor_inventario": valor_inventario,
            "mantenimientos_mes": mantenimientos_mes,
            "costo_mantenimiento_mes": costo_mantenimiento_mes
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/equipos-por-ubicacion")
async def get_equipos_por_ubicacion():
    """Obtener reporte de equipos por ubicación"""
    try:
        response = supabase.table("equipos").select("ubicacion_actual_id, ubicaciones(edificio, aula_oficina)").execute()
        
        # Agrupar por ubicación
        ubicaciones_dict = {}
        for equipo in response.data:
            if equipo.get('ubicaciones'):
                ubicacion_nombre = f"{equipo['ubicaciones']['edificio']} - {equipo['ubicaciones']['aula_oficina']}"
                ubicaciones_dict[ubicacion_nombre] = ubicaciones_dict.get(ubicacion_nombre, 0) + 1
        
        # Convertir a lista
        resultado = [{"ubicacion": k, "cantidad": v} for k, v in ubicaciones_dict.items()]
        resultado.sort(key=lambda x: x['cantidad'], reverse=True)
        
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/equipos-por-estado")
async def get_equipos_por_estado():
    """Obtener reporte de equipos por estado operativo"""
    try:
        response = supabase.table("equipos").select("estado_operativo").execute()
        
        # Agrupar por estado
        estados_dict = {}
        for equipo in response.data:
            estado = equipo.get('estado_operativo', 'sin_estado')
            estados_dict[estado] = estados_dict.get(estado, 0) + 1
        
        # Convertir a lista
        resultado = [{"estado": k, "cantidad": v} for k, v in estados_dict.items()]
        resultado.sort(key=lambda x: x['cantidad'], reverse=True)
        
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/costos-mantenimiento")
async def get_costos_mantenimiento():
    """Obtener reporte de costos de mantenimiento por mes"""
    try:
        # Obtener mantenimientos de los últimos 12 meses
        hoy = date.today()
        hace_12_meses = hoy - timedelta(days=365)
        
        response = supabase.table("mantenimientos").select("fecha_programada, costo_total, tipo").gte("fecha_programada", str(hace_12_meses)).execute()
        
        # Agrupar por mes
        meses_dict = {}
        for mant in response.data:
            if mant.get('fecha_programada') and mant.get('costo_total'):
                try:
                    fecha = datetime.strptime(mant['fecha_programada'], '%Y-%m-%d')
                    mes_anio = fecha.strftime('%Y-%m')
                    
                    if mes_anio not in meses_dict:
                        meses_dict[mes_anio] = {"preventivo": 0, "correctivo": 0}
                    
                    tipo = mant.get('tipo', 'correctivo')
                    meses_dict[mes_anio][tipo] += mant['costo_total']
                except:
                    pass
        
        # Convertir a lista
        resultado = []
        for mes, costos in sorted(meses_dict.items()):
            resultado.append({
                "mes": mes,
                "costo_preventivo": costos['preventivo'],
                "costo_correctivo": costos['correctivo'],
                "costo_total": costos['preventivo'] + costos['correctivo']
            })
        
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/antiguedad-equipos")
async def get_antiguedad_equipos():
    """Obtener reporte de antigüedad de equipos"""
    try:
        response = supabase.table("equipos").select("id, codigo_inventario, nombre, fecha_compra").execute()
        
        hoy = date.today()
        
        # Clasificar por antigüedad
        antiguedad_dict = {
            "0-1 años": 0,
            "1-3 años": 0,
            "3-5 años": 0,
            "5+ años": 0,
            "sin_fecha": 0
        }
        
        for equipo in response.data:
            if equipo.get('fecha_compra'):
                try:
                    fecha_compra = datetime.strptime(equipo['fecha_compra'], '%Y-%m-%d').date()
                    antiguedad_dias = (hoy - fecha_compra).days
                    antiguedad_anios = antiguedad_dias / 365
                    
                    if antiguedad_anios < 1:
                        antiguedad_dict["0-1 años"] += 1
                    elif antiguedad_anios < 3:
                        antiguedad_dict["1-3 años"] += 1
                    elif antiguedad_anios < 5:
                        antiguedad_dict["3-5 años"] += 1
                    else:
                        antiguedad_dict["5+ años"] += 1
                except:
                    antiguedad_dict["sin_fecha"] += 1
            else:
                antiguedad_dict["sin_fecha"] += 1
        
        # Convertir a lista
        resultado = [{"rango": k, "cantidad": v} for k, v in antiguedad_dict.items()]
        
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/equipos-por-categoria")
async def get_equipos_por_categoria():
    """Obtener reporte de equipos por categoría"""
    try:
        response = supabase.table("equipos").select("*, categorias_equipos(nombre)").execute()
        
        # Agrupar por categoría
        categorias_dict = {}
        for equipo in response.data:
            if equipo.get('categorias_equipos'):
                categoria = equipo['categorias_equipos']['nombre']
                categorias_dict[categoria] = categorias_dict.get(categoria, 0) + 1
        
        # Convertir a lista
        resultado = [{"categoria": k, "cantidad": v} for k, v in categorias_dict.items()]
        resultado.sort(key=lambda x: x['cantidad'], reverse=True)
        
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/valor-por-categoria")
async def get_valor_por_categoria():
    """Obtener valor de inventario por categoría"""
    try:
        response = supabase.table("equipos").select("*, categorias_equipos(nombre)").execute()
        
        # Agrupar por categoría
        categorias_dict = {}
        for equipo in response.data:
            if equipo.get('categorias_equipos'):
                categoria = equipo['categorias_equipos']['nombre']
                costo = equipo.get('costo_compra', 0) or 0
                categorias_dict[categoria] = categorias_dict.get(categoria, 0) + costo
        
        # Convertir a lista
        resultado = [{"categoria": k, "valor_total": v} for k, v in categorias_dict.items()]
        resultado.sort(key=lambda x: x['valor_total'], reverse=True)
        
        return resultado
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
