# creacion de qrs
import qrcode

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
