# 🐳 Guía Completa de Docker para Principiantes

## 📚 1. ¿Qué es Docker?

### Analogía Sencilla: La Caja de Mudanza

Imagina que Docker es como una **caja de mudanza estandarizada**:

- **Sin Docker**: Cuando te mudas, cada mueble tiene diferente tamaño. Algunos no caben en el camión, otros se rompen en el camino. Cada casa tiene diferentes dimensiones y conexiones eléctricas.

- **Con Docker**: Todos tus muebles vienen en cajas estándar del mismo tamaño. Estas cajas:
  - ✅ Caben perfectamente en cualquier camión
  - ✅ Se pueden apilar sin problemas
  - ✅ Protegen el contenido
  - ✅ Funcionan igual en cualquier casa

**Docker hace lo mismo con aplicaciones**:
- Empaqueta tu aplicación con TODO lo que necesita (código, librerías, configuraciones)
- La "caja" (contenedor) funciona igual en cualquier computadora
- No importa si usas Windows, Mac o Linux

### ¿Qué es un Contenedor?

Un **contenedor** es como una mini-computadora virtual que:
- Tiene su propio sistema operativo ligero
- Contiene tu aplicación y sus dependencias
- Está aislado de otros contenedores
- Se inicia en segundos (no minutos como una máquina virtual)

### ¿Qué es una Imagen?

Una **imagen** es la "receta" o "plantilla" para crear contenedores:
- Es como el molde de una galleta
- Define qué tiene el contenedor
- Se puede compartir y reutilizar
- Se crea con un archivo llamado `Dockerfile`

---

## 🎼 2. ¿Qué es Docker Compose?

### Analogía: El Director de Orquesta

Si Docker es un músico, **Docker Compose es el director de orquesta**:

- **Docker**: Ejecuta un contenedor a la vez (un músico)
- **Docker Compose**: Coordina múltiples contenedores trabajando juntos (toda la orquesta)

### Ejemplo Práctico

Nuestro proyecto tiene 7 servicios:
1. Frontend (Streamlit)
2. API Gateway
3. Servicio de Equipos
4. Servicio de Proveedores
5. Servicio de Mantenimiento
6. Servicio de Reportes
7. Servicio de Agentes

**Sin Docker Compose**: Tendrías que iniciar cada servicio manualmente, uno por uno.

**Con Docker Compose**: Un solo comando (`docker-compose up`) inicia todos los servicios a la vez, conectados entre sí.

---

## 🎯 3. ¿Por Qué es Necesario para Este Proyecto?

### Problemas que Resuelve Docker

#### ❌ Sin Docker:
```
Tú: "Profesor, el código no funciona en mi computadora"
Profesor: "En mi computadora sí funciona 🤷"

Problemas comunes:
- Versión diferente de Python
- Librerías faltantes
- Configuraciones diferentes
- Conflictos entre proyectos
```

#### ✅ Con Docker:
```
Tú: "Ejecuto docker-compose up"
Sistema: "Funciona perfectamente ✨"

Ventajas:
- Mismo entorno para todos
- Todas las dependencias incluidas
- No contamina tu sistema
- Fácil de limpiar y reiniciar
```

### Beneficios Específicos para Nuestro Proyecto

1. **Microservicios Aislados**: Cada servicio corre en su propio contenedor
2. **Fácil Desarrollo**: No necesitas instalar Python, PostgreSQL, etc. manualmente
3. **Portabilidad**: Funciona igual en Windows, Mac y Linux
4. **Escalabilidad**: Puedes crear múltiples instancias de un servicio
5. **Limpieza**: Eliminas todo con un comando, sin dejar rastros

---

## 💻 4. Instalación de Docker

### Para Windows

#### Opción 1: Docker Desktop (Recomendado)

1. **Requisitos**:
   - Windows 10/11 Pro, Enterprise o Education (64-bit)
   - Virtualización habilitada en BIOS
   - WSL 2 (Windows Subsystem for Linux)

2. **Descargar Docker Desktop**:
   - Ve a: https://www.docker.com/products/docker-desktop
   - Descarga "Docker Desktop for Windows"
   - Tamaño: ~500 MB

3. **Instalar**:
   ```
   1. Ejecuta el instalador descargado
   2. Acepta los términos
   3. Marca "Use WSL 2 instead of Hyper-V" (recomendado)
   4. Click en "Install"
   5. Reinicia tu computadora cuando termine
   ```

4. **Configurar WSL 2** (si no lo tienes):
   ```powershell
   # Abre PowerShell como Administrador y ejecuta:
   wsl --install
   
   # Reinicia tu computadora
   
   # Verifica la instalación:
   wsl --list --verbose
   ```

5. **Iniciar Docker Desktop**:
   - Busca "Docker Desktop" en el menú inicio
   - Ábrelo (verás un ícono de ballena en la barra de tareas)
   - Espera a que diga "Docker Desktop is running"

#### Opción 2: Docker Toolbox (Para Windows 10 Home)

Si tienes Windows 10 Home (sin Hyper-V):
1. Descarga Docker Toolbox: https://github.com/docker/toolbox/releases
2. Instala VirtualBox (incluido)
3. Usa Docker Quickstart Terminal

### Para Mac

1. **Descargar**:
   - Ve a: https://www.docker.com/products/docker-desktop
   - Descarga "Docker Desktop for Mac"
   - Elige según tu chip:
     - **Intel Chip**: Docker Desktop for Mac (Intel)
     - **Apple Silicon (M1/M2)**: Docker Desktop for Mac (Apple Silicon)

2. **Instalar**:
   ```
   1. Abre el archivo .dmg descargado
   2. Arrastra Docker a la carpeta Applications
   3. Abre Docker desde Applications
   4. Autoriza con tu contraseña de Mac
   5. Espera a que inicie
   ```

---

## ✅ 5. Verificar que Docker Funciona

### Paso 1: Abrir Terminal/PowerShell

**Windows**: 
- Presiona `Win + R`
- Escribe `powershell`
- Presiona Enter

**Mac**:
- Presiona `Cmd + Espacio`
- Escribe `terminal`
- Presiona Enter

### Paso 2: Verificar Versión de Docker

```bash
docker --version
```

**Salida esperada**:
```
Docker version 24.0.7, build afdd53b
```

### Paso 3: Verificar Docker Compose

```bash
docker-compose --version
```

**Salida esperada**:
```
Docker Compose version v2.23.0
```

### Paso 4: Ejecutar Contenedor de Prueba

```bash
docker run hello-world
```

**Salida esperada**:
```
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### Paso 5: Verificar que Docker Desktop Está Corriendo

**Windows/Mac**:
- Busca el ícono de Docker (ballena) en la barra de tareas
- Debe estar activo (no gris)

---

## 🚀 6. Comandos Básicos de Docker

### Comandos Esenciales

```bash
# Ver contenedores en ejecución
docker ps

# Ver TODOS los contenedores (incluso detenidos)
docker ps -a

# Ver imágenes descargadas
docker images

# Detener un contenedor
docker stop <nombre-contenedor>

# Eliminar un contenedor
docker rm <nombre-contenedor>

# Eliminar una imagen
docker rmi <nombre-imagen>

# Ver logs de un contenedor
docker logs <nombre-contenedor>

# Ver logs en tiempo real
docker logs -f <nombre-contenedor>

# Entrar a un contenedor en ejecución
docker exec -it <nombre-contenedor> /bin/bash
```

### Comandos de Docker Compose

```bash
# Iniciar todos los servicios
docker-compose up

# Iniciar en segundo plano (detached mode)
docker-compose up -d

# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs <nombre-servicio>

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (datos)
docker-compose down -v

# Reconstruir imágenes
docker-compose build

# Reconstruir sin caché
docker-compose build --no-cache

# Ver estado de servicios
docker-compose ps

# Reiniciar un servicio
docker-compose restart <nombre-servicio>
```

---

## 📦 7. Conceptos Clave del Proyecto

### Estructura de Archivos Docker

```
proyecto/
├── docker-compose.yml          # Orquestador principal
├── .env                        # Variables de entorno
├── frontend/
│   ├── Dockerfile             # Receta para contenedor frontend
│   └── requirements.txt       # Dependencias Python
└── services/
    ├── api_gateway/
    │   ├── Dockerfile
    │   └── requirements.txt
    └── equipos_service/
        ├── Dockerfile
        └── requirements.txt
```

### ¿Qué Hace Cada Archivo?

#### `Dockerfile`
Define cómo construir la imagen del contenedor:
```dockerfile
FROM python:3.11-slim          # Imagen base (Python 3.11)
WORKDIR /app                   # Carpeta de trabajo
COPY requirements.txt .        # Copiar dependencias
RUN pip install -r requirements.txt  # Instalar dependencias
COPY . .                       # Copiar código
CMD ["python", "main.py"]      # Comando al iniciar
```

#### `docker-compose.yml`
Define y conecta todos los servicios:
```yaml
services:
  frontend:
    build: ./frontend          # Construir desde carpeta frontend
    ports:
      - "8501:8501"           # Puerto: host:contenedor
    environment:
      - API_URL=http://api-gateway:8000
    depends_on:
      - api-gateway           # Esperar a que API esté lista
```

#### `.env`
Variables de configuración:
```bash
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-clave-aqui
```

---

## 🎓 8. Comandos Exactos para Ejecutar el Proyecto

### Paso 1: Navegar a la Carpeta del Proyecto

```bash
cd "C:\Users\ANTHONY\Documents\CLASES UNT\CICLO_8\INGENIERÍA DE SOFTWARE\SEMANA 14\EXAMEN III\Examen de Laboratorio Unidad III"
```

### Paso 2: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus credenciales de Supabase
notepad .env
```

### Paso 3: Construir las Imágenes

```bash
docker-compose build
```

**Qué hace**: Crea las imágenes de todos los servicios (puede tardar 5-10 minutos la primera vez)

### Paso 4: Iniciar los Servicios

```bash
docker-compose up -d
```

**Qué hace**: 
- Inicia todos los contenedores
- `-d` = modo detached (en segundo plano)

### Paso 5: Verificar que Todo Está Corriendo

```bash
docker-compose ps
```

**Salida esperada**:
```
NAME                    STATUS              PORTS
frontend                Up 30 seconds       0.0.0.0:8501->8501/tcp
api-gateway             Up 30 seconds       0.0.0.0:8000->8000/tcp
equipos-service         Up 30 seconds       8001/tcp
proveedores-service     Up 30 seconds       8002/tcp
...
```

### Paso 6: Acceder a la Aplicación

Abre tu navegador y ve a:
- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

### Paso 7: Ver Logs (Si Hay Problemas)

```bash
# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs frontend

# Ver logs en tiempo real
docker-compose logs -f
```

### Paso 8: Detener el Sistema

```bash
# Detener servicios (conserva datos)
docker-compose down

# Detener y eliminar TODO (incluyendo datos)
docker-compose down -v
```

---

## 🔧 9. Solución de Problemas Comunes

### Problema 1: "Docker daemon is not running"

**Solución**:
1. Abre Docker Desktop
2. Espera a que inicie completamente
3. Verifica que el ícono de la ballena no esté gris

### Problema 2: "Port is already allocated"

**Solución**:
```bash
# Ver qué está usando el puerto
netstat -ano | findstr :8501

# Detener el proceso o cambiar el puerto en docker-compose.yml
```

### Problema 3: "Cannot connect to Docker daemon"

**Solución Windows**:
```powershell
# Reiniciar Docker Desktop
# O ejecutar PowerShell como Administrador:
net stop com.docker.service
net start com.docker.service
```

### Problema 4: Contenedor se detiene inmediatamente

**Solución**:
```bash
# Ver logs para identificar el error
docker-compose logs <nombre-servicio>

# Reconstruir sin caché
docker-compose build --no-cache <nombre-servicio>
```

### Problema 5: "No space left on device"

**Solución**:
```bash
# Limpiar contenedores detenidos
docker container prune

# Limpiar imágenes no usadas
docker image prune

# Limpiar TODO (cuidado!)
docker system prune -a
```

---

## 📊 10. Monitoreo y Debugging

### Ver Recursos Usados

```bash
# Ver uso de CPU/RAM de contenedores
docker stats
```

### Entrar a un Contenedor

```bash
# Abrir shell interactivo
docker-compose exec frontend /bin/bash

# Ejecutar comando específico
docker-compose exec frontend ls -la
```

### Reiniciar un Servicio Específico

```bash
docker-compose restart frontend
```

### Ver Redes de Docker

```bash
docker network ls
```

---

## ✨ 11. Flujo de Trabajo Diario

### Iniciar el Día

```bash
# 1. Navegar al proyecto
cd "ruta/del/proyecto"

# 2. Iniciar servicios
docker-compose up -d

# 3. Ver que todo esté OK
docker-compose ps

# 4. Abrir navegador
start http://localhost:8501
```

### Durante el Desarrollo

```bash
# Si cambias código Python:
docker-compose restart <servicio>

# Si cambias Dockerfile o requirements.txt:
docker-compose build <servicio>
docker-compose up -d <servicio>

# Ver logs en tiempo real:
docker-compose logs -f <servicio>
```

### Terminar el Día

```bash
# Detener servicios (conserva datos)
docker-compose down
```

---

## 🎯 12. Resumen de Comandos Más Usados

```bash
# INICIAR TODO
docker-compose up -d

# VER ESTADO
docker-compose ps

# VER LOGS
docker-compose logs -f

# REINICIAR UN SERVICIO
docker-compose restart frontend

# RECONSTRUIR DESPUÉS DE CAMBIOS
docker-compose build
docker-compose up -d

# DETENER TODO
docker-compose down

# LIMPIAR TODO (CUIDADO: BORRA DATOS)
docker-compose down -v
docker system prune -a
```

---

## 📚 13. Recursos Adicionales

### Documentación Oficial
- Docker: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/

### Tutoriales en Español
- Docker para Principiantes: https://www.youtube.com/watch?v=CV_Uf3Dq-EU
- Docker Compose Tutorial: https://www.youtube.com/watch?v=Qw9zlE3t8Ko

### Comunidad
- Docker Community Forums: https://forums.docker.com/
- Stack Overflow (tag: docker): https://stackoverflow.com/questions/tagged/docker

---

## ✅ Checklist de Verificación

Antes de ejecutar el proyecto, verifica:

- [ ] Docker Desktop instalado y corriendo
- [ ] `docker --version` funciona
- [ ] `docker-compose --version` funciona
- [ ] `docker run hello-world` funciona
- [ ] Archivo `.env` configurado con credenciales de Supabase
- [ ] Estás en la carpeta correcta del proyecto
- [ ] Tienes conexión a internet (para descargar imágenes)

---

¡Ahora estás listo para usar Docker! 🎉
