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
        "Fondo mercado monetario USD (cobertura cambiaria a MXN)",
        11_200_000.0,
        11.0,
        672_000.0,
    ),
    Instrumento(
        22,
        "Bonos subordinados bancarios MX Tier 2 (cesta 3 emisoras)",
        16_100_000.0,
        27.0,
        1_287_000.0,
    ),
    Instrumento(
        23,
        "Dividend aristocrats USA (mandato long-only con hedge a MXN)",
        13_300_000.0,
        33.0,
        1_331_500.0,
    ),
    Instrumento(
        24,
        "Crédito revolver senior a emisor corporativo calificación BB-",
        8_900_000.0,
        40.0,
        801_000.0,
    ),
    Instrumento(
        25,
        "Factoring a Pymes (cartera diversificada, mandato fondo)",
        7_600_000.0,
        32.0,
        684_000.0,
    ),
    Instrumento(
        26,
        "ETF deuda soberana linkada a inflación global (hedge MXN)",
        14_200_000.0,
        25.0,
        1_136_000.0,
    ),
    Instrumento(
        27,
        "Secondaries private equity (ticket táctico, liquidez mejorada)",
        19_500_000.0,
        42.0,
        1_560_000.0,
    ),
    Instrumento(
        28,
        "Bonos Mbonos largo plazo (extensión de duration táctica)",
        17_200_000.0,
        21.0,
        946_000.0,
    ),
    Instrumento(
        29,
        "Bonos verdes municipales México (cesta cuatro emisoras)",
        12_300_000.0,
        20.0,
        861_000.0,
    ),
    Instrumento(
        30,
        "Deuda corporativa Asia investment grade (cesta regional)",
        15_100_000.0,
        30.0,
        1_283_500.0,
    ),
    Instrumento(
        31,
        "Renta variable Japón TOPIX (mandato activo, hedge divisa)",
        11_000_000.0,
        37.0,
        1_045_000.0,
    ),
    Instrumento(
        32,
        "ABS hipotecario residencial senior (cesta tramos locales)",
        18_300_000.0,
        24.0,
        1_281_000.0,
    ),
    Instrumento(
        33,
        "Estrategia carry G10 FX (overlay macro, bajo nominal)",
        9_100_000.0,
        35.0,
        728_000.0,
    ),
    Instrumento(
        34,
        "Infraestructura social (concesión educación, flujos indexados)",
        21_200_000.0,
        31.0,
        1_696_000.0,
    ),
    Instrumento(
        35,
        "Bonos AT1 bancarios europeos (tramo cauteloso, cupón fijo)",
        10_600_000.0,
        43.0,
        954_000.0,
    ),
    Instrumento(
        36,
        "Co-inversión VC growth late-stage (ticket único)",
        13_800_000.0,
        44.0,
        1_242_000.0,
    ),
    Instrumento(
        37,
        "Fondo temático agricultura y granos (futuros y roll rules)",
        8_200_000.0,
        39.0,
        738_000.0,
    ),
    Instrumento(
        38,
        "Híbridos corporativos MX (cesta high yield local)",
        16_700_000.0,
        36.0,
        1_502_300.0,
    ),
    Instrumento(
        39,
        "Deuda soberana EM moneda local (LatAm excl. México)",
        14_400_000.0,
        37.0,
        1_296_000.0,
    ),
    Instrumento(
        40,
        "Overlay corto USD/MXN táctico (derivados, nominal acotado)",
        5_500_000.0,
        38.0,
        605_000.0,
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
