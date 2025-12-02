import streamlit as st
import requests
import os
import pandas as pd

st.set_page_config(page_title="Proveedores", page_icon="🏢", layout="wide")

API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

st.title("🏢 Gestión de Proveedores")
st.markdown("---")

tab1, tab2 = st.tabs(["📋 Lista de Proveedores", "➕ Nuevo Proveedor"])

with tab1:
    st.markdown("### 📋 Proveedores Registrados")
    
    if st.button("🔄 Actualizar Lista"):
        try:
            response = requests.get(f"{API_URL}/api/proveedores")
            
            if response.status_code == 200:
                st.session_state['proveedores_results'] = response.json()
            else:
                st.error("Error al obtener proveedores")
        except Exception as e:
            st.error(f"Error: {e}")

    # Mostrar resultados si existen en sesión
    if 'proveedores_results' in st.session_state:
        proveedores = st.session_state['proveedores_results']
        
        if proveedores:
            # Crear DataFrame
            df_data = []
            for prov in proveedores:
                df_data.append({
                    "RUC": prov.get('ruc'),
                    "Razón Social": prov.get('razon_social'),
                    "Teléfono": prov.get('telefono', 'N/A'),
                    "Email": prov.get('email', 'N/A'),
                    "Contacto": prov.get('contacto_nombre', 'N/A'),
                    "Activo": "✅" if prov.get('activo') else "❌",
                    "ID": prov.get('id')
                })
            
            df = pd.DataFrame(df_data)
            st.success(f"✅ {len(proveedores)} proveedores encontrados")
            st.dataframe(df.drop('ID', axis=1), use_container_width=True)
            
            # Ver detalles
            st.markdown("### 🔍 Ver Detalles de Proveedor")
            
            prov_id = st.selectbox(
                "Seleccionar proveedor",
                options=df['ID'].tolist(),
                format_func=lambda x: df[df['ID'] == x]['Razón Social'].values[0]
            )
            
            if prov_id:
                with st.spinner("Cargando detalles..."):
                    try:
                        detail_response = requests.get(f"{API_URL}/api/proveedores/{prov_id}")
                        if detail_response.status_code == 200:
                            prov_detail = detail_response.json()
                            
                            st.markdown("---")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("#### 📝 Información General")
                                st.write(f"**RUC:** {prov_detail.get('ruc')}")
                                st.write(f"**Razón Social:** {prov_detail.get('razon_social')}")
                                st.write(f"**Nombre Comercial:** {prov_detail.get('nombre_comercial', 'N/A')}")
                                st.write(f"**Dirección:** {prov_detail.get('direccion', 'N/A')}")
                                st.write(f"**Teléfono:** {prov_detail.get('telefono', 'N/A')}")
                                st.write(f"**Email:** {prov_detail.get('email', 'N/A')}")
                            
                            with col2:
                                st.markdown("#### 👤 Contacto")
                                st.write(f"**Nombre:** {prov_detail.get('contacto_nombre', 'N/A')}")
                                st.write(f"**Teléfono:** {prov_detail.get('contacto_telefono', 'N/A')}")
                                st.write(f"**Email:** {prov_detail.get('contacto_email', 'N/A')}")
                                st.write(f"**Sitio Web:** {prov_detail.get('sitio_web', 'N/A')}")
                            
                            # Contratos
                            if prov_detail.get('contratos'):
                                st.markdown("#### 📄 Contratos")
                                contratos_df = pd.DataFrame(prov_detail['contratos'])
                                st.dataframe(contratos_df[['numero_contrato', 'tipo', 'fecha_inicio', 'estado']], use_container_width=True)
                            
                            # Equipos comprados
                            if prov_detail.get('equipos_comprados'):
                                st.markdown("#### 📦 Equipos Comprados")
                                equipos_df = pd.DataFrame(prov_detail['equipos_comprados'])
                                st.dataframe(equipos_df, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error al cargar detalles: {e}")
        
        else:
            st.info("No hay proveedores registrados")

with tab2:
    st.markdown("### ➕ Registrar Nuevo Proveedor")
    
    with st.form("form_nuevo_proveedor"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏢 Datos de la Empresa")
            ruc = st.text_input("RUC*", placeholder="20123456789")
            razon_social = st.text_input("Razón Social*", placeholder="Tecnología Avanzada S.A.C.")
            nombre_comercial = st.text_input("Nombre Comercial", placeholder="TechAdvance")
            direccion = st.text_area("Dirección", placeholder="Av. Principal 123")
            telefono = st.text_input("Teléfono", placeholder="044-123456")
            email = st.text_input("Email", placeholder="ventas@empresa.com")
            sitio_web = st.text_input("Sitio Web", placeholder="www.empresa.com")
        
        with col2:
            st.markdown("#### 👤 Datos del Contacto")
            contacto_nombre = st.text_input("Nombre del Contacto", placeholder="Juan Pérez")
            contacto_telefono = st.text_input("Teléfono del Contacto", placeholder="987654321")
            contacto_email = st.text_input("Email del Contacto", placeholder="jperez@empresa.com")
            
            st.markdown("#### 📊 Otros Datos")
            calificacion = st.slider("Calificación", 0.0, 5.0, 3.0, 0.5)
            notas = st.text_area("Notas / Observaciones")
        
        submitted = st.form_submit_button("💾 Guardar Proveedor", type="primary")
        
        if submitted:
            if not ruc or not razon_social:
                st.error("❌ Por favor complete los campos obligatorios (*)")
            else:
                try:
                    nuevo_proveedor = {
                        "ruc": ruc,
                        "razon_social": razon_social,
                        "nombre_comercial": nombre_comercial,
                        "direccion": direccion,
                        "telefono": telefono,
                        "email": email,
                        "contacto_nombre": contacto_nombre,
                        "contacto_telefono": contacto_telefono,
                        "contacto_email": contacto_email,
                        "sitio_web": sitio_web,
                        "calificacion": calificacion,
                        "notas": notas
                    }
                    
                    response = requests.post(f"{API_URL}/api/proveedores", json=nuevo_proveedor)
                    
                    if response.status_code == 200:
                        st.success("✅ Proveedor registrado exitosamente!")
                        st.balloons()
                    else:
                        st.error(f"❌ Error: {response.text}")
                
                except Exception as e:
                    st.error(f"❌ Error: {e}")
