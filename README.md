# 🖥️ Sistema de Gestión de Equipos de TI - Universidad

Sistema integral para la gestión de equipos de tecnología en universidades públicas, implementado con arquitectura de microservicios, Streamlit y Supabase.

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura](#arquitectura)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso del Sistema](#uso-del-sistema)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Solución de Problemas](#solución-de-problemas)

---

## ✨ Características

### 🎯 Funcionalidades Core

#### 1. Gestión de Equipos
- ✅ Inventario completo con código de barras/QR
- ✅ Historial de asignaciones y movimientos
- ✅ Rastreo de ubicación física
- ✅ Estados operativos (Operativo, En reparación, Obsoleto, De baja)
- ✅ Especificaciones técnicas en formato JSON

#### 2. Gestión de Proveedores
- ✅ Registro CRUD de proveedores
- ✅ Historial de compras
- ✅ Gestión de contratos
- ✅ Información de contacto y calificación

#### 3. Gestión de Mantenimientos
- ✅ Mantenimientos preventivos y correctivos
- ✅ Calendario de programación
- ✅ Historial de costos y reparaciones
- ✅ Seguimiento de técnicos responsables

#### 4. Reportes y Análisis
- ✅ Dashboard interactivo con métricas clave
- ✅ Gráficos estadísticos (Barras, Líneas, Torta)
- ✅ Análisis por ubicación, estado, categoría
- ✅ Reportes de costos y antigüedad

#### 5. Agentes Inteligentes
- ✅ Alertas de mantenimientos próximos
- ✅ Notificaciones de garantías por vencer
- ✅ Detección de equipos obsoletos
- ✅ Alertas de mantenimientos atrasados

---

## 🏗️ Arquitectura

### Microservicios

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                      │
│                      Puerto: 8501                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    API GATEWAY                               │
│                      Puerto: 8000                            │
└──────┬──────┬──────┬──────┬──────┬────────────────────────┘
       │      │      │      │      │
       ▼      ▼      ▼      ▼      ▼
    ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
    │8001│ │8002│ │8003│ │8004│ │8005│
    └────┘ └────┘ └────┘ └────┘ └────┘
    Equipos Prov. Mant. Report Agent
    
                       │
                       ▼
              ┌──────────────────┐
              │   SUPABASE       │
              │   (PostgreSQL)   │
              └──────────────────┘
```

### Servicios

1. **Frontend (Streamlit)** - Puerto 8501
   - Interfaz de usuario web
   - Dashboards interactivos
   - Formularios de gestión

2. **API Gateway** - Puerto 8000
   - Punto de entrada único
   - Enrutamiento de peticiones
   - Documentación automática (Swagger)

3. **Equipos Service** - Puerto 8001
   - Gestión de inventario
   - Movimientos de equipos
   - Categorías y ubicaciones

4. **Proveedores Service** - Puerto 8002
   - Gestión de proveedores
   - Contratos
   - Historial de compras

5. **Mantenimiento Service** - Puerto 8003
   - CRUD de mantenimientos
   - Calendario
   - Estadísticas de costos

6. **Reportes Service** - Puerto 8004
   - Dashboard de métricas
   - Gráficos estadísticos
   - Análisis de datos

7. **Agent Service** - Puerto 8005
   - Agentes inteligentes
   - Notificaciones automáticas
   - Alertas programadas

---

## 📋 Requisitos Previos

### 1. Docker y Docker Compose

**⚠️ IMPORTANTE:** Si nunca has usado Docker, lee primero la guía completa:
- 📖 **[GUIA_DOCKER.md](./GUIA_DOCKER.md)** - Explicación detallada de Docker

**Instalación:**
- **Windows/Mac:** [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux:** Docker Engine + Docker Compose

**Verificar instalación:**
```bash
docker --version
docker-compose --version
```

### 2. Cuenta de Supabase

**⚠️ IMPORTANTE:** Necesitas crear una cuenta y proyecto en Supabase:
- 📖 **[GUIA_SUPABASE.md](./GUIA_SUPABASE.md)** - Guía completa de configuración

**Pasos rápidos:**
1. Crear cuenta en [supabase.com](https://supabase.com)
2. Crear nuevo proyecto
3. Ejecutar el script SQL (ver guía)
4. Copiar credenciales (URL y API Key)

---

## 🚀 Instalación y Configuración

### Paso 1: Clonar o Descargar el Proyecto

Si tienes el proyecto en una carpeta, navega a ella:

```bash
cd "C:\Users\ANTHONY\Documents\CLASES UNT\CICLO_8\INGENIERÍA DE SOFTWARE\SEMANA 14\EXAMEN III\Examen de Laboratorio Unidad III"
```

### Paso 2: Configurar Variables de Entorno

1. **Copiar el archivo de ejemplo:**

```bash
copy .env.example .env
```

2. **Editar el archivo `.env`:**

```bash
notepad .env
```

3. **Configurar tus credenciales de Supabase:**

```env
# Reemplaza estos valores con tus credenciales reales
SUPABASE_URL=https://tu-proyecto-id.supabase.co
SUPABASE_KEY=tu-anon-key-aqui
```

**¿Dónde encontrar estas credenciales?**
- Ve a tu proyecto en Supabase
- Settings → API
- Copia "Project URL" y "anon/public key"

### Paso 3: Construir las Imágenes Docker

```bash
docker-compose build
```

**Qué hace:** Crea las imágenes de todos los servicios (puede tardar 5-10 minutos la primera vez)

**Salida esperada:**
```
Building api-gateway...
Building equipos-service...
Building proveedores-service...
...
Successfully built
```

### Paso 4: Iniciar los Servicios

```bash
docker-compose up -d
```

**Qué hace:** 
- Inicia todos los contenedores en segundo plano
- Conecta los servicios entre sí
- Expone los puertos necesarios

**Salida esperada:**
```
Creating api-gateway ... done
Creating equipos-service ... done
Creating proveedores-service ... done
Creating mantenimiento-service ... done
Creating reportes-service ... done
Creating agent-service ... done
Creating frontend-streamlit ... done
```

### Paso 5: Verificar que Todo Está Corriendo

```bash
docker-compose ps
```

**Salida esperada:**
```
NAME                    STATUS              PORTS
api-gateway             Up 30 seconds       0.0.0.0:8000->8000/tcp
equipos-service         Up 30 seconds       8001/tcp
proveedores-service     Up 30 seconds       8002/tcp
mantenimiento-service   Up 30 seconds       8003/tcp
reportes-service        Up 30 seconds       8004/tcp
agent-service           Up 30 seconds       8005/tcp
frontend-streamlit      Up 30 seconds       0.0.0.0:8501->8501/tcp
```

**Todos deben mostrar "Up"**

### Paso 6: Acceder a la Aplicación

Abre tu navegador y ve a:

- **🖥️ Frontend (Aplicación Principal):** http://localhost:8501
- **📚 API Documentation (Swagger):** http://localhost:8000/docs
- **🔍 Health Check:** http://localhost:8000/health

---

## 💻 Uso del Sistema

### Acceso Inicial

1. Abre http://localhost:8501 en tu navegador
2. Verás el dashboard principal con métricas
3. Usa el menú lateral para navegar entre módulos

### Módulos Disponibles

#### 📦 Equipos
- **Ver inventario:** Lista completa de equipos con filtros
- **Agregar equipo:** Formulario para registrar nuevos equipos
- **Ver detalles:** Información completa y historial de movimientos
- **Estadísticas:** Gráficos de distribución

#### 🏢 Proveedores
- **Lista de proveedores:** Todos los proveedores registrados
- **Agregar proveedor:** Formulario de registro
- **Ver detalles:** Información completa, contratos y equipos comprados

#### 🔧 Mantenimiento
- **Lista de mantenimientos:** Filtrar por estado y tipo
- **Programar mantenimiento:** Agendar preventivos o correctivos
- **Calendario:** Vista de próximos mantenimientos
- **Estadísticas:** Costos y métricas

#### 📊 Reportes
- **Dashboard:** Métricas principales
- **Por ubicación:** Distribución de equipos
- **Por estado:** Estados operativos
- **Costos:** Análisis de gastos de mantenimiento
- **Antigüedad:** Equipos por años de uso

### Agentes Inteligentes

En el sidebar, usa el botón **"🔄 Ejecutar Agentes"** para:
- Generar alertas de mantenimientos próximos
- Detectar garantías por vencer
- Identificar equipos obsoletos
- Encontrar mantenimientos atrasados

---

## 📁 Estructura del Proyecto

```
sistema-gestion-ti/
│
├── 📄 README.md                          # Este archivo
├── 📄 GUIA_DOCKER.md                     # Guía completa de Docker
├── 📄 GUIA_SUPABASE.md                   # Guía de configuración de Supabase
├── 📄 docker-compose.yml                 # Orquestación de servicios
├── 📄 .env.example                       # Plantilla de variables de entorno
├── 📄 .env                              # Variables de entorno (no incluir en git)
├── 📄 .gitignore                        # Archivos a ignorar por git
│
├── 📂 services/                          # Microservicios backend
│   ├── 📂 api_gateway/                  # API Gateway (Puerto 8000)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── main.py
│   │
│   ├── 📂 equipos_service/              # Servicio de Equipos (Puerto 8001)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── main.py
│   │
│   ├── 📂 proveedores_service/          # Servicio de Proveedores (Puerto 8002)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── main.py
│   │
│   ├── 📂 mantenimiento_service/        # Servicio de Mantenimiento (Puerto 8003)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── main.py
│   │
│   ├── 📂 reportes_service/             # Servicio de Reportes (Puerto 8004)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── main.py
│   │
│   └── 📂 agent_service/                # Servicio de Agentes (Puerto 8005)
│       ├── Dockerfile
│       ├── requirements.txt
│       └── main.py
│
└── 📂 frontend/                          # Aplicación Streamlit (Puerto 8501)
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py                           # Página principal
    └── pages/                           # Páginas adicionales
        ├── 1_📦_Equipos.py
        ├── 2_🏢_Proveedores.py
        ├── 3_🔧_Mantenimiento.py
        └── 4_📊_Reportes.py
```

---

## 🛠️ Tecnologías Utilizadas

### Frontend
- **Streamlit 1.28.2** - Framework de UI para Python
- **Plotly 5.18.0** - Gráficos interactivos
- **Pandas 2.1.3** - Manipulación de datos

### Backend
- **FastAPI 0.104.1** - Framework web moderno
- **Uvicorn 0.24.0** - Servidor ASGI
- **Supabase 2.0.3** - Cliente de base de datos
- **Pydantic 2.5.0** - Validación de datos

### Base de Datos
- **Supabase** - PostgreSQL en la nube
- **11 tablas** relacionales
- **Row Level Security (RLS)** habilitado

### Infraestructura
- **Docker** - Containerización
- **Docker Compose** - Orquestación de servicios

---

## 🔧 Comandos Útiles

### Gestión de Servicios

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs frontend

# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar un servicio
docker-compose restart frontend

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (datos)
docker-compose down -v

# Reconstruir servicios
docker-compose build

# Reconstruir sin caché
docker-compose build --no-cache

# Ver estado de servicios
docker-compose ps

# Ver uso de recursos
docker stats
```

### Debugging

```bash
# Entrar a un contenedor
docker-compose exec frontend /bin/bash

# Ver logs de errores
docker-compose logs --tail=50 frontend

# Reiniciar servicio específico
docker-compose restart api-gateway
```

---

## ❓ Solución de Problemas

### Problema 1: "No se puede conectar con el servidor"

**Síntomas:**
- Frontend muestra error de conexión
- Dashboard no carga datos

**Solución:**
```bash
# 1. Verificar que todos los servicios están corriendo
docker-compose ps

# 2. Ver logs del API Gateway
docker-compose logs api-gateway

# 3. Reiniciar servicios
docker-compose restart

# 4. Si persiste, reconstruir
docker-compose down
docker-compose build
docker-compose up -d
```

### Problema 2: "Error de credenciales de Supabase"

**Síntomas:**
- Errores 500 en las APIs
- Logs muestran "Invalid API key"

**Solución:**
1. Verifica el archivo `.env`
2. Asegúrate de que `SUPABASE_URL` y `SUPABASE_KEY` sean correctos
3. Reinicia los servicios:
```bash
docker-compose down
docker-compose up -d
```

### Problema 3: "Puerto ya en uso"

**Síntomas:**
- Error: "port is already allocated"

**Solución:**
```bash
# Ver qué está usando el puerto
netstat -ano | findstr :8501

# Opción 1: Detener el proceso
# Opción 2: Cambiar el puerto en docker-compose.yml
```

### Problema 4: "Docker daemon not running"

**Síntomas:**
- Comandos de Docker no funcionan

**Solución:**
1. Abre Docker Desktop
2. Espera a que inicie completamente
3. Verifica que el ícono de Docker no esté gris

### Problema 5: "Contenedor se detiene inmediatamente"

**Síntomas:**
- `docker-compose ps` muestra "Exit 1"

**Solución:**
```bash
# Ver logs para identificar el error
docker-compose logs <nombre-servicio>

# Reconstruir sin caché
docker-compose build --no-cache <nombre-servicio>
docker-compose up -d
```

### Problema 6: "No hay datos en Supabase"

**Síntomas:**
- Tablas vacías o no existen

**Solución:**
1. Ve a Supabase → SQL Editor
2. Ejecuta el script SQL completo de `GUIA_SUPABASE.md`
3. Verifica en Table Editor que las tablas existan

---

## 📊 Base de Datos

### Tablas Principales

1. **roles** - Roles de usuario
2. **usuarios** - Usuarios del sistema
3. **categorias_equipos** - Categorías de equipos
4. **ubicaciones** - Ubicaciones físicas
5. **proveedores** - Proveedores
6. **contratos** - Contratos con proveedores
7. **equipos** - Inventario de equipos
8. **movimientos_equipos** - Historial de movimientos
9. **mantenimientos** - Mantenimientos
10. **detalle_mantenimientos** - Detalles de mantenimientos
11. **notificaciones** - Notificaciones del sistema

### Diagrama de Relaciones

```
usuarios ─┬─ equipos (asignado_a)
          └─ movimientos_equipos (responsable)

categorias_equipos ── equipos

ubicaciones ─┬─ equipos (ubicacion_actual)
             └─ movimientos_equipos

proveedores ─┬─ equipos
             ├─ contratos
             └─ mantenimientos

equipos ─┬─ movimientos_equipos
         ├─ mantenimientos
         └─ notificaciones

mantenimientos ─┬─ detalle_mantenimientos
                └─ notificaciones
```

---

## 🎯 Flujo de Trabajo Recomendado

### Día a Día

1. **Iniciar el sistema:**
```bash
docker-compose up -d
```

2. **Acceder a la aplicación:**
- Abrir http://localhost:8501

3. **Ejecutar agentes (diariamente):**
- Click en "🔄 Ejecutar Agentes" en el sidebar

4. **Al terminar:**
```bash
docker-compose down
```

### Desarrollo

1. **Hacer cambios en el código**

2. **Reconstruir el servicio modificado:**
```bash
docker-compose build <servicio>
docker-compose up -d <servicio>
```

3. **Ver logs en tiempo real:**
```bash
docker-compose logs -f <servicio>
```

---

## 📞 Soporte

### Documentación
- 📖 [GUIA_DOCKER.md](./GUIA_DOCKER.md) - Guía completa de Docker
- 📖 [GUIA_SUPABASE.md](./GUIA_SUPABASE.md) - Configuración de Supabase

### Recursos Externos
- [Docker Documentation](https://docs.docker.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

### Contacto
- **Email:** ti@universidad.edu
- **Departamento:** TI - Universidad

---

## 📄 Licencia

MIT License - Desarrollado para fines educativos

---

## 🙏 Agradecimientos

- Comunidad Streamlit
- FastAPI Framework
- Supabase Team
- Docker Community

---

**Desarrollado con ❤️ para la Universidad**

**Versión:** 1.0.0  
**Última actualización:** Diciembre 2024
