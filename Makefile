.PHONY: help install install-dev test coverage lint format clean docker-build docker-up docs

help:
	@echo "Comandos disponibles:"
	@echo "  make install       - Instalar paquetes en modo editable"
	@echo "  make install-dev   - Instalar dependencias de desarrollo"
	@echo "  make test          - Ejecutar tests"
	@echo "  make coverage      - Ejecutar tests con cobertura"
	@echo "  make lint          - Ejecutar linters (ruff, mypy)"
	@echo "  make format        - Formatear código con black"
	@echo "  make clean         - Limpiar archivos temporales"
	@echo "  make docker-build  - Construir imagen Docker"
	@echo "  make docker-up     - Levantar contenedores"
	@echo "  make docs          - Generar documentación"

install:
	@echo "Instalando paquetes..."
	@. .venv/bin/activate && pip install -e ./engine -e ./strategies

install-dev: install
	@echo "Instalando dependencias de desarrollo..."
	@. .venv/bin/activate && pip install -r requirements-dev.txt
	@. .venv/bin/activate && pre-commit install || echo "⚠ pre-commit no instalado"

test:
	@echo "Ejecutando tests..."
	@. .venv/bin/activate && pytest -v

coverage:
	@echo "Ejecutando tests con cobertura..."
	@. .venv/bin/activate && pytest --cov=engine/src --cov=strategies/src --cov-report=html --cov-report=term

lint:
	@echo "Ejecutando linters..."
	@. .venv/bin/activate && ruff check . || echo "⚠ ruff no instalado"
	@. .venv/bin/activate && mypy engine/src strategies/src || echo "⚠ mypy no instalado"

format:
	@echo "Formateando código..."
	@. .venv/bin/activate && black engine/ strategies/ examples/ scripts/ || echo "⚠ black no instalado"
	@. .venv/bin/activate && ruff check --fix . || echo "⚠ ruff no instalado"

clean:
	@echo "Limpiando archivos temporales..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf htmlcov/ .coverage dist/ build/ 2>/dev/null || true
	@echo "✓ Limpieza completada"

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docs:
	@echo "Generando documentación..."
	@cd docs && make html || echo "⚠ Sphinx no configurado"
