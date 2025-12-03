import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from datetime import datetime

# ============================================
# PDF GENERATION FUNCTIONS
# ============================================

def create_pdf_with_chart_and_table(title, chart_fig, df):
    """Genera un PDF con un gráfico y una tabla"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Agregar título
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Agregar fecha de generación
    fecha_style = ParagraphStyle('Fecha', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10)
    fecha_texto = f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    elements.append(Paragraph(fecha_texto, fecha_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Convertir gráfico a imagen
    if chart_fig:
        try:
            # Renderizar el gráfico de Plotly a imagen PNG con alta calidad
            img_bytes = chart_fig.to_image(format="png", width=800, height=500, scale=2)
            img_buffer = BytesIO(img_bytes)
            
            # Agregar la imagen al PDF con buen tamaño
            img = Image(img_buffer, width=6.5*inch, height=4*inch)
            elements.append(img)
            elements.append(Spacer(1, 0.4*inch))
        except Exception as e:
            # Si falla la conversión, agregar un mensaje de error
            error_style = ParagraphStyle('Error', parent=styles['Normal'], textColor=colors.red)
            elements.append(Paragraph(f"Error al renderizar grafico: {str(e)}", error_style))
            elements.append(Spacer(1, 0.2*inch))
    
    # Agregar tabla de datos
    if df is not None and not df.empty:
        elements.append(Paragraph("Datos del Reporte", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Convertir DataFrame a lista para la tabla
        data = [df.columns.tolist()] + df.values.tolist()
        
        # Calcular ancho de columnas dinámicamente
        num_cols = len(df.columns)
        col_width = 6.5 * inch / num_cols
        
        # Crear tabla
        table = Table(data, colWidths=[col_width] * num_cols)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))
        
        elements.append(table)
    
    # Generar PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def create_dashboard_pdf(dashboard_data):
    """Genera un PDF con las métricas del dashboard"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1f77b4'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    elements.append(Paragraph("Dashboard de Metricas - Sistema de Gestion TI", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Fecha
    fecha_style = ParagraphStyle('Fecha', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10)
    fecha_texto = f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    elements.append(Paragraph(fecha_texto, fecha_style))
    elements.append(Spacer(1, 0.4*inch))
    
    # Métricas principales
    elements.append(Paragraph("Metricas Principales", styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))
    
    metricas_data = [
        ['Metrica', 'Valor'],
        ['Total Equipos', str(dashboard_data.get('total_equipos', 0))],
        ['Equipos Operativos', str(dashboard_data.get('equipos_operativos', 0))],
        ['Equipos en Reparacion', str(dashboard_data.get('equipos_reparacion', 0))],
        ['Tasa de Disponibilidad', f"{dashboard_data.get('tasa_disponibilidad', 0)}%"],
        ['Valor Inventario', f"S/. {dashboard_data.get('valor_inventario', 0):,.2f}"],
        ['Mantenimientos (Mes)', str(dashboard_data.get('mantenimientos_mes', 0))],
        ['Costo Mantenimiento (Mes)', f"S/. {dashboard_data.get('costo_mantenimiento_mes', 0):,.2f}"]
    ]
    
    table = Table(metricas_data, colWidths=[3.5*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('PADDING', (0, 0), (-1, -1), 8)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Pie de página
    footer_style = ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Sistema de Gestion de Equipos de TI - Universidad", footer_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

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
        
        # Botón de descarga PDF para dashboard
        st.markdown("---")
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            pdf_buffer = create_dashboard_pdf(dashboard)
            st.download_button(
                label="📥 Descargar Dashboard en PDF",
                data=pdf_buffer,
                file_name=f"dashboard_metricas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

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
                
                # Botón de descarga PDF
                pdf_buffer = create_pdf_with_chart_and_table(
                    "Equipos por Ubicacion",
                    fig,
                    df
                )
                st.download_button(
                    label="📥 Descargar Reporte en PDF",
                    data=pdf_buffer,
                    file_name=f"equipos_ubicacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
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
                
                # Botón de descarga PDF
                pdf_buffer = create_pdf_with_chart_and_table(
                    "Equipos por Estado Operativo",
                    fig,
                    df
                )
                st.download_button(
                    label="📥 Descargar Reporte en PDF",
                    data=pdf_buffer,
                    file_name=f"equipos_estado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
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
                
                # Botón de descarga PDF
                st.markdown("---")
                pdf_buffer = create_pdf_with_chart_and_table(
                    "Costos de Mantenimiento",
                    fig,
                    df
                )
                st.download_button(
                    label="📥 Descargar Reporte en PDF",
                    data=pdf_buffer,
                    file_name=f"costos_mantenimiento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
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
                
                # Botón de descarga PDF
                pdf_buffer = create_pdf_with_chart_and_table(
                    "Antiguedad de Equipos",
                    fig,
                    df
                )
                st.download_button(
                    label="📥 Descargar Reporte en PDF",
                    data=pdf_buffer,
                    file_name=f"antiguedad_equipos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
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
                
                # Botón de descarga PDF
                pdf_buffer = create_pdf_with_chart_and_table(
                    "Equipos por Categoria",
                    fig,
                    df
                )
                st.download_button(
                    label="📥 Descargar PDF",
                    data=pdf_buffer,
                    file_name=f"equipos_categoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="btn_cat1"
                )
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
                
                # Botón de descarga PDF
                pdf_buffer = create_pdf_with_chart_and_table(
                    "Valor por Categoria",
                    fig,
                    df
                )
                st.download_button(
                    label="📥 Descargar PDF",
                    data=pdf_buffer,
                    file_name=f"valor_categoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="btn_cat2"
                )
    except:
        st.error("Error al cargar datos")
