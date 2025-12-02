# 🗄️ Guía Completa de Supabase

## 📚 1. ¿Qué es Supabase?

**Supabase** es una alternativa open-source a Firebase que te proporciona:
- ✅ Base de datos PostgreSQL en la nube
- ✅ API REST automática
- ✅ Autenticación de usuarios
- ✅ Almacenamiento de archivos
- ✅ Funciones en tiempo real

### ¿Por Qué Usamos Supabase en Este Proyecto?

En lugar de instalar PostgreSQL localmente en Docker, usamos Supabase porque:
1. **Más Simple**: No necesitas configurar ni mantener una base de datos
2. **Gratis**: Tier gratuito generoso para desarrollo
3. **Accesible**: Puedes acceder desde cualquier lugar
4. **Panel Visual**: Interfaz web para ver y editar datos
5. **Backups Automáticos**: No pierdes datos

---

## 🚀 2. Crear Tu Cuenta en Supabase

### Paso 1: Registrarse

1. Ve a: **https://supabase.com**
2. Click en **"Start your project"**
3. Opciones para registrarse:
   - Con GitHub (recomendado)
   - Con Google
   - Con email

### Paso 2: Crear un Nuevo Proyecto

1. Una vez dentro, click en **"New Project"**
2. Selecciona tu organización (o crea una nueva)
3. Completa el formulario:

```
Project Name: sistema-gestion-ti-universidad
Database Password: [Genera una contraseña segura - GUÁRDALA!]
Region: South America (São Paulo) - [Elige la más cercana]
Pricing Plan: Free
```

4. Click en **"Create new project"**
5. **Espera 2-3 minutos** mientras Supabase crea tu base de datos

---

## 🔑 3. Obtener Tus Credenciales

### Paso 1: Ir a Project Settings

1. En el panel izquierdo, click en el ícono de **engranaje ⚙️** (Settings)
2. Click en **"API"** en el menú lateral

### Paso 2: Copiar las Credenciales

Verás dos valores importantes:

#### 📍 Project URL
```
https://abcdefghijklmnop.supabase.co
```
**Dónde encontrarlo**: Sección "Config" → "URL"

#### 🔐 API Key (anon/public)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYzMjc0ODAwMCwiZXhwIjoxOTQ4MzI0MDAwfQ.abcdefghijklmnopqrstuvwxyz123456789
```
**Dónde encontrarlo**: Sección "Project API keys" → "anon public"

### Paso 3: Guardar las Credenciales

**⚠️ IMPORTANTE**: Guarda estas credenciales en un lugar seguro. Las necesitarás para configurar el archivo `.env`

---

## 📊 4. Crear el Esquema de la Base de Datos

### Paso 1: Abrir el Editor SQL

1. En el panel izquierdo, click en **"SQL Editor"** (ícono de base de datos)
2. Click en **"New query"**

### Paso 2: Ejecutar el Script SQL

Copia y pega el siguiente script completo en el editor:

```sql
-- ============================================
-- SISTEMA DE GESTIÓN DE EQUIPOS DE TI
-- Base de Datos para Universidad
-- ============================================

-- Eliminar tablas existentes (si las hay)
DROP TABLE IF EXISTS notificaciones CASCADE;
DROP TABLE IF EXISTS detalle_mantenimientos CASCADE;
DROP TABLE IF EXISTS mantenimientos CASCADE;
DROP TABLE IF EXISTS movimientos_equipos CASCADE;
DROP TABLE IF EXISTS equipos CASCADE;
DROP TABLE IF EXISTS contratos CASCADE;
DROP TABLE IF EXISTS proveedores CASCADE;
DROP TABLE IF EXISTS ubicaciones CASCADE;
DROP TABLE IF EXISTS categorias_equipos CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- ============================================
-- TABLA: roles
-- ============================================
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLA: usuarios
-- ============================================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(200) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    rol_id INTEGER REFERENCES roles(id),
    telefono VARCHAR(20),
    departamento VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP
);

-- ============================================
-- TABLA: categorias_equipos
-- ============================================
CREATE TABLE categorias_equipos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    codigo VARCHAR(20) UNIQUE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLA: ubicaciones
-- ============================================
CREATE TABLE ubicaciones (
    id SERIAL PRIMARY KEY,
    edificio VARCHAR(100) NOT NULL,
    piso VARCHAR(20),
    aula_oficina VARCHAR(50),
    descripcion TEXT,
    capacidad INTEGER,
    responsable_id INTEGER REFERENCES usuarios(id),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLA: proveedores
-- ============================================
CREATE TABLE proveedores (
    id SERIAL PRIMARY KEY,
    ruc VARCHAR(20) UNIQUE NOT NULL,
    razon_social VARCHAR(200) NOT NULL,
    nombre_comercial VARCHAR(200),
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(200),
    contacto_nombre VARCHAR(200),
    contacto_telefono VARCHAR(20),
    contacto_email VARCHAR(200),
    sitio_web VARCHAR(200),
    calificacion DECIMAL(3,2),
    activo BOOLEAN DEFAULT TRUE,
    notas TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLA: contratos
-- ============================================
CREATE TABLE contratos (
    id SERIAL PRIMARY KEY,
    proveedor_id INTEGER REFERENCES proveedores(id) ON DELETE CASCADE,
    numero_contrato VARCHAR(100) UNIQUE NOT NULL,
    tipo VARCHAR(50),
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    monto_total DECIMAL(12,2),
    estado VARCHAR(50) DEFAULT 'vigente',
    archivo_url TEXT,
    notas TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLA: equipos
-- ============================================
CREATE TABLE equipos (
    id SERIAL PRIMARY KEY,
    codigo_inventario VARCHAR(100) UNIQUE NOT NULL,
    categoria_id INTEGER REFERENCES categorias_equipos(id),
    nombre VARCHAR(200) NOT NULL,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    numero_serie VARCHAR(200) UNIQUE,
    especificaciones JSONB,
    proveedor_id INTEGER REFERENCES proveedores(id),
    fecha_compra DATE,
    costo_compra DECIMAL(12,2),
    fecha_garantia_fin DATE,
    ubicacion_actual_id INTEGER REFERENCES ubicaciones(id),
    estado_operativo VARCHAR(50) DEFAULT 'operativo',
    estado_fisico VARCHAR(50) DEFAULT 'bueno',
    asignado_a_id INTEGER REFERENCES usuarios(id),
    notas TEXT,
    imagen_url TEXT,
    codigo_qr TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLA: movimientos_equipos
-- ============================================
CREATE TABLE movimientos_equipos (
    id SERIAL PRIMARY KEY,
    equipo_id INTEGER REFERENCES equipos(id) ON DELETE CASCADE,
    ubicacion_origen_id INTEGER REFERENCES ubicaciones(id),
    ubicacion_destino_id INTEGER REFERENCES ubicaciones(id),
    usuario_responsable_id INTEGER REFERENCES usuarios(id),
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivo VARCHAR(200),
    observaciones TEXT
);

-- ============================================
-- TABLA: mantenimientos
-- ============================================
CREATE TABLE mantenimientos (
    id SERIAL PRIMARY KEY,
    equipo_id INTEGER REFERENCES equipos(id) ON DELETE CASCADE,
    tipo VARCHAR(50) NOT NULL,
    fecha_programada DATE,
    fecha_realizada DATE,
    estado VARCHAR(50) DEFAULT 'programado',
    proveedor_id INTEGER REFERENCES proveedores(id),
    tecnico_responsable VARCHAR(200),
    costo_total DECIMAL(12,2),
    diagnostico TEXT,
    solucion TEXT,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLA: detalle_mantenimientos
-- ============================================
CREATE TABLE detalle_mantenimientos (
    id SERIAL PRIMARY KEY,
    mantenimiento_id INTEGER REFERENCES mantenimientos(id) ON DELETE CASCADE,
    descripcion TEXT NOT NULL,
    repuesto_usado VARCHAR(200),
    cantidad INTEGER,
    costo_unitario DECIMAL(12,2),
    costo_total DECIMAL(12,2),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABLA: notificaciones
-- ============================================
CREATE TABLE notificaciones (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    mensaje TEXT NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'media',
    usuario_destino_id INTEGER REFERENCES usuarios(id),
    equipo_relacionado_id INTEGER REFERENCES equipos(id),
    mantenimiento_relacionado_id INTEGER REFERENCES mantenimientos(id),
    leida BOOLEAN DEFAULT FALSE,
    fecha_leida TIMESTAMP,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- ÍNDICES PARA MEJORAR RENDIMIENTO
-- ============================================

CREATE INDEX idx_equipos_categoria ON equipos(categoria_id);
CREATE INDEX idx_equipos_ubicacion ON equipos(ubicacion_actual_id);
CREATE INDEX idx_equipos_estado ON equipos(estado_operativo);
CREATE INDEX idx_equipos_proveedor ON equipos(proveedor_id);
CREATE INDEX idx_mantenimientos_equipo ON mantenimientos(equipo_id);
CREATE INDEX idx_mantenimientos_fecha ON mantenimientos(fecha_programada);
CREATE INDEX idx_movimientos_equipo ON movimientos_equipos(equipo_id);
CREATE INDEX idx_notificaciones_usuario ON notificaciones(usuario_destino_id);
CREATE INDEX idx_notificaciones_leida ON notificaciones(leida);

-- ============================================
-- DATOS INICIALES
-- ============================================

-- Roles
INSERT INTO roles (nombre, descripcion) VALUES
('Administrador', 'Acceso completo al sistema'),
('Técnico', 'Gestión de mantenimientos y equipos'),
('Usuario', 'Consulta de información'),
('Jefe de Departamento', 'Gestión de equipos de su departamento');

-- Usuario administrador por defecto
INSERT INTO usuarios (nombre_completo, email, password_hash, rol_id, departamento, activo) VALUES
('Administrador del Sistema', 'admin@universidad.edu', 'admin123', 1, 'TI', TRUE),
('Juan Pérez', 'jperez@universidad.edu', 'user123', 2, 'TI', TRUE),
('María García', 'mgarcia@universidad.edu', 'user123', 3, 'Sistemas', TRUE);

-- Categorías de Equipos
INSERT INTO categorias_equipos (nombre, descripcion, codigo) VALUES
('Computadoras de Escritorio', 'PCs de escritorio para oficinas y laboratorios', 'PC-DESK'),
('Laptops', 'Computadoras portátiles', 'LAPTOP'),
('Servidores', 'Servidores de red y aplicaciones', 'SERVER'),
('Impresoras', 'Impresoras y multifuncionales', 'PRINT'),
('Proyectores', 'Proyectores multimedia', 'PROJ'),
('Switches de Red', 'Equipos de red y comunicaciones', 'SWITCH'),
('Routers', 'Routers y puntos de acceso', 'ROUTER'),
('UPS', 'Sistemas de alimentación ininterrumpida', 'UPS'),
('Monitores', 'Pantallas y monitores', 'MONITOR'),
('Tablets', 'Tabletas electrónicas', 'TABLET');

-- Ubicaciones
INSERT INTO ubicaciones (edificio, piso, aula_oficina, descripcion, capacidad) VALUES
('Edificio Central', '1', 'Oficina TI', 'Oficina principal de TI', 10),
('Edificio Central', '2', 'Lab 201', 'Laboratorio de Computación 1', 30),
('Edificio Central', '2', 'Lab 202', 'Laboratorio de Computación 2', 30),
('Edificio de Ingeniería', '1', 'Lab Redes', 'Laboratorio de Redes', 25),
('Edificio de Ingeniería', '3', 'Sala Servidores', 'Sala de Servidores Principal', 50),
('Biblioteca', '1', 'Sala Multimedia', 'Sala de recursos multimedia', 20),
('Edificio Administrativo', '2', 'Oficina Decano', 'Oficina del Decano', 5),
('Almacén Central', '1', 'Almacén TI', 'Almacén de equipos de TI', 100);

-- Proveedores
INSERT INTO proveedores (ruc, razon_social, nombre_comercial, telefono, email, contacto_nombre, contacto_telefono) VALUES
('20123456789', 'Tecnología Avanzada S.A.C.', 'TechAdvance', '044-123456', 'ventas@techadvance.com', 'Carlos Ruiz', '987654321'),
('20987654321', 'Computadoras del Norte E.I.R.L.', 'CompuNorte', '044-654321', 'info@compunorte.com', 'Ana Torres', '987123456'),
('20456789123', 'Servicios Informáticos Integrales S.A.', 'SII', '044-789456', 'contacto@sii.com.pe', 'Roberto Vega', '965432178');

-- Equipos de ejemplo
INSERT INTO equipos (codigo_inventario, categoria_id, nombre, marca, modelo, numero_serie, fecha_compra, costo_compra, ubicacion_actual_id, estado_operativo, proveedor_id) VALUES
('PC-2024-001', 1, 'Computadora HP ProDesk', 'HP', 'ProDesk 400 G7', 'SN123456789', '2024-01-15', 1200.00, 2, 'operativo', 1),
('PC-2024-002', 1, 'Computadora Dell OptiPlex', 'Dell', 'OptiPlex 7090', 'SN987654321', '2024-01-15', 1350.00, 2, 'operativo', 2),
('LAP-2024-001', 2, 'Laptop Lenovo ThinkPad', 'Lenovo', 'ThinkPad E14', 'SN456789123', '2024-02-10', 2100.00, 1, 'operativo', 1),
('SERV-2024-001', 3, 'Servidor Dell PowerEdge', 'Dell', 'PowerEdge R740', 'SN789123456', '2024-01-05', 8500.00, 5, 'operativo', 2),
('PRINT-2024-001', 4, 'Impresora HP LaserJet', 'HP', 'LaserJet Pro M404dn', 'SN321654987', '2024-03-01', 450.00, 2, 'operativo', 3),
('PROJ-2024-001', 5, 'Proyector Epson', 'Epson', 'PowerLite X49', 'SN654987321', '2024-02-20', 850.00, 3, 'operativo', 1);

-- Mantenimientos de ejemplo
INSERT INTO mantenimientos (equipo_id, tipo, fecha_programada, estado, proveedor_id, tecnico_responsable) VALUES
(1, 'preventivo', '2024-06-15', 'programado', 1, 'Carlos Ruiz'),
(4, 'preventivo', '2024-05-20', 'programado', 2, 'Ana Torres'),
(5, 'correctivo', '2024-04-10', 'completado', 3, 'Roberto Vega');

-- Notificaciones de ejemplo
INSERT INTO notificaciones (tipo, titulo, mensaje, prioridad, equipo_relacionado_id) VALUES
('mantenimiento', 'Mantenimiento Programado', 'El equipo PC-2024-001 tiene mantenimiento programado para el 15/06/2024', 'media', 1),
('garantia', 'Garantía Próxima a Vencer', 'La garantía del servidor SERV-2024-001 vence en 30 días', 'alta', 4);

-- ============================================
-- FUNCIONES Y TRIGGERS
-- ============================================

-- Función para actualizar fecha de actualización
CREATE OR REPLACE FUNCTION actualizar_fecha_actualizacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para equipos
CREATE TRIGGER trigger_actualizar_equipos
BEFORE UPDATE ON equipos
FOR EACH ROW
EXECUTE FUNCTION actualizar_fecha_actualizacion();

-- Trigger para mantenimientos
CREATE TRIGGER trigger_actualizar_mantenimientos
BEFORE UPDATE ON mantenimientos
FOR EACH ROW
EXECUTE FUNCTION actualizar_fecha_actualizacion();

-- ============================================
-- VISTAS ÚTILES
-- ============================================

-- Vista: Equipos con información completa
CREATE OR REPLACE VIEW vista_equipos_completa AS
SELECT 
    e.id,
    e.codigo_inventario,
    e.nombre,
    e.marca,
    e.modelo,
    e.numero_serie,
    c.nombre AS categoria,
    p.razon_social AS proveedor,
    u.edificio || ' - ' || u.aula_oficina AS ubicacion,
    e.estado_operativo,
    e.estado_fisico,
    e.fecha_compra,
    e.costo_compra,
    usr.nombre_completo AS asignado_a
FROM equipos e
LEFT JOIN categorias_equipos c ON e.categoria_id = c.id
LEFT JOIN proveedores p ON e.proveedor_id = p.id
LEFT JOIN ubicaciones u ON e.ubicacion_actual_id = u.id
LEFT JOIN usuarios usr ON e.asignado_a_id = usr.id;

-- Vista: Mantenimientos pendientes
CREATE OR REPLACE VIEW vista_mantenimientos_pendientes AS
SELECT 
    m.id,
    e.codigo_inventario,
    e.nombre AS equipo,
    m.tipo,
    m.fecha_programada,
    m.estado,
    p.razon_social AS proveedor,
    m.tecnico_responsable
FROM mantenimientos m
JOIN equipos e ON m.equipo_id = e.id
LEFT JOIN proveedores p ON m.proveedor_id = p.id
WHERE m.estado IN ('programado', 'en_proceso')
ORDER BY m.fecha_programada;

-- ============================================
-- PERMISOS (Row Level Security - RLS)
-- ============================================

-- Habilitar RLS en tablas principales
ALTER TABLE equipos ENABLE ROW LEVEL SECURITY;
ALTER TABLE mantenimientos ENABLE ROW LEVEL SECURITY;
ALTER TABLE proveedores ENABLE ROW LEVEL SECURITY;

-- Política: Permitir lectura a todos los usuarios autenticados
CREATE POLICY "Permitir lectura a usuarios autenticados" ON equipos
    FOR SELECT
    USING (auth.role() = 'authenticated');

CREATE POLICY "Permitir lectura a usuarios autenticados" ON mantenimientos
    FOR SELECT
    USING (auth.role() = 'authenticated');

CREATE POLICY "Permitir lectura a usuarios autenticados" ON proveedores
    FOR SELECT
    USING (auth.role() = 'authenticated');

-- Política: Permitir escritura a todos (para desarrollo)
-- En producción, deberías restringir esto según roles
CREATE POLICY "Permitir escritura a todos" ON equipos
    FOR ALL
    USING (true);

CREATE POLICY "Permitir escritura a todos" ON mantenimientos
    FOR ALL
    USING (true);

CREATE POLICY "Permitir escritura a todos" ON proveedores
    FOR ALL
    USING (true);

-- ============================================
-- SCRIPT COMPLETADO
-- ============================================

-- Verificar que todo se creó correctamente
SELECT 'Base de datos creada exitosamente!' AS mensaje;
SELECT 'Total de tablas: ' || COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';
```

### Paso 3: Ejecutar el Script

1. Click en el botón **"Run"** (o presiona `Ctrl + Enter`)
2. Espera a que termine (debería tomar 5-10 segundos)
3. Verás el mensaje: **"Success. No rows returned"**

### Paso 4: Verificar las Tablas

1. En el panel izquierdo, click en **"Table Editor"**
2. Deberías ver todas las tablas creadas:
   - roles
   - usuarios
   - categorias_equipos
   - ubicaciones
   - proveedores
   - contratos
   - equipos
   - movimientos_equipos
   - mantenimientos
   - detalle_mantenimientos
   - notificaciones

---

## 🔍 5. Explorar los Datos

### Ver Datos en las Tablas

1. Click en **"Table Editor"** en el panel izquierdo
2. Selecciona una tabla (ej: `equipos`)
3. Verás los datos de ejemplo que se insertaron

### Agregar Datos Manualmente

1. Selecciona una tabla
2. Click en **"Insert"** → **"Insert row"**
3. Completa los campos
4. Click en **"Save"**

### Editar Datos

1. Click en cualquier celda
2. Modifica el valor
3. Presiona `Enter` para guardar

---

## 🔐 6. Configurar Row Level Security (RLS)

El script ya habilitó RLS básico, pero puedes ajustarlo:

### Ver Políticas de Seguridad

1. Click en **"Authentication"** → **"Policies"**
2. Verás las políticas creadas para cada tabla

### Modificar Políticas (Opcional)

Para producción, deberías crear políticas más restrictivas basadas en roles de usuario.

---

## 📝 7. Configurar el Archivo .env del Proyecto

Ahora que tienes tus credenciales, configura el archivo `.env`:

```bash
# SUPABASE CONFIGURATION
SUPABASE_URL=https://tu-proyecto-id.supabase.co
SUPABASE_KEY=tu-anon-key-aqui

# Ejemplo real:
# SUPABASE_URL=https://abcdefghijklmnop.supabase.co
# SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Reemplaza**:
- `tu-proyecto-id` con tu Project URL
- `tu-anon-key-aqui` con tu API Key (anon/public)

---

## 🧪 8. Probar la Conexión

### Desde Python (Prueba Rápida)

Crea un archivo `test_supabase.py`:

```python
from supabase import create_client, Client
import os

# Tus credenciales
SUPABASE_URL = "https://tu-proyecto-id.supabase.co"
SUPABASE_KEY = "tu-anon-key-aqui"

# Crear cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Probar consulta
try:
    response = supabase.table('equipos').select("*").limit(5).execute()
    print("✅ Conexión exitosa!")
    print(f"Equipos encontrados: {len(response.data)}")
    print(response.data)
except Exception as e:
    print(f"❌ Error: {e}")
```

Ejecutar:
```bash
pip install supabase
python test_supabase.py
```

---

## 📊 9. Panel de Administración de Supabase

### Database

- **Table Editor**: Ver y editar datos visualmente
- **SQL Editor**: Ejecutar consultas SQL personalizadas
- **Database**: Ver esquema y relaciones

### Funciones Útiles

#### Exportar Datos

1. SQL Editor → New query
2. Ejecutar:
```sql
COPY (SELECT * FROM equipos) TO STDOUT WITH CSV HEADER;
```
3. Copiar resultado

#### Importar Datos CSV

1. Table Editor → Seleccionar tabla
2. Click en **"..."** → **"Import data from CSV"**
3. Seleccionar archivo
4. Mapear columnas
5. Click en **"Import"**

#### Ver Logs

1. Click en **"Logs"** en el panel izquierdo
2. Filtra por:
   - API Requests
   - Database
   - Auth

---

## 🔧 10. Solución de Problemas

### Error: "Invalid API key"

**Solución**:
- Verifica que copiaste la **anon/public key**, no la service_role key
- Asegúrate de no tener espacios extra al copiar

### Error: "relation does not exist"

**Solución**:
- Verifica que ejecutaste el script SQL completo
- Revisa en Table Editor que las tablas existan

### Error: "Row Level Security policy violation"

**Solución**:
- Las políticas RLS están bloqueando el acceso
- Temporalmente, puedes deshabilitarlas:
```sql
ALTER TABLE equipos DISABLE ROW LEVEL SECURITY;
```

### No puedo ver datos en Table Editor

**Solución**:
- Verifica que hay datos insertados
- Ejecuta en SQL Editor:
```sql
SELECT COUNT(*) FROM equipos;
```

---

## 📚 11. Recursos Adicionales

### Documentación Oficial

- Supabase Docs: https://supabase.com/docs
- Python Client: https://supabase.com/docs/reference/python/introduction
- SQL Reference: https://supabase.com/docs/guides/database

### Tutoriales

- Getting Started: https://supabase.com/docs/guides/getting-started
- Database Design: https://supabase.com/docs/guides/database/tables

---

## ✅ Checklist de Verificación

Antes de continuar, verifica:

- [ ] Cuenta de Supabase creada
- [ ] Proyecto creado en Supabase
- [ ] Script SQL ejecutado sin errores
- [ ] Tablas visibles en Table Editor
- [ ] Datos de ejemplo insertados
- [ ] Project URL copiada
- [ ] API Key (anon) copiada
- [ ] Archivo `.env` configurado con credenciales

---

## 🎯 Próximos Pasos

Una vez completada esta guía:

1. ✅ Configura el archivo `.env` del proyecto
2. ✅ Ejecuta `docker-compose up -d`
3. ✅ Accede a http://localhost:8501
4. ✅ ¡Disfruta tu sistema funcionando!

---

¡Tu base de datos en Supabase está lista! 🎉
