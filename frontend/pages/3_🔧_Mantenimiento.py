import streamlit as st
import requests
import os
import pandas as pd
from datetime import date

st.set_page_config(page_title="Mantenimiento", page_icon="🔧", layout="wide")

API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

st.title("🔧 Gestión de Mantenimientos")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📋 Mantenimientos", "➕ Programar Mantenimiento", "📅 Calendario"])

with tab1:
    st.markdown("### 📋 Lista de Mantenimientos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        estado_filter = st.selectbox(
            "Estado",
            ["Todos", "programado", "en_proceso", "completado", "cancelado"]
        )
    
    with col2:
        tipo_filter = st.selectbox(
            "Tipo",
            ["Todos", "preventivo", "correctivo"]
        )
    
    if st.button("🔍 Buscar"):
        try:
            params = {}
            if estado_filter != "Todos":
                params['estado'] = estado_filter
            if tipo_filter != "Todos":
                params['tipo'] = tipo_filter
            
            response = requests.get(f"{API_URL}/api/mantenimientos", params=params)
            
            if response.status_code == 200:
                st.session_state['mantenimientos_results'] = response.json()
            else:
                st.error("Error al obtener mantenimientos")
        except Exception as e:
            st.error(f"Error: {e}")

    # Mostrar resultados si existen en sesión
    if 'mantenimientos_results' in st.session_state:
        mantenimientos = st.session_state['mantenimientos_results']
        
        if mantenimientos:
            # Crear DataFrame
            df_data = []
            for mant in mantenimientos:
                df_data.append({
                    "Equipo": mant.get('equipos', {}).get('nombre', 'N/A') if mant.get('equipos') else 'N/A',
                    "Tipo": mant.get('tipo'),
                    "Fecha Programada": mant.get('fecha_programada'),
                    "Estado": mant.get('estado'),
                    "Técnico": mant.get('tecnico_responsable', 'N/A'),
                    "Costo": f"S/. {mant.get('costo_total', 0):,.2f}" if mant.get('costo_total') else 'N/A',
                    "ID": mant.get('id')
                })
            
            df = pd.DataFrame(df_data)
            st.success(f"✅ {len(mantenimientos)} mantenimientos encontrados")
            st.dataframe(df.drop('ID', axis=1), use_container_width=True)
        
        else:
            st.info("No se encontraron mantenimientos")

with tab2:
    st.markdown("### ➕ Programar Nuevo Mantenimiento")
    
    with st.form("form_nuevo_mantenimiento"):
        # Obtener equipos
        try:
            equipos_response = requests.get(f"{API_URL}/api/equipos")
            if equipos_response.status_code == 200:
                equipos = equipos_response.json()
                equipo_id = st.selectbox(
                    "Equipo*",
                    options=[e['id'] for e in equipos],
                    format_func=lambda x: next(e['nombre'] for e in equipos if e['id'] == x)
                )
            else:
                equipo_id = None
                st.error("No se pudieron cargar los equipos")
        except:
            equipo_id = None
            st.error("Error al cargar equipos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tipo = st.selectbox("Tipo de Mantenimiento*", ["preventivo", "correctivo"])
            fecha_programada = st.date_input("Fecha Programada*")
            tecnico = st.text_input("Técnico Responsable", placeholder="Nombre del técnico")
        
        with col2:
            # Obtener proveedores
            try:
                proveedores_response = requests.get(f"{API_URL}/api/proveedores")
                if proveedores_response.status_code == 200:
                    proveedores = proveedores_response.json()
                    proveedor_options = [None] + [p['id'] for p in proveedores]
                    proveedor_id = st.selectbox(
                        "Proveedor (opcional)",
                        options=proveedor_options,
                        format_func=lambda x: "Ninguno" if x is None else next(p['razon_social'] for p in proveedores if p['id'] == x)
                    )
                else:
                    proveedor_id = None
            except:
                proveedor_id = None
            
            diagnostico = st.text_area("Diagnóstico / Descripción")
            observaciones = st.text_area("Observaciones")
        
        submitted = st.form_submit_button("💾 Programar Mantenimiento", type="primary")
        
        if submitted:
            if not equipo_id or not tipo or not fecha_programada:
                st.error("❌ Por favor complete los campos obligatorios (*)")
            else:
                try:
                    nuevo_mantenimiento = {
                        "equipo_id": equipo_id,
                        "tipo": tipo,
                        "fecha_programada": str(fecha_programada),
                        "proveedor_id": proveedor_id,
                        "tecnico_responsable": tecnico,
                        "diagnostico": diagnostico,
                        "observaciones": observaciones
                    }
                    
                    response = requests.post(f"{API_URL}/api/mantenimientos", json=nuevo_mantenimiento)
                    
                    if response.status_code == 200:
                        st.success("✅ Mantenimiento programado exitosamente!")
                        st.balloons()
                    else:
                        st.error(f"❌ Error: {response.text}")
                
                except Exception as e:
                    st.error(f"❌ Error: {e}")

with tab3:
    st.markdown("### 📅 Calendario de Mantenimientos")
    
    try:
        response = requests.get(f"{API_URL}/api/mantenimientos/calendario")
        
        if response.status_code == 200:
            calendario = response.json()
            
            if calendario:
                st.success(f"📅 {len(calendario)} mantenimientos programados en los próximos 30 días")
                
                df_data = []
                for mant in calendario:
                    df_data.append({
                        "Fecha": mant.get('fecha_programada'),
                        "Equipo": mant.get('equipos', {}).get('nombre', 'N/A') if mant.get('equipos') else 'N/A',
                        "Código": mant.get('equipos', {}).get('codigo_inventario', 'N/A') if mant.get('equipos') else 'N/A',
                        "Tipo": mant.get('tipo'),
                        "Técnico": mant.get('tecnico_responsable', 'N/A')
                    })
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No hay mantenimientos programados en los próximos 30 días")
        else:
            st.error(f"Error al obtener calendario: {response.status_code} - {response.text}")
    
    except Exception as e:
        st.error(f"Error: {e}")
    
    # Estadísticas
    st.markdown("### 📊 Estadísticas de Mantenimientos")
    
    try:
        response = requests.get(f"{API_URL}/api/mantenimientos/estadisticas")
        
        if response.status_code == 200:
            stats = response.json()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total", stats.get('total', 0))
            
            with col2:
                st.metric("Programados", stats.get('programados', 0))
            
            with col3:
                st.metric("Completados", stats.get('completados', 0))
            
            with col4:
                st.metric("Costo Total", f"S/. {stats.get('costo_total', 0):,.2f}")
    
    except Exception as e:
        st.error(f"Error al cargar estadísticas: {e}")
