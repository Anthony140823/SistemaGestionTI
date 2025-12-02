# 🚀 Guía de Inicio Rápido

## ⚡ Pasos para Ejecutar el Sistema (5 minutos)

### ✅ Antes de Empezar

Asegúrate de tener:
- [ ] Docker Desktop instalado y corriendo
- [ ] Cuenta de Supabase creada
- [ ] Script SQL ejecutado en Supabase
- [ ] Credenciales de Supabase (URL y API Key)

**¿No tienes esto?** Lee primero:
- 📖 [GUIA_DOCKER.md](./GUIA_DOCKER.md) - Para instalar Docker
- 📖 [GUIA_SUPABASE.md](./GUIA_SUPABASE.md) - Para configurar Supabase

---

## 🎯 Paso a Paso

### 1️⃣ Configurar Variables de Entorno (1 minuto)

```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar con tus credenciales
notepad .env
```

**Edita estas líneas:**
```env
SUPABASE_URL=https://tu-proyecto-id.supabase.co
SUPABASE_KEY=tu-anon-key-aqui
```

**Guarda el archivo** (Ctrl + S)

---

### 2️⃣ Construir las Imágenes (3-5 minutos)

```bash
docker-compose build
```

**Espera a que termine.** Verás:
```
Successfully built
Successfully tagged ...
```

---

### 3️⃣ Iniciar el Sistema (30 segundos)

```bash
docker-compose up -d
```

**Verás:**
```
Creating api-gateway ... done
Creating equipos-service ... done
...
Creating frontend-streamlit ... done
```

---

### 4️⃣ Verificar que Todo Funciona (10 segundos)

```bash
docker-compose ps
```

**Todos deben mostrar "Up":**
```
NAME                    STATUS
api-gateway             Up
equipos-service         Up
proveedores-service     Up
mantenimiento-service   Up
reportes-service        Up
agent-service           Up
frontend-streamlit      Up
```

---

### 5️⃣ Abrir la Aplicación

**Abre tu navegador:**
- 🖥️ **Aplicación:** http://localhost:8501
- 📚 **API Docs:** http://localhost:8000/docs

---

## ✨ ¡Listo!

Deberías ver el dashboard principal con métricas.

### Primeros Pasos en la Aplicación

1. **Ejecutar Agentes:**
   - Click en "🔄 Ejecutar Agentes" en el sidebar
   - Esto generará notificaciones con los datos de ejemplo

2. **Explorar Equipos:**
   - Ve a la página "📦 Equipos"
   - Click en "🔍 Buscar" para ver los equipos de ejemplo

3. **Ver Reportes:**
   - Ve a "📊 Reportes"
   - Explora los gráficos interactivos

---

## 🛑 Detener el Sistema

Cuando termines:

```bash
docker-compose down
```

---

## ❌ Si Algo Sale Mal

### Problema: "No se puede conectar"

```bash
# Ver logs
docker-compose logs

# Reiniciar
docker-compose restart
```

### Problema: "Error de Supabase"

1. Verifica que el archivo `.env` tenga las credenciales correctas
2. Reinicia:
```bash
docker-compose down
docker-compose up -d
```

### Problema: "Puerto en uso"

Cambia el puerto en `docker-compose.yml`:
```yaml
ports:
  - "8502:8501"  # Cambiar 8501 por 8502
```

---

## 📖 Documentación Completa

Para más detalles, lee:
- 📄 [README.md](./README.md) - Documentación completa
- 📖 [GUIA_DOCKER.md](./GUIA_DOCKER.md) - Guía de Docker
- 📖 [GUIA_SUPABASE.md](./GUIA_SUPABASE.md) - Guía de Supabase

---

## 🎓 Comandos Útiles

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio
docker-compose logs frontend

# Reiniciar un servicio
docker-compose restart frontend

# Reconstruir todo
docker-compose down
docker-compose build
docker-compose up -d

# Ver uso de recursos
docker stats
```

---

**¡Disfruta tu sistema de gestión de equipos! 🎉**
