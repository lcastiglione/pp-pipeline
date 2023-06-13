"""
Módulo que contiene los tipos de excepciones que pueden ocurrir en peticiones http.
"""


class ResponseHTTPException(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, msg,url,method):
        super().__init__(f"Se produjo un error al procesar la url '{url}' con el metodo '{method}': {msg}")
