# Proyecto ETL - Antonio Cardenas Jurado - 2230433

Este proyecto implementa un pipeline ETL completo que integra y analiza datos musicales provenientes de **Spotify (CSV)**, **Premios Grammy (CSV)** y una **API de Spotify**. El objetivo es construir un dataset consolidado para su visualización en un dashboard interactivo que permite explorar insights clave sobre la industria musical.

Toda la solución está desarrollada en **Python** y desplegada usando **Docker Compose**, incluyendo un entorno de orquestación con **Apache Airflow** y una base de datos **PostgreSQL**.

---

## Tabla de Contenidos

1. [Tecnologías y Requisitos](#1-tecnologías-y-requisitos)
2. [Estructura del Proyecto](#2-estructura-del-proyecto)
3. [Orden de Ejecución del Proyecto](#3-orden-de-ejecución-del-proyecto)
4. [Detalles del Pipeline ETL](#4-detalles-del-pipeline-etl)
5. [Orquestación con Airflow](#5-orquestación-con-airflow)
6. [Dashboard Interactivo](#6-dashboard-interactivo)
7. [Carga a Google Drive](#7-carga-a-google-drive)
8. [Configuración Local Paso a Paso](#8-configuración-local-paso-a-paso)
9. [Conclusiones](#9-conclusiones)

---

## 1. Tecnologías y Requisitos

### Requisitos Previos

* Python >= 3.8
* Docker y Docker Compose
* Git

### Librerías y Servicios Usados

* `pandas`, `polars`, `numpy`
* `dash`, `plotly`, `psycopg2`, `sqlalchemy`
* `apache-airflow`, `pydrive2`
* PostgreSQL (vía contenedor)

---

## 2. Estructura del Proyecto

```plaintext
.
├── notebooks/               # Exploraciones EDA
├── data/
│   ├── raw/                # Datos originales
│   ├── processed/          # Datos limpios
│   └── final/              # Dataset consolidado (CSV final)
├── dags/
│   └── etl_pipeline.py     # DAG principal para Airflow
├── src/
│   ├── extract/
│   ├── transform/
│   ├── merge_data/
│   └── load/
├── dashboard/              # App Dash/Plotly (opcional)
├── client_secrets.json     # OAuth para Google Drive
├── .env                    # Variables de entorno
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 3. Orden de Ejecución del Proyecto

### Paso a paso sugerido:

1. Clonar repositorio y configurar entorno virtual.
2. Crear y activar `.env` con credenciales PostgreSQL.
3. Colocar `client_secrets.json` en la carpeta raíz.
4. Levantar servicios con Docker Compose.
5. Inicializar Airflow: `airflow db init` + crear usuario admin.
6. Ingresar a la interfaz Airflow: [http://localhost:9090](http://localhost:9090).
7. Activar DAG `etl_music_pipeline` y ejecutarlo manualmente.
8. Verificar carga de datos en PostgreSQL (`final_tracks`).
9. Ejecutar script `upload_to_drive.py` para subir CSV consolidado a Google Drive.
10. (Opcional) Levantar dashboard local con `python app.py`.

---

## 4. Detalles del Pipeline ETL

### Extracción

* `extract_spotify_csv`: Lee archivo local con top tracks de Spotify.
* `extract_grammy_csv`: Carga los registros de premiaciones Grammy.
* `extract_spotify_api`: Consulta API pública para top 50 tracks recientes.

### Transformación

* `transform_spotify`: Limpieza, tipado, cálculo de duración, normalización.
* `transform_grammys`: Selección de columnas clave, limpieza de nulos.
* `transform_api`: Conversión de formato y deduplicación de valores.

### Unificación y Carga

* `merge_all_data`: Une los tres datasets (por `track_name` y `artist`).
* `load_to_postgres`: Carga final en la tabla `public.final_tracks`.
* `upload_to_drive`: Sube el archivo final consolidado (`merged_music_data.csv`) a Google Drive.

---

## 5. Orquestación con Airflow

El archivo `etl_pipeline.py` define las siguientes tareas:

```python
extract_spotify_csv
extract_grammy_csv
extract_spotify_api
  └──> transform_spotify
  └──> transform_grammys
  └──> transform_api
          └──> merge_all_data
                └──> load_to_postgres
                      └──> upload_to_drive
```

Puedes ejecutarlo manualmente o con `@daily` una vez completada la configuración inicial.

---

## 6. Dashboard Interactivo

El dashboard creado con Dash + Plotly permite:

* Visualizar distribución de popularidad
* Canciones explícitas vs no explícitas
* Duración promedio por año
* Top artistas con premios Grammy
* Cobertura de fuentes (API, CSV, etc.)
* Análisis de "danceability" y "valence"

---

## 7. Carga a Google Drive

Para cargar automáticamente el archivo final:

1. Genera `client_secrets.json` en [Google Cloud Console](https://console.cloud.google.com/)
2. Habilita la **Google Drive API**
3. Coloca el archivo en la raíz del proyecto
4. El DAG ejecutará la función `upload_to_drive` si está bien configurado

---

## 8. Configuración Local Paso a Paso

```bash
# 1. Clona el repositorio
https://github.com/usuario/proyecto-etl-musica

# 2. Crea entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Levanta Airflow y PostgreSQL
docker-compose up --build

# 4. Inicializa la DB de Airflow
docker-compose run --rm webserver airflow db init

# 5. Accede a Airflow
http://localhost:9090 (usuario: airflow / contraseña: airflow)

# 6. Ejecuta el DAG 'etl_music_pipeline'
```

---

## 9. Conclusiones

Este proyecto demuestra cómo integrar distintas fuentes de datos musicales en un solo flujo ETL, transformarlos y almacenarlos para su análisis visual e interactivo. El uso de Airflow permite automatizar la actualización de los datos, mientras que el dashboard facilita la exploración de tendencias como:

* Popularidad por artista o año
* Patrón de duraciones musicales
* Análisis de lenguaje explícito
* Comparativas entre plataformas y premiaciones

Una solución versátil, moderna y adaptada a proyectos de ciencia de datos musicales.

---

© Universidad Autónoma de Occidente - Proyecto Académico ETL 2025

