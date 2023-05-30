# Calculadora de Similitud de Texto

Esta aplicación permite cargar archivos CSV que contienen pares de frases y calcular la similitud semántica entre ellas utilizando diferentes modelos de lenguaje de última generación. La aplicación consta de dos partes: un front-end desarrollado en Angular y un back-end que es una API creada con Flask.

## Funcionalidades

- Carga de archivos CSV con formato específico
- Cálculo de similitud semántica utilizando varios modelos de lenguaje
- Visualización de resultados en una tabla
- Diseño atractivo y fácil de usar

## Tecnologías utilizadas

- Front-end: Angular
- Back-end: Flask
- Bootstrap (opcional, si lo utilizas)
- Modelos de lenguaje de Hugging Face

## Cómo usar la aplicación

### Front-end

1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener instalado Node.js y npm en tu máquina local.
3. Navega al directorio del front-end y ejecuta `npm install` para instalar todas las dependencias necesarias.
4. Ejecuta `ng serve` para iniciar un servidor de desarrollo local y abrir la aplicación en tu navegador.

### Back-end

1. Asegúrate de tener instalado Python y pip en tu máquina local.
2. Navega al directorio del back-end y crea un entorno virtual con `python -m venv venv`.
3. Activa el entorno virtual (`source venv/bin/activate` en Linux/Mac o `venv\Scripts\activate` en Windows).
4. Ejecuta `pip install -r requirements.txt` para instalar todas las dependencias necesarias.
5. Ejecuta `flask run` para iniciar el servidor de la API en tu máquina local.

### Uso de la aplicación

1. Asegúrate de que tanto el front-end como el back-end estén en ejecución.
2. Carga un archivo CSV con el formato adecuado y presiona el botón "Calcular similitudes" para ver los resultados.

## Formato de archivo CSV

El archivo CSV debe tener un formato específico para funcionar correctamente con esta aplicación. Debe contener tres columnas separadas por punto y coma (;): frase_original, frase_adaptada y semanticamente_similares. La aplicación procesará el archivo y calculará las similitudes semánticas entre las frases originales y adaptadas en cada fila.

## Modelos de lenguaje utilizados

- [Maite89/Roberta_finetuning_semantic_similarity_stsb_multi_mt](https://huggingface.co/Maite89/Roberta_finetuning_semantic_similarity_stsb_multi_mt)
- [symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli](https://huggingface.co/symanto/sn-xlm-roberta-base-snli-mnli-anli-xnli)
- [hiiamsid/sentence_similarity_spanish_es](https://huggingface.co/hiiamsid/sentence_similarity_spanish_es)

## Contribuciones

Si tienes sugerencias o mejoras para este proyecto, no dudes en abrir un Issue o Pull Request en GitHub.

