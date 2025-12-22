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
	pip install -e ./engine -e ./strategies

install-dev: install
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest -v

coverage:
	pytest --cov=engine/src --cov=strategies/src --cov-report=html --cov-report=term

lint:
	ruff check .
	mypy engine/src strategies/src

format:
	black engine/ strategies/ examples/ scripts/
	ruff check --fix .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docs:
	cd docs && make html
