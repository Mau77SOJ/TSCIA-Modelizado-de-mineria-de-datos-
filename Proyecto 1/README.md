# 📊 Sistema de Gestión de CSV con Streamlit

Sistema integral para gestionar, editar y analizar archivos CSV con una interfaz web intuitiva construida en Streamlit. Ideal para administrar bases de datos tabulares, mantener versiones y realizar conversiones entre formatos.

## ✨ Características Principales

- **📁 Gestión Completa de CSV**: Visualiza, agrega, edita y elimina registros
- **🔄 Conversión de Formatos**: Convierte entre CSV y JSON bidireccionalmente
- **📜 Sistema de Versionado**: Respaldo automático con timestamp antes de cada modificación
- **🔍 Búsqueda Avanzada**: Busca por ID, columna específica o texto libre
- **📊 Comparación Visual**: Compara versiones original vs modificada
- **🎯 Interfaz Intuitiva**: Dashboard interactivo con métricas en tiempo real
- **💾 Preservación de Índices**: Maneja correctamente los IDs sin duplicación

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/csv-manager.git
cd csv-manager
```

2. **Instalar dependencias**
```bash
pip install streamlit pandas
```

3. **Crear estructura de carpetas**
```bash
mkdir Tables data_modificada historico
```

4. **Colocar archivos CSV**
   - Coloca tus archivos CSV en la carpeta `Tables/`
   - Asegúrate de que tengan encabezados en la primera fila
   - La primera columna debe ser el ID único

## 📂 Estructura del Proyecto

```
csv-manager/
│
├── app.py                  # Aplicación principal
├── README.md              # Este archivo
│
├── Tables/                # 📁 Archivos CSV originales
│   ├── autores.csv
│   ├── generos.csv
│   └── paises.csv
│
├── data_modificada/       # 📝 Archivos editados (se crea automáticamente)
│   ├── autores_modificado.csv
│   └── generos_modificado.csv
│
└── historico/             # 🗄️ Respaldos con timestamp (se crea automáticamente)
    ├── autores_20241029_153045.csv
    └── generos_20241029_160230.csv
```

## 🎮 Uso

### Iniciar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Funcionalidades

#### 🏠 **Inicio**
- Dashboard con estadísticas
- Vista rápida de archivos disponibles
- Indicadores de archivos modificados

#### 👁️ **Visualizar**
- Ver archivos CSV base
- Ver archivos CSV modificados
- Ver archivos JSON convertidos
- Exploración interactiva de datos

#### ➕ **Agregar Fila**
- ID autoincremental automático
- Formulario dinámico según columnas
- Validación de datos
- Opción de trabajar sobre versión modificada

#### ✏️ **Editar Fila**
- Selección por ID
- Edición protegida (ID no modificable)
- Vista previa de datos actuales
- Respaldo automático antes de guardar

#### 🗑️ **Eliminar Fila**
- Solo disponible para archivos modificados
- Selección segura por ID
- Confirmación antes de eliminar
- Vista previa del registro a eliminar

#### 🔍 **Buscar**
- **Por ID**: Búsqueda exacta por identificador
- **Por columna**: Búsqueda en columna específica
- **Texto libre**: Búsqueda en todo el archivo
- Resultados en tiempo real

#### 🔄 **Convertir CSV/JSON**
- CSV → JSON: Preserva estructura e índices
- JSON → CSV: Detecta automáticamente columna ID
- Selección de versión (base o modificada)

#### 📊 **Comparar Versiones**
- Vista lado a lado
- Detección de filas añadidas
- Detección de filas eliminadas
- Métricas de cambios

## 📋 Formato de Archivos CSV

### Estructura Recomendada

```csv
id_autor,nombre_autor,id_pais
1,Gabriel García Márquez,1
2,Jorge Luis Borges,2
3,Isabel Allende,3
```

**Importante:**
- Primera fila: Encabezados de columnas
- Primera columna: ID único (será usado como índice)
- No usar caracteres especiales en nombres de columnas

## 🔧 Sistema de Versionado

### Funcionamiento Automático

Cada vez que modificas un archivo:

1. **Primera modificación**: Crea `archivo_modificado.csv` en `data_modificada/`
2. **Modificaciones posteriores**: 
   - Crea respaldo con timestamp en `historico/`
   - Formato: `archivo_YYYYMMDD_HHMMSS.csv`
   - Actualiza el archivo modificado

### Ejemplo de Flujo

```
1. Editas autores.csv
   → Crea: data_modificada/autores_modificado.csv

2. Editas nuevamente autores_modificado.csv
   → Respaldo: historico/autores_20241029_153045.csv
   → Actualiza: data_modificada/autores_modificado.csv

3. Tercera edición
   → Respaldo: historico/autores_20241029_160230.csv
   → Actualiza: data_modificada/autores_modificado.csv
```

## 💡 Casos de Uso

### Gestión de Base de Datos de Librería

```
Tables/
├── autores.csv       (id_autor, nombre_autor, id_pais)
├── libros.csv        (id_libro, titulo, id_autor, id_genero)
├── generos.csv       (id_genero, nombre_genero)
└── paises.csv        (id_pais, nombre_pais)
```

### Inventario de Productos

```
Tables/
├── productos.csv     (id_producto, nombre, precio, stock)
├── categorias.csv    (id_categoria, nombre_categoria)
└── proveedores.csv   (id_proveedor, nombre_proveedor, contacto)
```

## 🛠️ Tecnologías

- **[Streamlit](https://streamlit.io/)**: Framework para aplicaciones web interactivas
- **[Pandas](https://pandas.pydata.org/)**: Manipulación y análisis de datos
- **Python 3.8+**: Lenguaje de programación