# Fast API MNIST en Docker

Este proyecto implementa una API desarrollada con FastAPI para trabajar con el modelo MNIST utilizando contenedores Docker.

## Comandos Principales

### Crear y Construir el Modelo
```bash
docker-compose up --build #modificar el yaml
```

### Correr el Modelo
```bash
docker-compose start <nombre del contenedor> #dependera de como lo nombres en el yaml
docker-compose up <nombre del contenedor>
```

### Detener el Modelo
```bash
docker-compose stop <nombre del contenedor>
```

## Estructura del Proyecto

### Dockerfile
```dockerfile
# Use python base image
FROM python:3.10

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/
COPY ./app/numeros.h5 /app/numeros.h5

# Expose the desired port (the app will run on port 8000 inside the container)
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8280", "--reload"]
```

### `requirements.txt`
```text
fastapi
uvicorn[standard]
tensorflow
werkzeug
numpy
python-multipart
pillow
```

### `docker-compose.yml`
```yaml
services:
  fastapi:
    image: image-fastapi 
    build: .
    container_name: mnistAPI #nombre del contendeor
    ports:
      - "8000:8280"
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
```

## Configuración
1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
2. Coloca el modelo entrenado `numeros.h5` en el directorio `app` antes de construir el contenedor.
3. Modifica los archivos según sea necesario para tu entorno.

## Uso de la API
1. Construye y levanta el contenedor con:
   ```bash
   docker-compose up --build
   ```
2. Accede a la API en: `http://localhost:8000`.
3. Consulta la documentación interactiva en `http://localhost:8000/docs` o `http://localhost:8000/redoc`.

## Notas Adicionales
- La API está configurada para ejecutarse en el puerto `8280` dentro del contenedor y se expone al puerto `8000` en el host.
- Este proyecto utiliza un modelo de TensorFlow (`numeros.h5`) y es compatible con dispositivos que tienen GPU para aceleración.

## Futuras Mejoras
- Agregar autenticación para la API.
- Integrar pruebas automatizadas para las rutas de la API.
- Implementar un sistema de logs más robusto para monitoreo.

---
## Ligas de referencia para la creación del proyecto
## Referencias
- [Video tutorial: FastAPI con TensorFlow](https://www.youtube.com/watch?v=I8WTQGUUYHo&t)
- [Video tutorial: Creación de APIs con Docker](https://www.youtube.com/watch?v=4sWhhQwHqug&t)

---
---

