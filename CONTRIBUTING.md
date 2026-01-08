# Guía de Contribución

¡Gracias por tu interés en contribuir al Trading AI Bot! 🎉

## 📋 Código de Conducta

Este proyecto sigue un código de conducta. Al participar, te comprometes a mantener un ambiente respetuoso y profesional.

## 🚀 Cómo Contribuir

### Reportar Bugs

1. Verifica que el bug no esté ya reportado en [Issues](../../issues)
2. Usa la plantilla de bug report
3. Incluye:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Versión de Python y dependencias
   - Logs relevantes

### Proponer Features

1. Abre un issue con la plantilla de feature request
2. Describe claramente:
   - El problema que resuelve
   - La solución propuesta
   - Alternativas consideradas
   - Impacto en el código existente

### Pull Requests

#### Antes de Empezar

1. **Fork** el repositorio
2. **Crea una rama** desde `develop`:
   ```bash
   git checkout -b feature/GH-123-descripcion
   ```
3. **Configura el entorno**:
   ```bash
   make install-dev
   ```

#### Durante el Desarrollo

1. **Sigue el estilo de código**:
   ```bash
   make format  # Formatea con black
   make lint    # Verifica con ruff y mypy
   ```

2. **Escribe tests**:
   - Mínimo 80% de cobertura
   - Tests unitarios para lógica nueva
   - Tests de integración si aplica

3. **Documenta tu código**:
   - Docstrings en formato Google
   - Comentarios para lógica compleja
   - Actualiza README si es necesario

4. **Commits atómicos**:
   ```bash
   git commit -m "feat: añadir estrategia MACD (#123)"
   ```
   
   Formatos de commit:
   - `feat:` Nueva funcionalidad
   - `fix:` Corrección de bug
   - `docs:` Cambios en documentación
   - `test:` Añadir o modificar tests
   - `refactor:` Refactorización sin cambio funcional
   - `perf:` Mejora de rendimiento
   - `chore:` Tareas de mantenimiento

#### Antes de Abrir el PR

1. **Asegúrate que todo pasa**:
   ```bash
   make test
   make coverage
   make lint
   ```

2. **Actualiza documentación**:
   - README si cambió la API pública
   - Docstrings actualizados
   - CHANGELOG.md con tus cambios

3. **Rebase con develop**:
   ```bash
   git fetch origin
   git rebase origin/develop
   ```

#### Abrir el Pull Request

1. Usa la plantilla de PR
2. Incluye:
   - Descripción clara de los cambios
   - Screenshots si hay cambios visuales
   - Referencias a issues relacionados
   - Checklist completada

3. Solicita review de al menos 1 maintainer

## 📝 Estándares de Código

### Python

- **Versión**: Python 3.10+
- **Estilo**: PEP 8 con black (line-length=100)
- **Type hints**: Obligatorios en funciones públicas
- **Imports**: Organizados con isort (automático con ruff)

### Estructura de Archivos

```python
"""Módulo para gestión de portfolio.

Este módulo proporciona clases para gestionar posiciones,
calcular PnL y aplicar risk management.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd
from loguru import logger

if TYPE_CHECKING:
    from .types import Position


class Portfolio:
    """Gestiona el portfolio de trading."""

    def __init__(self, initial_cash: float) -> None:
        """Inicializa el portfolio.
        
        Args:
            initial_cash: Capital inicial disponible
        """
        self.cash = initial_cash
        self._positions: dict[str, Position] = {}
        logger.info(f"Portfolio initialized with ${initial_cash:,.2f}")
    
    def add_position(self, symbol: str, position: Position) -> None:
        """Añade una nueva posición al portfolio."""
        self._positions[symbol] = position
```

### Testing

```python
"""Tests para el módulo de portfolio."""

import pytest
from trading_engine.portfolio import Portfolio


class TestPortfolio:
    """Suite de tests para Portfolio."""

    @pytest.fixture
    def portfolio(self) -> Portfolio:
        """Fixture que retorna un portfolio con $10k."""
        return Portfolio(initial_cash=10000.0)

    def test_initial_cash(self, portfolio: Portfolio) -> None:
        """Verifica que el cash inicial sea correcto."""
        assert portfolio.cash == 10000.0

    def test_add_position(self, portfolio: Portfolio) -> None:
        """Test añadir posición actualiza el portfolio."""
        # Arrange
        position = Position(symbol="AAPL", quantity=10, price=150.0)
        
        # Act
        portfolio.add_position("AAPL", position)
        
        # Assert
        assert "AAPL" in portfolio._positions
        assert portfolio._positions["AAPL"].quantity == 10
```

## 🔍 Review Process

1. **Automated checks** deben pasar (CI/CD)
2. **Code review** por al menos 1 maintainer
3. **Testing** en diferentes escenarios
4. **Documentation** verificada
5. **Merge** a develop (main para releases)

## 📚 Recursos

- [Documentación técnica](docs/)
- [Architecture](docs/architecture.md)
- [GitHub Issues](../../issues)
- [GitHub Projects](../../projects)

## ❓ ¿Preguntas?

Abre un [Discussion](../../discussions) o contacta a los maintainers.

¡Gracias por contribuir! 🚀
