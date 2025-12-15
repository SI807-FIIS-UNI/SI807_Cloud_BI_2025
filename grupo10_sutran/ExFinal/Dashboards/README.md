# ExFinal – Dashboard SUTRAN (Looker Studio + BigQuery)


---

## 1) Requisitos

### 1.1 Cuenta / acceso
- Cuenta Google para usar **Looker Studio**
- Acceso a **GCP BigQuery** 

### 1.2 Permisos mínimos (IAM)
Para el usuario o service account que abrirá el reporte:
- `BigQuery Data Viewer` (leer tablas/vistas)
- `BigQuery Job User` (ejecutar consultas desde Looker Studio)


---

## 2) Añadir fuentes de datos en Looker Studio (BigQuery)

### 2.1 Crear el reporte
1. Entrar a Looker Studio: https://lookerstudio.google.com/
2. Click en **Crear → Reporte**
3. Si no aparece el panel para añadir datos, igual se puede añadir luego desde **Recursos**.

---

### 2.2 Añadir las fuentes de datos a Looker Studio
Objetivo: jalar las fuentes de datos del BigQuery al Looker Studio para comenzar con las gráficas.

Ruta:
**Recursos → Gestionar las fuentes de datos añadidas → Añadir una fuente de datos**

![looker01.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker01.png)  
![evidencia_02.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/evidencia_02.png)

---

### 2.3 Conectar BigQuery y añadir tablas del modelo estrella (dims + hechos)
Luego de eso se selecciona **BigQuery** y se conecta al proyecto **`sutran-bi-2025`** y al dataset **`sutran_mr`**, para añadir las tablas del modelo estrella.

Pasos:
1. Seleccionar conector: **BigQuery**
2. Elegir proyecto: **`sutran-bi-2025`**
3. Elegir dataset: **`sutran_mr`**
4. Añadir como fuentes (si deseas tenerlas disponibles por separado):
   - `dim_persona`
   - `dim_vehiculo`
   - `dim_tiempo`
   - `dim_tipo_via`
   - `hechos_siniestros`

![looker02.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker02.png)  
![looker03.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker03.png)

> Nota: Aunque se añadan las tablas por separado, para el dashboard final se usa una fuente principal tipo estrella “aplanada” mediante una **Consulta personalizada**.

---

### 2.4 Fuente principal (Consulta personalizada / Custom Query)
Adicionalmente se genera una consulta personalizada (Custom Query) que realiza el JOIN del modelo estrella para consumo del dashboard.

Pasos:
1. **Añadir datos → BigQuery**
2. Elegir **Consulta personalizada / Custom Query**
3. Pegar el SQL de abajo
4. Guardar la fuente (nombre sugerido: `vw_siniestros_star` o `custom_star`)

**SQL (Custom Query):**
```sql
SELECT 
  h.id_siniestro,
  p.tipo_persona,
  p.sexo,
  p.edad,
  p.gravedad,
  v.vehiculo,
  v.estado_soat,
  v.posee_citv,
  t.fecha,
  t.anio,
  t.mes,
  t.dia_semana,
  t.trimestre,
  tv.tipo_de_via_normalizado,
  h.latitud,
  h.longitud
FROM `sutran-bi-2025.sutran_mr.hechos_siniestros` h
LEFT JOIN `sutran-bi-2025.sutran_mr.dim_persona`   p ON h.id_persona  = p.id_persona
LEFT JOIN `sutran-bi-2025.sutran_mr.dim_vehiculo`  v ON h.id_vehiculo = v.id_vehiculo
LEFT JOIN `sutran-bi-2025.sutran_mr.dim_tiempo`    t ON h.id_tiempo   = t.id_tiempo
LEFT JOIN `sutran-bi-2025.sutran_mr.dim_tipo_via`  tv ON h.id_tipo_via = tv.id_tipo_via;
```




## 3) Creación de páginas y campos calculados

### 3.1 Creación de páginas (5 dashboards integrados)
Ruta: **Página → Nueva página**

Crear y nombrar estas **5 páginas**:
1. **Principal**
2. **Personas**
3. **Vehículos**
4. **Vías**
5. **Tendencias**

![looker04.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker04.png)

---

### 3.2 Creación de campos calculados (en la fuente principal)
Los campos calculados se deben crear en la **fuente principal** (la **Consulta personalizada / Custom Query** que une el modelo estrella).

Formas válidas (usa la que te aparezca en tu UI):
- **Forma A:** Seleccionar un gráfico que use la fuente principal → panel derecho **Datos** → **Añadir un campo**  
- **Forma B:** **Recursos → Gestionar fuentes de datos añadidas** → seleccionar la fuente principal → **Editar** → **Añadir un campo**

#### 3.2.1 Campos calculados obligatorios (nombres finales usados en el dashboard)

**A) `cant_fallecido`**
```text
CASE WHEN gravedad = "FALLECIDO" THEN 1 ELSE 0 END
```

**B) `cant_lesionado`**
```text
CASE WHEN gravedad = "LESIONADO" THEN 1 ELSE 0 END
```

**C) `pct_fallecidos`**
```text
SUM(cant_fallecido) / Record Count
```
- Formato recomendado: **Porcentaje** (2 decimales)

**D) `pct_lesionados`**
```text
SUM(cant_lesionado) / Record Count
```
- Formato recomendado: **Porcentaje** (2 decimales)

**E) `es_fin_de_semana_txt`** (días en inglés con mayúscula inicial: Monday/Tuesday/…)
```text
CASE
  WHEN dia_semana IN ("Saturday","Sunday") THEN "Fin de semana"
  ELSE "Día de semana"
END
```

**EVIDENCIAS (creación de campos calculados looker05–looker10):**
![looker05.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker05.png)  
![looker06.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker06.png)  
![looker07.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker07.png)  
![looker08.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker08.png)  
![looker09.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker09.png)  
![looker10.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker10.png)

---

#### 3.2.2 Campos calculados en otras fuentes 


**En `dim_vehiculo` :**
![looker11.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker11.png)


**En `hechos_siniestros`:**
![looker12.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/looker12.png)



---

## 4) Control global “Selecciona un periodo” (filtro de fechas)

Objetivo: que el rango de fechas afecte **todas** las páginas y gráficos.

Pasos:
1. Ir a la página **Principal** (o cualquiera).
2. Ruta: **Insertar → Control → Intervalo de fechas**
3. Seleccionar el campo de fecha: **`fecha`**
4. Colocar el control en el header (parte superior del reporte).
5. Probar cambiando el periodo y verificar que cambian tarjetas y gráficos.



---

## 5) Creación de gráficos (paso a paso por página)

### 5.0 Reglas de métricas usadas en el dashboard
- **Siniestros:** `COUNT(id_siniestro)` 
- **Personas involucradas:** `Record Count`
- **Fallecidos:** `SUM(cant_fallecido)`
- **Lesionados:** `SUM(cant_lesionado)`
- **% Fallecidos:** `pct_fallecidos`
- **% Lesionados:** `pct_lesionados`



---

### 5.1 Página: Principal

#### 5.1.1 Tarjetas KPI (Scorecards)
Ruta: **Insertar → Gráfico → Tarjeta**

Crear 4 tarjetas:

1) **Siniestros**
- Fuente: fuente principal (Custom Query)
- Métrica: **Recuento de `id_siniestro`**

2) **Fallecidos**
- Fuente: fuente principal
- Métrica: **SUM(`cant_fallecido`)**

3) **Lesionados**
- Fuente: fuente principal
- Métrica: **SUM(`cant_lesionado`)**

4) **<KPI 4>** 
- Fuente: fuente principal
- Métrica: `Dañados`

#### 5.1.2 Mapa de puntos
Ruta: **Insertar → Gráfico → Google Maps → Mapa (puntos)**

- Dimensiones geográficas:
  - Latitud: `latitud`
  - Longitud: `longitud`
- Métrica: **Recuento de `id_siniestro`**


#### 5.1.3 Mapa de calor (Heatmap)
Ruta: **Insertar → Gráfico → Google Maps → Mapa de calor**

- Latitud: `latitud`
- Longitud: `longitud`
- Intensidad/Métrica: **Recuento de `id_siniestro`**

**EVIDENCIA (página Principal):**
![evidencia_04.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/evidencia_04.png)

---

### 5.2 Página: Personas

#### 5.2.1 Tarjetas KPI
Ruta: **Insertar → Gráfico → Tarjeta**

- **Personas involucradas:** `Record Count`
- **Fallecidos:** `SUM(cant_fallecido)`
- **Lesionados:** `SUM(cant_lesionado)`
- **% Fallecidos:** `pct_fallecidos` (formato %)
- **% Lesionados:** `pct_lesionados` (formato %)

#### 5.2.2 Gráficos recomendados (sin abuso de donas)
1) **Barras Top tipo_persona**
- Tipo: Barras horizontales
- Dimensión: `tipo_persona`
- Métrica: `Record Count`
- Orden: Descendente (Top 8–10)

2) **Barra 100% por sexo**
- Tipo: Barra 100% apilada
- Dimensión: `sexo`
- Métrica: `Record Count`

3) **Estado de licencia (si aplica)**
- Tipo: Barras o Tabla
- Dimensión: `estado_licencia`
- Métrica: `COUNT(id_siniestro)` o `Record Count`


4) **Dosaje etílico (si aplica)**
- Tipo: Barras
- Dimensión: `resultado_del_dosaje_etilico_cualitativo`
- Métrica: `COUNT(id_siniestro)` o `Record Count`
- (Opcional) Filtro: `tipo_persona = "CONDUCTOR"`

**EVIDENCIA (página Personas):**
![evidencia_05.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/evidencia_05.png)

---

### 5.3 Página: Vehículos

1) **Top tipo de vehículo**
- Tipo: Barras horizontales
- Dimensión: `vehiculo`
- Métrica: `COUNT(id_siniestro)`
- Top 10

2) **Estado SOAT**
- Tipo: Barra 100% apilada
- Dimensión: `estado_soat`
- Métrica: `COUNT(id_siniestro)`

3) **CITV**
- Tipo: Barra 100% apilada
- Dimensión: `posee_citv`
- Métrica: `COUNT(id_siniestro)`

4) **Situación del vehículo**
- Tipo: Barras
- Dimensión: `situacion_vehiculo`
- Métrica: `COUNT(id_siniestro)`

**EVIDENCIA (página Vehículos):**
![evidencia_06.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/evidencia_06.png)

---

### 5.4 Página: Vías

1) **Top tipos de vía**
- Tipo: Barras horizontales
- Dimensión: `tipo_de_via_normalizado`
- Métrica: `COUNT(id_siniestro)`
- Top 10

2) **Gravedad por tipo de vía**
- Tipo: Barras apiladas
- Dimensión: `tipo_de_via_normalizado`
- Desglose: `gravedad`
- Métrica: `Record Count`

3) **Fin de semana vs día de semana**
- Tipo: Barras
- Dimensión: `es_fin_de_semana_txt` 
- Métrica: `COUNT(id_siniestro)`

**EVIDENCIA (página Vías):**
![evidencia_07.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/evidencia_07.png)

---

### 5.5 Página: Tendencias (sin ranking duplicado)

1) **Serie temporal mensual**
- Tipo: Serie temporal (línea)
- Dimensión: `fecha` 
- Métrica A: `COUNT(id_siniestro)`
- Métrica B (opcional): `SUM(cant_fallecido)`

2) **Fin de semana vs semana**
- Tipo: Barras
- Dimensión: `es_fin_de_semana_txt`
- Métrica: `COUNT(id_siniestro)`

3) **Día de semana**
- Tipo: Barras
- Dimensión: `dia_semana`
- Métrica: `COUNT(id_siniestro)`

4) **Heatmap día_semana vs tipo_persona**
- Tipo: Tabla dinámica / Heatmap
- Filas: `dia_semana`
- Columnas: `tipo_persona`
- Métrica: `Record Count`

**EVIDENCIA (página Tendencias):**
![evidencia_08.png](/grupo10_sutran/ExFinal/Dashboards/evidencias/evidencia_08.png)




