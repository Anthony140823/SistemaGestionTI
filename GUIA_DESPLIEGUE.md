# 🚀 Guía de Despliegue: GitHub, Docker y Nube

Esta guía te explica paso a paso cómo subir tu proyecto a GitHub y desplegarlo en la nube.

---

## 1. 🐙 Subir a GitHub

Ya he creado el archivo `.gitignore` para evitar subir archivos basura o contraseñas.

### Pasos:
1.  **Crea un repositorio vacío** en [GitHub.com](https://github.com/new).
2.  Abre una terminal en la carpeta de tu proyecto y ejecuta:

```bash
# Inicializar repositorio
git init

# Agregar todos los archivos
git add .

# Guardar cambios
git commit -m "Versión inicial del Sistema TI"

# Conectar con GitHub (reemplaza URL_DE_TU_REPO)
git remote add origin URL_DE_TU_REPO

# Subir código
git push -u origin master
```

---

## 2. 🐳 Docker (Local)

¡Buenas noticias! **Tu sistema YA está en Docker.**
El archivo `docker-compose.yml` es la "receta" que le dice a Docker cómo construir todo.

Para ejecutarlo en cualquier computadora con Docker instalado:
```bash
docker-compose up -d --build
```
*(Eso es todo. Docker se encarga de instalar Python, las librerías y configurar la red).*

---

## 3. ☁️ Despliegue en la Nube

Tienes dos opciones principales. Para un proyecto universitario, recomiendo la **Opción A** por ser más fácil.

### Opción A: Railway (Recomendado)
Railway es una plataforma que lee tu GitHub y despliega todo automáticamente.

1.  Crea una cuenta en [Railway.app](https://railway.app/).
2.  Haz click en **"New Project"** -> **"Deploy from GitHub repo"**.
3.  Selecciona tu repositorio.
4.  Railway detectará el `docker-compose.yml` o los `Dockerfile`.
5.  **IMPORTANTE:** Debes configurar las "Variables de Entorno" en Railway:
    - Ve a la pestaña "Variables".
    - Agrega `SUPABASE_URL` y `SUPABASE_KEY` (copialas de tu archivo `.env`).
6.  Railway construirá y desplegará tu aplicación. Te dará una URL pública (ej: `https://sistema-ti.up.railway.app`).

### Opción B: VPS (Servidor Virtual - Método "Profesional")
Si el profesor pide un servidor Linux real (como AWS EC2, DigitalOcean, Google Compute Engine).

1.  **Alquila un servidor** (Ubuntu 22.04 es estándar).
2.  **Conéctate por SSH:** `ssh root@tu_ip_servidor`
3.  **Instala Docker:**
    ```bash
    apt update
    apt install docker.io docker-compose
    ```
4.  **Clona tu código:**
    ```bash
    git clone URL_DE_TU_REPO
    cd nombre_repo
    ```
5.  **Crea el archivo .env:**
    ```bash
    nano .env
    # (Pega aquí tus credenciales de Supabase y guarda con Ctrl+O, Enter, Ctrl+X)
    ```
6.  **Ejecuta:**
    ```bash
    docker-compose up -d --build
    ```
7.  Tu sistema estará disponible en `http://tu_ip_servidor:8501`.

---

## 📝 Resumen para tu Profesor

- **Repositorio:** GitHub (Código fuente).
- **Contenedorización:** Docker + Docker Compose (Microservicios).
- **Base de Datos:** Supabase (PostgreSQL en la nube).
- **Despliegue:** Railway / VPS (Ejecución en la nube).
