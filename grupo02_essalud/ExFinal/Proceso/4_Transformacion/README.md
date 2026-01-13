# **Proceso de Transformación de Datos**

A continuación, se describe el flujo utilizado para desarrollar, probar y desplegar la transformación de datos mediante JupyterLab y Google BigQuery, siguiendo la arquitectura *etl_script* (Bronce → Plata → Oro).

---

## **1. Creación del Entorno de Trabajo**

Primero, se crea una instancia denominada **“transformacion”**, la cual se utilizará para ejecutar JupyterLab y realizar las pruebas de transformación de datos antes de generar el script final en Python.

![Creación de la instancia](Pruebas/I001.png)

Una vez creada la instancia, seleccionamos **“Abrir JupyterLab”**.

![Botón para abrir JupyterLab](Pruebas/I002.png)

---

## **2. Configuración Inicial en JupyterLab**

Dentro de JupyterLab, procedemos a crear un nuevo cuaderno:

1. Seleccionamos **File → New → Notebook**.
2. Elegimos el kernel por defecto (**ipykernel**) y presionamos **Select**.

![Selección de File → New → Notebook](Pruebas/I003.png)

![Pantalla de selección del kernel](Pruebas/I004.png)

Posteriormente, asignamos un nombre al cuaderno haciendo clic derecho sobre él y seleccionando la opción para renombrarlo.

![Opción para renombrar el notebook](Pruebas/I005.png)

---

## **3. Creación de las Bases de Datos en BigQuery (Bronce, Plata y Oro)**

Antes de iniciar la transformación, es necesario crear tres *datasets* en BigQuery, correspondientes a las capas de la arquitectura *etl_script*. Esto permitirá cargar automáticamente los datos procesados a cada capa.

1. Ingresamos a BigQuery y seleccionamos **“Crear Conjunto de Datos”**.

   ![Opción para crear conjunto de datos](Pruebas/I006.png)

2. Completamos la información solicitada para las capas Bronce, Plata y Oro.

   ![Formulario de creación del dataset Bronce](Pruebas/I007.png)

3. Finalmente, los tres datasets deben visualizarse de la siguiente manera:

   ![Vista de los datasets creados](Pruebas/I008.png)

---

## **4. Desarrollo de la Transformación**

El procesamiento completo —desde la capa Bronce hasta la capa Oro— se implementó en un único notebook:

* **Notebook de Transformación Bronce → Plata → Oro**
  [etl_script.ipynb](etl_script.ipynb)

Una vez finalizada la transformación y verificados los resultados, el notebook se exportó como script en Python, para ser utilizado posteriormente dentro del orquestador.

* **Script en Python de la Transformación Bronce → Plata → Oro**
  [etl_script.py](Script/etl_script.py)

