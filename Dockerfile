FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de configuración
COPY engine/pyproject.toml engine/pyproject.toml
COPY strategies/pyproject.toml strategies/pyproject.toml
COPY requirements-dev.txt .

# Copiar código fuente
COPY engine/ engine/
COPY strategies/ strategies/
COPY config/ config/
COPY examples/ examples/
COPY scripts/ scripts/

# Instalar paquetes
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e ./engine -e ./strategies && \
    pip install --no-cache-dir -r requirements-dev.txt

# Crear directorios necesarios
RUN mkdir -p data logs reports

CMD ["python", "examples/run_rsi.py"]
