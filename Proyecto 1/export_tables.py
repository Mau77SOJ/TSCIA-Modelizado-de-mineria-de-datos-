import pandas as pd 
from sqlalchemy import create_engine

# Motor de conexión
host = "localhost"
user = "root"
password = ""
port = 3306
database = "libreria"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4")

# Importación y lectura de las tablas

# clientes
df_clientes = pd.read_sql_query("SELECT * FROM clientes;", engine)
df_clientes.to_csv("clientes.csv", index=False)

# autores
df_autores = pd.read_sql_query("SELECT * FROM autores;", engine)
df_autores.to_csv("autores.csv", index=False)

# factura
df_factura = pd.read_sql_query("SELECT * FROM factura;", engine)
df_factura.to_csv("factura.csv", index=False)

# formatos
df_formatos = pd.read_sql_query("SELECT * FROM formatos;", engine)
df_formatos.to_csv("formato.csv", index=False)

# genero
df_generos = pd.read_sql_query("SELECT * FROM generos;", engine)
df_generos.to_csv("genero.csv", index=False)

# libros
df_libros = pd.read_sql_query("SELECT * FROM libros;", engine)
df_libros.to_csv("libros.csv", index=False)

# localidades
df_localidades = pd.read_sql_query("SELECT * FROM localidades;", engine)
df_localidades.to_csv("localidades.csv", index=False)

# métodos de pago
df_metodos_de_pago = pd.read_sql_query("SELECT * FROM metodos_de_pago;", engine)
df_metodos_de_pago.to_csv("metodos_de_pago.csv", index=False)

# paises
df_paises = pd.read_sql_query("SELECT * FROM paises;", engine)
df_paises.to_csv("paises.csv", index=False)

# proveedores
df_proveedores = pd.read_sql_query("SELECT * FROM proveedores;", engine)
df_proveedores.to_csv("proovedores.csv", index=False)

# ventas
df_ventas = pd.read_sql_query("SELECT * FROM ventas;", engine)
df_ventas.to_csv("ventas.csv", index=False)