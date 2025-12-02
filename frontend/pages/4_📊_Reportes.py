import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Reportes", page_icon="📊", layout="wide")

API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

st.title("📊 Reportes y Análisis")
st.markdown("---")

# Dashboard de métricas
st.markdown("### 📈 Dashboard de Métricas")

try:
    response = requests.get(f"{API_URL}/api/reportes/dashboard")
    
    if response.status_code == 200:
        dashboard = response.json()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Total Equipos", dashboard.get('total_equipos', 0))
        
        with col2:
            st.metric("✅ Disponibilidad", f"{dashboard.get('tasa_disponibilidad', 0)}%")
        
        with col3:
            st.metric("💰 Valor Inventario", f"S/. {dashboard.get('valor_inventario', 0):,.2f}")
        
        with col4:
            st.metric("🔧 Mantenimientos (Mes)", dashboard.get('mantenimientos_mes', 0))

except Exception as e:
    st.error(f"Error al cargar dashboard: {e}")

st.markdown("---")

# Tabs para diferentes reportes
tab1, tab2, tab3, tab4 = st.tabs(["📍 Por Ubicación", "📊 Por Estado", "💰 Costos", "📅 Antigüedad"])

with tab1:
    st.markdown("### 📍 Equipos por Ubicación")
    
    try:
        response = requests.get(f"{API_URL}/api/reportes/equipos-por-ubicacion")
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                df = pd.DataFrame(data)
                
                # Gráfico de barras
                fig = px.bar(
                    df,
                    x='ubicacion',
                    y='cantidad',
                    title='Distribución de Equipos por Ubicación',
                    labels={'ubicacion': 'Ubicación', 'cantidad': 'Cantidad de Equipos'},
                    color='cantidad',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabla de datos
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No hay datos disponibles")
    
    except Exception as e:
        st.error(f"Error: {e}")

with tab2:
    st.markdown("### 📊 Equipos por Estado Operativo")
    
    try:
        response = requests.get(f"{API_URL}/api/reportes/equipos-por-estado")
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                df = pd.DataFrame(data)
                
                # Gráfico de pastel
                fig = px.pie(
                    df,
                    values='cantidad',
                    names='estado',
                    title='Distribución de Equipos por Estado',
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabla de datos
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No hay datos disponibles")
    
    except Exception as e:
        st.error(f"Error: {e}")

with tab3:
    st.markdown("### 💰 Costos de Mantenimiento")
    
    try:
        response = requests.get(f"{API_URL}/api/reportes/costos-mantenimiento")
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                df = pd.DataFrame(data)
                
                # Gráfico de líneas
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=df['mes'],
                    y=df['costo_preventivo'],
                    mode='lines+markers',
                    name='Preventivo',
                    line=dict(color='green', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=df['mes'],
                    y=df['costo_correctivo'],
                    mode='lines+markers',
                    name='Correctivo',
                    line=dict(color='red', width=2)
                ))
                
                fig.update_layout(
                    title='Costos de Mantenimiento por Mes',
                    xaxis_title='Mes',
                    yaxis_title='Costo (S/.)',
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabla de datos
                st.dataframe(df, use_container_width=True)
                
                # Resumen
                total_preventivo = df['costo_preventivo'].sum()
                total_correctivo = df['costo_correctivo'].sum()
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("💚 Total Preventivo", f"S/. {total_preventivo:,.2f}")
                
                with col2:
                    st.metric("❤️ Total Correctivo", f"S/. {total_correctivo:,.2f}")
                
                with col3:
                    st.metric("💰 Total General", f"S/. {total_preventivo + total_correctivo:,.2f}")
            else:
                st.info("No hay datos disponibles")
    
    except Exception as e:
        st.error(f"Error: {e}")

with tab4:
    st.markdown("### 📅 Antigüedad de Equipos")
    
    try:
        response = requests.get(f"{API_URL}/api/reportes/antiguedad-equipos")
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                df = pd.DataFrame(data)
                
                # Gráfico de barras horizontales
                fig = px.bar(
                    df,
                    x='cantidad',
                    y='rango',
                    orientation='h',
                    title='Distribución de Equipos por Antigüedad',
                    labels={'rango': 'Rango de Antigüedad', 'cantidad': 'Cantidad de Equipos'},
                    color='cantidad',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabla de datos
                st.dataframe(df, use_container_width=True)
                
                # Alertas
                equipos_5_plus = df[df['rango'] == '5+ años']['cantidad'].values
                if len(equipos_5_plus) > 0 and equipos_5_plus[0] > 0:
                    st.warning(f"⚠️ Hay {equipos_5_plus[0]} equipos con más de 5 años. Considere su reemplazo.")
            else:
                st.info("No hay datos disponibles")
    
    except Exception as e:
        st.error(f"Error: {e}")

# Sección adicional: Reportes por categoría
st.markdown("---")
st.markdown("### 📦 Análisis por Categoría")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Cantidad por Categoría")
    try:
        response = requests.get(f"{API_URL}/api/reportes/equipos-por-categoria")
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                df = pd.DataFrame(data)
                fig = px.bar(df, x='categoria', y='cantidad', color='cantidad')
                st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Error al cargar datos")

with col2:
    st.markdown("#### Valor por Categoría")
    try:
        response = requests.get(f"{API_URL}/api/reportes/valor-por-categoria")
        
        if response.status_code == 200:
            data = response.json()
            
            if data:
                df = pd.DataFrame(data)
                fig = px.pie(df, values='valor_total', names='categoria', title='Valor de Inventario por Categoría')
                st.plotly_chart(fig, use_container_width=True)
    except:
        st.error("Error al cargar datos")
