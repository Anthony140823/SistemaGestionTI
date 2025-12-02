import streamlit as st
import requests
import os
import pandas as pd
from datetime import date

st.set_page_config(page_title="Equipos", page_icon="📦", layout="wide")

API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

st.title("📦 Gestión de Equipos")
st.markdown("---")

# Tabs para diferentes funciones
tab1, tab2, tab3 = st.tabs(["📋 Lista de Equipos", "➕ Nuevo Equipo", "📊 Estadísticas"])

with tab1:
    st.markdown("### 📋 Inventario de Equipos")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        estado_filter = st.selectbox(
            "Estado",
            ["Todos", "operativo", "en_reparacion", "obsoleto", "de_baja"]
        )
    
    with col2:
        # Obtener categorías
        try:
            categorias_response = requests.get(f"{API_URL}/api/categorias")
            if categorias_response.status_code == 200:
                categorias = categorias_response.json()
                categoria_nombres = ["Todas"] + [c['nombre'] for c in categorias]
                categoria_filter = st.selectbox("Categoría", categoria_nombres)
            else:
                categoria_filter = "Todas"
        except:
            categoria_filter = "Todas"
    
    with col3:
        # Obtener ubicaciones
        try:
            ubicaciones_response = requests.get(f"{API_URL}/api/ubicaciones")
            if ubicaciones_response.status_code == 200:
                ubicaciones = ubicaciones_response.json()
                ubicacion_nombres = ["Todas"] + [u['nombre_completo'] for u in ubicaciones]
                ubicacion_filter = st.selectbox("Ubicación", ubicacion_nombres)
            else:
                ubicacion_filter = "Todas"
        except:
            ubicacion_filter = "Todas"
    
    # Botón de búsqueda
    if st.button("🔍 Buscar", type="primary"):
        try:
            params = {}
            if estado_filter != "Todos":
                params['estado'] = estado_filter
            
            response = requests.get(f"{API_URL}/api/equipos", params=params)
            
            if response.status_code == 200:
                st.session_state['equipos_results'] = response.json()
            else:
                st.error("Error al obtener equipos")
        except Exception as e:
            st.error(f"Error: {e}")

    # Mostrar resultados si existen en sesión
    if 'equipos_results' in st.session_state:
        equipos = st.session_state['equipos_results']
        
        if equipos:
            # Crear DataFrame
            df_data = []
            for eq in equipos:
                df_data.append({
                    "Código": eq.get('codigo_inventario', 'N/A'),
                    "Nombre": eq.get('nombre', 'N/A'),
                    "Marca": eq.get('marca', 'N/A'),
                    "Modelo": eq.get('modelo', 'N/A'),
                    "Categoría": eq.get('categorias_equipos', {}).get('nombre', 'N/A') if eq.get('categorias_equipos') else 'N/A',
                    "Estado": eq.get('estado_operativo', 'N/A'),
                    "Ubicación": eq.get('ubicaciones', {}).get('edificio', 'N/A') if eq.get('ubicaciones') else 'N/A',
                    "ID": eq.get('id')
                })
            
            df = pd.DataFrame(df_data)
            
            st.success(f"✅ Se encontraron {len(equipos)} equipos")
            
            # Mostrar tabla
            st.dataframe(df.drop('ID', axis=1), use_container_width=True)
            
            # Detalles de equipo seleccionado
            st.markdown("### 🔍 Ver Detalles")
            
            equipo_seleccionado = st.selectbox(
                "Seleccionar equipo",
                options=df['ID'].tolist(),
                format_func=lambda x: df[df['ID'] == x]['Nombre'].values[0]
            )
            
            if equipo_seleccionado:
                # Usar clave única para el spinner para evitar conflictos
                with st.spinner("Cargando detalles..."):
                    try:
                        detail_response = requests.get(f"{API_URL}/api/equipos/{equipo_seleccionado}")
                        if detail_response.status_code == 200:
                            equipo_detail = detail_response.json()
                            
                            st.markdown("---")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("#### 📝 Información General")
                                st.write(f"**Código:** {equipo_detail.get('codigo_inventario')}")
                                st.write(f"**Nombre:** {equipo_detail.get('nombre')}")
                                st.write(f"**Marca:** {equipo_detail.get('marca', 'N/A')}")
                                st.write(f"**Modelo:** {equipo_detail.get('modelo', 'N/A')}")
                                st.write(f"**Serie:** {equipo_detail.get('numero_serie', 'N/A')}")
                                st.write(f"**Estado:** {equipo_detail.get('estado_operativo')}")
                            
                            with col2:
                                st.markdown("#### 💰 Información Financiera")
                                st.write(f"**Fecha Compra:** {equipo_detail.get('fecha_compra', 'N/A')}")
                                st.write(f"**Costo:** S/. {equipo_detail.get('costo_compra', 0):,.2f}")
                                st.write(f"**Garantía hasta:** {equipo_detail.get('fecha_garantia_fin', 'N/A')}")
                                
                                if equipo_detail.get('proveedores'):
                                    st.write(f"**Proveedor:** {equipo_detail['proveedores'].get('razon_social', 'N/A')}")
                            
                            # Historial de movimientos
                            if equipo_detail.get('historial_movimientos'):
                                st.markdown("#### 📍 Historial de Movimientos")
                                movimientos_df = pd.DataFrame(equipo_detail['historial_movimientos'])
                                st.dataframe(movimientos_df[['fecha_movimiento', 'motivo', 'observaciones']], use_container_width=True)
                    except Exception as e:
                        st.error(f"Error al cargar detalles: {e}")
        
        else:
            st.info("No se encontraron equipos con los filtros seleccionados")

with tab2:
    st.markdown("### ➕ Registrar Nuevo Equipo")
    
    with st.form("form_nuevo_equipo"):
        col1, col2 = st.columns(2)
        
        with col1:
            codigo = st.text_input("Código de Inventario*", placeholder="PC-2024-001")
            nombre = st.text_input("Nombre del Equipo*", placeholder="Computadora HP ProDesk")
            marca = st.text_input("Marca", placeholder="HP")
            modelo = st.text_input("Modelo", placeholder="ProDesk 400 G7")
            numero_serie = st.text_input("Número de Serie", placeholder="SN123456789")
            
            # Obtener categorías
            try:
                categorias_response = requests.get(f"{API_URL}/api/categorias")
                if categorias_response.status_code == 200:
                    categorias = categorias_response.json()
                    categoria_id = st.selectbox(
                        "Categoría*",
                        options=[c['id'] for c in categorias],
                        format_func=lambda x: next(c['nombre'] for c in categorias if c['id'] == x)
                    )
                else:
                    categoria_id = None
                    st.error("No se pudieron cargar las categorías")
            except:
                categoria_id = None
                st.error("Error al cargar categorías")
        
        with col2:
            fecha_compra = st.date_input("Fecha de Compra")
            costo_compra = st.number_input("Costo de Compra (S/.)", min_value=0.0, step=100.0)
            fecha_garantia = st.date_input("Fecha Fin de Garantía")
            
            estado_operativo = st.selectbox(
                "Estado Operativo",
                ["operativo", "en_reparacion", "obsoleto", "de_baja"]
            )
            
            estado_fisico = st.selectbox(
                "Estado Físico",
                ["excelente", "bueno", "regular", "malo"]
            )
            
            # Obtener ubicaciones
            try:
                ubicaciones_response = requests.get(f"{API_URL}/api/ubicaciones")
                if ubicaciones_response.status_code == 200:
                    ubicaciones = ubicaciones_response.json()
                    ubicacion_id = st.selectbox(
                        "Ubicación",
                        options=[u['id'] for u in ubicaciones],
                        format_func=lambda x: next(u['nombre_completo'] for u in ubicaciones if u['id'] == x)
                    )
                else:
                    ubicacion_id = None
            except:
                ubicacion_id = None
        
        notas = st.text_area("Notas / Observaciones")
        
        submitted = st.form_submit_button("💾 Guardar Equipo", type="primary")
        
        if submitted:
            if not codigo or not nombre or not categoria_id:
                st.error("❌ Por favor complete los campos obligatorios (*)")
            else:
                try:
                    nuevo_equipo = {
                        "codigo_inventario": codigo,
                        "categoria_id": categoria_id,
                        "nombre": nombre,
                        "marca": marca,
                        "modelo": modelo,
                        "numero_serie": numero_serie,
                        "fecha_compra": str(fecha_compra),
                        "costo_compra": costo_compra,
                        "fecha_garantia_fin": str(fecha_garantia),
                        "ubicacion_actual_id": ubicacion_id,
                        "estado_operativo": estado_operativo,
                        "estado_fisico": estado_fisico,
                        "notas": notas
                    }
                    
                    response = requests.post(f"{API_URL}/api/equipos", json=nuevo_equipo)
                    
                    if response.status_code == 200:
                        st.success("✅ Equipo registrado exitosamente!")
                        st.balloons()
                    else:
                        st.error(f"❌ Error al registrar equipo: {response.text}")
                
                except Exception as e:
                    st.error(f"❌ Error: {e}")

with tab3:
    st.markdown("### 📊 Estadísticas de Equipos")
    
    try:
        # Equipos por estado
        response = requests.get(f"{API_URL}/api/reportes/equipos-por-estado")
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                st.bar_chart(df.set_index('estado'))
        
        # Equipos por ubicación
        response = requests.get(f"{API_URL}/api/reportes/equipos-por-ubicacion")
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                st.bar_chart(df.set_index('ubicacion'))
    
    except Exception as e:
        st.error(f"Error al cargar estadísticas: {e}")
