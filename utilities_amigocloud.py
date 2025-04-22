# IMPORTACIONES
import sys
from docxtpl import InlineImage
from docx.shared import Mm
import os
import requests

sys.path.append('../_amigocloud')
from amigocloud import AmigoCloud

class AmigocloudFunctions:
    
    def __init__(self, token):
        self.token = token
        self.conectar()
    
    def conectar(self):
        """
        Establece conexión con la API de AmigoCloud utilizando el token proporcionado.
    
        Guarda la instancia de conexión en self.amigocloud.
    
        Manejo de errores:
        ------------------
        Captura errores al instanciar la conexión, como token inválido u otros errores de red o autenticación.
        """
        try:
            self.amigocloud = AmigoCloud(token=self.token)
            return True
        except Exception as e:
            print(f"Error al conectar con AmigoCloud: {e}")
            self.amigocloud = None
            return False
    
    def ejecutar_query_sql(self, id_project, query, tipo_sql):
        """
        Ejecuta una consulta SQL en un proyecto de AmigoCloud.
    
        Parámetros:
        -----------
        id_project : int o str
            ID del proyecto de AmigoCloud donde se ejecutará la consulta.
    
        query : str
            Sentencia SQL a ejecutar.
    
        tipo_sql : str
            Tipo de solicitud HTTP: 'get' o 'post'.
        
        Retorna:
        --------
        dict o str
            Resultado de la consulta o mensaje de error si algo falla.

        Excepciones:
        ------------
        ValueError:
            Si se proporciona un tipo de solicitud no válido.
        Exception:
            Si ocurre un error al realizar la solicitud a AmigoCloud.
        """
        url_proyecto_sql = f'https://app.amigocloud.com/api/v1/projects/{id_project}/sql'
        query_sql = {'query': query}

        try:
            tipo_sql = tipo_sql.lower()
            if tipo_sql == 'get':
                return self.amigocloud.get(url_proyecto_sql, query_sql)
            elif tipo_sql == 'post':
                return self.amigocloud.post(url_proyecto_sql, query_sql)
            else:
                raise ValueError(f"Tipo de solicitud inválido: '{tipo_sql}'. Usa 'get' o 'post'.")
        except Exception as e:
            print(f"Error al ejecutar la consulta SQL: {e}")
            return None
    
    def ejecutar_query_por_id(self, id_project, id_query):
        """
        Ejecuta un query almacenado en un proyecto de AmigoCloud, identificado por su ID.
        Este tipo de consulta se usa comúnmente para ejecutar instrucciones como UPDATE, DELETE, etc.
    
        Parámetros:
        -----------
        id_project : int o str
            ID del proyecto de AmigoCloud.
    
        id_query : int o str
            ID del query almacenado previamente en AmigoCloud.
    
        Retorna:
        --------
        int
            Número de filas afectadas por la ejecución del query.
    
        Manejo de errores:
        ------------------
        - Si la consulta no existe.
        - Si ocurre un error en la conexión o en la estructura del resultado.
        """
        try: 
            # obtiene el contenido del query según el ID
            get_query = self.amigocloud.get(
                f'https://app.amigocloud.com/api/v1/projects/{id_project}/queries/{id_query}'
            )
            # verifica que el query exista
            query = get_query.get('query')
            if not query:
                raise ValueError("No se encontró el texto del query con el ID proporcionado.")
            # ejecuta el query mediante método POST
            respuesta_post = self.ejecutar_query_sql(id_project, query, 'post')
            # retorna el número de filas afectadas
            return respuesta_post.get('count', 0)
        except Exception as e:
            print(f"Error al ejecutar el query con ID {id_query}: {e}")
            return None

    def buscar_fotos(self, id_project, galeria, source_id):
        """
        Busca fotos en una galería de AmigoCloud que correspondan a un source_id específico.
    
        Parámetros:
        -----------
        galeria : str
            Nombre de la galería (tabla) donde se buscarán las fotos.

        source_id : str o int
            ID del recurso al que deben estar asociadas las fotos.

        Retorna:
        --------
        dict o list
            Resultado completo (en formato JSON) de la consulta, que contiene las fotos encontradas.

        Manejo de errores:
        ------------------
        - Verifica errores en la construcción o ejecución del query.
        - Captura excepciones generales para evitar fallos inesperados.
        """
        try:
            if not galeria or not source_id:
                raise ValueError("La galería y el source_id son obligatorios.")
            # construye el query SQL
            query_sql = f"SELECT * FROM {galeria} WHERE source_amigo_id = '{source_id}'"
            # ejecuta el query (se espera que ejecutar_query_sql esté definido en la clase)
            respuesta = self.ejecutar_query_sql(id_project, query_sql, 'get')
            return respuesta
        except Exception as e:
            print(f"Error al buscar fotos en la galería '{galeria}' para source_id '{source_id}': {e}")
            return []

    def convertir_img_to_inline(self, docu, filename, ancho):
        """
        Convierte una imagen en un objeto InlineImage para incrustarla en un documento Word.
    
        Parámetros:
        -----------
        docu : docxtpl.DocxTemplate
            Objeto de documento donde se insertará la imagen.
    
        filename : str
            Ruta completa del archivo de imagen.
    
        ancho : int o float
            Ancho de la imagen en milímetros (mm).

        Retorna:
        --------
        InlineImage
            Imagen lista para insertarse en el documento con el tamaño especificado.

        Manejo de errores:
        ------------------
        - Verifica si la imagen existe.
        - Controla errores de tipo o problemas al crear el InlineImage.
        """
        try:
            if not isinstance(ancho, (int, float)):
                raise TypeError("El ancho debe ser un número (int o float).")
            return docxtpl.InlineImage(docu, image_descriptor=filename, width=Mm(ancho))
        except Exception as e:
            print(f"Error al convertir la imagen '{filename}' a InlineImage: {e}")
            return None

    def descargar_convertir_fotos_inline(self, lista_fotos, ruta_destino, documento):
        """
        Descarga fotos desde URLs de AmigoCloud y las convierte en objetos InlineImage para insertarlas en un documento Word.

        Parámetros:
        -----------
        lista_fotos : list[dict]
            Lista de diccionarios con los datos de las fotos, cada uno debe contener al menos la clave 's3_filename'.

        ruta_destino : str
            Ruta local donde se guardarán temporalmente las fotos descargadas.

        documento : docxtpl.DocxTemplate
            Documento Word donde se usarán las imágenes como InlineImage.
    
        Retorna:
        --------
        list[InlineImage]
            Lista de imágenes listas para insertarse en el documento.
    
        Manejo de errores:
        ------------------
        - Verifica que cada imagen tenga clave 's3_filename'.
        - Captura errores de red o archivos al descargar o guardar las imágenes.
        - Controla posibles errores al convertir a InlineImage.
        """
        lista_fotos_inline = []
        for foto in lista_fotos:
            try:
                s3_filename = foto['s3_filename']
                if not s3_filename:
                    print("Foto sin 's3_filename'. Se omite.")
                    continue
                url = f"https://www-amigocloud.s3.amazonaws.com/gallery/{s3_filename}"
                response = requests.get(url)
                # Ruta donde guardar la imagen
                file_path = os.path.join(ruta_destino, s3_filename)
                # Guardar imagen
                with open(file_path, "wb") as file:
                    file.write(response.content)
                # Convertir a InlineImage
                inline_img = self.convertir_img_to_inline(documento, file_path, 60)
                if inline_img:
                    lista_fotos_inline.append(inline_img)
            except Exception as e:
                print(f"Error al procesar la imagen {foto}: {e}")
        if len(lista_fotos_inline) > 0:
            return lista_fotos_inline
        else:
            print(f"Lista de imagenes descargadas en blaco")
            return []

    def modificar_reporte_generado(self, id_project, id_reg):
        """
        Modifica el campo 'informe_generado' de un registro en la base de datos y lo establece en True.

        Parámetros:
        -----------
        id_reg : int
            ID del registro que se desea actualizar.

        Retorna:
        --------
        int
            Número de registros afectados por la actualización. Si hay un error, retorna 0.

        Manejo de errores:
        ------------------
        - Valida que el ID sea un entero positivo.
        - Captura errores durante la ejecución del query.
        """
        try:
            if not isinstance(id_reg, int) or id_reg <= 0:
                raise ValueError("El ID debe ser un número entero positivo.")
            query = f"UPDATE dataset_341171 SET informe_generado = true WHERE id = {id_reg}"
            ejecutar = self.ejecutar_query_sql(id_project, query, 'post')
            return ejecutar.get('count', 0)
        except Exception as e:
            print(f"[ERROR] No se pudo modificar el registro {id_reg}: {e}")
            return 0
