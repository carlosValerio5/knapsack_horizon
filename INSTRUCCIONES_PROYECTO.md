# Producto Integrador de Aprendizaje (PIA)

**Investigación de Operaciones (IO)**  
Facultad de Ciencias Físico Matemáticas, UANL — Semestre Enero-Junio 2026

Este documento recopila los lineamientos y la rúbrica del proyecto final según el material oficial del curso (`PIA_IO_EJ2026.pdf`).

---

## 1. Objetivo del proyecto

El Producto Integrador de Aprendizaje (PIA) tiene como propósito fundamental que el estudiante aplique los modelos de optimización, administración de proyectos, teoría de juegos y teoría de colas a un problema de negocio y operaciones. El alumno deberá demostrar su capacidad para plantear un escenario hipotético altamente realista, modelarlo matemáticamente, resolverlo computacionalmente utilizando Python y sus librerías, e interpretar los resultados técnicos para la toma de decisiones gerenciales.

---

## 2. Especificaciones generales

- **Modalidad:** Trabajo estrictamente individual.
- **Asignación de tema:** Cada estudiante trabajará con un “caso de estudio” específico asignado por el profesor. No se evaluarán proyectos con temas duplicados.
- **Naturaleza de los datos:** Los escenarios deben ser hipotéticos pero con una estructura de datos altamente realista (costos, tiempos, capacidades, demandas, probabilidades). Se busca evitar la generación de datos planos mediante instrucciones simples a herramientas de IA. El modelo debe presentar una complejidad operativa propia de la industria.
- **Herramienta computacional:** Uso estricto y exclusivo del lenguaje de programación Python y sus módulos/librerías (por ejemplo: PuLP, SciPy, NetworkX, NumPy, Pandas, SimPy, según el tema).

---

## 3. Metodología de investigación de operaciones requerida

Dependiendo del tema asignado, el trabajo debe modelar y resolver de forma obligatoria la problemática central utilizando la teoría correspondiente:

| Área | Contenido obligatorio |
|------|------------------------|
| **Modelos de redes** | Algoritmos para determinar la **ruta mínima** o la **ruta de máximo flujo** en sistemas de logística, transporte o telecomunicaciones. |
| **Administración de proyectos (PERT/CPM)** | Definición de actividades, predecesoras, tiempos (determinísticos o probabilísticos), cálculo de la ruta crítica y holguras. |
| **Problema de la mochila** | Optimización entera para maximizar el valor de selección bajo restricciones de capacidad (volumen, peso, presupuesto). |
| **Teoría de juegos** | Resolución de problemas competitivos (juegos de suma cero, juegos de dos personas, estrategias mixtas), determinando el punto de silla o las probabilidades óptimas de cada estrategia. |
| **Teoría de colas** | Análisis de líneas de espera: descripción del sistema, tasas de llegada, tasas de servicio y disciplinas (FIFO, LIFO). Modelar sistemas **M/M/1** o **M/M/c** y calcular métricas de desempeño (\(L_q\), \(L_s\), \(W_q\), \(W_s\), probabilidades de estado). |

---

## 4. Estructura del trabajo escrito

El documento final debe estructurarse como un reporte técnico de ingeniería/negocios:

1. **Portada y declaración de originalidad:** Datos institucionales y declaración honesta sobre la autoría del código.
2. **Introducción y contexto:** Descripción detallada del escenario hipotético realista, la empresa (ficticia) y la problemática a resolver.
3. **Definición de datos y variables:** Tablas de datos (costos, tiempos, nodos, tasas). Justificación de por qué los datos son realistas y no triviales.
4. **Modelado matemático:** Planteamiento formal del modelo (función objetivo, restricciones, ecuaciones de colas o matrices de pago).
5. **Desarrollo computacional (Python):** Explicación de las librerías utilizadas y fragmentos clave del código que dan solución al modelo.
6. **Conclusiones ejecutivas:** Interpretación de los resultados obtenidos por Python en lenguaje de negocios. ¿Qué decisión operativa debe tomar la empresa?
7. **Anexos:** Enlace al repositorio (por ejemplo GitHub o Google Colab) con el código fuente en Python (archivos `.py` o `.ipynb`) funcional y documentado.

---

## 5. Lineamientos de la exposición

- **Duración:** Máximo 20 minutos por alumno (15 minutos de presentación y 5 minutos de defensa).
- **Defensa técnica:** La evaluación de competencia quedará completamente abierta. Durante la sesión, el profesor podrá realizar cualquier tipo de pregunta técnica, teórica, de modificación de código en Python o sobre el impacto en el negocio al alterar parámetros del modelo, para comprobar el dominio real del alumno sobre el tema.

---

## 6. Rúbrica de evaluación (100 puntos)

| Criterio | Puntos | Descripción para nivel excelente |
|----------|--------|-----------------------------------|
| Escenario y calidad de datos | 20 | Caso hipotético con variables y parámetros de alta complejidad y realismo, evitando datos genéricos. |
| Modelado matemático y computacional | 30 | Ecuaciones del modelo planteadas correctamente y resolución sin errores usando de forma óptima Python y sus librerías. |
| Reporte escrito y conclusiones | 25 | Redacción profesional, código documentado y conclusiones orientadas a la toma de decisiones gerenciales. |
| Defensa y exposición | 25 | Dominio absoluto del tema. Respuestas sólidas a cualquier pregunta teórica, de código o de escenarios hipotéticos planteada por el profesor. |

---

TEMA ESCOGIDO:
14. Problema de la mochila para la selección de portafolios de inversión bajo un presupuesto de riesgo estricto.

## 8. Anexo: medio de entrega y fechas importantes

1. Entrega en **Microsoft Teams**, en la tarea especificada para este tema: **PIA_IO_EJ2026**.
2. **Un solo archivo ZIP.** Debe contener todo lo que se entregue (documento y archivos de Python).
3. Cada documento debe incluir una **portada** con los datos del alumno y los de la Unidad de Aprendizaje.
4. **Fecha de entrega:** 3 de mayo a las **11:30 h**. El retraso se penaliza con **5 puntos por cada 2 horas de retraso o fracción**.
5. **Presentación ante grupo y profesor:** martes **5** y miércoles **6** de mayo (hora de clase). Se permiten presentaciones anticipadas previa cita.
6. **Resultados y revisión:** martes **12** de mayo, hora de clase.
7. Cualquier situación no prevista se tratará con el profesor a cargo del grupo; su decisión es inapelable.

---

*Fuente: lineamientos del curso IO, UANL, EJ 2026.*
