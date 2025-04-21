# config.py
from dotenv import load_dotenv
import os
load_dotenv(override=True)

# CONSTANTES
RUTA_UNIDAD_ONE_DRIVE = os.getenv('RUTA_UNIDAD_ONE_DRIVE')
RUTA_LOCAL_ONE_DRIVE = os.getenv('RUTA_LOCAL_ONE_DRIVE')
RUTA_COMPLETA = os.path.join(os.getenv('RUTA_UNIDAD_ONE_DRIVE'), os.getenv('RUTA_LOCAL_ONE_DRIVE'))
API_AMIGOCLOUD_TOKEN_ADM = os.getenv('API_KEY_AMIGOCLOUD_TOKEN_ADM')