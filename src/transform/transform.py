import polars as pl
import os
import re

# Definir rutas absolutas
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_RAW = os.path.join(BASE_DIR, "data/raw")
DATA_PROCESSED = os.path.join(BASE_DIR, "data/processed")

def normalize_text(value: str) -> str:
    if isinstance(value, str):
        value = value.lower()
        value = re.sub(r"[^a-z0-9\s]", "", value)
        value = re.sub(r"\s+", " ", value)
        return value.strip()
    return value

def transform_spotify(**kwargs):
    df = pl.read_csv(f"{DATA_RAW}/spotify_dataset_clean.csv")
    df = df.rename({col: col.strip().lower().replace(" ", "_") for col in df.columns})

    df = df.with_columns([
        pl.col("track_name").map_elements(normalize_text, return_dtype=pl.Utf8),
        pl.col("artists").map_elements(normalize_text, return_dtype=pl.Utf8)
    ])

    df = df.select([
        pl.col("track_name").alias("song_name"),
        pl.col("artists").alias("artist"),
        "track_genre", "popularity", "explicit",
        "tempo", "valence", "energy", "danceability",
        "acousticness", "duration_ms"
    ])

    df = df.with_columns([
        (pl.col("duration_ms") / 60000).alias("duration_minutes")
    ])

    df.write_csv(f"{DATA_PROCESSED}/spotify_transformed.csv")
    print("Spotify transformado.")

def transform_grammys(**kwargs):
    df = pl.read_csv(f"{DATA_RAW}/the_grammy_awards_clean.csv")
    df = df.rename({col: col.strip().lower().replace(" ", "_") for col in df.columns})

    df = df.with_columns([
        pl.col("nominee").map_elements(normalize_text, return_dtype=pl.Utf8),
        pl.col("artist").map_elements(normalize_text, return_dtype=pl.Utf8),
        pl.col("category").map_elements(normalize_text, return_dtype=pl.Utf8)
    ])

    df = df.filter(
        (pl.col("category").str.contains("song") | pl.col("category").str.contains("record")) &
        ~(pl.col("category").str.contains("album") | pl.col("category").str.contains("artist"))
    )

    df = df.with_columns([
        pl.col("nominee").alias("song_name")
    ])

    df.write_csv(f"{DATA_PROCESSED}/grammys_transformed.csv")
    print("Grammys transformado.")

def transform_api(**kwargs):
    df = pl.read_csv(f"{DATA_RAW}/datos_api_spotify_expandido.csv")
    df = df.rename({
        "track_name": "song_name",
        "artist_name": "artist"
    })

    df = df.with_columns([
        pl.col("song_name").map_elements(normalize_text, return_dtype=pl.Utf8),
        pl.col("artist").map_elements(normalize_text, return_dtype=pl.Utf8),
        (pl.col("duration_ms") / 60000).alias("duration_minutes")
    ])

    columnas_deseadas = [
        "song_name", "artist", "popularity", "explicit",
        "tempo", "valence", "energy", "danceability", "acousticness",
        "duration_minutes", "album_name", "release_date", "spotify_url"
    ]

    columnas_finales = [col for col in columnas_deseadas if col in df.columns]
    df = df.select(columnas_finales)

    df.write_csv(f"{DATA_PROCESSED}/api_spotify_transformed.csv")
    print("API Spotify transformado.")


# Ejecución local (solo útil si pruebas fuera de Airflow)
if __name__ == "__main__":
    transform_spotify()
    transform_grammys()
    transform_api()
