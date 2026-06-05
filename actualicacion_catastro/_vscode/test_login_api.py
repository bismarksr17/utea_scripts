import requests

# Configuración de la API
API_URL = "https://guabirasistemas.com:9062/Auth/login"
USUARIO = "USRUCAF"
CLAVE = "DC513EA4FBDAA7A14786FFDEBC4EF64E"

# Realizar la solicitud GET para obtener el token
def obtener_token():
    params = {
        "Usuario": USUARIO,
        "Clave": CLAVE
    }
    response = requests.get(API_URL, params=params, verify=False)  # verify=False para ignorar SSL si es necesario
    if response.status_code == 200:
        print("Token obtenido:", response.text)
        return response.text
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

if __name__ == "__main__":
    obtener_token()
