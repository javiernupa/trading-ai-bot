"""Utilidad para cargar configuración de estrategias desde archivo .env

Este módulo permite configurar todas las estrategias de trading
desde el archivo .env sin necesidad de modificar código.

Ejemplo de uso:
    from strategies import load_strategies_from_env
    
    strategies, consensus = load_strategies_from_env()
    combined = CombinedStrategy(strategies, consensus)
"""

import os
from typing import List, Tuple, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .base import Strategy

# Importaciones locales para evitar circular imports
def _import_strategies():
    """Importa las estrategias solo cuando se necesitan."""
    from .rsi import RsiStrategy
    from .macd import MacdStrategy
    from .bollinger import BollingerBandsStrategy
    from .elliott_waves import ElliottWavesStrategy
    from .ichimoku import IchimokuStrategy
    from .ma50 import Ma50Strategy
    from .ma100 import Ma100Strategy
    from .ma200 import Ma200Strategy
    from .stochastic import StochasticStrategy
    from .parabolic_sar import ParabolicSARStrategy
    from .ema import EMAStrategy
    from .sma import SMAStrategy
    from .obv import OBVStrategy
    
    return {
        'RSI': RsiStrategy,
        'MACD': MacdStrategy,
        'BOLLINGER': BollingerBandsStrategy,
        'ELLIOTT': ElliottWavesStrategy,
        'ICHIMOKU': IchimokuStrategy,
        'MA50': Ma50Strategy,
        'MA100': Ma100Strategy,
        'MA200': Ma200Strategy,
        'STOCHASTIC': StochasticStrategy,
        'PSAR': ParabolicSARStrategy,
        'EMA': EMAStrategy,
        'SMA': SMAStrategy,
        'OBV': OBVStrategy,
    }


def parse_strategy_config(config_str: str) -> Dict[str, Any]:
    """Parsea configuración de estrategia desde string.
    
    Formato: "param1:value1,param2:value2,param3:value3"
    
    Args:
        config_str: String de configuración
        
    Returns:
        Diccionario con parámetros parseados
        
    Example:
        >>> parse_strategy_config("period:14,lower:30,upper:70")
        {'period': 14, 'lower': 30, 'upper': 70}
    """
    if not config_str:
        return {}
    
    params = {}
    for param in config_str.split(','):
        if ':' not in param:
            continue
            
        key, value = param.split(':', 1)
        key = key.strip()
        value = value.strip()
        
        # Convertir tipos
        if value.lower() == 'true':
            params[key] = True
        elif value.lower() == 'false':
            params[key] = False
        elif value.replace('.', '', 1).isdigit():
            # Es un número (int o float)
            params[key] = float(value) if '.' in value else int(value)
        else:
            params[key] = value
    
    return params


def load_strategy_from_env(strategy_name: str) -> "Strategy":
    """Carga una estrategia individual desde variables de entorno.
    
    Args:
        strategy_name: Nombre de la estrategia (RSI, MACD, BOLLINGER, MA50, MA100, MA200)
        
    Returns:
        Instancia de la estrategia configurada
        
    Raises:
        ValueError: Si el nombre de estrategia no es válido
    """
    strategy_classes = _import_strategies()
    
    if strategy_name not in strategy_classes:
        raise ValueError(
            f"Estrategia '{strategy_name}' no válida. "
            f"Opciones: {', '.join(strategy_classes.keys())}"
        )
    
    # Obtener configuración desde .env
    env_key = f"STRATEGY_{strategy_name}"
    config_str = os.getenv(env_key, "")
    params = parse_strategy_config(config_str)
    
    # Crear instancia de estrategia
    strategy_class = strategy_classes[strategy_name]
    return strategy_class(**params)


def load_strategies_from_env() -> Tuple[List["Strategy"], int]:
    """Carga todas las estrategias activas desde archivo .env.
    
    Lee las variables de entorno:
    - ACTIVE_STRATEGIES: Estrategias a usar (ej: "RSI,MACD,MA200")
    - CONSENSUS_THRESHOLD: Consenso mínimo requerido
    - STRATEGY_<NOMBRE>: Parámetros de cada estrategia
    
    Returns:
        Tupla con (lista de estrategias, consensus_threshold)
        
    Example:
        >>> strategies, consensus = load_strategies_from_env()
        >>> combined = CombinedStrategy(strategies, consensus)
    """
    # Obtener lista de estrategias activas
    active_str = os.getenv('ACTIVE_STRATEGIES', 'RSI,MACD,BOLLINGER')
    active_names = [s.strip().upper() for s in active_str.split(',')]
    
    # Cargar cada estrategia
    strategies = []
    for name in active_names:
        try:
            strategy = load_strategy_from_env(name)
            strategies.append(strategy)
            print(f"✓ Cargada: {name} - {strategy}")
        except Exception as e:
            print(f"✗ Error cargando {name}: {e}")
            continue
    
    # Obtener consenso
    consensus = int(os.getenv('CONSENSUS_THRESHOLD', '2'))
    
    # Validar consenso
    if consensus > len(strategies):
        print(
            f"⚠️  CONSENSUS_THRESHOLD ({consensus}) mayor que número de estrategias ({len(strategies)}). "
            f"Ajustando a {len(strategies)}"
        )
        consensus = len(strategies)
    
    return strategies, consensus


def get_strategy_config_summary() -> Dict[str, Any]:
    """Obtiene resumen de configuración de estrategias desde .env.
    
    Returns:
        Diccionario con configuración actual
    """
    active_str = os.getenv('ACTIVE_STRATEGIES', 'RSI,MACD,BOLLINGER')
    active_names = [s.strip().upper() for s in active_str.split(',')]
    
    summary = {
        'active_strategies': active_names,
        'consensus_threshold': int(os.getenv('CONSENSUS_THRESHOLD', '2')),
        'strategy_configs': {}
    }
    
    for name in active_names:
        env_key = f"STRATEGY_{name}"
        config_str = os.getenv(env_key, "")
        if config_str:
            summary['strategy_configs'][name] = parse_strategy_config(config_str)
    
    return summary


def print_strategy_config():
    """Imprime la configuración actual de estrategias de forma legible."""
    summary = get_strategy_config_summary()
    
    print("\n" + "=" * 70)
    print("CONFIGURACIÓN DE ESTRATEGIAS DESDE .ENV")
    print("=" * 70)
    print()
    
    print(f"Estrategias Activas: {', '.join(summary['active_strategies'])}")
    print(f"Consenso Requerido: {summary['consensus_threshold']}/{len(summary['active_strategies'])}")
    print()
    
    print("Parámetros por Estrategia:")
    print("-" * 70)
    for name, params in summary['strategy_configs'].items():
        print(f"  {name}:")
        for key, value in params.items():
            print(f"    • {key}: {value}")
    print()


if __name__ == "__main__":
    """Prueba de carga de configuración."""
    from dotenv import load_dotenv
    
    # Cargar .env
    load_dotenv()
    
    print("\n🔧 PRUEBA DE CARGA DE CONFIGURACIÓN\n")
    
    # Mostrar configuración
    print_strategy_config()
    
    # Cargar estrategias
    print("Cargando estrategias...")
    print("-" * 70)
    strategies, consensus = load_strategies_from_env()
    print()
    
    print(f"✅ {len(strategies)} estrategias cargadas correctamente")
    print(f"📊 Consenso configurado: {consensus}/{len(strategies)}")
    print()
    
    # Crear estrategia combinada
    from .combined import CombinedStrategy
    
    combined = CombinedStrategy(strategies, consensus)
    print(f"🎯 Estrategia Combinada: {combined}")
