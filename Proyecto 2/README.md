# 📊 Proyecto de Análisis de Recompra de Clientes

## 🎯 Descripción del Proyecto

Este proyecto analiza el comportamiento de recompra de clientes utilizando técnicas de análisis exploratorio de datos (EDA) y modelado predictivo con Machine Learning. El objetivo es identificar qué factores influyen en la decisión de recompra y desarrollar un modelo predictivo para optimizar estrategias de marketing.

---

## 📁 Estructura del Proyecto

```
PROYECTO 2/
│
├── modelo_predictivo/
│   ├── app.py                              # Aplicación principal de Streamlit
│   ├── anexo_1.py                          # Página de análisis inicial
│   └── anexo_2.py                          # Página de modelo predictivo
│
├── Mini_Proyecto_Clientes_Pro...xlsx       # Dataset original (Excel)
├── Ejercicio_Minería_Datos.docx           # Documentación del ejercicio
└── notebook.ipynb                          # Análisis exploratorio (EDA)
```

---

## 📄 Descripción de Archivos

### 📓 **notebook.ipynb**
Jupyter Notebook con el análisis exploratorio de datos (EDA) inicial.

**Contenido:**
- 🔍 Carga y limpieza de datos
- 📊 Análisis descriptivo de variables
- 📈 Visualizaciones exploratorias:
  - Distribución de recompra por género y edad
  - Relación entre monto de promoción y recompra
  - Impacto del ingreso mensual
  - Análisis de correlaciones
- 💡 Hallazgos preliminares y patrones identificados

**Hallazgos clave documentados:**
- Clientes con montos promocionales < $400 tienen menor probabilidad de recompra
- Montos > $800 aumentan significativamente la tasa de recompra
- La edad (40-60 años) muestra influencia en la recompra
- El ingreso mensual tiene menor impacto del esperado

---

### 📊 **Mini_Proyecto_Clientes_Pro...xlsx**
Archivo Excel original con los datos de clientes.

**Estructura de datos:**
- `Cliente_ID`: Identificador único del cliente
- `Genero`: Género del cliente (F/M)
- `Edad`: Edad del cliente
- `Recibio_Promo`: Si recibió promoción (Si/No)
- `Monto_Promo`: Monto de la promoción en pesos
- `Recompra`: Variable objetivo - Si recompró o no (Si/No)
- `Total_Compras`: Número total de compras realizadas
- `Ingreso_Mensual`: Ingreso mensual del cliente

**Total de registros:** 20 clientes

---

### 🌐 **modelo_predictivo/app.py**
Aplicación principal de Streamlit que sirve como punto de entrada del proyecto.

**Funcionalidad:**
- 🏠 Página de inicio con navegación
- 🔗 Integración de las páginas de análisis (anexo_1 y anexo_2)
- 📱 Interfaz responsiva y moderna
- 🎨 Diseño con CSS personalizado

**Tecnologías:**
- Streamlit
- Pandas
- Plotly

---

### 📈 **modelo_predictivo/anexo_1.py**
Página de Streamlit con el análisis inicial y visualizaciones interactivas.

**Secciones:**
1. **Análisis Inicial:**
   - ¿Recibir una promoción influye en la recompra?
   - ¿Importa el monto de la promoción?
   - ¿Influyen la edad o el ingreso?

2. **Visualizaciones incluidas:**
   - 📊 Tasa de recompra por recepción de promoción
   - 💰 Análisis de recompra por rangos de monto
   - 👥 Distribución por edad y género
   - 💵 Boxplots de ingreso vs recompra

3. **Conclusiones Estratégicas:**
   - Variables más importantes para predecir recompra
   - Perfil de cliente ideal vs perfil de riesgo
   - Recomendaciones para stakeholders
   - Mensaje ejecutivo simplificado

**Tecnologías:**
- Streamlit
- Plotly para gráficos interactivos
- Pandas para análisis de datos

---

### 🤖 **modelo_predictivo/anexo_2.py**
Página de Streamlit con el modelado predictivo completo.

**Secciones:**
1. **📊 Exploración de Datos:**
   - Vista del dataset completo
   - Distribución de la variable objetivo
   - Balance de clases

2. **🎓 Entrenamiento del Modelo:**
   - División train/test (80/20)
   - Árbol de Decisión (Decision Tree Classifier)
   - Importancia de variables
   - Visualización del árbol completo

3. **🔮 Predicciones:**
   - Tabla detallada de predicciones
   - Comparación Real vs Predicho
   - Niveles de confianza del modelo
   - Análisis cliente por cliente

4. **📈 Evaluación del Modelo:**
   - Accuracy, Precision, Recall
   - Matriz de confusión interactiva
   - Reporte de clasificación completo
   - Explicación de métricas

5. **🎯 Conclusiones:**
   - Resumen del rendimiento del modelo
   - Aplicaciones prácticas
   - Recomendaciones estratégicas (corto, mediano, largo plazo)
   - **Simulador interactivo**: Predice nuevos clientes en tiempo real

**Algoritmo utilizado:**
- **Decision Tree Classifier** (Árbol de Decisión)
  - `max_depth=3`: Profundidad máxima para evitar overfitting
  - `random_state=42`: Reproducibilidad
  - Fácil interpretación y visualización

**Tecnologías:**
- Streamlit
- scikit-learn (sklearn)
- Plotly
- Matplotlib
- Pandas y NumPy

---

### 📝 **Ejercicio_Minería_Datos.docx**
Documento con las especificaciones y requerimientos del proyecto.

**Contiene:**
- Objetivos del análisis
- Preguntas de investigación
- Metodología sugerida
- Criterios de evaluación

---

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 1. Instalar Dependencias

```bash
pip install streamlit pandas numpy plotly scikit-learn matplotlib seaborn openpyxl
```

### 2. Ejecutar el Análisis Exploratorio (Notebook)

```bash
jupyter notebook notebook.ipynb
```

### 3. Ejecutar las Aplicaciones Streamlit

**Opción A: Análisis Inicial**
```bash
cd modelo_predictivo
streamlit run anexo_1.py
```

**Opción B: Modelo Predictivo**
```bash
cd modelo_predictivo
streamlit run anexo_2.py
```

**Opción C: Aplicación Principal (si está configurada)**
```bash
cd modelo_predictivo
streamlit run app.py
```

---

## 📊 Flujo de Trabajo Recomendado

1. **📓 Notebook (notebook.ipynb)**
   - Comienza aquí para entender los datos
   - Realiza el análisis exploratorio
   - Identifica patrones y relaciones

2. **📈 Análisis Inicial (anexo_1.py)**
   - Visualiza los hallazgos del notebook
   - Responde preguntas de negocio
   - Obtén conclusiones estratégicas

3. **🤖 Modelo Predictivo (anexo_2.py)**
   - Entrena el modelo de clasificación
   - Evalúa el rendimiento
   - Utiliza el simulador para predecir nuevos clientes

---

## 🎯 Resultados Clave

### Variables Más Importantes:
1. 🥇 **Monto de Promoción**: Factor más influyente
2. 🥈 **Edad**: Clientes de 40-60 años recompran más
3. 🥉 **Género**: Influencia menor

### Perfil de Cliente Ideal:
- ✅ Edad: 40-60 años
- ✅ Monto de promoción: > $800
- ✅ ROI esperado: ALTO

### Rendimiento del Modelo:
- 🎯 Accuracy: Varía según la ejecución (dataset pequeño)
- 📊 Interpretabilidad: Excelente (árbol de decisión)
- 💡 Utilidad: Identificación de clientes de alto potencial

---

## ⚠️ Limitaciones

- **Dataset pequeño:** Solo 20 clientes (resultados pueden variar)
- **Validación limitada:** Se recomienda validar con más datos
- **Generalización:** Los resultados son específicos a este dataset

---

## 🔮 Próximos Pasos

1. **Corto Plazo:**
   - Aplicar el modelo a la base actual
   - Identificar clientes de alto potencial
   - Diseñar campañas segmentadas

2. **Mediano Plazo:**
   - Recopilar más datos
   - Re-entrenar y validar el modelo
   - Ajustar estrategias según resultados

3. **Largo Plazo:**
   - Implementar sistema predictivo automatizado
   - Integrar con CRM
   - Escalar a toda la base de clientes

---

## 👨‍💻 Tecnologías Utilizadas

- **Python 3.8+**
- **Jupyter Notebook**: Análisis exploratorio
- **Streamlit**: Aplicaciones web interactivas
- **Pandas**: Manipulación de datos
- **NumPy**: Cálculos numéricos
- **Plotly**: Visualizaciones interactivas
- **Matplotlib/Seaborn**: Visualizaciones estáticas
- **scikit-learn**: Machine Learning (Árbol de Decisión)