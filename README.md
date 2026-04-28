# PIA — Selección de portafolio (mochila 0-1 bidimensional)

Implementación en Python del **tema 14** del Producto Integrador de Aprendizaje (Investigación de Operaciones): maximizar la utilidad esperada de un conjunto de mandatos de inversión discretos, respetando límites de **capital** y de **presupuesto de riesgo** (problema de la mochila con dos restricciones).

---

## Estructura del proyecto

| Ruta | Descripción |
|------|-------------|
| `docs/Reporte_2049129.pdf` | Reporte del proyecto explicando las decisiones y proceso de desarrollo. |
| `solve.py` | Punto de entrada y lógica de resolución: programación dinámica en dos dimensiones (capital en miles de MXN y riesgo) y, si está instalado PuLP, modelo de **programación lineal entera** (PuLP + CBC) para contrastar la misma solución. Incluye utilidades de medición de tiempos y ejecución en paralelo de métodos. |
| `datos_portafolio.py` | Datos del escenario: clase `Instrumento`, presupuestos globales (`PRESUPUESTO_CAPITAL_MXN`, `PRESUPUESTO_RIESGO_PTS`), catálogo `INSTRUMENTOS` y función `resumen_escenario()` usada al arrancar la solución. |
| `__init__.py` | Marca el directorio como paquete Python (metadatos del módulo del proyecto). |
| `requirements.txt` | Dependencias: `pulp>=3.0` (el solver CBC suele distribuirse con PuLP). |
| `docs/INSTRUCCIONES_PROYECTO.md` | Lineamientos del PIA, rúbrica y contexto académico del curso. |
| `docs/estructura_datos_portafolio.md` | Documentación del escenario ficticio, variables del modelo y convenciones de datos (alineado con el catálogo en `datos_portafolio.py`). |

Los archivos `.py` deben ejecutarse con el directorio del proyecto en el `PYTHONPATH` (por ejemplo, situándose en la carpeta raíz del repositorio antes de invocar `python`).

---

## Requisitos

- **Python** 3.10 o superior (el proyecto usa anotaciones de tipos modernas).
- Opcional pero recomendado: entorno virtual (`.venv` u otro nombre).

---

## Instalación

Desde la raíz del proyecto (`pia/`):

```bash
python3 -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
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

## Referencia académica

Los criterios de entrega, fechas y formato del trabajo escrito se describen en `INSTRUCCIONES_PROYECTO.md`.
