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
	1)


4) Activar entorno virtual

	En linux:
	. /path/to/new/virtual/environment/bin/activate

	En windows:
	C:\path/to/new/virtual/environment\Scripts\activate.bat

3) Instalar Dependencias

	pip3 install -r /path/to/new/virtual/environment/requirements.txt


4) Instalar Postgre si no se lo tiene instalado (www.postgresql.org)
       

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
	1) Descarguelo de la pagina de postgresql
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

5) Correr el archivo python3.8 descargar.py para descargar las bases
6) Correr el archivo python3.8 tablas.py para generar y/o actualizar las tablas
