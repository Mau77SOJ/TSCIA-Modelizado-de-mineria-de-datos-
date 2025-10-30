import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Modelado Predictivo - Árbol de Decisión",
    page_icon="🌳",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #6b7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-box h3 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .metric-box p {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }
    .insight-box {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
    }
    .warning-box {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
    }
    .info-box {
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
    }
    .danger-box {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
    }
    .step-box {
        background: #f9fafb;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def load_data():
    data = {
        'Cliente_ID': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
        'Genero': ['F','M','F','M','M','M','F','F','F','F','F','M','F','M','M','F','M','F','F','M'],
        'Edad': [23,45,60,22,32,54,67,70,25,34,35,45,55,56,37,41,62,68,24,34],
        'Recibio_Promo': ['Si','Si','No','Si','Si','No','No','No','Si','Si','No','Si','No','No','No','Si','No','Si','No','No'],
        'Monto_Promo': [500,500,700,800,300,500,600,500,700,300,400,500,900,100,900,400,500,600,700,800],
        'Recompra': ['Si','Si','No','No','Si','Si','Si','No','No','No','Si','Si','Si','No','Si','No','Si','No','No','Si'],
        'Total_Compras': [2,2,3,1,2,3,5,2,3,4,1,2,3,6,4,1,3,2,4,3],
        'Ingreso_Mensual': [30000,40000,60000,30000,50000,30000,45000,55000,30000,25000,30000,60000,50000,40000,55000,65000,30000,25000,50000,60000]
    }
    return pd.DataFrame(data)

@st.cache_resource
def train_model(df):
    # Codificar variables categóricas
    le_genero = LabelEncoder()
    le_promo = LabelEncoder()
    
    df_copy = df.copy()
    df_copy['Genero_Cod'] = le_genero.fit_transform(df_copy['Genero'])
    df_copy['Recibio_Promo_Cod'] = le_promo.fit_transform(df_copy['Recibio_Promo'])
    
    # Features y target
    features = ['Genero_Cod', 'Edad', 'Recibio_Promo_Cod', 'Monto_Promo', 'Total_Compras', 'Ingreso_Mensual']
    X = df_copy[features]
    y = df_copy['Recompra']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Entrenar modelo
    modelo = DecisionTreeClassifier(max_depth=3, min_samples_split=2, random_state=42)
    modelo.fit(X_train, y_train)
    
    # Predicciones
    y_pred = modelo.predict(X_test)
    y_pred_proba = modelo.predict_proba(X_test)
    
    return modelo, X_train, X_test, y_train, y_test, y_pred, y_pred_proba, features

# Header
st.markdown('<p class="main-header">🌳 Modelado Predictivo - Árbol de Decisión</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Predicción de Recompra de Clientes usando Machine Learning</p>', unsafe_allow_html=True)

# Cargar datos y entrenar modelo
df = load_data()
modelo, X_train, X_test, y_train, y_test, y_pred, y_pred_proba, features = train_model(df)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 1. Datos", 
    "🎓 2. Entrenamiento", 
    "🔮 3. Predicciones", 
    "📈 4. Evaluación",
    "🎯 5. Conclusiones"
])

# ==================== TAB 1: DATOS ====================
with tab1:
    st.markdown("## 📋 Exploración de Datos")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <h3>{len(df)}</h3>
            <p>Total Clientes</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <h3>{(df['Recompra'] == 'Si').sum()}</h3>
            <p>Recompraron</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-box">
            <h3>{(df['Recompra'] == 'No').sum()}</h3>
            <p>No Recompraron</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Dataset Completo")
        st.dataframe(df, use_container_width=True, height=400)
    
    with col2:
        st.markdown("### 🎯 Distribución de Recompra")
        
        # Gráfico de torta
        recompra_counts = df['Recompra'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=recompra_counts.index,
            values=recompra_counts.values,
            marker=dict(colors=['#ef4444', '#10b981']),
            hole=0.4
        )])
        fig.update_layout(
            title="Proporción de Recompra",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Información
        st.markdown(f"""
        <div class="insight-box info-box">
            <h4>📌 Balance de Clases</h4>
            <ul>
                <li>Recompra SÍ: <strong>{(df['Recompra'] == 'Si').sum()} ({(df['Recompra'] == 'Si').sum()/len(df)*100:.1f}%)</strong></li>
                <li>Recompra NO: <strong>{(df['Recompra'] == 'No').sum()} ({(df['Recompra'] == 'No').sum()/len(df)*100:.1f}%)</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 2: ENTRENAMIENTO ====================
with tab2:
    st.markdown("## 🎓 Entrenamiento del Modelo")
    
    st.markdown("""
    <div class="step-box">
        <h3>📚 ¿Qué es el Entrenamiento?</h3>
        <p>El modelo <strong>aprende patrones</strong> de los datos históricos para predecir si un cliente recomprará o no.</p>
        <p>Dividimos los datos en:</p>
        <ul>
            <li><strong>Entrenamiento (80%):</strong> El modelo aprende de estos datos</li>
            <li><strong>Prueba (20%):</strong> Evaluamos qué tan bien aprendió</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);">
            <h3>{len(X_train)}</h3>
            <p>Datos de Entrenamiento (80%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
            <h3>{len(X_test)}</h3>
            <p>Datos de Prueba (20%)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Importancia de las Variables")
    st.markdown("**¿Qué variables usa el modelo para tomar decisiones?**")
    
    # Calcular importancias
    feature_names = ['Género', 'Edad', 'Recibió Promo', 'Monto Promo', 'Total Compras', 'Ingreso Mensual']
    importancias = pd.DataFrame({
        'Variable': feature_names,
        'Importancia': modelo.feature_importances_
    }).sort_values('Importancia', ascending=True)
    
    fig = go.Figure(go.Bar(
        x=importancias['Importancia'],
        y=importancias['Variable'],
        orientation='h',
        marker=dict(
            color=importancias['Importancia'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Importancia")
        ),
        text=[f'{v:.3f}' for v in importancias['Importancia']],
        textposition='auto'
    ))
    fig.update_layout(
        title="Importancia de las Variables en el Modelo",
        xaxis_title="Importancia (Mayor = Más Influyente)",
        yaxis_title="",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top 3 variables
    top3 = importancias.sort_values('Importancia', ascending=False).head(3)
    st.markdown(f"""
    <div class="insight-box success-box">
        <h4>🥇 Top 3 Variables Más Importantes:</h4>
        <ol>
            <li><strong>{top3.iloc[0]['Variable']}</strong>: {top3.iloc[0]['Importancia']:.3f}</li>
            <li><strong>{top3.iloc[1]['Variable']}</strong>: {top3.iloc[1]['Importancia']:.3f}</li>
            <li><strong>{top3.iloc[2]['Variable']}</strong>: {top3.iloc[2]['Importancia']:.3f}</li>
        </ol>
        <p style="margin-top: 1rem;">Estas son las variables que más influyen en la decisión del modelo.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visualizar el árbol
    st.markdown("### 🌳 Visualización del Árbol de Decisión")
    st.markdown("**El árbol muestra las reglas que usa el modelo para clasificar:**")
    
    fig, ax = plt.subplots(figsize=(20, 10))
    plot_tree(modelo, 
              feature_names=feature_names,
              class_names=['No', 'Si'],
              filled=True,
              rounded=True,
              fontsize=10,
              ax=ax)
    plt.title('Árbol de Decisión - Reglas de Clasificación', fontsize=16, fontweight='bold', pad=20)
    st.pyplot(fig)
    
    st.markdown("""
    <div class="insight-box info-box">
        <h4>📖 Cómo Leer el Árbol:</h4>
        <ul>
            <li><strong>Nodos (cajas):</strong> Cada caja representa una pregunta/regla</li>
            <li><strong>Colores:</strong> Naranja = "No recompra", Verde = "Sí recompra"</li>
            <li><strong>Intensidad del color:</strong> Más intenso = más confianza en la predicción</li>
            <li><strong>Valores en cada nodo:</strong>
                <ul>
                    <li><em>samples</em>: Cantidad de clientes en ese nodo</li>
                    <li><em>value</em>: [No recompra, Sí recompra]</li>
                    <li><em>class</em>: Predicción final del nodo</li>
                </ul>
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== TAB 3: PREDICCIONES ====================
with tab3:
    st.markdown("## 🔮 Predicciones del Modelo")
    
    st.markdown("""
    <div class="step-box">
        <h3>🎯 ¿Qué son las Predicciones?</h3>
        <p>El modelo usa lo que aprendió para <strong>predecir si cada cliente recomprará o no</strong>.</p>
        <p>Además, nos da la <strong>confianza</strong> (probabilidad) de cada predicción.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear DataFrame de resultados
    resultados = pd.DataFrame({
        'Cliente_ID': df.loc[X_test.index, 'Cliente_ID'].values,
        'Edad': df.loc[X_test.index, 'Edad'].values,
        'Monto_Promo': df.loc[X_test.index, 'Monto_Promo'].values,
        'Real': y_test.values,
        'Predicho': y_pred,
        'Prob_No': y_pred_proba[:, 0],
        'Prob_Si': y_pred_proba[:, 1],
        'Acierto': ['✅ Correcto' if r == p else '❌ Error' for r, p in zip(y_test.values, y_pred)]
    })
    resultados['Confianza'] = resultados.apply(lambda row: max(row['Prob_No'], row['Prob_Si']), axis=1)
    
    st.markdown("### 📋 Tabla de Predicciones")
    
    # Estilizar DataFrame
    def color_acierto(val):
        if '✅' in val:
            return 'background-color: #d1fae5'
        else:
            return 'background-color: #fee2e2'
    
    styled_df = resultados.style.applymap(color_acierto, subset=['Acierto'])
    st.dataframe(styled_df, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Real vs Predicho")
        
        # Gráfico de comparación
        fig = go.Figure()
        
        x_pos = list(range(len(resultados)))
        real_encoded = [1 if val == 'Si' else 0 for val in resultados['Real']]
        pred_encoded = [1 if val == 'Si' else 0 for val in resultados['Predicho']]
        
        fig.add_trace(go.Bar(
            x=resultados['Cliente_ID'],
            y=real_encoded,
            name='Real',
            marker_color='#3b82f6',
            opacity=0.7
        ))
        
        fig.add_trace(go.Bar(
            x=resultados['Cliente_ID'],
            y=pred_encoded,
            name='Predicho',
            marker_color='#f59e0b',
            opacity=0.7
        ))
        
        fig.update_layout(
            title="Comparación: Valores Reales vs Predichos",
            xaxis_title="Cliente ID",
            yaxis_title="Recompra (0=No, 1=Si)",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎲 Confianza del Modelo")
        
        # Gráfico de confianza
        colors_conf = ['#10b981' if '✅' in a else '#ef4444' for a in resultados['Acierto']]
        
        fig = go.Figure(go.Bar(
            x=resultados['Cliente_ID'],
            y=resultados['Confianza'],
            marker_color=colors_conf,
            text=[f'{v:.1%}' for v in resultados['Confianza']],
            textposition='auto'
        ))
        
        fig.add_hline(y=0.5, line_dash="dash", line_color="gray", 
                      annotation_text="50% (Umbral de decisión)")
        
        fig.update_layout(
            title="Confianza de cada Predicción (Verde=Acierto, Rojo=Error)",
            xaxis_title="Cliente ID",
            yaxis_title="Confianza",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Resumen
    aciertos = (resultados['Real'] == resultados['Predicho']).sum()
    st.markdown(f"""
    <div class="insight-box success-box">
        <h4>✅ Resumen de Predicciones</h4>
        <ul>
            <li><strong>Total de predicciones:</strong> {len(resultados)}</li>
            <li><strong>Aciertos:</strong> {aciertos} ({aciertos/len(resultados)*100:.1f}%)</li>
            <li><strong>Errores:</strong> {len(resultados) - aciertos} ({(len(resultados) - aciertos)/len(resultados)*100:.1f}%)</li>
            <li><strong>Confianza promedio:</strong> {resultados['Confianza'].mean():.1%}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==================== TAB 4: EVALUACIÓN ====================
with tab4:
    st.markdown("## 📈 Evaluación del Modelo")
    
    # Calcular métricas
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred, labels=['No', 'Si'])
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
            <h3>{accuracy:.1%}</h3>
            <p>Accuracy (Precisión)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        vp = cm[1,1]
        fn = cm[1,0]
        recall = vp / (vp + fn) if (vp + fn) > 0 else 0
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);">
            <h3>{recall:.1%}</h3>
            <p>Recall (Sensibilidad)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        vp = cm[1,1]
        fp = cm[0,1]
        precision = vp / (vp + fp) if (vp + fp) > 0 else 0
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
            <h3>{precision:.1%}</h3>
            <p>Precision</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Matriz de Confusión")
        
        # Heatmap de matriz de confusión
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=['No', 'Si'],
            y=['No', 'Si'],
            text=cm,
            texttemplate='%{text}',
            textfont={"size": 20},
            colorscale='Blues',
            showscale=True
        ))
        
        fig.update_layout(
            title=f"Matriz de Confusión (Accuracy: {accuracy:.1%})",
            xaxis_title="Predicción",
            yaxis_title="Real",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Explicación
        st.markdown(f"""
        <div class="insight-box info-box">
            <h4>📖 Interpretación:</h4>
            <ul>
                <li><strong>VN (Verdaderos Negativos):</strong> {cm[0,0]} - Predijo "No" y era "No" ✅</li>
                <li><strong>FP (Falsos Positivos):</strong> {cm[0,1]} - Predijo "Si" pero era "No" ❌</li>
                <li><strong>FN (Falsos Negativos):</strong> {cm[1,0]} - Predijo "No" pero era "Si" ❌</li>
                <li><strong>VP (Verdaderos Positivos):</strong> {cm[1,1]} - Predijo "Si" y era "Si" ✅</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📋 Reporte de Clasificación")
        
        # Generar reporte
        report = classification_report(y_test, y_pred, target_names=['No Recompra', 'Recompra'], output_dict=True)
        
        report_df = pd.DataFrame({
            'Clase': ['No Recompra', 'Recompra'],
            'Precision': [report['No Recompra']['precision'], report['Recompra']['precision']],
            'Recall': [report['No Recompra']['recall'], report['Recompra']['recall']],
            'F1-Score': [report['No Recompra']['f1-score'], report['Recompra']['f1-score']],
            'Support': [report['No Recompra']['support'], report['Recompra']['support']]
        })
        
        st.dataframe(report_df.style.format({
            'Precision': '{:.2%}',
            'Recall': '{:.2%}',
            'F1-Score': '{:.2%}',
            'Support': '{:.0f}'
        }), use_container_width=True)
        
        # Explicación de métricas
        st.markdown("""
        <div class="insight-box warning-box">
            <h4>💡 ¿Qué significa cada métrica?</h4>
            <ul>
                <li><strong>Precision:</strong> De los que predije como "Sí", ¿cuántos acerté?</li>
                <li><strong>Recall:</strong> De los que realmente son "Sí", ¿cuántos encontré?</li>
                <li><strong>F1-Score:</strong> Balance entre Precision y Recall (0-1, mejor=1)</li>
                <li><strong>Support:</strong> Cantidad de casos reales en cada categoría</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 5: CONCLUSIONES ====================
with tab5:
    st.markdown("## 🎯 Conclusiones y Recomendaciones")
    
    # Resumen del modelo
    top_var = importancias.sort_values('Importancia', ascending=False).iloc[0]
    
    st.markdown(f"""
    <div class="insight-box" style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border-left: 6px solid #3b82f6;">
        <h3 style="color: #1e40af; margin-top: 0;">📌 RESUMEN DEL MODELO</h3>
        <ul style="font-size: 1.1rem; color: #1e3a8a;">
            <li><strong>Accuracy:</strong> {accuracy:.1%} - El modelo acierta en {accuracy:.1%} de los casos</li>
            <li><strong>Variable más importante:</strong> {top_var['Variable']} (Importancia: {top_var['Importancia']:.3f})</li>
            <li><strong>Aciertos:</strong> {(y_pred == y_test).sum()}/{len(y_test)} predicciones correctas</li>
            <li><strong>Confianza promedio:</strong> {resultados['Confianza'].mean():.1%}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Interpretación
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box success-box">
            <h4>✅ Fortalezas del Modelo</h4>
            <ul>
                <li>Identifica patrones claros en los datos</li>
                <li>Fácil de interpretar (árbol de decisión)</li>
                <li>Útil para segmentación de clientes</li>
                <li>Puede mejorar decisiones de marketing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box warning-box">
            <h4>⚠️ Limitaciones</h4>
            <ul>
                <li>Dataset pequeño (20 clientes)</li>
                <li>Puede haber overfitting</li>
                <li>Se recomienda validar con más datos</li>
                <li>Los resultados pueden variar</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Aplicación práctica
    st.markdown("""
    <div class="insight-box" style="background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); border-left: 6px solid #a855f7;">
        <h3 style="color: #6b21a8; margin-top: 0;">🚀 APLICACIÓN PRÁCTICA</h3>
        <h4 style="color: #7c3aed;">Este modelo puede usarse para:</h4>
        <ol style="font-size: 1.05rem; color: #7c3aed;">
            <li><strong>Identificar clientes con alta probabilidad de recompra</strong>
                <ul>
                    <li>Focalizar esfuerzos de marketing en los más prometedores</li>
                </ul>
            </li>
            <li><strong>Optimizar inversión en promociones</strong>
                <ul>
                    <li>No todas las promociones funcionan igual</li>
                    <li>Invertir en las que tienen más probabilidad de éxito</li>
                </ul>
            </li>
            <li><strong>Segmentar estrategias de marketing</strong>
                <ul>
                    <li>Diferentes mensajes para diferentes perfiles</li>
                    <li>Personalizar ofertas según características del cliente</li>
                </ul>
            </li>
            <li><strong>Predecir comportamiento de nuevos clientes</strong>
                <ul>
                    <li>Evaluar el potencial de recompra antes de invertir</li>
                </ul>
            </li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recomendaciones estratégicas
    st.markdown("""
    <div class="insight-box" style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border-left: 6px solid #10b981;">
        <h3 style="color: #065f46; margin-top: 0;">💼 RECOMENDACIONES ESTRATÉGICAS</h3>
    </div>
    """, unsafe_allow_html=True)
    
    rec1, rec2, rec3 = st.columns(3)
    
    with rec1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 8px; border: 2px solid #10b981; height: 100%;">
            <h4 style="color: #065f46;">🎯 Corto Plazo</h4>
            <ul style="color: #047857;">
                <li>Aplicar el modelo a la base actual</li>
                <li>Identificar clientes de alto potencial</li>
                <li>Diseñar campañas segmentadas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with rec2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 8px; border: 2px solid #3b82f6; height: 100%;">
            <h4 style="color: #1e40af;">📈 Mediano Plazo</h4>
            <ul style="color: #1e3a8a;">
                <li>Recopilar más datos</li>
                <li>Re-entrenar el modelo</li>
                <li>Validar con datos nuevos</li>
                <li>Ajustar estrategias según resultados</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with rec3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 8px; border: 2px solid #f59e0b; height: 100%;">
            <h4 style="color: #92400e;">🚀 Largo Plazo</h4>
            <ul style="color: #78350f;">
                <li>Implementar sistema predictivo</li>
                <li>Automatizar segmentación</li>
                <li>Integrar con CRM</li>
                <li>Escalar a toda la base</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Ejemplo práctico
    st.markdown("### 🧪 Simulador: Predecir un Nuevo Cliente")
    st.markdown("**Prueba el modelo con diferentes características:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        genero_sim = st.selectbox("Género", ["Femenino", "Masculino"], key="sim_genero")
        edad_sim = st.slider("Edad", 18, 80, 40, key="sim_edad")
        recibio_promo_sim = st.selectbox("Recibió Promoción", ["Sí", "No"], key="sim_promo")
    
    with col2:
        monto_promo_sim = st.slider("Monto de Promoción ($)", 0, 1000, 500, 50, key="sim_monto")
        total_compras_sim = st.slider("Total de Compras", 1, 10, 3, key="sim_compras")
        ingreso_sim = st.slider("Ingreso Mensual ($)", 20000, 80000, 40000, 5000, key="sim_ingreso")
    
    if st.button("🔮 Predecir Recompra", type="primary"):
        # Preparar datos
        genero_cod = 0 if genero_sim == "Femenino" else 1
        recibio_promo_cod = 0 if recibio_promo_sim == "No" else 1
        
        nuevo_cliente = np.array([[genero_cod, edad_sim, recibio_promo_cod, 
                                   monto_promo_sim, total_compras_sim, ingreso_sim]])
        
        # Predecir
        prediccion = modelo.predict(nuevo_cliente)[0]
        probabilidad = modelo.predict_proba(nuevo_cliente)[0]
        
        prob_no = probabilidad[0]
        prob_si = probabilidad[1]
        confianza = max(prob_no, prob_si)
        
        # Mostrar resultado
        if prediccion == "Si":
            st.markdown(f"""
            <div class="insight-box success-box" style="text-align: center; font-size: 1.2rem;">
                <h2 style="color: #065f46; margin: 0;">✅ PREDICCIÓN: SÍ RECOMPRARÁ</h2>
                <p style="font-size: 2rem; margin: 1rem 0; color: #10b981; font-weight: bold;">
                    {prob_si:.1%}
                </p>
                <p style="color: #047857; margin: 0;">Probabilidad de Recompra</p>
                <hr style="border-color: #10b981;">
                <p style="color: #047857; margin-top: 1rem;">
                    <strong>Recomendación:</strong> Este cliente es un buen candidato para inversión en marketing.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="insight-box danger-box" style="text-align: center; font-size: 1.2rem;">
                <h2 style="color: #991b1b; margin: 0;">❌ PREDICCIÓN: NO RECOMPRARÁ</h2>
                <p style="font-size: 2rem; margin: 1rem 0; color: #ef4444; font-weight: bold;">
                    {prob_no:.1%}
                </p>
                <p style="color: #b91c1c; margin: 0;">Probabilidad de NO Recompra</p>
                <hr style="border-color: #ef4444;">
                <p style="color: #b91c1c; margin-top: 1rem;">
                    <strong>Recomendación:</strong> Considerar estrategias alternativas o ajustar la oferta.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Mostrar probabilidades detalladas
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Probabilidad NO Recompra", f"{prob_no:.1%}")
        with col_b:
            st.metric("Probabilidad SÍ Recompra", f"{prob_si:.1%}")
    
    st.markdown("---")
    
    # Mensaje final
    st.markdown("""
    <div class="insight-box" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-left: 6px solid #f59e0b;">
        <h3 style="color: #92400e; margin-top: 0;">⚡ CONCLUSIÓN FINAL</h3>
        <p style="font-size: 1.1rem; color: #78350f; line-height: 1.8;">
            El modelo de <strong>Árbol de Decisión</strong> nos permite predecir la recompra con un <strong>accuracy del {:.1%}</strong>.
            Aunque el dataset es pequeño, los insights son valiosos para orientar decisiones de marketing.
            <br><br>
            <strong>Próximos pasos:</strong> Recopilar más datos, validar el modelo con nuevos clientes y ajustar 
            las estrategias de promoción basándose en las predicciones del modelo.
        </p>
    </div>
    """.format(accuracy), unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <p>🌳 Modelo: Árbol de Decisión | 📊 Datos: 20 clientes | ✅ Accuracy: {:.1%}</p>
    <p style="font-size: 0.9rem; margin-top: 0.5rem;">
        Desarrollado con Streamlit, scikit-learn y Plotly
    </p>
</div>
""".format(accuracy), unsafe_allow_html=True)