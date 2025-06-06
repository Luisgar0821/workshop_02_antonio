import polars as pl
import os
import re

DATA_PROCESSED = "/opt/airflow/data/processed"
DATA_FINAL = "/opt/airflow/data/final"

os.makedirs(DATA_FINAL, exist_ok=True)

def normalize_text(value: str) -> str:
    if isinstance(value, str):
        value = value.lower()
        value = re.sub(r"[^a-z0-9\s]", "", value)
        value = re.sub(r"\s+", " ", value)
        return value.strip()
    return value

def merge_all_data(**kwargs):  # 👈 agregado **kwargs
    df_spotify = pl.read_csv(f"{DATA_PROCESSED}/spotify_transformed.csv")
    df_grammy = pl.read_csv(f"{DATA_PROCESSED}/grammys_transformed.csv")
    df_api = pl.read_csv(f"{DATA_PROCESSED}/api_spotify_transformed.csv")

    df_spotify = df_spotify.with_columns([
        pl.col("song_name").map_elements(normalize_text, return_dtype=pl.Utf8),
        pl.col("artist").map_elements(normalize_text, return_dtype=pl.Utf8)
    ])
    df_grammy = df_grammy.with_columns([
        pl.col("song_name").map_elements(normalize_text, return_dtype=pl.Utf8),
        pl.col("artist").map_elements(normalize_text, return_dtype=pl.Utf8)
    ])
    df_api = df_api.with_columns([
        pl.col("song_name").map_elements(normalize_text, return_dtype=pl.Utf8),
        pl.col("artist").map_elements(normalize_text, return_dtype=pl.Utf8)
    ])

    merged = df_spotify.join(df_grammy, on=["song_name", "artist"], how="left")
    merged = merged.join(df_api, on=["song_name", "artist"], how="left")

    output_path = f"{DATA_FINAL}/merged_music_data.csv"
    merged.write_csv(output_path)
    print(f"Dataset combinado guardado en: {output_path}")

