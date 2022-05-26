CREATE TABLE IF NOT EXISTS museos (
cod_loc bigint,
idprovincia bigint,
iddepartamento bigint,
categoria varchar(100),
provincia varchar(100),
localidad  varchar(100),
nombre varchar(250),
direccion varchar(250),
cp varchar(50),
telefono varchar(50),
mail varchar(100),
web varchar(250),
fuente varchar(100),
fecha_carga date
);

CREATE TABLE IF NOT EXISTS cines (
cod_loc bigint,
idprovincia bigint,
iddepartamento bigint,
categoria varchar(100),
provincia varchar(100),
localidad varchar(100),
nombre varchar(250),
direccion varchar(250),
cp varchar(50),
telefono varchar(50),
mail varchar(100),
web varchar(250),
fuente varchar(100),
pantallas integer,
butacas integer,
espacio_incaa varchar(100),
fecha_carga date
);

CREATE TABLE IF NOT EXISTS bibliotecas (
cod_loc bigint,
idprovincia bigint,
iddepartamento bigint,
categoria varchar(100),
provincia varchar(100),
localidad varchar(100),
nombre varchar(250),
direccion varchar(250),
cp varchar(50),
telefono varchar(50),
mail varchar(100),
web varchar(250),
fuente varchar(100),
fecha_carga date
);

CREATE TABLE IF NOT EXISTS base (
cod_loc bigint,
idprovincia bigint,
iddepartamento bigint,
categoria varchar(100),
provincia varchar(100) ,
localidad varchar(100),
nombre varchar(250),
direccion varchar(250),
cp varchar(50),
telefono varchar(50),
mail varchar(100),
web varchar(250),
fuente varchar(100),
fecha_carga date
);

CREATE TABLE IF NOT EXISTS base_s_fuente (
cod_loc bigint,
idprovincia bigint,
iddepartamento bigint,
categoria varchar(100),
provincia varchar(100) ,
localidad varchar(100),
nombre varchar(250),
direccion varchar(250),
cp varchar(50),
telefono varchar(50),
mail varchar(100),
web varchar(250), 
fecha_carga date
);
