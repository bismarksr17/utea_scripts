# config.py
from dotenv import load_dotenv
import os
load_dotenv(override=True)

# CONSTANTES

# Rutas de carpetas, unidad local y ruta de ONEDRIVE
RUTA_UNIDAD_ONE_DRIVE = os.getenv('RUTA_UNIDAD_ONE_DRIVE')
RUTA_LOCAL_ONE_DRIVE = os.getenv('RUTA_LOCAL_ONE_DRIVE')

# API Admin para amigocloud
API_AMIGOCLOUD_TOKEN_ADM = os.getenv('API_AMIGOCLOUD_TOKEN_ADM')

# Conexion postgress
POSTGRES_UTEA = {
    "HOST": os.getenv("HOST"),
    "PORT": os.getenv("PORT"),
    "DATABASE": os.getenv("DATABASE"),
    "USER": os.getenv("USER"),
    "PASSWORD": os.getenv("PASSWORD"),
}