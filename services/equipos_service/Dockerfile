FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8001

# Comando para ejecutar el servicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
