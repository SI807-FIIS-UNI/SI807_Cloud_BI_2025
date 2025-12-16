# Sustentación de Diseño y Visualización del Dashboard (Power BI)

En esta sección se documenta la **decisión de diseño (estética + disposición)** aplicada a los dashboards desarrollados en **Power BI** para el caso de **retrasos de vuelos y sus causas**.  
El objetivo fue construir una visualización **clara, comparativa y ejecutiva**, donde el usuario pueda **entender el estado general en segundos** y luego profundizar con gráficos de ranking y distribución de causas.

---

## Dashboard 1: KPIs + Ranking (visión ejecutiva)

<img width="886" height="499" alt="image" src="https://github.com/user-attachments/assets/89d95e80-dd42-480f-a6b6-c5bc87a53eee" />


### Justificación de diseño (estética)
- **Paleta sobria (fondo oscuro + tarjetas claras):** el fondo oscuro reduce fatiga visual y hace que los indicadores principales resalten. Las tarjetas claras actúan como “puntos de foco” para lectura rápida.
- **Color dominante para barras:** se usa un tono uniforme en el ranking para evitar ruido visual; el mensaje es el orden/jerarquía, no la comparación de colores.
- **Consistencia tipográfica:** títulos grandes y métricas en formato “tarjeta” para comunicar valor sin que el usuario deba interpretar el gráfico primero.

### Justificación de diseño (posicionamiento)
- **Arriba: KPIs principales** (lectura inmediata)
  - *Retraso Promedio* y *% Vuelos Retrasados* son los dos indicadores más importantes para entender el desempeño global.
- **Centro/izquierda: filtro temporal** (control del análisis)
  - el slicer de **Mes** se ubica cerca de KPIs para que el usuario note que puede “cambiar el contexto” y ver cómo se mueven los indicadores.
- **Abajo/izquierda: causas del retraso**
  - el gráfico de “minutos perdidos por causa” permite explicar el “por qué” del KPI (no solo el “cuánto”).
- **Derecha: rankings**
  - el ranking de aerolíneas y el ranking geográfico (mapa) se colocan a la derecha para análisis comparativo: “quiénes” y “dónde” se concentran los retrasos.

---

## Dashboard 2: Desempeño comparativo (relación puntualidad vs frecuencia)

<img width="1104" height="618" alt="image" src="https://github.com/user-attachments/assets/fc1d9822-f4e4-4147-afd1-c7152fe75450" />

### Justificación de diseño (estética)
- **Gráfico de dispersión con estilo limpio:** se prioriza la lectura de patrón (tendencia/relación) sobre adornos.  
- **Tabla resumen complementaria:** se usa para validar rápidamente valores y facilitar comparación puntual cuando el usuario necesita detalle.

### Justificación de diseño (posicionamiento)
- **Izquierda: scatter (relación entre métricas)**
  - muestra el comportamiento comparativo por aerolínea: si a mayor retraso promedio también aumenta la frecuencia de retrasos.
- **Derecha: tabla (detalle y verificación)**
  - permite ver valores numéricos exactos y confirmar la interpretación del scatter sin necesidad de tooltips.

---

## Principios aplicados en ambos dashboards

- **Jerarquía visual clara:** primero KPIs, luego explicación (causas) y finalmente comparación (ranking/relación).
- **Diseño orientado a decisiones:** el tablero responde rápido a preguntas típicas del caso:
  - ¿Cuál es el retraso promedio y qué tan frecuente ocurre?
  - ¿Qué causa acumula más minutos perdidos?
  - ¿Qué aerolíneas y aeropuertos se ven más afectados?
- **Minimización de ruido visual:** se evita el exceso de colores y elementos decorativos para mantener foco en los datos.

---
