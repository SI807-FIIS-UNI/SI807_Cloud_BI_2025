# Documentación Técnica: Implementación Dashboard Power BI - Análisis Financiero

## 1. Conexión a Azure SQL Database

### 1.1 Pasos de Conexión

#### Paso 1: Abrir Power BI Desktop

1. Iniciar Power BI Desktop
2. Click en **"Obtener datos"**
3. Buscar y seleccionar **"Azure SQL Database"**
4. Click en **"Conectar"**

#### Paso 2: Configurar Conexión

Ingresar los siguientes parámetros:

```
Servidor (Server): sql-server-grupo03.database.windows.net
Base de Datos (Database): grupo03_credicorp
```

#### Paso 3: Autenticación

1. Seleccionar **"Base de datos"**
2. Ingresar:
   - **Nombre de usuario:** rootadmin
   - **Contraseña:** Pa$$12345678
3. Click en **"Conectar"**

#### Paso 4: Selección de Tablas

Marcar las siguientes tablas:
- ☑️ `empresa_financiera`
- ☑️ `calendario`
- ☑️ `kpi_financiero`

Click en **"Cargar"**

---

### 3.2 Configuración de Conexión mediante Import

#### Modo Import 

✅ **Ventajas:**
- Rendimiento más rápido
- Permite todas las funciones DAX
- Ideal para datasets < 1 GB

**Configuración:**
- Seleccionar modo **"Import"** al cargar datos

## 4. Medidas DAX Calculadas

### 4.1 Medidas Básicas de KPIs

Crear las siguientes medidas en la tabla `kpi_financiero`:

#### ROA Promedio

```dax
ROA_Promedio = 
AVERAGE(kpi_financiero[ROA])
```

#### ROE Promedio

```dax
ROE_Promedio = 
AVERAGE(kpi_financiero[ROE])
```

#### NIM Promedio

```dax
NIM_Promedio = 
AVERAGE(kpi_financiero[NIM])
```

#### Morosidad Promedio

```dax
Morosidad_Promedio = 
AVERAGE(kpi_financiero[Mora])
```

#### Cobertura Provisiones Promedio

```dax
Cobertura_Promedio = 
AVERAGE(kpi_financiero[Cobertura de provisiones])
```

#### Índice Capital Total Promedio

```dax
Capital_Total_Promedio = 
AVERAGE(kpi_financiero[Índice Capital Total])
```

### 5.3 Medidas de Rankings y Posicionamiento

Ir a 'Introducir datos' y crear la tabla Indicadores, dónde se debe subir el catálogo de indicadores (ROA, ROE, NIM, Cobertura de Provisiones, Mora y Índice de Capital Total). Dentro de esa misma tabla crear las siguientes medidas:

#### Valor Indicador Seleccionado
```dax
Valor Indicador Seleccionado = 
VAR IndicadorSeleccionado = SELECTEDVALUE(Indicadores[Indicador])
RETURN 
SWITCH(
    TRUE(),
    IndicadorSeleccionado = "ROE", [nROE],
    IndicadorSeleccionado = "ROA", [nROA],
    IndicadorSeleccionado = "NIM", [nNIM],
    IndicadorSeleccionado = "Mora", [nMora],
    IndicadorSeleccionado = "Cobertura Provisiones", [Cobertura Provisiones],
    IndicadorSeleccionado = "Índice de Capital Total", [Indice Capital Total],
    BLANK()
)
```

#### Entidad Líder

```dax
Entidad Líder = 
VAR IndicadorSeleccionado = SELECTEDVALUE(Indicadores[Indicador])
VAR TablaEmpresas =
    ADDCOLUMNS(
        VALUES(empresa_financiera[Empresa]),
        "Valor", [Valor Indicador Seleccionado]
    )
VAR EmpresaTop =
    TOPN(1, TablaEmpresas, [Valor], DESC)
RETURN
MAXX(EmpresaTop, empresa_financiera[Empresa])
```
#### Valor del Líder

```dax
Valor del Líder = 
VAR IndicadorSeleccionado = SELECTEDVALUE(Indicadores[Indicador])
VAR TablaEmpresas =
    ADDCOLUMNS(
        VALUES(empresa_financiera[Empresa]),
        "Valor", [Valor Indicador Seleccionado]
    )
VAR EmpresaTop =
    TOPN(1, TablaEmpresas, [Valor], DESC)
RETURN
MAXX(EmpresaTop, [Valor])
```

#### Líder del Período

```dax
Líder del Periodo (Texto) = 
[Entidad Líder] &
UNICHAR(10) &
" — " &
SELECTEDVALUE(Indicadores[Indicador]) &
": " &
FORMAT([Valor del Líder], "0.00") & "%"
```

---

### 5.5 Visualizaciones

### Páginas 1 y 2 del dashboard
 Usamos los objetos visuales **tarjetas** para mostrar los indicadores financieros calculados. También incluimos el objeto visual **segmentación de datos** para generar filtros por entidad, año, trimestre y mes.

* **Filtro por entidad:** usamos el campo Empresa de la tabla empresa_financiera

  *vamos a formato visual -> objeto visual -> estilo -> lista desplegable*
  
* **Filtro por año:** usamos el campo Año de la tabla calendario 

  *vamos a formato visual -> objeto visual -> estilo -> lista vertical, luego a selección ->   selección múltiple*

* **Filtro por trimestre:** usamos el campo Trimestre de la tabla dim_fecha 

  *vamos a formato visual -> objeto visual -> estilo -> mosaico , luego a selección -> selección múltiple*

* **Filtro por mes:** usamos el campo nombre_mes de la tabla calendario

  *vamos a formato visual -> objeto visual -> estilo -> lista vertical , luego a selección -> selección múltiple*

Asimismo, en cada página usamos el objeto visual **gráfico de líneas**, seleccionado los siguientes campos para ver la evolución de los indicadores por año.

- **Eje X:** campo Año de la tabla calendario
- **Eje Y:** indicadores calculados con fórmulas DAX (ROE_Promedio, ROA_Promedio, NIM_Promedio,Cobertura_Promedio,Morosidad_Promedio, Capital_Total_Promedio)

Por último agregamos la tabla que representa los 'semáforos' que representan los rangos correctos e incorrectos para cada indicador.

* La tabla llamada "Semáforo" guardaran los datos de los rangos para los indicadores

  *Inicio -> Datos -> Introducir datos*

Pusimos las columnas Color, Indicador y Rango%, con el siguiente formato:

Para la página 1:
| Indicador | Color | Rango % |
|------------|:------:|:--------|
| ROE | 🟥 Rojo | < 5% |
| ROE | 🟨 Amarillo | 5% – 10% |
| ROE | 🟩 Verde | > 10% |
| ROA | 🟥 Rojo | < 0.5% |
| ROA | 🟨 Amarillo | 0.5% – 1% |
| ROA | 🟩 Verde | > 1% |
| NIM | 🟥 Rojo | < 2% |
| NIM | 🟨 Amarillo | 2% – 3% |
| NIM | 🟩 Verde | > 3% |
| Índice de capital total | 🟥 Rojo | < 8% |
| Índice de capital total  | 🟨 Amarillo | 8% – 10% |
| Índice de capital total  | 🟩 Verde | > 10% |

* Luego en cada página, insertamos el objeto visual **matriz**, seleccionado los siguientes campos:

Para la página 1: 
- **Filas:** Indicador
- **Columnas:** Color
- **Valores:** Rango %

Para la página 2:
- **Filas:**  Color
- **Columnas:** Indicador
- **Valor:** Rango %

### Página 3 del dashboard

Primero creamos una tabla llamada 'Indicadores' listando los nombres de todos los indicadores financieros, nuevamente nos dirigimos a:

  *Inicio -> Datos -> Introducir datos*

Dónde creamos una única columa llamada Indicador, donde guardamos los nombres de todos los indicadores que hemos calculado.

Luego agregamos los filtros por año y trimestre y adicionalmente agregamos el filtro por indicador:

**Filtro por indicador:** usamos el campo Indicador de la tabla Indicadores

  *vamos a formato visual -> objeto visual -> estilo -> lista vertical, luego a selección -> selección única*


#### Objetos visuales usados

* Tarjeta: seleccionamos el campo *Líder del Período (Texto)* que acabamos de crear.

* Gráfico de barras agrupadas: para el Eje Y seleccionamos el campo *nombre_entidad* de la tabla dim_entidad y para el Eje X seleccionamos el *Valor Indicador Seleccionado.* para mostrar el ranking de las entidades por indicador.

* Gráfico de líneas: para el Eje X seleccionamos el campo *anio* de la tabla dim_fecha y para el Eje Y el campo *Valor Indicador Seleccionado* y para leyenda seleccionamos el campo *nombre_entidad*. Asimismo agregamos un filtro al campo entidad: *tipo filtro -> Top N -> Mostrar artículos -> Superior 5 -> Por valor -> Valor Indicador Seleccionado* para mostrar la evolución de las 5 primeras entidades por año.
---
