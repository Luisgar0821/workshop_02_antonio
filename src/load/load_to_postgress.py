import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def load_and_store_final_dataset(**kwargs):  # <- Aceptar argumentos extra
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()

        # Eliminar la tabla si ya existe
        cur.execute("DROP TABLE IF EXISTS public.final_tracks;")
        conn.commit()

        # Crear tabla con todas las columnas del CSV
        create_table_query = """
        CREATE TABLE IF NOT EXISTS public.final_tracks (
            song_name TEXT,
            artist TEXT,
            track_genre TEXT,
            popularity INTEGER,
            explicit BOOLEAN,
            tempo FLOAT,
            valence FLOAT,
            energy FLOAT,
            danceability FLOAT,
            acousticness FLOAT,
            duration_ms INTEGER,
            duration_minutes FLOAT,
            year INTEGER,
            title TEXT,
            category TEXT,
            nominee TEXT,
            workers TEXT,
            img TEXT,
            winner TEXT,
            published_date TEXT,
            published_time TEXT,
            updated_date TEXT,
            updated_time TEXT,
            popularity_right INTEGER,
            explicit_right BOOLEAN,
            duration_minutes_right FLOAT,
            album_name TEXT,
            release_date TEXT,
            spotify_url TEXT
        );
        """
        cur.execute(create_table_query)
        conn.commit()

        # Ruta absoluta al CSV final
        final_path = "/opt/airflow/data/final/merged_music_data.csv"

        # Cargar datos desde el CSV
        copy_query = """
        COPY public.final_tracks (
            song_name, artist, track_genre, popularity, explicit, tempo, valence, energy,
            danceability, acousticness, duration_ms, duration_minutes, year, title,
            category, nominee, workers, img, winner, published_date, published_time,
            updated_date, updated_time, popularity_right, explicit_right,
            duration_minutes_right, album_name, release_date, spotify_url
        )
        FROM STDIN WITH CSV HEADER DELIMITER ',' NULL ''
        """
        with open(final_path, 'r', encoding='utf-8') as f:
            cur.copy_expert(copy_query, f)

        conn.commit()
        print(" Datos cargados en PostgreSQL.")

    except psycopg2.Error as e:
        print(" Error al conectar o cargar datos en PostgreSQL:", e)

    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    load_and_store_final_dataset()

