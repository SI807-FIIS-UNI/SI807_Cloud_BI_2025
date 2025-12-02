# 📥 Funcionamiento Detallado de la Pantalla "SUBIR DATOS"
Esta es la pantalla de inicio del dashboard. Su único propósito es permitirte cargar los datos que necesitas para que el sistema funcione. Es como la puerta de entrada al mundo de los reportes y análisis.

<img width="2235" height="1157" alt="image" src="https://github.com/user-attachments/assets/a9c35c03-8571-4e4f-bcd0-da9ede1ef904" />

## 1. La Barra de Navegación Superior
En la parte superior, tienes tres botones que te permiten moverte por el dashboard:

* SUBIR DATOS (Botón Azul): Este es el botón activo en esta pantalla. Al hacer clic aquí, llegas a esta misma vista, donde puedes cargar nuevos archivos. Es el punto de partida.
* VER DASHBOARD GLOBAL: Este botón está desactivado (apagado) cuando no hay datos cargados. Una vez que subas un archivo y el sistema lo procese, podrás hacer clic aquí para ver una vista general de todos los servicios, con gráficos y tablas resumen.
* VER DASHBOARD POR SERVICIO: Este botón también está desactivado inicialmente. Cuando tengas datos cargados, te llevará a una vista más profunda, donde podrás analizar el rendimiento de un servicio específico en detalle.


## 2. El Formulario de Carga: Tu Área de Trabajo Principal
Este es el corazón de la pantalla. Aquí es donde tú, como usuario, interactúas con el sistema para subir la información.

a) Campo: DESTINO DEL DATO
* Qué es: Un menú desplegable (una cajita con una flechita abajo).
* Qué hace: Te permite decirle al sistema a qué nivel de madurez pertenecen los datos que vas a subir. Solo tienes dos opciones:
  * Practitioner: Si tu archivo CSV contiene métricas sobre este nivel.
  * Continuous Integration: Si tu archivo CSV contiene métricas sobre este otro nivel.
* Por qué es importante: El sistema necesita saber esto porque los archivos de estos dos niveles tienen estructuras diferentes. Al seleccionar uno, el sistema prepara todo su interior para recibir y procesar ese tipo de datos específicamente. Es como elegir el idioma en una máquina antes de usarla.

b) Campo: SELECCIONAR ARCHIVO CSV
* Qué es: Un botón que dice NINGÚN ARCHIVO SELECCIONADO.
* Qué hace: Cuando haces clic en él, se abre una ventana de tu computadora (como el Explorador de Archivos de Windows o Finder de Mac) para que busques y selecciones el archivo .csv que descargaste desde el Marco Playbook.
* Qué pasa después: Una vez que eliges un archivo, el texto en el botón cambiará para mostrar el nombre del archivo que seleccionaste (por ejemplo, datos_practitioner_marzo.csv). Si cambias de opinión, puedes volver a hacer clic para seleccionar otro.

c) Botón: SUBIR ARCHIVO
* Qué es: El botón azul grande y brillante en el centro.
* Qué hace: Este es el botón mágico. Cuando haces clic en él, inicias el proceso de carga.
* Qué pasa cuando lo presionas:
1. Validación: El sistema primero revisa que el archivo que seleccionaste tenga el formato correcto (.csv) y que las columnas dentro del archivo coincidan con lo que espera para el nivel que elegiste (Practitioner o Continuous Integration). Si algo no coincide, te mostrará un mensaje de error explicando qué salió mal.
2. Carga y Procesamiento: Si todo está bien, el sistema toma tu archivo y lo envía a su "laboratorio interno" (el backend). Allí, el archivo será limpiado, organizado y transformado para que pueda ser usado en los gráficos.
3. Feedback al Usuario: Mientras el sistema trabaja (lo cual puede tomar unos segundos), la pantalla se actualizará para mostrarte el progreso. Verás mensajes como "Limpiando...", "Subiendo...", "Procesando..." hasta que finalmente aparezca "¡Carga completada!".
4. Resultado Final: Una vez terminado, los otros dos botones de la barra superior (VER DASHBOARD GLOBAL y VER DASHBOARD POR SERVICIO) se activarán, y podrás navegar a las vistas de análisis.


# 📊 Funcionamiento Detallado de la Pantalla "VER DASHBOARD GLOBAL"
<img width="2559" height="1396" alt="image" src="https://github.com/user-attachments/assets/23958dc3-ec1b-486f-9037-2a98d20c4926" />

## 1. La Barra de Navegación Superior
Al igual que en la pantalla anterior, aquí tienes los tres botones principales:

<img width="1714" height="268" alt="image" src="https://github.com/user-attachments/assets/7dfe6b41-d5e8-45ef-983e-7a69dfe23e4c" />

* SUBIR DATOS (Botón Inactivo): Este botón está apagado porque estás en la vista de análisis. Si necesitas cargar nuevos datos, puedes hacer clic aquí para volver a la pantalla de carga.
* VER DASHBOARD GLOBAL (Botón Activo): Este es el botón que te trajo a esta pantalla. Está resaltado en azul brillante, indicando que estás viendo la vista global.
* VER DASHBOARD POR SERVICIO (Botón Inactivo): Este botón te llevará a la vista de análisis profundo de un servicio específico. Lo usarás cuando quieras profundizar en un caso concreto.

## 2. Selección del Nivel de Madurez
Justo debajo del título de la pantalla, encontrarás dos botones que te permiten cambiar entre los dos niveles de certificación:

<img width="1603" height="111" alt="image" src="https://github.com/user-attachments/assets/c14a9b40-2912-46f1-b705-9c28484d65b8" />

* PRACTITIONER: Al hacer clic en este botón, la pantalla se actualiza para mostrar todos los datos, gráficos y tablas relacionados con el nivel Practitioner. El botón se pondrá en azul brillante para indicar que está seleccionado.
* CONTINUOUS INTEGRATION: Al hacer clic en este botón, la pantalla cambia para mostrar los datos del nivel Continuous Integration. El botón se resaltará y el contenido de la pantalla se actualizará completamente.

## 3. Tarjetas Resumen (Summary Cards)
En la parte superior de la pantalla, hay tres tarjetas que te dan una visión rápida de los datos clave:

<img width="1625" height="201" alt="image" src="https://github.com/user-attachments/assets/f8ca4d44-a520-4ca0-9bb9-f8dd85814c99" />

* Total de Registros: Muestra el número total de registros (filas) que se han cargado para el nivel de madurez seleccionado. Por ejemplo, para Practitioner, muestra 3095.
* Geografías Analizadas: Indica cuántas regiones o países diferentes están siendo evaluadas. En el ejemplo, son 14.
* Adopción Total Promedio: Este es el KPI más importante. Muestra el promedio ponderado de adopción de todas las métricas para el nivel seleccionado. Para Practitioner, es 81.92%, y para CI, es 79.53%.
  
## 4. Filtros de Análisis
Debajo de las tarjetas, encontrarás dos filtros que te permiten ajustar la vista de los datos:

<img width="1624" height="191" alt="image" src="https://github.com/user-attachments/assets/688addc7-27cf-40b2-a3bd-5e625ca3046f" />

* Filtro FECHA: Un menú desplegable que te permite seleccionar un mes específico o elegir Todas para ver todos los datos disponibles. Esto es útil si quieres analizar el rendimiento de un periodo concreto.
* Filtro GEOGRAFÍA: Otro menú desplegable que te permite seleccionar una región específica (por ejemplo, ARGENTINA, PERU, MEXICO) o elegir Todas para ver la vista global.

## 5. Gráfico: "Niveles de Certificación por % de Adopción"
Este es un gráfico de tarta que te muestra cómo se distribuyen todos los servicios según su nivel de certificación.

<img width="1623" height="744" alt="image" src="https://github.com/user-attachments/assets/20908183-96de-4814-9406-0b6501748434" />

* Qué representa: El gráfico divide el círculo en cuatro sectores, cada uno representando un nivel de certificación:
   * LEVEL 3: Servicios con 90% o más de adopción. (Color Azul Claro)
   * LEVEL 2: Servicios con entre 80% y 89% de adopción. (Color Azul Medio)
   * LEVEL 1: Servicios con entre 70% y 79% de adopción. (Color Azul Oscuro)
   * No Certificado: Servicios con menos del 70% de adopción. (Color Gris)
* Qué ves en el centro: El número total de servicios que cumplen con los criterios de filtro (por ejemplo, 3021).
* Leyenda: A la derecha, una leyenda explica qué color corresponde a cada nivel y muestra el porcentaje y el número de servicios en cada categoría.

## 6. Gráfico: "Niveles de Certificación por Geografía"
Este es un gráfico de barras apiladas que te permite comparar el rendimiento entre diferentes regiones.

<img width="1597" height="1155" alt="image" src="https://github.com/user-attachments/assets/fd2d44e5-47ad-4b2c-8351-015c39ab5951" />

* Qué representa: Cada barra horizontal corresponde a una geografía (por ejemplo, ARGENTINA, PERU, ESPAÑA). Dentro de cada barra, los colores de los segmentos muestran la cantidad de servicios en cada nivel de certificación (LEVEL 3, LEVEL 2, LEVEL 1, No Certificado).
* Qué ves al final de cada barra: El número total de servicios analizados en esa geografía.
* Cómo leerlo: Puedes ver fácilmente qué regiones tienen una mayor proporción de servicios en LEVEL 3 (azul claro) y cuáles tienen muchos servicios sin certificar (gris).

## 7. Tabla: "Cálculo de los KPI's"
Esta es la tabla detallada que muestra los datos granulares de cada servicio.

<img width="1574" height="1311" alt="image" src="https://github.com/user-attachments/assets/f8b830db-47fc-478e-88ed-91cbd4eb3756" />

* Qué contiene: La tabla tiene columnas para:
   * FECHA: El mes al que corresponden los datos.
   * GEOGRAFÍA: La región del servicio.
   * SERVICE1 NAME: El nombre del servicio.
   * RFO OK PCT, DEP PCT, ADOPCION SN2 PCT, CALIDAD FEATURES PCT, SEGURIDAD PCT: Los porcentajes      individuales de cada KPI.
   * ADOPCION TOTAL PCT: El porcentaje de adopción total ponderado, que es el resultado final.
* Paginación: Debajo de la tabla, hay botones Anterior y Siguiente para navegar por las páginas. También muestra cuántos registros se están mostrando (por ejemplo, Mostrando 1 a 10 de 3095).

# 📈 Funcionamiento Detallado de la Pantalla "VER DASHBOARD POR SERVICIO"
## 1. La Barra de Navegación Superior
Al igual que en las otras pantallas, aquí tienes los tres botones principales:

<img width="1935" height="1395" alt="image" src="https://github.com/user-attachments/assets/3993c225-dcc1-4a59-9462-85b1b26de91d" />

* SUBIR DATOS (Botón Inactivo): Este botón te permitirá volver a la pantalla de carga si necesitas actualizar los datos.
* VER DASHBOARD GLOBAL (Botón Inactivo): Te llevará de vuelta a la vista macro, donde puedes ver todos los servicios juntos.
* VER DASHBOARD POR SERVICIO (Botón Activo): Este es el botón que te trajo a esta pantalla. Está resaltado en azul brillante, indicando que estás viendo la vista de análisis profundo por servicio.

## 2. Filtros "Service Owner": Tu Panel de Control Personalizado
En esta pantalla, los filtros son el corazón del sistema. Son los controles que te permiten elegir exactamente qué servicio quieres analizar. El diseño es inteligente porque los filtros se actualizan en cascada, lo que significa que la selección de uno afecta las opciones disponibles en el siguiente.

<img width="1605" height="285" alt="image" src="https://github.com/user-attachments/assets/324b2638-c8ae-473c-b410-fdc7c61e28c9" />

a) NIVEL DE MADUREZ
* Qué es: Un menú desplegable que te permite seleccionar el nivel de certificación que deseas analizar: Practitioner o Continuous Integration.
* Qué hace: Al hacer clic en este filtro, el sistema consulta la base de datos y te muestra solo las geografías que tienen datos para ese nivel de madurez. Esto evita que veas opciones inválidas.
* Por qué es importante: Es el primer paso para enfocar tu análisis. Si quieres ver cómo va un servicio en Practitioner, debes seleccionar este nivel primero.

b) GEOGRAFÍA
* Qué es: Otro menú desplegable que te permite seleccionar una región específica (por ejemplo, ARGENTINA, PERU, URUGUAY).
* Qué hace: Una vez que has seleccionado un nivel de madurez, este filtro se actualiza automáticamente para mostrarte solo las geografías que tienen datos para ese nivel. Por ejemplo, si seleccionas Practitioner, no podrás elegir una geografía que solo tenga datos de CI.
* Por qué es importante: Te permite acotar tu análisis a una región específica. Si eres el Service Owner de Uruguay, puedes filtrar solo por esa geografía.

c) SERVICIO N1
* Qué es: Un tercer menú desplegable que te permite seleccionar un servicio específico dentro de la geografía que elegiste.
* Qué hace: Al seleccionar una geografía, este filtro se actualiza para mostrarte solo los servicios que existen en esa región para el nivel de madurez seleccionado. Por ejemplo, si eliges URUGUAY y Practitioner, te mostrará servicios como ENGINEERING & DATA o RETAIL CLIENT SOLUTIONS.
* Por qué es importante: Este es el filtro final que te lleva al análisis de un servicio concreto. Es aquí donde empieza la magia del dashboard.

## 3. Área de Visualización: El Análisis Profundo del Servicio
Una vez que has seleccionado un nivel de madurez, una geografía y un servicio específico, el dashboard se actualiza para mostrarte una serie de gráficos y métricas detalladas. Aquí es donde puedes ver el rendimiento de ese servicio en profundidad.

<img width="1587" height="564" alt="image" src="https://github.com/user-attachments/assets/4d5151e0-d409-4deb-9d60-bf12d16edeca" />

a) Gráfico de Evolución de Adopción Total
Este es un gráfico de líneas que te muestra cómo ha cambiado el porcentaje de adopción total del servicio a lo largo del tiempo.

*Qué representa: Cada punto en la línea corresponde al porcentaje de adopción total del servicio para un mes específico. Por ejemplo, puedes ver cómo fue en marzo, abril, mayo, etc.
* Modos de Visualización:
   * MENSUAL: Muestra los datos puntuales de cada mes. Es útil para ver los picos y valles.
   * ACUMULADO: Muestra un promedio progresivo. Es útil para ver la tendencia general a lo largo del  tiempo.
* Cómo funciona: El sistema toma los datos de los últimos 12 meses del servicio seleccionado y los grafica. Puedes ver claramente si el servicio está mejorando, empeorando o manteniéndose estable.

b) Gauge Chart (Velocímetro) de Adopción Total
Este es un medidor tipo velocímetro que te muestra el valor más reciente de la adopción total del servicio.

* Qué representa: El número grande en el centro (por ejemplo, 49.06%) es el porcentaje de adopción total del servicio en el último mes disponible.
* Colores: El velocímetro tiene zonas de color:
    * Verde: Indica un buen estado (>= 90%).
    * Amarillo: Indica un estado medio (70-89%).
    * Rojo: Indica un estado crítico (< 70%).
* Texto: Debajo del número, te dice en qué categoría de certificación se encuentra el servicio (por ejemplo, NO CERTIFICADO).

c) Selector de KPI's
Este es un conjunto de botones que te permiten cambiar el gráfico de evolución para ver otros KPIs individuales del servicio.

<img width="1599" height="207" alt="image" src="https://github.com/user-attachments/assets/012d9e94-6999-45ee-af93-bd020d4b55e8" />

* Qué hace: Al hacer clic en un botón (por ejemplo, RFO OK, DEP, CALIDAD FEATURES), el gráfico de evolución cambia para mostrar la tendencia de ese KPI específico en lugar de la adopción total.
* Por qué es importante: Te permite profundizar en un aspecto concreto del servicio. Si ves que la adopción total está baja, puedes usar este selector para ver si el problema está en la calidad de las features, en las dependencias o en otro KPI.

d) Gráfico Radar de KPIs
Este es un gráfico tipo radar que te muestra una vista holística de todos los KPIs del servicio para un mes específico.

<img width="1591" height="703" alt="image" src="https://github.com/user-attachments/assets/0615a921-6fd5-4fc4-8f39-3c9d9fb77335" />

* Qué representa: Cada eje del radar corresponde a un KPI diferente (por ejemplo, RFO OK, DEP, ADOPCIÓN SN2, CALIDAD FEATURES, SEGURIDAD). La distancia desde el centro indica el valor del KPI.
* Comparación: Puedes seleccionar un mes pasado (por ejemplo, Julio 2025) para compararlo con el mes actual (Agosto 2025). El gráfico superpondrá ambos períodos, permitiéndote ver fácilmente si el servicio ha mejorado o empeorado en cada KPI.
* Leyenda: A la derecha, una leyenda explica qué color corresponde a cada período.
