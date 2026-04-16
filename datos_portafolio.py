"""
Datos del escenario de optimización de portafolio (tema 14, PIA IO).

Define la estructura de instrumentos y parámetros globales para un modelo
tipo mochila 0-1 con dos restricciones: capital y presupuesto de riesgo.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Instrumento:
    """
    Representa un mandato de inversión discreto (incluir o no el tramo completo).

    Attributes:
        id: Identificador entero único.
        nombre: Descripción breve del mandato.
        capital_mxn: Capital comprometido si se selecciona (MXN).
        riesgo_pts: Consumo del presupuesto de riesgo del comité (puntos Sigma-Risk).
        utilidad_esperada_mxn: Contribución esperada al resultado en 12 meses (MXN).
    """

    id: int
    nombre: str
    capital_mxn: float
    riesgo_pts: float
    utilidad_esperada_mxn: float


# Presupuesto máximo de capital desplegable en la ventana táctica (MXN).
PRESUPUESTO_CAPITAL_MXN: float = 118_750_000.0

# Presupuesto máximo agregado de riesgo (puntos internos del comité).
PRESUPUESTO_RIESGO_PTS: float = 95.0

# Catálogo de mandatos alineado con estructura_datos_portafolio.md.
INSTRUMENTOS: tuple[Instrumento, ...] = (
    Instrumento(
        1,
        "Escalera CETES 91/182 d (rollover automatizado)",
        19_200_000.0,
        9.0,
        835_200.0,
    ),
    Instrumento(
        2,
        "Cesta bonos corporativos IG (5 emisores, duration media)",
        24_600_000.0,
        24.0,
        1_624_800.0,
    ),
    Instrumento(
        3,
        "Tramo bonos high yield latam (hedge FX parcial)",
        11_800_000.0,
        31.0,
        1_062_000.0,
    ),
    Instrumento(
        4,
        "FIBRA industrial (logística última milla, 2 activos)",
        16_400_000.0,
        28.0,
        1_345_800.0,
    ),
    Instrumento(
        5,
        "ETF accionario global (hedge a MXN)",
        14_250_000.0,
        36.0,
        1_424_850.0,
    ),
    Instrumento(
        6,
        "Deuda privada (club deal, senior secured)",
        21_500_000.0,
        33.0,
        1_828_750.0,
    ),
    Instrumento(
        7,
        "Estrategia commodities (roll rules, gestor externo)",
        8_750_000.0,
        41.0,
        831_250.0,
    ),
    Instrumento(
        8,
        "Fondo bonos EM moneda local (hedge parcial)",
        12_900_000.0,
        38.0,
        1_213_800.0,
    ),
    Instrumento(
        9,
        "Market neutral equity (L/S, low net)",
        18_600_000.0,
        22.0,
        1_302_000.0,
    ),
    Instrumento(
        10,
        "Deuda infraestructura (proyecto energía, bono bullet)",
        22_800_000.0,
        29.0,
        1_710_000.0,
    ),
    Instrumento(
        11,
        "Crédito estructurado (tramo mezzanine CLO interno)",
        9_400_000.0,
        44.0,
        987_000.0,
    ),
    Instrumento(
        12,
        "Renta variable México small-mid cap (mandato activo)",
        15_700_000.0,
        39.0,
        1_492_300.0,
    ),
    Instrumento(
        13,
        "Bonos gubernamentales UDI (inflación real, duration larga)",
        13_600_000.0,
        18.0,
        972_400.0,
    ),
    Instrumento(
        14,
        "Deuda corporativa ESG IG (emisores utilities y consumo)",
        17_900_000.0,
        23.0,
        1_253_000.0,
    ),
    Instrumento(
        15,
        "Infraestructura carretera (fideicomiso de peajes)",
        20_300_000.0,
        32.0,
        1_664_600.0,
    ),
    Instrumento(
        16,
        "REIT logístico USA con cobertura parcial de divisa",
        12_400_000.0,
        30.0,
        1_091_200.0,
    ),
    Instrumento(
        17,
        "Crédito privado middle-market (tramo senior)",
        18_800_000.0,
        35.0,
        1_635_600.0,
    ),
    Instrumento(
        18,
        "Estrategia cuantitativa trend-following multi-activo",
        9_900_000.0,
        27.0,
        861_300.0,
    ),
    Instrumento(
        19,
        "Bonos soberanos Asia emergente (duración corta)",
        14_700_000.0,
        26.0,
        1_117_200.0,
    ),
    Instrumento(
        20,
        "Mandato de arbitraje de volatilidad delta-neutral",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        21,
        "Ejemplo 1",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        22,
        "Ejemplo 2",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        23,
        "Ejemplo 3",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        24,
        "Ejemplo 4",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        25,
        "Ejemplo 5",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        26,
        "Ejemplo 6",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        27,
        "Ejemplo 7",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        28,
        "Ejemplo 8",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        29,
        "Ejemplo 9",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        30,
        "Ejemplo 10",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        31,
        "Ejemplo 11",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        32,
        "Ejemplo 12",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        33,
        "Ejemplo 13",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        34,
        "Ejemplo 14",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        35,
        "Ejemplo 15",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        36,
        "Ejemplo 16",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        37,
        "Ejemplo 17",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        38,
        "Ejemplo 18",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        39,
        "Ejemplo 19",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
    Instrumento(
        40,
        "Ejemplo 20",
        10_500_000.0,
        34.0,
        997_500.0,
    ),
)


def resumen_escenario() -> dict[str, float]:
    """
    Devuelve totales del catálogo si se seleccionaran todos los mandatos.

    Returns:
        Diccionario con sumas de capital, riesgo y utilidad esperada.
    """
    c = sum(i.capital_mxn for i in INSTRUMENTOS)
    r = sum(i.riesgo_pts for i in INSTRUMENTOS)
    e = sum(i.utilidad_esperada_mxn for i in INSTRUMENTOS)
    return {
        "capital_total_si_todos_mxn": c,
        "riesgo_total_si_todos_pts": r,
        "utilidad_total_si_todos_mxn": e,
    }
