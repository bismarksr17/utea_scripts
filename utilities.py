# creacion de qrs
import qrcode
import datetime
import collections

# windows dialog
import tkinter as tk
from tkinter import filedialog

# general
import os

def generar_qr(content_qr, output_path):
    '''
    Genera un codigo qr (.jpg)
    
    Parametor:
        content_qr: texto contenido en el qr
        output_path: ruta de carpetas donde segardara el .jpg
    
    Return: retorna la ruta local del archivo qr
    
    Nota: el archivo se guardara en la ruta indicada bajo el nombre qr_img.jpg
    '''
    # declara obj del qrocode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4)
    # se agrega el contenido del qr
    qr.add_data(content_qr)
    qr.make(fit=True)
    # define colores del qr
    img = qr.make_image(fill_color="black", back_color="white")
    # define ruta y nombre para guardar el qr
    ruta_qr = os.path.join(output_path + '\qr_img.png')
    # guardar el código QR en un archivo .png
    img.save(ruta_qr)
    # retorna la ruta del qr
    return ruta_qr

def convertir_formato_fecha(self, fecha):
    """
    Convierte una fecha desde el formato 'YYYY-mm-dd H:M:S+z' al formato 'd/m/YYYY'.
        
    Parámetros:
    -----------
    fecha : str
        Fecha en formato string, por ejemplo: '2023-09-15 14:30:00+0000'

    Retorna:
    --------
    str
        Fecha en formato 'dd/mm/YYYY'.
    Excepciones:
    ------------
    ValueError:
        Si el formato de la fecha no es válido.
    """
    try:
        new_formato = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S%z").strftime("%d/%m/%Y")
        return new_formato
    except ValueError as e:
        print(f"Error al convertir la fecha: {e}")
        return None

def convertir_dict_obj(self, diccionario, name):
    """
    Convierte un diccionario en un objeto tipo namedtuple.
    Esta función es útil cuando se desea acceder a los valores del diccionario 
    como atributos de un objeto en lugar de usar claves.
    
    Parámetros:
    -----------
    diccionario : dict
        El diccionario que se desea convertir.
    
    name : str
        Nombre de la clase del objeto que se creará.
    
    Retorna:
    --------
    namedtuple
        Objeto con los mismos campos que el diccionario.
    
    Ejemplo:
    --------
    >>> d = {'id': 1, 'nombre': 'Juan'}
    >>> obj = convertir_dict_obj(d, 'Usuario')
    >>> obj.nombre
    'Juan'
   
    Manejo de errores:
    ------------------
    - Retorna None si el argumento no es un diccionario válido.
    """
    try:
        if not isinstance(diccionario, dict):
            raise TypeError("Se esperaba un diccionario como primer parámetro.")
        if not isinstance(name, str):
            raise TypeError("El nombre del objeto debe ser una cadena de texto.")
        return collections.namedtuple(name, diccionario.keys())(*diccionario.values())
    except Exception as e:
        print(f"Error al convertir el diccionario a objeto: {e}")
        return None
   
def seleccionar_archivo(titulo, extension):
    """
    Abre un diálogo para seleccionar un archivo con la extensión dada.
    
    Parámetros:
    - titulo (str): titulo para mostrar en el titulo del dialog
    - extension (str): extensión del archivo sin el punto (por ejemplo, 'shp', 'geojson')
    
    Retorna:
    - str: ruta del archivo seleccionado, o cadena vacía si se canceló.
    """
    root = tk.Tk()
    root.withdraw()
    tipo_archivo = [(f"{extension.upper()} files", f"*.{extension}")]
    ruta = filedialog.askopenfilename(
        title=f"{titulo} (.{extension})",
        filetypes=tipo_archivo
    )
    return ruta

def guardar_como(titulo, extension):
    """
    Abre un cuadro de diálogo para guardar un archivo con una extensión dada.
    
    Parámetros:
    - titulo (str): título del cuadro de diálogo.
    - extension (str): extensión del archivo (sin el punto), por ejemplo 'shp', 'csv', 'gpkg'.
    
    Retorna:
    - str: ruta completa del archivo con la extensión seleccionada.
    """
    root = tk.Tk()
    root.withdraw()
    tipos = [(f"{extension.upper()} files", f"*.{extension}")]
    ruta = filedialog.asksaveasfilename(
        title=titulo,
        defaultextension=f".{extension}",
        filetypes=tipos
    )
    return ruta
