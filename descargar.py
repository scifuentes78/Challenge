import sys
import requests
from decouple import config
import logging
import os
import datetime

from funciones import download_file
#
#import locale
#Idioma "es-ES" (código para el español de Argentina)
#locale.setlocale(locale.LC_ALL, 'es-AR') 
now = datetime.datetime.now()

def main():
    l=config('archivo_log')
    logging.basicConfig(format = '%(asctime)s:%(message)s', filename = l, level = logging.DEBUG)
    
    #Seteo de variables/listas/diccionarios para que sea mas facil organizar la info
    categorias = ['museos','cines','bibliotecas']
    urls = {'museos':config('MUSEOS_URL'),'cines':config('CINES_URL'),'bibliotecas':config('BIBLIOTECA_URL')}
    files_down = {'fecha':now.strftime("%Y/%m/%d")}
    
    #crea los nombres de directorios con los formatos especificados en las instrucciones
    for cat in categorias:
        new_path = os.path.join(cat,'-'.join([str(now.year),str(now.strftime("%B"))]))
        local_archivo = os.path.join(new_path,'.'.join(['-'.join([cat,str(now.strftime("%d")),str(now.strftime("%m")),str(now.year)]),'csv']))
        
        #crea los directorios
        try:
            os.makedirs(new_path, exist_ok=True)
        except OSError:
            logging.info("Fallo la creacion del directorio %s por favor verifique que el usuario tiene permiso", new_path)
            print("Fallo la creacion del directorio %s . Por Favor verifique que el usuario tiene permiso" % new_path)
            sys.exit(1)
        else:
            logging.info("El archivo sera guardado en el directorio %s", new_path)

         
        # baja la info
        files_down[cat] = local_archivo
        try:
            download_file(urls[cat], local_archivo)
        except requests.exceptions.RequestException as e:
            print('Error:', e.response.text)
            print('Por favor corrobore que los url en settings.ini sigan siendo validos')
            sys.exit(1)
        
        

    #Guarda la informacion para cuando sea necesario actualizar las tablas sin efectuar la bajada
    with open(config('archivos'), 'wt') as f:
        files_down = str(files_down)
        f.write(files_down)
    
    print('Se ha descargado con exito la informacion. Para actualizar las tablas ejecute el archivo tablas.py')

if __name__ == "__main__":
    main()
