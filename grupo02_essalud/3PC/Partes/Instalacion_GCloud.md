# ☁️ Instalación de GCloud

1. Descargamos el instalador de Google Cloud desde la página oficial:  
   [https://cloud.google.com/sdk/docs/install?hl=es-419](https://cloud.google.com/sdk/docs/install?hl=es-419)

2. Aceptamos todo lo que muestra el instalador Wizard. Al finalizar, se abrirá el CMD de esta forma:  
   <img src="../Media/Fotos/Pruebas/I01.png" width="420"/>

3. Escribimos **y** y damos Enter. Esto nos redirigirá a la página de Google para iniciar sesión con nuestra cuenta:  
   <img src="../Media/Fotos/Pruebas/I02.png" width="420"/>

4. Aceptamos todos los permisos. Una vez hecho, estaremos autenticados:  
   <img src="../Media/Fotos/Pruebas/I03.png" width="420"/>

5. Seleccionamos el proyecto que vamos a usar. En este caso: **grupo2-EsSalud**  
   <img src="../Media/Fotos/Pruebas/I04.png" width="420"/>

6. ¡Listo! Ya estamos dentro del proyecto deseado:  
   <img src="../Media/Fotos/Pruebas/I05.png" width="420"/>

7. Podemos verificar si la conexión fue exitosa ejecutando:  
   **gcloud config list**  
   Si nos pide activar el API *cloudresourcemanager.googleapis.com*, escribimos **y**.  
   <img src="../Media/Fotos/Pruebas/I06.png" width="420"/>

8. Finalmente, podemos confirmar que el proyecto está seleccionado con la cuenta correcta:  
   <img src="../Media/Fotos/Pruebas/I07.png" width="420"/>
