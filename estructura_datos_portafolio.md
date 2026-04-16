# Estructura de datos — Tema 14: mochila en portafolios con presupuesto de riesgo estricto

Escenario alineado con `INSTRUCCIONES_PROYECTO.md`: datos hipotéticos con orden de magnitud y relaciones típicas de un comité de inversiones institucional en México (MXN, horizonte táctico 12 meses).

---

## 1. Contexto operativo (ficticio)

**Mandante:** Fondo de pensiones *Horizonte Norte* (ficticio).  
**Unidad:** Mesa táctica de asignación con **cupo de capital** a desplegar en una sola ventana y **cupo de riesgo** aprobado por el comité de riesgos.  
**Decisión:** Elegir un subconjunto de **mandatos/instrumentos discretos** (cada uno es tomar o no tomar el tramo completo; no fracciones).  
**Objetivo de gestión:** Maximizar la **contribución esperada al resultado** del bucket (en MXN anualizado), sin exceder capital ni el **presupuesto de riesgo** en puntos internos *Sigma-Risk* (escala del comité, no lineal con la volatilidad para reflejar límites por concentración, liquidez y colas).

---

## 2. Variables del modelo (mapeo a mochila)

| Símbolo | Significado |
|---------|-------------|
| \(i\) | Índice del instrumento o mandato \(i = 1,\ldots,n\). |
| \(x_i \in \{0,1\}\) | 1 si se selecciona el mandato \(i\); 0 si no. |
| \(C_i\) | Capital comprometido si se selecciona \(i\) (MXN). |
| \(r_i\) | Consumo de **presupuesto de riesgo** si se selecciona \(i\) (puntos *Sigma-Risk*). |
| \(E_i\) | **Utilidad esperada** anualizada atribuible al mandato \(i\) si se incluye (MXN). |
| \(B\) | Presupuesto máximo de capital desplegable (MXN). |
| \(R\) | Presupuesto máximo agregado de riesgo (puntos *Sigma-Risk*). |

**Interpretación:** Es una **mochila bidimensional** (o mochila con dos restriciones knapsack): maximizar \(\sum_i E_i x_i\) sujeto a \(\sum_i C_i x_i \le B\) y \(\sum_i r_i x_i \le R\), con \(x_i \in \{0,1\}\).

---

## 3. Parámetros globales del escenario

| Parámetro | Valor | Notas |
|-----------|--------|--------|
| \(B\) | 118 750 000 | MXN; remanente táctico tras restricciones regulatorias y liquidez mínima en otras cubetas. |
| \(R\) | 95 | Tope de comité para esta ventana; incluye buffer explícito respecto al límite duro (100). |
| Moneda | MXN | Todos los montos coherentes con mandatos en pesos o cobertura cambiaria ya reflejada en \(E_i\) y \(r_i\). |
| Horizonte implícito en \(E_i\) | 12 meses | Retornos esperados y riesgo calibrados a esa ventana. |

---

## 4. Tabla de instrumentos / mandatos

Montos en MXN; \(E_i\) es utilidad esperada **en pesos** (no porcentaje), para alinear la función objetivo con decisión gerencial.

| id | Mandato (descripción breve) | \(C_i\) (MXN) | \(r_i\) (pts) | \(E_i\) (MXN) | Nota de calibración |
|----|-----------------------------|---------------|---------------|----------------|----------------------|
| 1 | Escalera CETES 91/182 d (rollover automatizado) | 19 200 000 | 9 | 835 200 | Bajo riesgo; retorno acorde a tasa gubernamental corta + pequeño alpha operativo. |
| 2 | Cesta bonos corporativos IG (5 emisores, duration media) | 24 600 000 | 24 | 1 624 800 | Spread corporativo; \(r_i\) refleja duration y concentración por emisor. |
| 3 | Tramo bonos high yield latam (hedge FX parcial) | 11 800 000 | 31 | 1 062 000 | Mayor cupón; riesgo de crédito y vol FX residual. |
| 4 | FIBRA industrial (logística última milla, 2 activos) | 16 400 000 | 28 | 1 345 800 | Mix renta/capital; riesgo de tasa y ocupación. |
| 5 | ETF accionario global (hedge a MXN) | 14 250 000 | 36 | 1 424 850 | Beta global; comité penaliza por correlación con book existente. |
| 6 | Deuda privada (club deal, senior secured) | 21 500 000 | 33 | 1 828 750 | Illiquidity premium; riesgo operativo de documentación. |
| 7 | Estrategia commodities (roll rules, gestor externo) | 8 750 000 | 41 | 831 250 | Contango/backwardation; \(r_i\) alto por colas y límites de VAR interno. |
| 8 | Fondo bonos EM moneda local (hedge parcial) | 12 900 000 | 38 | 1 213 800 | Beta soberana + FX. |
| 9 | Market neutral equity (L/S, low net) | 18 600 000 | 22 | 1 302 000 | Riesgo bajo neto pero riesgo de modelo y de contraparte. |
| 10 | Deuda infraestructura (proyecto energía, bono bullet) | 22 800 000 | 29 | 1 710 000 | Riesgo regulatorio y completion embedded en \(r_i\). |
| 11 | Crédito estructurado (tramo mezzanine CLO interno) | 9 400 000 | 44 | 987 000 | Cola de pérdidas; alto peso en presupuesto de riesgo. |
| 12 | Renta variable México small-mid cap (mandato activo) | 15 700 000 | 39 | 1 492 300 | Concentración local; beta y liquidez. |

**Totales si se eligieran todos:** \(\sum C_i = 195\,900\,000\) (excede \(B\)); \(\sum r_i = 374\) (excede \(R\)); \(\sum E_i \approx 15{,}657\,750\). El problema obliga **trade-offs** realistas entre retorno esperado, capital y riesgo.

---

## 5. Por qué no es un conjunto “plano”

- **Capas de restricción:** Capital y riesgo no son proporcionales (mismo capital puede consumir muy distinto \(r_i\) por tipo de riesgo).  
- **Órdenes de magnitud heterogéneos:** Mandatos desde ~8.75 M hasta ~24.6 M; \(E_i/C_i\) (retorno esperado implícito) no es constante.  
- **Fricciones institucionales:** Instrumentos ilíquidos con \(r_i\) alto aunque el cupón parezca atractivo (id 11 vs id 6).  
- **Coherencia regional:** Mezcla de peso, hedges y EM que un comité mexicano podría discutir en la misma mesa.

---

## 6. Esquema sugerido para implementación en Python

- **`list[Instrumento]`** donde cada `Instrumento` tiene: `id: int`, `nombre: str`, `capital_mxn: int | float`, `riesgo_pts: int | float`, `utilidad_esperada_mxn: int | float`.  
- **Parámetros globales:** `presupuesto_capital_mxn`, `presupuesto_riesgo_pts`.  
- Los valores numéricos están centralizados en `datos_portafolio.py` para reutilizarlos en PuLP u otra librería.

---

*Datos hipotéticos para el PIA; no constituyen asesoría de inversión.*
