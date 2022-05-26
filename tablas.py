import pandas as pd
import ast
from sqlalchemy import create_engine
from decouple import config
import logging
from funciones import enviar_sql
import sys


def main():
    
    
    l=config('archivo_log')
    logging.basicConfig(format='%(asctime)s:%(message)s', filename=l, level=logging.DEBUG)

    #Crea la conexion con el sql para crear y actualizar las tablas
    my_pass=config('Pwd_sql')
    engine = create_engine(f'postgresql://postgres:{my_pass}@localhost:5432/challenge')

    #Variables donde estan guardadas las bases
    try:
        with open(config('archivos'), 'rt') as f:
            files_down=ast.literal_eval(f.read())
            
    except:
        print('No se ha encontrado la informacion descargada, por favor ejecute nuevamente el archivo descargar.py')
        sys.exit(1)
        
    #limpio si ya existen las tablas finales
    query_union_exc_1='drop table if exists base_s_fuente, registros_cines, registros_totales;'
    enviar_sql(query_union_exc_1, 'query',engine)

    #Variables/Listas/diccionarios necesarios para normalizar la informacion descargada
    categorias=['museos','cines','bibliotecas']
    columnass={'cines':['cod_loc','idprovincia','iddepartamento','Observaciones','categoria','provincia','Departamento','localidad',
    'nombre','direccion','Piso','cp','cod_area','telefono','mail','web','Información adicional','Latitud','Longitud','TipoLatitudLongitud',
    'fuente','tipo_gestion','pantallas','butacas','espacio_incaa','año_actualizacion'],
    'museos':['cod_loc','idprovincia','iddepartamento','Observaciones','categoria','subcategoria','provincia','localidad','nombre',
    'direccion','Piso','cp','cod_area','telefono','mail','web','Latitud','Longitud','TipoLatitudLongitud','Info_adicional','fuente',
    'jurisdiccion','año_inauguracion','actualizacion'],
    'bibliotecas':['cod_loc','idprovincia','iddepartamento', 'Observacion','categoria','Subcategoria','provincia','Departamento','localidad',
    'nombre','direccion','Piso','cp','Cod_tel','telefono','mail','web','Información adicional','Latitud','Longitud','TipoLatitudLongitud',
    'fuente','Tipo_gestion',"año_inicio","Año_actualizacion"]}

    #Creacion de las tablas en el sql a traves del archivo sql_challen.sql
    enviar_sql("sql_challen.sql",'file',engine)
    
    #Columnas para tablas del sql
    col_sql=[ 'categoria','provincia' ,'localidad','nombre' ,'direccion','cp' ,'telefono','mail','web' ,'fuente' ]
    col_to_sql=['cod_loc','idprovincia','iddepartamento', 'fecha_carga'] + col_sql
    col_to_sql_cines=col_to_sql+['pantallas','butacas','espacio_incaa']

    #Para cada categoria lee las bases y las transforma para obtener las tablas finales
    for cat in categorias:
        df =pd.read_csv(files_down[cat],skiprows=1,names=columnass[cat])
        df['fecha_carga']=files_down['fecha']
        df[col_sql]=df[col_sql].convert_dtypes(convert_string=True)
        df['fuente']=df['fuente'].str.upper()
        df['categoria']=df['categoria'].str.upper()
        df['provincia']=df['provincia'].str.upper()
        df['provincia']=df['provincia'].str.strip()
        df['provincia'].replace('NEUQUÉN ','NEUQUÉN',inplace=True) 
        df['provincia'].replace('SANTA FÉ','SANTA FE',inplace=True)
        df['telefono'].replace('\s+', '-',regex=True,inplace=True)
        df.replace('s/d', 'NULL',regex=True,inplace=True)
        df.replace(r'^\s*$', 'NULL', regex=True,inplace=True)
        #Para cines para poder definir espacios incaa
        if cat=='cines':
            df['espacio_incaa'].replace('si', 'SI',regex=True,inplace=True)
            df_out=df[col_to_sql_cines]
        else:
            df_out=df[col_to_sql]

        #Envia el dataframe al sql
        try:
            df_out.to_sql(cat, engine, index=False, if_exists='append')

        except Exception as ex:
            
            query_union_exc_1='drop table base, bibliotecas, cines, museos;'
            enviar_sql(query_union_exc_1, 'query',engine)
            print(ex, 'Ha occurrido un error ejecute nuevamente el archivo por favor')
            sys.exit(1)

        else:
            logging.info("Tabla creadas correctamente.")

    #Tomo las tablas para crear la tabla base
    query_union='insert into base select cod_loc, idprovincia, iddepartamento, categoria, provincia, localidad, nombre, direccion, cp, \
    telefono, mail, web, fuente, fecha_carga from cines union all select * from museos union all select * from bibliotecas;'
    enviar_sql(query_union, 'query',engine)

    #Cargo en un dataframe el resultado    
    dataFrame=enviar_sql('select * from base;','read',engine)
    
    #Modifico el dataframe para poder crear la tabla de doble entrada con registros totales
    query_lista=[]
    d_cat=dataFrame['categoria'].unique()
    d_fuente=dataFrame['fuente'].unique()
    j=len(d_fuente)
    i=1
    tip='cat_'
    for d in d_cat:
        ds=d.replace(' ', '_').replace('/', '').replace('-', '').replace('.', '').replace('Ó',
        'O')
        ds=ds[:59]
        query_lista.append(f' count(case when categoria={d!r} then 1 else NULL end) as ' + tip + ds +' ,')

    tip='fte_'
    for d in d_fuente:
        ds=d.replace(' ', '_').replace('/', '').replace('-', '').replace('.', '').replace('MUNICIPALIDAD',
            'MUNIC').replace('DIRECCIÓN', 'DIR').replace('EDUCACIÓN', 'EDU').replace('CULTURA', 'CUL').replace('Ó',
        'O').replace('Í', 'I').replace('Á', 'A').replace('É','E')
        ds=ds[:59]
        co='' if j==i else ','
        query_lista.append(f' count(case when fuente= {d!r} then 1 else NULL end) as ' + tip + ds + co )
        i+=1

    #Creo la tabla de registros
    query_union_2='create table registros as select '+ ''.join(query_lista) + ' from base ;'
    enviar_sql(query_union_2, 'query',engine)
  
    #Creo la tabla de prov_cat
    s="_"
    query_union_3=f'create table prov_cat as select provincia, categoria, (provincia ||{s!r}|| categoria) as prov_cat, \
    count(1) as cuenta from base group by provincia, categoria;'
    enviar_sql(query_union_3, 'query',engine)


    #Cargo en un dataframe el resultado
    dataFrame=enviar_sql('select distinct prov_cat from prov_cat ;','read',engine)

    #Modifico el dataframe para poder crear la tabla de doble entrada con registros totales
    query_lista=[]
    d_prov_cat=dataFrame['prov_cat'].unique()
    j=len(d_prov_cat)
    i=1

    tip='pr_cat_'
    for d in d_prov_cat:
        ds=d.replace('CIUDAD AUTÓNOMA DE BUENOS AIRES','CABA').replace('TIERRA DEL FUEGO, ANTÁRTIDA E ISLAS DEL ATLÁNTICO SUR',
            'TIERRA DEL FUEGO').replace(' ', '_').replace('/', '').replace('-', '').replace('.', '').replace('Ó',
            'O').replace('Í', 'I').replace('Á', 'A').replace('É','E')
        ds=ds[:59]
        co='' if j==i else ','
        query_lista.append(f' sum(case when prov_cat={d!r} then cuenta else NULL end) as ' + tip + ds + co)
        i+=1

    #Creo tabla intermedia
    query_union_4='create table registros_2 as select '+ ''.join(query_lista) + ' from prov_cat ;'
    enviar_sql(query_union_4, 'query',engine)
    
    #Creo la tabla final de registros totales
    try:
        query_union_5='create table registros_totales as select a.*, b.*, c.* from registros a, registros_2 b \
        ,(select distinct fecha_carga from base) c;'
        enviar_sql(query_union_5, 'query',engine)
    except Exception:
        query_union_exc_1='drop table registros_totales;'
        enviar_sql(query_union_exc_1, 'query',engine)
        query_union_5='create table registros_totales as select a.*, b.*, c.* from registros a, registros_2 b \
        ,(select distinct fecha_carga from base) c;'
        enviar_sql(query_union_5, 'query',engine)
        
            
    #Elimino la fuente que no se requeria en la consigna
    try:
        query_union_6='insert into base_s_fuente select cod_loc, idprovincia, iddepartamento, categoria, provincia, \
        localidad, nombre, direccion, cp, telefono, mail, web, fecha_carga from base;'
        enviar_sql(query_union_6, 'query',engine)
    except Exception:
        query_union_exc_1='drop table base_s_fuente;'
        enviar_sql(query_union_exc_1, 'query',engine)
        query_union_6='insert into base_s_fuente select cod_loc, idprovincia, iddepartamento, categoria, provincia, \
        localidad, nombre, direccion, cp, telefono, mail, web, fecha_carga from base;'
        enviar_sql(query_union_6, 'query',engine)
    
    #Creo las tablas de cines
    t='SI'
    try:
        query_union_7=f'create table registros_cines as select provincia, sum(butacas) as butacas, sum(pantallas) as pantallas, \
        count(case when espacio_incaa={t!r} then 1 else NULL end) as espacios_INCAA, fecha_carga  from cines group by provincia \
        , fecha_carga  order by provincia;'
        enviar_sql(query_union_7, 'query',engine)
    except Exception:
        query_union_exc_1='drop table registros_cines;'
        enviar_sql(query_union_exc_1, 'query',engine)
        query_union_7=f'create table registros_cines as select provincia, sum(butacas) as butacas, sum(pantallas) as pantallas, \
        count(case when espacio_incaa={t!r} then 1 else NULL end) as espacios_INCAA, fecha_carga  from cines group by provincia \
        , fecha_carga  order by provincia;'
        enviar_sql(query_union_7, 'query',engine)
    
    #Elimino las tablas que no se necesitan
    query_union_8='drop table base, bibliotecas, cines, museos, prov_cat, registros, registros_2;'
    enviar_sql(query_union_8, 'query',engine)
    
    #Mensaje Final
    print('Se han generado y/o actualizado las tablas: \n',
          '\t base_s_fuente tabla que contiene la base completa.\n',
          '\t registros_totales contiene la cantidad de registros totales por categoria (cat_), por fuente (fte_) y por provincia_categoria (pr_cat_).\n',
          '\t registros_cines contine las cantidades totales de pantallas, butacas y espacios incaa por provincia.\n')
    
if __name__ == "__main__":
    main()