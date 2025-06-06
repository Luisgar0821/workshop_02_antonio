from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging
import sys
import os

# === CONFIGURACIÓN DE RUTA PARA IMPORTAR MÓDULOS ===
# Asegúrate de que ./src está montado en /opt/airflow/src desde docker-compose
sys.path.append("/opt/airflow/src")

# === IMPORTACIÓN DE FUNCIONES ===
from extract.extract import extract_spotify_csv, extract_grammy_csv, extract_spotify_api
from transform.transform import transform_spotify, transform_grammys, transform_api
from merge_data.merge import merge_all_data
from load.load_to_postgress import load_and_store_final_dataset
from load.upload_to_drive import upload_to_drive

# === CONFIGURACIÓN DE LOGGING ===
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def log_task(task_name, func):
    def wrapper(*args, **kwargs):
        logger.info(f"[START] Task: {task_name}")
        result = func(*args, **kwargs)
        logger.info(f"[END] Task: {task_name}")
        return result
    return wrapper

def return_none_wrapper(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        return None
    return wrapper

# === CONFIGURACIÓN DEL DAG ===
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='etl_music_pipeline',
    default_args=default_args,
    description='Pipeline ETL para integrar Spotify, Grammy y API',
    schedule_interval=None,
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="extract_spotify",
        python_callable=log_task("extract_spotify", return_none_wrapper(extract_spotify_csv))
    )

    t2 = PythonOperator(
        task_id="extract_grammy",
        python_callable=log_task("extract_grammy", return_none_wrapper(extract_grammy_csv))
    )

    t3 = PythonOperator(
        task_id="extract_api",
        python_callable=log_task("extract_api", return_none_wrapper(extract_spotify_api))
    )

    t4 = PythonOperator(
        task_id="transform_spotify",
        python_callable=log_task("transform_spotify", return_none_wrapper(transform_spotify))
    )

    t5 = PythonOperator(
        task_id="transform_grammys",
        python_callable=log_task("transform_grammys", return_none_wrapper(transform_grammys))
    )

    t6 = PythonOperator(
        task_id="transform_api",
        python_callable=log_task("transform_api", return_none_wrapper(transform_api))
    )

    t7 = PythonOperator(
        task_id="merge_data",
        python_callable=log_task("merge_data", return_none_wrapper(merge_all_data))
    )

    t8 = PythonOperator(
        task_id="load_postgres",
        python_callable=log_task("load_postgres", return_none_wrapper(load_and_store_final_dataset))
    )

    t9 = PythonOperator(
        task_id="upload_drive",
        python_callable=log_task("upload_drive", return_none_wrapper(upload_to_drive))
    )

    # === DEPENDENCIAS ENTRE TASKS ===
    # === DEPENDENCIAS ENTRE TASKS ===
t1 >> t4
t2 >> t5
t3 >> t6
[t4, t5, t6] >> t7 >> t8 >> t9


