# 🚀 Quick Start - Trading en Vivo con Alpaca

Guía de 5 minutos para empezar a operar.

## Paso 1: Crear Cuenta en Alpaca (2 min)

1. Ve a https://alpaca.markets/
2. Click en "Start Trading" → "Sign Up"
3. Completa el registro (email, contraseña)
4. Activa **Paper Trading** (dinero simulado)

## Paso 2: Obtener API Keys (1 min)

1. Inicia sesión en https://app.alpaca.markets/
2. Asegúrate de estar en modo "Paper Trading" (esquina superior derecha)
3. Ve a: **Your API Keys** (menú lateral)
4. Click en "Generate New Key"
5. Copia:
   - `API Key ID` (ejemplo: PKxxxx...)
   - `Secret Key` (ejemplo: xxx...) ⚠️ Solo se muestra una vez

## Paso 3: Configurar el Proyecto (1 min)

```bash
# 1. Instalar dependencias
pip install alpaca-py python-dotenv

# 2. Crear archivo .env
cp .env.example .env

# 3. Editar .env (con nano, vim, o tu editor)
nano .env
```

Añadir tus credenciales:

```env
ALPACA_API_KEY=PKxxxx...
ALPACA_SECRET_KEY=xxx...
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

Guardar y cerrar.

## Paso 4: Test de Conexión (30 seg)

```bash
python examples/test_alpaca_connection.py
```

**Debe mostrar:**
```
✓ Conexión exitosa
✓ Capital: $100,000.00
✓ Cash: $100,000.00
✓ Poder de compra: $400,000.00
```

Si ves ✓ en todos, ¡estás listo!

## Paso 5: ¡Iniciar Trading! (30 seg)

```bash
python examples/live_trading_alpaca.py
```

**El sistema:**
1. Conecta a Alpaca (paper trading)
2. Carga datos históricos de AAPL, GOOGL, MSFT, TSLA, AMZN
3. Analiza cada símbolo cada 5 minutos
4. Ejecuta órdenes automáticamente cuando hay señales
5. Muestra estado del portfolio

**Salida esperada:**
```
============================================================
SISTEMA DE TRADING EN VIVO - ALPACA MARKETS
============================================================

Fecha: 2024-12-22 10:30:00
Modo: PAPER TRADING

Símbolos: AAPL, GOOGL, MSFT, TSLA, AMZN
Capital por símbolo: $20,000
Capital total: $100,000
Intervalo de actualización: 300s

Presiona ENTER para iniciar el trading en vivo...
```

Presiona ENTER y verás el loop de trading:

```
============================================================
ITERACIÓN 1 - 2024-12-22 10:30:00
============================================================

AAPL: Actualizando datos...
🟢 AAPL: COMPRA 50 @ $180.50 (Total: $9,025.00)

MSFT: Actualizando datos...
Sin acción (Signal: 0, Position: False)

...

📊 ESTADO ACTUAL:
  Capital: $100,000.00
  Cash: $90,975.00
  Posiciones: 1
    AAPL: 50.00 @ $180.50 → $181.20 | PnL: $35.00 (+0.39%)
```

## Detener el Sistema

Presiona `Ctrl+C`:

```
⚠️  Interrupción detectada
Deteniendo sistema...

============================================================
RESUMEN FINAL
============================================================
Capital Final: $100,035.00
Retorno: +0.04%
Posiciones Abiertas: 1
```

## Monitorear en Alpaca Dashboard

Mientras el sistema corre, puedes ver todo en tiempo real:

https://app.alpaca.markets/paper/dashboard

Verás:
- 📊 Equity del portfolio
- 📈 Posiciones abiertas
- 🧾 Historial de órdenes
- 💰 Capital actual

## Personalizar

### Cambiar Símbolos

Edita `.env`:

```env
SYMBOLS=NVDA,AMD,INTC,TSLA,META
```

### Cambiar Capital

```env
CAPITAL_PER_SYMBOL=50000  # $50k por símbolo
```

### Cambiar Intervalo

```env
UPDATE_INTERVAL=60  # Actualizar cada 1 minuto
```

### Cambiar Estrategia

Edita [live_trading_alpaca.py](../examples/live_trading_alpaca.py):

```python
# En lugar de CombinedStrategy
from strategies import RsiStrategy

strategy = RsiStrategy(period=14, lower_threshold=30, upper_threshold=70)
```

## Próximos Pasos

1. **Backtest primero:** Prueba tu estrategia con datos históricos
   ```bash
   python examples/run_rsi_advanced.py
   ```

2. **Paper trading por 1-2 semanas:** Verifica que todo funcione bien

3. **Monitorea resultados:** Revisa métricas diarias en Alpaca Dashboard

4. **Ajusta parámetros:** Modifica estrategia según resultados

5. **Considera live trading:** Solo después de probar extensivamente

## Ayuda

**Problemas de conexión:**
```bash
# Verificar que alpaca-py esté instalado
pip show alpaca-py

# Reinstalar si es necesario
pip install --upgrade alpaca-py
```

**Credenciales incorrectas:**
- Verifica que hayas copiado las keys completas (sin espacios)
- Asegúrate de estar en modo Paper Trading
- Regenera las keys en Alpaca Dashboard si es necesario

**El sistema no ejecuta órdenes:**
- Verifica que sea horario de mercado (9:30-16:00 ET, lun-vie)
- Revisa los logs para ver las señales generadas
- Puede que la estrategia no genere señales en ese momento

## Recursos

- [Guía Completa](ALPACA_LIVE_TRADING.md) - Documentación detallada
- [Alpaca Docs](https://docs.alpaca.markets/) - API oficial
- [Dashboard](https://app.alpaca.markets/paper/dashboard) - Monitoreo en vivo

---

⚠️ **IMPORTANTE:** Usa siempre Paper Trading primero. El live trading implica riesgo de pérdida de capital. Opera bajo tu propia responsabilidad.

🎉 **¡Disfruta del trading algorítmico!**
