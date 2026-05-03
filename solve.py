"""
Instrucciones de ejecucion:
## Requisitos

- **Python** 3.10 o superior (el proyecto usa anotaciones de tipos modernas).
- Opcional pero recomendado: entorno virtual (`.venv` u otro nombre).

---

## Instalación

Desde la raíz del proyecto (`pia/`):

```bash
python3 -m venv .venv
source .venv/bin/activate   # En Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Si no instala PuLP, el programa igual ejecutará la solución por **programación dinámica**; el mensaje en consola indicará que PuLP no está disponible y no se comparará con el modelo entero.

---

## Cómo ejecutar la solución

Con el entorno activado y estando en la carpeta que contiene `solve.py` y `datos_portafolio.py`:

```bash
python solve.py
```

La salida incluye:

1. Un **resumen del escenario** (valores devueltos por `datos_portafolio.resumen_escenario()`).
2. **Tiempos de ejecución** de los métodos habilitados (DP y, si aplica, PuLP), calculados en procesos separados.
3. **Utilidad esperada**, capital y riesgo usados frente a los presupuestos.
4. La **lista de instrumentos seleccionados** según la máscara de la solución óptima.

Para modificar el caso de estudio, edita los presupuestos y el catálogo en `datos_portafolio.py` y, si cambias la semántica de los datos, actualiza la narrativa en `estructura_datos_portafolio.md` para mantener coherencia con el reporte escrito del PIA.

---

Resolución del problema de mochila 0-1 bidimensional (capital y riesgo).

Incluye: enumeración por máscaras (fuerza bruta), programación dinámica en
tabla 2D (capital en miles de MXN) y modelo de programación lineal entera
(PuLP + CBC) según librerías permitidas en el PIA.
"""

from __future__ import annotations

from typing import Iterator
import math
import time
from contextlib import contextmanager
from concurrent.futures import ProcessPoolExecutor, as_completed

import datos_portafolio as dp

try:
    import pulp
except ImportError:  # pragma: no cover - dependencia opcional en entornos mínimos
    pulp = None  # type: ignore[assignment]

@contextmanager
def timer(name: str) -> Iterator[None]:
    """
    Mide el tiempo de ejecución de un bloque de código.

    Args:
        name: Nombre del bloque de código.
    """
    start = time.time()
    yield
    end = time.time()
    print("-"*20 + f" {name} " + "-"*20)
    print(f"{name}: {end - start:.2f} seconds\n")

def _capital_en_miles_pesos(capital_mxn: float) -> int:
    """
    Convierte capital a miles de pesos enteros.

    La DP bidimensional requiere índices enteros; se asume que los montos
    son múltiplos de 1000 MXN (como en el catálogo actual).

    Args:
        capital_mxn: Capital en pesos.

    Returns:
        Capital en miles de pesos.

    Raises:
        ValueError: Si el monto no es múltiplo de 1000 (salvo tolerancia numérica).
    """
    residuo = abs(capital_mxn % 1000.0)
    if residuo > 1e-6 and residuo < 1000.0 - 1e-6:
        raise ValueError(
            "capital_mxn debe ser múltiplo de 1000 para la DP en miles de pesos"
        )
    return int(round(capital_mxn / 1000.0))


def mejor_portafolio_iterativo(
    instrumentos: tuple[dp.Instrumento, ...],
    presupuesto_capital: float,
    presupuesto_riesgo: float,
) -> tuple[float, float, float, int]:
    """
    Encuentra la utilidad esperada máxima eligiendo un subconjunto de instrumentos.

    Restricciones: suma de capital <= presupuesto_capital y suma de riesgo
    <= presupuesto_riesgo. Cada instrumento se toma completo o no se toma.

    Esta solucion tiene una complejidad temporal de O(2^n), donde n es el numero de instrumentos.
    Por lo tanto, es ineficiente para un numero grande de instrumentos.

    Args:
        instrumentos: Catálogo de mandatos.
        presupuesto_capital: Tope de capital (MXN).
        presupuesto_riesgo: Tope de riesgo (puntos).

    Returns:
        Tupla (capital_usado, riesgo_usado, utilidad_total, mascara_bits).
        La máscara tiene el bit i en 1 si el instrumento i está seleccionado.
    """
    n = len(instrumentos)
    mejor_utilidad = -1.0
    mejor_cap = 0.0
    mejor_riesgo = 0.0
    mejor_mascara = 0

    for mascara in range(1 << n):
        cap = 0.0
        riesgo = 0.0
        util = 0.0
        for i in range(n):
            if (mascara >> i) & 1:
                inst = instrumentos[i]
                cap += inst.capital_mxn
                riesgo += inst.riesgo_pts
                util += inst.utilidad_esperada_mxn

        if cap <= presupuesto_capital and riesgo <= presupuesto_riesgo:
            if util > mejor_utilidad:
                mejor_utilidad = util
                mejor_cap = cap
                mejor_riesgo = riesgo
                mejor_mascara = mascara

    return mejor_cap, mejor_riesgo, mejor_utilidad, mejor_mascara


def mejor_portafolio_dp(
    instrumentos: tuple[dp.Instrumento, ...],
    presupuesto_capital: float,
    presupuesto_riesgo: float,
) -> tuple[float, float, float, int]:
    """
    Resuelve la mochila 0-1 con dos restricciones mediante programación dinámica.

    Estado ``dp[c][r]``: utilidad máxima con capital total exactamente ``c``
    miles de pesos y riesgo total exactamente ``r`` puntos. Se recorre cada
    instrumento una vez con actualización hacia atrás en ``c`` y ``r`` (0-1).

    Complejidad temporal aproximada: O(n · B' · R), con B' el presupuesto de
    capital en miles de pesos y R el tope de riesgo en puntos enteros.

    Args:
        instrumentos: Catálogo de mandatos (capital en múltiplos de 1000 MXN).
        presupuesto_capital: Tope de capital (MXN).
        presupuesto_riesgo: Tope de riesgo (puntos enteros o semienteros).

    Returns:
        Tupla (capital_usado, riesgo_usado, utilidad_total, mascara_bits).

    Raises:
        ValueError: Si algún capital no es discretizable en miles de pesos.
    """
    b_mil = _capital_en_miles_pesos(presupuesto_capital)
    r_max = int(round(presupuesto_riesgo))

    pesos_cap = [_capital_en_miles_pesos(i.capital_mxn) for i in instrumentos]
    pesos_riesgo = [int(round(i.riesgo_pts)) for i in instrumentos]

    neg_inf = float("-inf")
    dp = [[neg_inf] * (r_max + 1) for _ in range(b_mil + 1)]
    ultimo = [[-1] * (r_max + 1) for _ in range(b_mil + 1)]
    dp[0][0] = 0.0

    for idx, inst in enumerate(instrumentos):
        w_c = pesos_cap[idx]
        w_r = pesos_riesgo[idx]
        v = inst.utilidad_esperada_mxn
        for c in range(b_mil, w_c - 1, -1):
            for r in range(r_max, w_r - 1, -1):
                prev = dp[c - w_c][r - w_r]
                if prev == neg_inf:
                    continue
                cand = prev + v
                if cand > dp[c][r]:
                    dp[c][r] = cand
                    ultimo[c][r] = idx

    mejor_util = neg_inf
    mejor_c_mil = 0
    mejor_r = 0
    for c in range(b_mil + 1):
        for r in range(r_max + 1):
            if dp[c][r] > mejor_util:
                mejor_util = dp[c][r]
                mejor_c_mil = c
                mejor_r = r

    if mejor_util == neg_inf:
        return 0.0, 0.0, 0.0, 0

    mascara = 0
    c_act, r_act = mejor_c_mil, mejor_r
    while c_act > 0 or r_act > 0:
        idx = ultimo[c_act][r_act]
        if idx < 0:
            break
        mascara |= 1 << idx
        c_act -= pesos_cap[idx]
        r_act -= pesos_riesgo[idx]

    return (
        float(mejor_c_mil * 1000),
        float(mejor_r),
        mejor_util,
        mascara,
    )


def mejor_portafolio_pulp(
    instrumentos: tuple[dp.Instrumento, ...],
    presupuesto_capital: float,
    presupuesto_riesgo: float,
) -> tuple[float, float, float, int]:
    """
    Resuelve la mochila 0-1 con dos restricciones mediante PL entera (PuLP).

    Modelo: maximizar ``sum_i E_i x_i`` con ``x_i`` binarias, ``sum C_i x_i <= B``,
    ``sum R_i x_i <= R``. El solver por defecto es CBC (incluido con PuLP).

    Args:
        instrumentos: Catálogo de mandatos.
        presupuesto_capital: Tope de capital (MXN).
        presupuesto_riesgo: Tope de riesgo (puntos).

    Returns:
        Tupla (capital_usado, riesgo_usado, utilidad_total, mascara_bits).

    Raises:
        ImportError: Si PuLP no está instalado.
        RuntimeError: Si el solver no devuelve solución óptima.
    """
    if pulp is None:
        raise ImportError(
            "Se requiere el paquete 'pulp'. Instálelo con: pip install pulp"
        )

    n = len(instrumentos)
    prob = pulp.LpProblem("Mochila_portafolio", pulp.LpMaximize)
    x = pulp.LpVariable.dicts("x", range(n), cat=pulp.LpBinary)

    prob += pulp.lpSum(
        instrumentos[i].utilidad_esperada_mxn * x[i] for i in range(n)
    )
    prob += (
        pulp.lpSum(instrumentos[i].capital_mxn * x[i] for i in range(n))
        <= presupuesto_capital
    )
    prob += (
        pulp.lpSum(instrumentos[i].riesgo_pts * x[i] for i in range(n))
        <= presupuesto_riesgo
    )

    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if prob.status != pulp.LpStatusOptimal:
        raise RuntimeError(
            f"PuLP no alcanzó óptimo (estado={pulp.LpStatus[prob.status]})"
        )

    mascara = 0
    cap = 0.0
    riesgo = 0.0
    util = 0.0
    for i in range(n):
        val = pulp.value(x[i])
        if val is not None and val > 0.5:
            mascara |= 1 << i
            inst = instrumentos[i]
            cap += inst.capital_mxn
            riesgo += inst.riesgo_pts
            util += inst.utilidad_esperada_mxn

    obj = pulp.value(prob.objective)
    if obj is None:
        raise RuntimeError("No se pudo leer el valor objetivo del modelo PuLP")

    return cap, riesgo, float(obj), mascara


def instrumentos_seleccionados(
    instrumentos: tuple[dp.Instrumento, ...], mascara: int
) -> list[dp.Instrumento]:
    """
    Devuelve la lista de instrumentos cuyo índice está activo en la máscara.

    Args:
        instrumentos: Catálogo completo.
        mascara: Entero con bits por posición de instrumento.

    Returns:
        Lista ordenada por índice creciente.
    """
    return [
        instrumentos[i]
        for i in range(len(instrumentos))
        if (mascara >> i) & 1
    ]


def _ejecutar_metodo_con_tiempo(
    nombre_metodo: str,
    instrumentos: tuple[dp.Instrumento, ...],
    presupuesto_capital: float,
    presupuesto_riesgo: float,
) -> tuple[str, float, tuple[float, float, float, int]]:
    """
    Ejecuta un método de solución y devuelve su tiempo de ejecución.

    Args:
        nombre_metodo: Nombre del método a ejecutar.
        instrumentos: Catálogo de instrumentos.
        presupuesto_capital: Tope de capital (MXN).
        presupuesto_riesgo: Tope de riesgo (puntos).

    Returns:
        Tupla (nombre_metodo, tiempo_segundos, resultado_metodo).
    """
    inicio = time.perf_counter()
    if nombre_metodo == "mejor_portafolio_iterativo":
        resultado = mejor_portafolio_iterativo(
            instrumentos, presupuesto_capital, presupuesto_riesgo
        )
    elif nombre_metodo == "mejor_portafolio_dp":
        resultado = mejor_portafolio_dp(
            instrumentos, presupuesto_capital, presupuesto_riesgo
        )
    elif nombre_metodo == "mejor_portafolio_pulp":
        resultado = mejor_portafolio_pulp(
            instrumentos, presupuesto_capital, presupuesto_riesgo
        )
    else:
        raise ValueError(f"Método no reconocido: {nombre_metodo}")
    fin = time.perf_counter()
    return nombre_metodo, fin - inicio, resultado


def main() -> None:
    """Ejecuta la búsqueda y muestra el resumen del escenario y la solución."""
    for nombre, valor in dp.resumen_escenario().items():
        print(f"{nombre}: {valor}")

    instrumentos = dp.INSTRUMENTOS
    metodos = ["mejor_portafolio_dp"]
    if pulp is not None:
        metodos.append("mejor_portafolio_pulp")
    else:
        print(
            "(PuLP no instalado: omita o ejecute pip install -r requirements.txt)\n"
        )

    resultados: dict[str, tuple[float, float, float, int]] = {}
    tiempos: dict[str, float] = {}

    print("-" * 24 + " Tiempos de ejecución " + "-" * 24)
    with ProcessPoolExecutor(max_workers=len(metodos)) as executor:
        futuros = [
            executor.submit(
                _ejecutar_metodo_con_tiempo,
                metodo,
                instrumentos,
                dp.PRESUPUESTO_CAPITAL_MXN,
                dp.PRESUPUESTO_RIESGO_PTS,
            )
            for metodo in metodos
        ]
        for futuro in as_completed(futuros):
            nombre, segundos, resultado = futuro.result()
            resultados[nombre] = resultado
            tiempos[nombre] = segundos
            print(f"{nombre}: {segundos:.6f} s")
    print()

    # cap_bf, riesgo_bf, util_bf, mascara_bf = resultados["mejor_portafolio_iterativo"]
    cap_dp, riesgo_dp, util_dp, mascara_dp = resultados["mejor_portafolio_dp"]
    cap_pl, riesgo_pl, util_pl, mascara_pl = 0.0, 0.0, 0.0, 0
    if "mejor_portafolio_pulp" in resultados:
        cap_pl, riesgo_pl, util_pl, mascara_pl = resultados["mejor_portafolio_pulp"]

    if pulp is not None:
        assert math.isclose(util_dp, util_pl, rel_tol=0, abs_tol=1e-2)
        assert math.isclose(cap_dp, cap_pl, rel_tol=0, abs_tol=1e-2)
        assert math.isclose(riesgo_dp, riesgo_pl, rel_tol=0, abs_tol=1e-2)

    print("-" * 26 + " Misma solución (DP 2D) " + "-" * 26)
    print(f"Utilidad esperada total (MXN): {util_dp:,.2f}")
    print(f"Capital usado (MXN): {cap_dp:,.2f} / {dp.PRESUPUESTO_CAPITAL_MXN:,.2f}")
    print(f"Riesgo usado (pts): {riesgo_dp:.2f} / {dp.PRESUPUESTO_RIESGO_PTS:.2f}")

    if pulp is not None:
        print("-" * 22 + " Misma solución (PuLP / PL entera) " + "-" * 22)
        print(f"Utilidad esperada total (MXN): {util_pl:,.2f}")
        print(
            f"Capital usado (MXN): {cap_pl:,.2f} / {dp.PRESUPUESTO_CAPITAL_MXN:,.2f}"
        )
        print(f"Riesgo usado (pts): {riesgo_pl:.2f} / {dp.PRESUPUESTO_RIESGO_PTS:.2f}")

    mascara = mascara_dp if not pulp else mascara_pl
    print("-" * 24 + " Instrumentos seleccionados " + "-" * 24)
    for inst in instrumentos_seleccionados(instrumentos, mascara):
        print(f"  [{inst.id}] {inst.nombre}")
    print(f"Total seleccionados: {bin(mascara).count('1')}")


if __name__ == "__main__":
    main()
