# Challenge 

1) Crear un entorno virtual de python:

	Correr en consola los siguientes comandos:

	En linux:

	sudo apt-get install libpq-dev

	sudo apt-get install python3.8-dev

	sudo apt-get install python3.8-venv

	python3 -m venv /path/to/new/virtual/environment


	En Windows:

	c:\>c:\Python35\python -m venv c:\path\to\myenv

2) Copiar los archivos al directorio del entorno virtual

	1)descargar.py
	2)tablas.py
	3)funciones.py
	4)requirements.txt
	5)sql_challen.sql
	6)settings.ini
	7)readme.txt


3) Activar entorno virtual

	En linux:
	. /path/to/new/virtual/environment/bin/activate

	En windows:
	C:\path/to/new/virtual/environment\Scripts\activate.bat

4) Instalar Dependencias

	pip3 install -r /path/to/new/virtual/environment/requirements.txt


5) Instalar Postgre si no se lo tiene instalado (www.postgresql.org)
       

	En linux:
	1) sudo apt-get update
	2) sudo apt-get install postgresql o sudo apt-get install postgresql-XX (XX la Version a instalar segun distro)
	3) sudo -i -u postgres
 	4) createuser --interactive
	5) challenge - super user yes
	6) createdb challenge
	7) exit
	8) sudo adduser challenge
	9) sudo -i -u challenge
	10) psql 
	11) \password postgres (poner password challenge)
	12) \q
	13) exit


	En windows:
	1) Descarguelo de la pagina de postgresql.
	2) Ejecute la instalacion estandar pero omita el lanzar Stackbuilder al final.
	3) Durante la instalacion cree un usuario challenge con permisos de superusuario.
	4) Añada la ruta al directorio PostgreSQL bin a las rustas de variables enviromentales(the PATH environmental variable).
	5) Abra la herramienta psql command-line
   	6) En el Command Prompt de windows, corra el comando: psql -U challenge
	7) Corra el comando CREATE DATABASE para crear una nueva database. CREATE DATABASE challenge;
	8) psql 
	9) \password postgres (poner password challenge)
	10) \q
	11) exit

6) Correr el comando python3.8 descargar.py para descargar las bases
7) Correr el comando python3.8 tablas.py para generar y/o actualizar las tablas
8) En el sql se generaran las tablas:
	1) base_s_fuente tabla que contiene la base completa.
	2) registros_totales contiene la cantidad de registros totales por categoria (cat_), por fuente (fte_) y por provincia_categoria (pr_cat_).
	3) registros_cines contine las cantidades totales de pantallas, butacas y espacios incaa por provincia.
    
