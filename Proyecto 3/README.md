# Análisis de Base de Datos de Ventas de Librería

## Descripción general
El proyecto analiza una base de datos de **ventas de una librería** mediante Python y SQL.  
El objetivo es **explorar, visualizar y extraer conocimiento** de los datos, detectando patrones y comportamientos relevantes en las ventas.  

El análisis se ejecuta directamente desde un **notebook de Jupyter**, utilizando **SQLAlchemy** para conectarse a la base de datos, junto con herramientas de análisis y minería de datos.

---

## Estructura del proyecto

```
SQL-PYTHON/
│
├── Tables/
│   ├── autores.csv
│   ├── clientes.csv
│   ├── factura.csv
│   ├── formato.csv
│   ├── genero.csv
│   ├── libros.csv
│   ├── localidades.csv
│   ├── metodos_de_pago.csv
│   ├── paises.csv
│   ├── proovedores.csv
│   └── ventas.csv
│
└── main.ipynb
```

### Descripción
- **Tables/**: contiene archivos `.csv` que reflejan las tablas de la base de datos.  
  Estos archivos sirven únicamente para consultar la estructura y el contenido de referencia de cada tabla.  
- **main.ipynb**: notebook principal que realiza la conexión SQL con la base de datos, ejecuta consultas y desarrolla el análisis exploratorio y de minería de datos.

---

## Tecnologías utilizadas
- **Python 3**
- **SQLAlchemy** – conexión y ejecución de consultas SQL  
- **Pandas** – manipulación y limpieza de datos  
- **Matplotlib / Seaborn** – visualización gráfica  
- **Scikit-learn** – minería de datos y modelado básico  
- **Jupyter Notebook** – entorno interactivo de análisis  

---

## Ejecución del notebook

### 1. Clonar o descargar el repositorio
```bash
git clone https://github.com/usuario/SQL-PYTHON-LIBRERIA.git
cd SQL-PYTHON-LIBRERIA
```

### 2. Crear y activar un entorno virtual (opcional)
```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

> Si no existe un `requirements.txt`, podés instalar manualmente:
```bash
pip install pandas sqlalchemy matplotlib seaborn scikit-learn jupyter
```

### 4. Ejecutar Jupyter Notebook
```bash
jupyter notebook
```

### 5. Abrir y ejecutar el notebook
Abrí `main.ipynb` y corré las celdas en orden.  
El notebook establecerá la conexión con la base de datos, cargará las tablas y generará análisis y visualizaciones.

---

## Objetivos del análisis
- Evaluar desempeño de ventas por **género literario, formato y país**.  
- Identificar **clientes más rentables** y **productos más vendidos**.  
- Detectar **patrones de comportamiento** mediante técnicas básicas de minería de datos.  
- Apoyar la **toma de decisiones comerciales** de la librería.
