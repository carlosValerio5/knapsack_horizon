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
| \(i\) | Índice del instrumento o mandato \(i = 1,\ldots,n\) (en el escenario base, \(n=40\)). |
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
| 13 | Bonos gubernamentales UDI (inflación real, duration larga) | 13 600 000 | 18 | 972 400 | Protección inflacionaria; \(r_i\) captura sensibilidad a tasas reales y convexidad. |
| 14 | Deuda corporativa ESG IG (emisores utilities y consumo) | 17 900 000 | 23 | 1 253 000 | Perfil defensivo IG; spread acotado con sesgo ESG en selección de emisor. |
| 15 | Infraestructura carretera (fideicomiso de peajes) | 20 300 000 | 32 | 1 664 600 | Flujos ligados a tráfico y marco regulatorio de concesión. |
| 16 | REIT logístico USA con cobertura parcial de divisa | 12 400 000 | 30 | 1 091 200 | Beta inmobiliaria USA; residual de FX y correlación con curva USA. |
| 17 | Crédito privado middle-market (tramo senior) | 18 800 000 | 35 | 1 635 600 | Senior secured; premio de iliquidez y diligencia de covenants. |
| 18 | Estrategia cuantitativa trend-following multi-activo | 9 900 000 | 27 | 861 300 | Riesgo de colas y reversión brusca; \(r_i\) refleja límites de estrés interno. |
| 19 | Bonos soberanos Asia emergente (duración corta) | 14 700 000 | 26 | 1 117 200 | Exposición soberana regional; duration corta reduce sensibilidad a tasas. |
| 20 | Mandato de arbitraje de volatilidad delta-neutral | 10 500 000 | 34 | 997 500 | Vega/skew; riesgo de modelo, de pin y de contraparte en derivados. |
| 21 | Fondo mercado monetario USD (cobertura cambiaria a MXN) | 11 200 000 | 11 | 672 000 | Colchón de liquidez; basis del hedge y límites de MM en divisa extranjera. |
| 22 | Bonos subordinados bancarios MX Tier 2 (cesta 3 emisoras) | 16 100 000 | 27 | 1 287 000 | Subordinación bancaria; riesgo de extensión y eventos regulatorios. |
| 23 | Dividend aristocrats USA (mandato long-only con hedge a MXN) | 13 300 000 | 33 | 1 331 500 | Acciones defensivas USA; residual beta y coste/riesgo del hedge a peso. |
| 24 | Crédito revolver senior a emisor corporativo calificación BB- | 8 900 000 | 40 | 801 000 | Concentración en un solo prestatario; spread alto con riesgo de deterioro. |
| 25 | Factoring a Pymes (cartera diversificada, mandato fondo) | 7 600 000 | 32 | 684 000 | Riesgo de cobranza y estacionalidad; diversificación limita pero no elimina colas. |
| 26 | ETF deuda soberana linkada a inflación global (hedge MXN) | 14 200 000 | 25 | 1 136 000 | Tasas reales globales; tracking y basis del instrumento sintético/ETF. |
| 27 | Secondaries private equity (ticket táctico, liquidez mejorada) | 19 500 000 | 42 | 1 560 000 | Descuento a NAV y selección de fondos; sigue siendo capital semi-ilíquido. |
| 28 | Bonos Mbonos largo plazo (extensión de duration táctica) | 17 200 000 | 21 | 946 000 | Apuesta direccional a curva larga MX; \(r_i\) por duration y volatilidad de precios. |
| 29 | Bonos verdes municipales México (cesta cuatro emisoras) | 12 300 000 | 20 | 861 000 | Crédito sub-soberano local; uso de recursos vinculado a proyectos verdes. |
| 30 | Deuda corporativa Asia investment grade (cesta regional) | 15 100 000 | 30 | 1 283 500 | Spread regional IG; componente divisa y liquidez secundaria asimétrica. |
| 31 | Renta variable Japón TOPIX (mandato activo, hedge divisa) | 11 000 000 | 37 | 1 045 000 | Equity Japón con cobertura; riesgo de basis y de factor value/carry. |
| 32 | ABS hipotecario residencial senior (cesta tramos locales) | 18 300 000 | 24 | 1 281 000 | Riesgo prepago y modelo de severidad; tramo senior amortigua cola. |
| 33 | Estrategia carry G10 FX (overlay macro, bajo nominal) | 9 100 000 | 35 | 728 000 | Desapalancamiento brusco del carry; \(r_i\) alto pese a nominal contenido. |
| 34 | Infraestructura social (concesión educación, flujos indexados) | 21 200 000 | 31 | 1 696 000 | Flujos largos plazo indexados; riesgo político y de ejecución del contrato. |
| 35 | Bonos AT1 bancarios europeos (tramo cauteloso, cupón fijo) | 10 600 000 | 43 | 954 000 | CoCos / bail-in; cola de capital regulatorio con eventos de conversión. |
| 36 | Co-inversión VC growth late-stage (ticket único) | 13 800 000 | 44 | 1 242 000 | Valoraciones de mercado privado y riesgo de marca a cierre de ronda. |
| 37 | Fondo temático agricultura y granos (futuros y roll rules) | 8 200 000 | 39 | 738 000 | Roll y contango; choques de oferta/demanda y correlación con clima. |
| 38 | Híbridos corporativos MX (cesta high yield local) | 16 700 000 | 36 | 1 502 300 | Calls/resets y subordinación en crédito local; spread con premio de complejidad. |
| 39 | Deuda soberana EM moneda local (LatAm excl. México) | 14 400 000 | 37 | 1 296 000 | Beta soberana regional sin MX; FX local y eventos idiosincráticos por país. |
| 40 | Overlay corto USD/MXN táctico (derivados, nominal acotado) | 5 500 000 | 38 | 605 000 | Poca notional con alto consumo de riesgo por colas FX y basis del overlay. |

**Totales si se eligieran todos:** \(\sum C_i = 578\,200\,000\) (excede \(B\)); \(\sum r_i = 1\,244\) (excede \(R\)); \(\sum E_i = 46\,899\,850\). El problema obliga **trade-offs** realistas entre retorno esperado, capital y riesgo.

---

## 5. Por qué no es un conjunto “plano”

- **Capas de restricción:** Capital y riesgo no son proporcionales (mismo capital puede consumir muy distinto \(r_i\) por tipo de riesgo).  
- **Órdenes de magnitud heterogéneas:** Mandatos desde ~5.5 M hasta ~24.6 M; \(E_i/C_i\) (retorno esperado implícito) no es constante.  
- **Fricciones institucionales:** Instrumentos ilíquidos con \(r_i\) alto aunque el cupón parezca atractivo (id 11 vs id 6).  
- **Coherencia regional:** Mezcla de peso, hedges y EM que un comité mexicano podría discutir en la misma mesa.

---

## 6. Esquema sugerido para implementación en Python

- **`list[Instrumento]`** donde cada `Instrumento` tiene: `id: int`, `nombre: str`, `capital_mxn: int | float`, `riesgo_pts: int | float`, `utilidad_esperada_mxn: int | float`.  
- **Parámetros globales:** `presupuesto_capital_mxn`, `presupuesto_riesgo_pts`.  
- Los valores numéricos están centralizados en `datos_portafolio.py` para reutilizarlos en PuLP u otra librería; el catálogo base define \(n=40\) instrumentos.

---

*Datos hipotéticos para el PIA; no constituyen asesoría de inversión.*
