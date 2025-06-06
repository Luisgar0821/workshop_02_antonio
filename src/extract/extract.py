import os
import polars as pl
import pandas as pd
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")


# ---------------------------------------
# 1. Extraer Spotify desde CSV local
# ---------------------------------------
def extract_spotify_csv(**kwargs):
    """
    Carga el dataset limpio de Spotify desde archivo local y lo guarda como copia base.
    """
    df = pl.read_csv(f"{RAW_DIR}/spotify_dataset_clean.csv")
    df.write_csv(f"{RAW_DIR}/spotify_dataset.csv")
    print(" Extraído: spotify_dataset_clean.csv")


# ---------------------------------------
# 2. Extraer Grammy desde CSV local
# ---------------------------------------
def extract_grammy_csv(**kwargs):
    """
    Carga el dataset limpio de los Grammy desde archivo local y lo guarda como copia base.
    """
    df = pl.read_csv(f"{RAW_DIR}/the_grammy_awards_clean.csv")
    df.write_csv(f"{RAW_DIR}/grammy_awards_full.csv")
    print(" Extraído: the_grammy_awards_clean.csv")


# ---------------------------------------
# 3. Extraer desde la API de Spotify (múltiples artistas)
# ---------------------------------------
def extract_spotify_api(**kwargs):
    """
    Extrae los top tracks de múltiples artistas populares desde la API de Spotify.
    Guarda el resultado en un CSV en 'data/raw/datos_api_spotify_expandido.csv'.
    """
    load_dotenv()
    token = os.getenv("SPOTIFY_TOKEN")

    if not token:
        print(" No se encontró SPOTIFY_TOKEN en el .env")
        return

    headers = {
        "Authorization": token
    }

    artist_ids = {
        "Ed Sheeran": "6eUKZXaKkcviH0Ku9w2n3V",
        "Drake": "3TVXtAsR1Inumwj472S9r4",
        "The Weeknd": "1Xyo4u8uXC1ZmMpatF05PJ",
        "Ariana Grande": "66CXWjxzNUsdJxJ2JdwvnR",
        "Taylor Swift": "06HL4z0CvFAxyc27GXpf02",
        "Coldplay": "4gzpq5DPGxSnKTe4SA8HAU",
        "Lady Gaga": "1HY2Jd0NmPuamShAr6KMms",
        "U2": "51Blml2LZPmy7TTiAg47vQ",
        "Beyoncé": "6vWDO969PvNqNYHIOW5v0m",
        "Stevie Wonder": "7guDJrEfX3qb6FEbdPA5qi"
    }

    all_tracks = []

    for artist_name, artist_id in artist_ids.items():
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            tracks = response.json().get("tracks", [])
            for track in tracks:
                all_tracks.append({
                    "track_name": track["name"],
                    "artist_name": track["artists"][0]["name"],
                    "album_name": track["album"]["name"],
                    "release_date": track["album"]["release_date"],
                    "duration_ms": track["duration_ms"],
                    "popularity": track["popularity"],
                    "explicit": track["explicit"],
                    "spotify_url": track["external_urls"]["spotify"]
                })
        else:
            print(f" Error al obtener datos de {artist_name}: {response.status_code}")

    if all_tracks:
        df = pd.DataFrame(all_tracks)
        df.to_csv(f"{RAW_DIR}/datos_api_spotify_expandido.csv", index=False)
        print(f" Extraído: {len(df)} canciones desde la API de Spotify.")
    else:
        print(" No se extrajeron canciones. Verifica el token o los IDs.")

if __name__ == "__main__":
    extract_spotify_csv()
    extract_grammy_csv()
    extract_spotify_api()

# ---------------------------------------
# Exportación para Airflow
# ---------------------------------------
__all__ = [
    "extract_spotify_csv",
    "extract_grammy_csv",
    "extract_spotify_api"
]
