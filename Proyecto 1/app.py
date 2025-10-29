import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

# Configuración de carpetas
CARPETA_BASE = "Tables"
CARPETA_MODIFICADA = "data_modificada"
CARPETA_HISTORICO = "historico"

# Crear carpetas si no existen
os.makedirs(CARPETA_MODIFICADA, exist_ok=True)
os.makedirs(CARPETA_HISTORICO, exist_ok=True)

# Configuración de la página
st.set_page_config(
    page_title="Gestor de CSV",
    page_icon="📊",
    layout="wide"
)

# Funciones auxiliares
def obtener_archivos_csv(carpeta):
    """Retorna lista de archivos CSV en una carpeta"""
    if not os.path.exists(carpeta):
        return []
    return sorted([f for f in os.listdir(carpeta) if f.endswith('.csv')])

def cargar_csv(archivo, usar_modificado=False):
    """Carga un archivo CSV con la primera columna como índice"""
    carpeta = CARPETA_MODIFICADA if usar_modificado else CARPETA_BASE
    ruta = os.path.join(carpeta, archivo)
    
    if usar_modificado:
        # Buscar el archivo modificado
        nombre_base = archivo.replace('.csv', '')
        archivo_mod = f"{nombre_base}_modificado.csv"
        ruta = os.path.join(CARPETA_MODIFICADA, archivo_mod)
    
    if os.path.exists(ruta):
        # Cargar con la primera columna como índice
        return pd.read_csv(ruta, index_col=0)
    return None

def existe_modificado(archivo):
    """Verifica si existe versión modificada"""
    nombre_base = archivo.replace('.csv', '')
    archivo_mod = f"{nombre_base}_modificado.csv"
    return os.path.exists(os.path.join(CARPETA_MODIFICADA, archivo_mod))

def guardar_csv(df, archivo, respaldar=True):
    """Guarda CSV con índice y crea respaldo si existe versión anterior"""
    nombre_base = archivo.replace('.csv', '')
    archivo_mod = f"{nombre_base}_modificado.csv"
    ruta_destino = os.path.join(CARPETA_MODIFICADA, archivo_mod)
    
    # Respaldar versión anterior si existe
    if respaldar and os.path.exists(ruta_destino):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_respaldo = f"{nombre_base}_{timestamp}.csv"
        ruta_respaldo = os.path.join(CARPETA_HISTORICO, nombre_respaldo)
        df_anterior = pd.read_csv(ruta_destino, index_col=0)
        df_anterior.to_csv(ruta_respaldo)
        st.success(f"✅ Respaldo guardado: {nombre_respaldo}")
    
    # Guardar nueva versión con índice
    df.to_csv(ruta_destino)
    return ruta_destino

def csv_a_json(archivo, usar_modificado=False):
    """Convierte CSV a JSON"""
    df = cargar_csv(archivo, usar_modificado)
    if df is None:
        return None
    
    # Reset index para incluirlo en el JSON
    df_reset = df.reset_index()
    registros = df_reset.to_dict('records')
    
    carpeta = CARPETA_MODIFICADA if usar_modificado else CARPETA_BASE
    nombre_json = archivo.replace('.csv', '.json')
    ruta_json = os.path.join(carpeta, nombre_json)
    
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)
    
    return ruta_json

def json_a_csv(ruta_json):
    """Convierte JSON a CSV"""
    with open(ruta_json, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    df = pd.DataFrame(datos)
    
    # Si el primer campo parece un ID, usarlo como índice
    primera_col = df.columns[0]
    if 'id' in primera_col.lower():
        df = df.set_index(primera_col)
    
    nombre_csv = os.path.basename(ruta_json).replace('.json', '.csv')
    ruta_csv = os.path.join(CARPETA_MODIFICADA, nombre_csv)
    df.to_csv(ruta_csv)
    
    return ruta_csv

# ==================== INTERFAZ ====================

st.title("📊 Sistema de Gestión de CSV")
st.markdown("---")

# Sidebar para navegación
menu = st.sidebar.selectbox(
    "Seleccione una opción",
    ["🏠 Inicio", "👁️ Visualizar", "➕ Agregar Fila", "✏️ Editar Fila", 
     "🗑️ Eliminar Fila", "🔍 Buscar", "🔄 Convertir CSV/JSON", "📊 Comparar Versiones"]
)

# ==================== INICIO ====================
if menu == "🏠 Inicio":
    st.header("Bienvenido al Gestor de CSV")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        archivos_base = obtener_archivos_csv(CARPETA_BASE)
        st.metric("Archivos Base", len(archivos_base))
    
    with col2:
        archivos_mod = obtener_archivos_csv(CARPETA_MODIFICADA)
        st.metric("Archivos Modificados", len(archivos_mod))
    
    with col3:
        archivos_hist = obtener_archivos_csv(CARPETA_HISTORICO)
        st.metric("Respaldos", len(archivos_hist))
    
    st.markdown("### 📁 Archivos disponibles")
    if archivos_base:
        for archivo in archivos_base:
            modificado = "✅" if existe_modificado(archivo) else "⚪"
            st.write(f"{modificado} {archivo}")
    else:
        st.warning("No hay archivos CSV en la carpeta Tables")

# ==================== VISUALIZAR ====================
elif menu == "👁️ Visualizar":
    st.header("Visualizar Archivos")
    
    tipo = st.radio("Tipo de archivo", ["CSV Base", "CSV Modificado", "JSON"])
    
    if tipo == "CSV Base":
        archivos = obtener_archivos_csv(CARPETA_BASE)
        carpeta = CARPETA_BASE
    elif tipo == "CSV Modificado":
        archivos = obtener_archivos_csv(CARPETA_MODIFICADA)
        carpeta = CARPETA_MODIFICADA
    else:  # JSON
        # Buscar JSON en ambas carpetas
        archivos = []
        archivos_info = []  # Para guardar (nombre, carpeta)
        
        for carpeta_buscar in [CARPETA_BASE, CARPETA_MODIFICADA]:
            if os.path.exists(carpeta_buscar):
                jsons = [f for f in os.listdir(carpeta_buscar) if f.endswith('.json')]
                for j in jsons:
                    origen = "Base" if carpeta_buscar == CARPETA_BASE else "Modificada"
                    archivos.append(f"{j} ({origen})")
                    archivos_info.append((j, carpeta_buscar))
        
        carpeta = None  # Se determinará según selección
    
    if archivos:
        archivo_seleccionado = st.selectbox("Seleccione un archivo", archivos)
        
        if st.button("Mostrar"):
            if tipo == "JSON":
                # Obtener el índice seleccionado y buscar la carpeta correcta
                indice_seleccionado = archivos.index(archivo_seleccionado)
                nombre_real, carpeta = archivos_info[indice_seleccionado]
                ruta = os.path.join(carpeta, nombre_real)
            else:
                ruta = os.path.join(carpeta, archivo_seleccionado)
            
            if archivo_seleccionado.endswith('.csv') or ruta.endswith('.csv'):
                df = pd.read_csv(ruta, index_col=0)
                st.dataframe(df, use_container_width=True)
                st.info(f"📊 Filas: {len(df)} | Columnas: {len(df.columns)}")
            else:  # JSON
                with open(ruta, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                st.json(datos[:50])  # Mostrar primeros 50 registros
                if isinstance(datos, list):
                    st.info(f"📊 Total registros: {len(datos)}")
    else:
        st.warning(f"No hay archivos disponibles de tipo: {tipo}")

# ==================== AGREGAR FILA ====================
elif menu == "➕ Agregar Fila":
    st.header("Agregar Nueva Fila")
    
    archivos = obtener_archivos_csv(CARPETA_BASE)
    
    if archivos:
        archivo = st.selectbox("Seleccione archivo", archivos)
        
        usar_mod = False
        if existe_modificado(archivo):
            usar_mod = st.checkbox("Usar versión modificada")
        
        df = cargar_csv(archivo, usar_mod)
        
        if df is not None:
            st.write("Vista previa:")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Calcular nuevo ID basado en el índice
            if len(df.index) > 0:
                ids_numericos = pd.to_numeric(df.index, errors='coerce')
                ids_validos = ids_numericos.dropna()
                nuevo_id = int(ids_validos.max()) + 1 if len(ids_validos) > 0 else 1
            else:
                nuevo_id = 1
            
            st.info(f"Nuevo ID asignado: {nuevo_id}")
            
            # Crear formulario para nueva fila
            with st.form("agregar_fila"):
                valores = {}
                
                # Mostrar el ID que se asignará
                st.text_input(f"{df.index.name or 'ID'} (Auto)", value=str(nuevo_id), disabled=True)
                
                # Resto de columnas
                for col in df.columns:
                    valores[col] = st.text_input(f"{col}", key=f"col_{col}")
                
                submitted = st.form_submit_button("Agregar Fila")
                
                if submitted:
                    # Crear nueva fila con el ID como índice
                    nueva_fila = pd.DataFrame([valores], index=[nuevo_id])
                    nueva_fila.index.name = df.index.name
                    df_modificado = pd.concat([df, nueva_fila])
                    guardar_csv(df_modificado, archivo)
                    st.success("✅ Fila agregada exitosamente")
                    st.rerun()
    else:
        st.warning("No hay archivos disponibles")

# ==================== EDITAR FILA ====================
elif menu == "✏️ Editar Fila":
    st.header("Editar Fila")
    
    archivos = obtener_archivos_csv(CARPETA_BASE)
    
    if archivos:
        archivo = st.selectbox("Seleccione archivo", archivos)
        
        usar_mod = False
        if existe_modificado(archivo):
            usar_mod = st.checkbox("Usar versión modificada")
        
        df = cargar_csv(archivo, usar_mod)
        
        if df is not None:
            st.write("Datos actuales:")
            st.dataframe(df, use_container_width=True)
            
            # Seleccionar por ID (índice)
            ids_disponibles = df.index.tolist()
            id_seleccionado = st.selectbox("Seleccione el ID a editar", ids_disponibles)
            
            with st.form("editar_fila"):
                st.write(f"Editando registro con ID: {id_seleccionado}")
                valores_nuevos = {}
                
                # Mostrar ID (no editable)
                st.text_input(f"{df.index.name or 'ID'} (no editable)", value=str(id_seleccionado), disabled=True)
                
                for col in df.columns:
                    valor_actual = df.loc[id_seleccionado, col]
                    valores_nuevos[col] = st.text_input(f"{col}", value=str(valor_actual), key=f"edit_{col}")
                
                submitted = st.form_submit_button("Guardar Cambios")
                
                if submitted:
                    for col, val in valores_nuevos.items():
                        df.loc[id_seleccionado, col] = val
                    guardar_csv(df, archivo)
                    st.success("✅ Fila modificada exitosamente")
                    st.rerun()
    else:
        st.warning("No hay archivos disponibles")

# ==================== ELIMINAR FILA ====================
elif menu == "🗑️ Eliminar Fila":
    st.header("Eliminar Fila")
    
    archivos_mod = []
    for arch in obtener_archivos_csv(CARPETA_BASE):
        if existe_modificado(arch):
            archivos_mod.append(arch)
    
    if archivos_mod:
        archivo = st.selectbox("Seleccione archivo (solo modificados)", archivos_mod)
        
        df = cargar_csv(archivo, usar_modificado=True)
        
        if df is not None:
            st.write("Datos actuales:")
            st.dataframe(df, use_container_width=True)
            
            # Seleccionar por ID
            ids_disponibles = df.index.tolist()
            id_eliminar = st.selectbox("Seleccione el ID a eliminar", ids_disponibles)
            
            st.warning(f"⚠️ Se eliminará el registro con ID: {id_eliminar}")
            st.dataframe(df.loc[[id_eliminar]], use_container_width=True)
            
            if st.button("Confirmar Eliminación", type="primary"):
                df = df.drop(id_eliminar)
                guardar_csv(df, archivo)
                st.success("✅ Fila eliminada exitosamente")
                st.rerun()
    else:
        st.warning("No hay archivos modificados disponibles")

# ==================== BUSCAR ====================
elif menu == "🔍 Buscar":
    st.header("Buscar en CSV")
    
    archivos = obtener_archivos_csv(CARPETA_BASE)
    
    if archivos:
        archivo = st.selectbox("Seleccione archivo", archivos)
        
        usar_mod = False
        if existe_modificado(archivo):
            usar_mod = st.checkbox("Buscar en versión modificada")
        
        df = cargar_csv(archivo, usar_mod)
        
        if df is not None:
            tipo_busqueda = st.radio("Tipo de búsqueda", ["Por ID", "Por columna", "Texto libre"])
            
            if tipo_busqueda == "Por ID":
                id_buscar = st.text_input("ID a buscar")
                if st.button("Buscar") and id_buscar:
                    try:
                        # Convertir a tipo apropiado
                        if df.index.dtype == 'int64':
                            id_buscar = int(id_buscar)
                        resultado = df.loc[[id_buscar]]
                        st.success("Encontrado:")
                        st.dataframe(resultado, use_container_width=True)
                    except:
                        st.warning("No se encontró el ID")
            
            elif tipo_busqueda == "Por columna":
                columnas_disponibles = list(df.columns)
                col_seleccionada = st.selectbox("Seleccione columna", columnas_disponibles)
                texto = st.text_input("Texto a buscar")
                if st.button("Buscar") and texto:
                    resultado = df[df[col_seleccionada].astype(str).str.contains(texto, case=False, na=False)]
                    if not resultado.empty:
                        st.success(f"Encontrados {len(resultado)} resultados:")
                        st.dataframe(resultado, use_container_width=True)
                    else:
                        st.warning("No se encontraron coincidencias")
            
            else:  # Texto libre
                texto = st.text_input("Buscar en todo el archivo")
                if st.button("Buscar") and texto:
                    resultado = df[df.apply(lambda row: row.astype(str).str.contains(texto, case=False, na=False).any(), axis=1)]
                    if not resultado.empty:
                        st.success(f"Encontrados {len(resultado)} resultados:")
                        st.dataframe(resultado, use_container_width=True)
                    else:
                        st.warning("No se encontraron coincidencias")
    else:
        st.warning("No hay archivos disponibles")

# ==================== CONVERTIR ====================
elif menu == "🔄 Convertir CSV/JSON":
    st.header("Conversión de Archivos")
    
    tipo_conv = st.radio("Tipo de conversión", ["CSV → JSON", "JSON → CSV"])
    
    if tipo_conv == "CSV → JSON":
        archivos = obtener_archivos_csv(CARPETA_BASE)
        if archivos:
            archivo = st.selectbox("Seleccione CSV", archivos)
            usar_mod = st.checkbox("Usar versión modificada")
            
            if st.button("Convertir a JSON"):
                ruta_json = csv_a_json(archivo, usar_mod)
                if ruta_json:
                    st.success(f"✅ Convertido: {ruta_json}")
                else:
                    st.error("Error en la conversión")
    
    else:  # JSON → CSV
        archivos_json = []
        for carpeta in [CARPETA_BASE, CARPETA_MODIFICADA]:
            if os.path.exists(carpeta):
                archivos_json.extend([os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith('.json')])
        
        if archivos_json:
            archivo_json = st.selectbox("Seleccione JSON", archivos_json)
            
            if st.button("Convertir a CSV"):
                ruta_csv = json_a_csv(archivo_json)
                if ruta_csv:
                    st.success(f"✅ Convertido: {ruta_csv}")
                else:
                    st.error("Error en la conversión")
        else:
            st.warning("No hay archivos JSON disponibles")

# ==================== COMPARAR ====================
elif menu == "📊 Comparar Versiones":
    st.header("Comparar Original vs Modificado")
    
    archivos_mod = []
    for arch in obtener_archivos_csv(CARPETA_BASE):
        if existe_modificado(arch):
            archivos_mod.append(arch)
    
    if archivos_mod:
        archivo = st.selectbox("Seleccione archivo", archivos_mod)
        
        if st.button("Comparar"):
            df_original = cargar_csv(archivo, usar_modificado=False)
            df_modificado = cargar_csv(archivo, usar_modificado=True)
            
            if df_original is not None and df_modificado is not None:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Original")
                    st.dataframe(df_original, use_container_width=True)
                    st.info(f"Filas: {len(df_original)}")
                
                with col2:
                    st.subheader("Modificado")
                    st.dataframe(df_modificado, use_container_width=True)
                    st.info(f"Filas: {len(df_modificado)}")
                
                # Análisis de diferencias
                st.markdown("### Análisis de cambios")
                
                ids_orig = set(df_original.index)
                ids_mod = set(df_modificado.index)
                
                nuevas = ids_mod - ids_orig
                eliminadas = ids_orig - ids_mod
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.metric("Filas añadidas", len(nuevas))
                    if nuevas:
                        st.write(sorted(nuevas))
                
                with col_b:
                    st.metric("Filas eliminadas", len(eliminadas))
                    if eliminadas:
                        st.write(sorted(eliminadas))
    else:
        st.warning("No hay archivos modificados para comparar")