import streamlit as st
import requests
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Gestión TI - Universidad",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL del API Gateway
API_URL = os.getenv("API_GATEWAY_URL", "http://api-gateway:8000")

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def get_dashboard_data():
    """Obtiene los datos del dashboard"""
    try:
        response = requests.get(f"{API_URL}/api/reportes/dashboard", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error al obtener datos del dashboard: {e}")
        return None

def get_notificaciones():
    """Obtiene las notificaciones no leídas"""
    try:
        response = requests.get(f"{API_URL}/api/agents/notificaciones?leida=false", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

# Título principal
st.markdown('<h1 class="main-header">🖥️ Sistema de Gestión de Equipos de TI</h1>', unsafe_allow_html=True)
st.markdown("### Universidad - Centro de Tecnología de Información")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/667eea/ffffff?text=UNIVERSIDAD")
    st.markdown("### 👤 Usuario")
    st.info("**Administrador**\\nadmin@universidad.edu")
    
    st.markdown("---")
    st.markdown("### 🔔 Notificaciones")
    notificaciones = get_notificaciones()
    if notificaciones:
        st.warning(f"**{len(notificaciones)}** notificaciones pendientes")
        with st.expander("Ver notificaciones"):
            for notif in notificaciones[:5]:
                st.markdown(f"**{notif.get('titulo', 'Sin título')}**")
                st.caption(notif.get('mensaje', '')[:100] + "...")
                st.divider()
    else:
        st.success("✅ Sin notificaciones pendientes")
    
    st.markdown("---")
    st.markdown("### ⚙️ Sistema")
    if st.button("🔄 Ejecutar Agentes", use_container_width=True):
        with st.spinner("Ejecutando agentes inteligentes..."):
            try:
                response = requests.post(f"{API_URL}/api/agents/run-all-agents", timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ Agentes ejecutados: {result.get('total_notificaciones_creadas', 0)} notificaciones creadas")
                    st.rerun()
                else:
                    st.error("❌ Error al ejecutar agentes")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# Dashboard principal
dashboard_data = get_dashboard_data()

if dashboard_data:
    # Métricas principales
    st.markdown("### 📊 Métricas Principales")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📦 Total Equipos",
            value=dashboard_data.get("total_equipos", 0),
            delta=None
        )
    
    with col2:
        disponibilidad = dashboard_data.get("tasa_disponibilidad", 0)
        st.metric(
            label="✅ Disponibilidad",
            value=f"{disponibilidad}%",
            delta=f"{disponibilidad - 95:.1f}%" if disponibilidad else None
        )
    
    with col3:
        valor = dashboard_data.get("valor_inventario", 0)
        st.metric(
            label="💰 Valor Inventario",
            value=f"S/. {valor:,.2f}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="🔧 Mantenimientos (Mes)",
            value=dashboard_data.get("mantenimientos_mes", 0),
            delta=None
        )
    
    st.markdown("---")
    
    # Segunda fila de métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        operativos = dashboard_data.get("equipos_operativos", 0)
        st.metric(
            label="🟢 Equipos Operativos",
            value=operativos
        )
    
    with col2:
        reparacion = dashboard_data.get("equipos_reparacion", 0)
        st.metric(
            label="🔴 En Reparación",
            value=reparacion
        )
    
    with col3:
        costo = dashboard_data.get("costo_mantenimiento_mes", 0)
        st.metric(
            label="💵 Costo Mantenim. (Mes)",
            value=f"S/. {costo:,.2f}"
        )
    
    st.markdown("---")
    
    # Información rápida
    st.markdown("### 📋 Información del Sistema")
    
    tab1, tab2, tab3 = st.tabs(["🎯 Resumen", "📈 Estado", "ℹ️ Acerca de"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Estado del Inventario")
            total = dashboard_data.get("total_equipos", 1)
            operativos = dashboard_data.get("equipos_operativos", 0)
            reparacion = dashboard_data.get("equipos_reparacion", 0)
            
            st.progress(operativos / total if total > 0 else 0)
            st.caption(f"Equipos Operativos: {operativos}/{total}")
            
            if reparacion > 0:
                st.warning(f"⚠️ {reparacion} equipos en reparación")
            else:
                st.success("✅ Todos los equipos operativos")
        
        with col2:
            st.markdown("#### 🔧 Mantenimientos")
            st.info(f"📅 {dashboard_data.get('mantenimientos_mes', 0)} programados este mes")
            st.info(f"💵 Costo mensual: S/. {dashboard_data.get('costo_mantenimiento_mes', 0):,.2f}")
    
    with tab2:
        st.markdown("#### 📊 Indicadores de Rendimiento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Tasa de Disponibilidad", f"{dashboard_data.get('tasa_disponibilidad', 0)}%")
            if dashboard_data.get('tasa_disponibilidad', 0) >= 95:
                st.success("✅ Excelente disponibilidad")
            elif dashboard_data.get('tasa_disponibilidad', 0) >= 85:
                st.warning("⚠️ Disponibilidad aceptable")
            else:
                st.error("❌ Disponibilidad baja")
        
        with col2:
            st.metric("Equipos Totales", dashboard_data.get("total_equipos", 0))
            st.metric("Valor Total", f"S/. {dashboard_data.get('valor_inventario', 0):,.2f}")
    
    with tab3:
        st.markdown("""
        ### 🖥️ Sistema de Gestión de Equipos de TI
        
        **Versión:** 1.0.0  
        **Última actualización:** Diciembre 2024
        
        #### 🎯 Características:
        - ✅ Gestión integral de inventario de equipos
        - ✅ Control de mantenimientos preventivos y correctivos
        - ✅ Administración de proveedores y contratos
        - ✅ Reportes y análisis avanzados con gráficos
        - ✅ Agentes inteligentes de automatización
        - ✅ Alertas y notificaciones en tiempo real
        - ✅ Historial completo de movimientos
        
        #### 🛠️ Tecnologías:
        - **Frontend:** Streamlit (Python)
        - **Backend:** Microservicios con FastAPI
        - **Base de datos:** Supabase (PostgreSQL)
        - **Despliegue:** Docker & Docker Compose
        
        #### 📚 Módulos:
        1. **Equipos:** Gestión completa del inventario
        2. **Proveedores:** Administración de proveedores y contratos
        3. **Mantenimiento:** Programación y seguimiento
        4. **Reportes:** Análisis y visualización de datos
        
        ---
        **Desarrollado para:** Universidad - Departamento de TI  
        **Contacto:** ti@universidad.edu
        """)

else:
    st.error("⚠️ No se pudo conectar con el servidor. Verifique que todos los servicios estén activos.")
    st.info("💡 **Pasos para solucionar:**")
    st.code("""
    1. Verifique que Docker Desktop esté corriendo
    2. Ejecute: docker-compose up -d
    3. Espere 30 segundos a que los servicios inicien
    4. Recargue esta página
    """)
    
    with st.expander("🔍 Ver detalles técnicos"):
        st.code(f"API Gateway URL: {API_URL}")
        st.code("Servicios esperados: api-gateway, equipos-service, proveedores-service, mantenimiento-service, reportes-service, agent-service")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("📧 Soporte: ti@universidad.edu")
with col2:
    st.caption(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
with col3:
    st.caption("🔒 Sistema Seguro")


# http://localhost:8501