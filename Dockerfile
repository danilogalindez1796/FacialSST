# Imagen base compatible con dlib
FROM python:3.10-slim

# Instalar dependencias del sistema necesarias para face_recognition y dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    && apt-get clean

# Crear directorio de la app
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python (incluyendo dlib)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Exponer puerto
EXPOSE 8000

# Ejecutar la API
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
