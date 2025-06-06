import os
from dotenv import load_dotenv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive2.auth import ServiceAccountCredentials

# Cargar variables de entorno si las usas
load_dotenv()

# Ruta base del proyecto
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
final_file_path = os.path.join(base_dir, "Data/final/merged_music_data.csv")
service_account_file = os.path.join(base_dir, "client_secrets01.json")
filename_on_drive = "merged_music_data.csv"

def upload_to_drive(**kwargs):
    try:
        # Verificar existencia del archivo a subir
        if not os.path.exists(final_file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {final_file_path}")

        # Autenticación con cuenta de servicio
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            service_account_file,
            scopes=["https://www.googleapis.com/auth/drive"]
        )
        drive = GoogleDrive(gauth)

        # Subir archivo
        file_to_upload = drive.CreateFile({'title': filename_on_drive})
        file_to_upload.SetContentFile(final_file_path)
        file_to_upload.Upload()
        print(f"✅ Archivo subido como '{filename_on_drive}'")

        # Verificación
        file_list = drive.ListFile({'q': f"title = '{filename_on_drive}'"}).GetList()
        if file_list:
            print("🔍 Archivo en Drive:")
            for file in file_list:
                print(f"📄 Nombre: {file['title']} | ID: {file['id']}")
        else:
            print("❌ El archivo no se encontró en Drive.")

    except Exception as e:
        print("❌ Error al subir a Google Drive:", e)

if __name__ == "__main__":
    upload_to_drive()
