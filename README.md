#  Análisis de Artículos Científicos sobre Pinnípedos con IA

##  Description
Este proyecto automatiza la extracción de metadata, abstracts y enlaces de artículos científicos en formato PDF. Utiliza **Grobid** (una herramienta de IA basada en Deep Learning para documentos técnicos) y un script personalizado de **Python**. El objetivo es analizar una muestra de 10 artículos sobre pinnípedos para generar visualizaciones que faciliten la comprensión rápida del estado de la investigación.

##  Requirements
Para garantizar la reproducibilidad total bajo los estándares de **Ciencia Abierta**, el único requisito es:
* **Docker Desktop** (versión 20.10 o superior).
* No es necesario instalar Python ni dependencias locales; el entorno se autoconstruye mediante contenedores.

##  Installation Instructions
1. Clona este repositorio o descarga la carpeta del proyecto.
2. Asegúrate de que Docker Desktop esté iniciado.
3. El sistema descargará e instalará automáticamente todas las librerías necesarias (Matplotlib, Wordcloud, lxml) dentro del contenedor la primera vez que se ejecute.

##  Execution Instructions
1. Coloca los 10 archivos PDF a analizar en la carpeta `/Articles`.
2. Abre una terminal en la raíz del proyecto y ejecuta:
   ```bash
   docker-compose up --build --abort-on-container-exit
