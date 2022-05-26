import requests
import logging
from sqlalchemy import text
import pandas as pd


def download_file(url, n_archivo):
    ''' Funcion para bajar los archivos por partes por si son muy grandes'''
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(n_archivo, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    logging.info("Archivo descargado %s", n_archivo)
    return n_archivo


def enviar_sql(origen, tipo, engine):
    '''Funcion para trabajar con el sql'''
    with engine.connect() as con:
        if tipo == 'file':
            with open(origen) as file:
                query = text(file.read())
                con.execute(query)
            logging.info("Archivo creado %s", origen)
        elif tipo == 'query':
            query = text(origen)
            con.execute(query)
            logging.info("Query enviada %s", query)
        else:
            v = pd.read_sql(origen, con)
            logging.info("Archivo leido %s", origen)
            return v
