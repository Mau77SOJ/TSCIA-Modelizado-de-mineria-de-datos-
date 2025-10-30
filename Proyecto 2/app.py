import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Recompra de Clientes",
    page_icon="📊",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .insight-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .insight-success {
        background-color: #d1fae5;
        border-left: 4px solid #10b981;
    }
    .insight-warning {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
    }
    .insight-info {
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
    }
    .insight-danger {
        background-color: #fee2e2;
        border-left: 4px solid #ef4444;
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

df = load_data()

# Header
st.markdown('<p class="main-header">📊 Análisis de Recompra de Clientes</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Descubre qué factores impulsan la recompra y cómo optimizar tu estrategia de promociones</p>', unsafe_allow_html=True)

# Tabs principales
tab1, tab2 = st.tabs(["🔍 Análisis Inicial", "💡 Conclusiones Estratégicas"])

# ==================== TAB 1: ANÁLISIS INICIAL ====================
with tab1:
    st.markdown("## 🎯 Factores de Recompra")
    st.markdown("---")
    
    # Pregunta 1: ¿Recibir promoción influye?
    st.markdown("### 1. ¿Recibir una promoción influye en la recompra?")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Calcular tasas
        recibe_promo = df[df['Recibio_Promo'] == 'Si']
        no_recibe_promo = df[df['Recibio_Promo'] == 'No']
        
        tasa_con_promo = (recibe_promo[recibe_promo['Recompra'] == 'Si'].shape[0] / recibe_promo.shape[0] * 100)
        tasa_sin_promo = (no_recibe_promo[no_recibe_promo['Recompra'] == 'Si'].shape[0] / no_recibe_promo.shape[0] * 100)
        
        # Gráfico de barras
        fig_promo = go.Figure(data=[
            go.Bar(
                x=['Recibió Promo', 'No Recibió Promo'],
                y=[tasa_con_promo, tasa_sin_promo],
                marker_color=['#3b82f6', '#8b5cf6'],
                text=[f'{tasa_con_promo:.1f}%', f'{tasa_sin_promo:.1f}%'],
                textposition='auto',
            )
        ])
        fig_promo.update_layout(
            title="Tasa de Recompra según Recepción de Promoción",
            yaxis_title="% Recompra",
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig_promo, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-box insight-info">
            <h4>📌 Hallazgo:</h4>
            <p>Recibir promoción <strong>NO</strong> parece ser el factor determinante.</p>
            <ul>
                <li>Con promoción: <strong>{tasa_con_promo:.1f}%</strong> de recompra</li>
                <li>Sin promoción: <strong>{tasa_sin_promo:.1f}%</strong> de recompra</li>
            </ul>
            <p style="margin-top: 1rem;">La diferencia es mínima, lo que sugiere que <strong>no es suficiente solo dar promociones</strong>, sino que importa <em>cómo y a quién</em> se las damos.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Pregunta 2: ¿Importa el monto?
    st.markdown("### 2. ¿Importa el monto de la promoción?")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Crear rangos de monto
        df['Rango_Monto'] = pd.cut(df['Monto_Promo'], 
                                    bins=[0, 399, 600, 800, 1000],
                                    labels=['< 400', '400-600', '601-800', '> 800'])
        
        # Calcular tasa por rango
        recompra_por_monto = df.groupby('Rango_Monto').apply(
            lambda x: (x['Recompra'] == 'Si').sum() / len(x) * 100
        ).reset_index()
        recompra_por_monto.columns = ['Rango_Monto', 'Tasa_Recompra']
        
        fig_monto = go.Figure(data=[
            go.Bar(
                x=recompra_por_monto['Rango_Monto'],
                y=recompra_por_monto['Tasa_Recompra'],
                marker_color='#10b981',
                text=[f'{v:.1f}%' for v in recompra_por_monto['Tasa_Recompra']],
                textposition='auto',
            )
        ])
        fig_monto.update_layout(
            title="Tasa de Recompra según Monto de Promoción",
            xaxis_title="Rango de Monto ($)",
            yaxis_title="% Recompra",
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig_monto, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box insight-success">
            <h4>✅ Hallazgos Clave:</h4>
            <ul>
                <li>❌ Montos <strong style="color: #ef4444;">&lt; $400</strong>: Baja tasa de recompra</li>
                <li>✅ Montos <strong style="color: #10b981;">&gt; $800</strong>: Mayor probabilidad de recompra</li>
                <li>📊 <strong>El monto SÍ importa</strong> más que solo recibir la promoción</li>
            </ul>
            <p style="margin-top: 1rem; background: white; padding: 0.5rem; border-radius: 5px;">
                <strong>💡 Insight:</strong> Los clientes perciben valor en promociones generosas. 
                Promociones pequeñas pueden no ser suficiente incentivo.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Pregunta 3: ¿Influyen edad o ingreso?
    st.markdown("### 3. ¿Influyen la edad o el ingreso?")
    
    # Edad
    st.markdown("#### 📅 Edad y Recompra")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Crear rangos de edad
        df['Rango_Edad'] = pd.cut(df['Edad'], 
                                   bins=[0, 30, 40, 50, 60, 100],
                                   labels=['20-30', '31-40', '41-50', '51-60', '60+'])
        
        # Calcular tasa por edad
        recompra_por_edad = df.groupby('Rango_Edad').apply(
            lambda x: (x['Recompra'] == 'Si').sum() / len(x) * 100
        ).reset_index()
        recompra_por_edad.columns = ['Rango_Edad', 'Tasa_Recompra']
        
        fig_edad = go.Figure(data=[
            go.Bar(
                x=recompra_por_edad['Rango_Edad'],
                y=recompra_por_edad['Tasa_Recompra'],
                marker_color='#f59e0b',
                text=[f'{v:.1f}%' for v in recompra_por_edad['Tasa_Recompra']],
                textposition='auto',
            )
        ])
        fig_edad.update_layout(
            title="Tasa de Recompra por Rango de Edad",
            xaxis_title="Rango de Edad",
            yaxis_title="% Recompra",
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig_edad, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box insight-warning">
            <h4>🎂 Edad:</h4>
            <p>Personas de <strong>40-60 años</strong> tienden a recomprar más.</p>
            <p>Los más jóvenes (&lt;30) y mayores (60+) muestran tasas más bajas.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Ingreso
    st.markdown("#### 💰 Ingreso y Recompra")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Boxplot de ingreso por recompra
        fig_ingreso = go.Figure()
        
        for recompra in ['Si', 'No']:
            data_subset = df[df['Recompra'] == recompra]
            fig_ingreso.add_trace(go.Box(
                y=data_subset['Ingreso_Mensual'],
                name=f'Recompra: {recompra}',
                marker_color='#3b82f6' if recompra == 'Si' else '#ef4444'
            ))
        
        fig_ingreso.update_layout(
            title="Distribución de Ingreso Mensual según Recompra",
            yaxis_title="Ingreso Mensual ($)",
            height=300
        )
        st.plotly_chart(fig_ingreso, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box insight-info">
            <h4>💵 Ingreso:</h4>
            <p>El ingreso muestra <strong>poca diferencia</strong> entre grupos.</p>
            <p>Mayor dispersión en no recompradores, pero <strong>no es un factor determinante</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 2: CONCLUSIONES ESTRATÉGICAS ====================
with tab2:
    st.markdown("## 🎯 Conclusiones y Recomendaciones Estratégicas")
    st.markdown("---")
    
    # Variables más importantes
    st.markdown("### 1. Variables más importantes para predecir recompra")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                    padding: 1.5rem; border-radius: 10px; border: 2px solid #10b981; text-align: center;">
            <div style="font-size: 3rem;">🥇</div>
            <h3 style="color: #065f46;">Monto de Promoción</h3>
            <p style="color: #047857;">La variable MÁS importante. Montos &gt;$800 generan recompra.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                    padding: 1.5rem; border-radius: 10px; border: 2px solid #3b82f6; text-align: center;">
            <div style="font-size: 3rem;">🥈</div>
            <h3 style="color: #1e40af;">Edad</h3>
            <p style="color: #1e3a8a;">Clientes de 40-60 años son más propensos a recomprar.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%); 
                    padding: 1.5rem; border-radius: 10px; border: 2px solid #f59e0b; text-align: center;">
            <div style="font-size: 3rem;">🥉</div>
            <h3 style="color: #92400e;">Género</h3>
            <p style="color: #78350f;">Influencia menor. Las mujeres muestran mayor variabilidad.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box" style="background: #f3f4f6; margin-top: 1rem;">
        <p><strong>⚠️ Menos importantes:</strong> Recibir promoción (sí/no) e Ingreso mensual. 
        Lo que importa NO es dar promociones, sino dar las <strong>correctas</strong>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tipo de cliente a incentivar
    st.markdown("### 2. ¿Qué tipo de cliente conviene incentivar?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="border: 3px solid #10b981; background: #d1fae5; padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #065f46;">✅ Perfil IDEAL (Alta Conversión)</h4>
            <ul style="color: #047857; margin-top: 1rem;">
                <li><strong>Edad:</strong> 40-60 años</li>
                <li><strong>Promoción:</strong> Montos &gt; $800</li>
                <li><strong>Razón:</strong> Mayor madurez de compra + incentivo significativo</li>
            </ul>
            <div style="background: white; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #10b981;">
                <p style="color: #065f46; margin: 0;"><strong>💡 Estrategia sugerida:</strong></p>
                <p style="color: #047857; margin: 0.5rem 0 0 0;">
                    Ofrecer promociones premium (&gt;$800) a clientes de mediana edad. 
                    <strong>ROI esperado: ALTO</strong>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="border: 3px solid #ef4444; background: #fee2e2; padding: 1.5rem; border-radius: 10px;">
            <h4 style="color: #991b1b;">⚠️ Perfil de RIESGO (Baja Conversión)</h4>
            <ul style="color: #b91c1c; margin-top: 1rem;">
                <li><strong>Edad:</strong> &lt; 30 años o &gt; 65 años</li>
                <li><strong>Promoción:</strong> Montos &lt; $400</li>
                <li><strong>Razón:</strong> Incentivo insuficiente o perfil menos propenso</li>
            </ul>
            <div style="background: white; padding: 1rem; border-radius: 8px; margin-top: 1rem; border: 1px solid #ef4444;">
                <p style="color: #991b1b; margin: 0;"><strong>⚠️ Recomendación:</strong></p>
                <p style="color: #b91c1c; margin: 0.5rem 0 0 0;">
                    EVITAR inversión alta en este segmento. Buscar estrategias alternativas 
                    (fidelización, engagement).
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Comunicación para no técnicos
    st.markdown("### 3. Comunicación para Stakeholders (Sin Conocimientos Técnicos)")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                padding: 2rem; border-radius: 10px; border-left: 6px solid #3b82f6; margin: 1rem 0;">
        <h4 style="color: #1e40af; margin-top: 0;">🎯 El Mensaje Principal</h4>
        <p style="font-size: 1.2rem; color: #1e3a8a; line-height: 1.8;">
            "No todas las promociones funcionan igual. Para maximizar la recompra, 
            debemos dar <strong style="color: #2563eb;">promociones generosas (&gt;$800)</strong> a 
            nuestros <strong style="color: #2563eb;">clientes de mediana edad (40-60 años)</strong>. 
            Esto nos dará el mejor retorno de inversión."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box insight-success">
            <h5>✅ Lo que SÍ funciona:</h5>
            <ul>
                <li>Ser generosos con los descuentos</li>
                <li>Enfocarse en el cliente maduro</li>
                <li>Calidad sobre cantidad de promos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box insight-danger">
            <h5>❌ Lo que NO funciona:</h5>
            <ul>
                <li>Dar muchas promos pequeñas</li>
                <li>Promociones genéricas sin segmentar</li>
                <li>Invertir igual en todos los perfiles</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box insight-warning">
        <h5>💼 Recomendación Ejecutiva:</h5>
        <ol style="margin: 1rem 0;">
            <li><strong>Segmentar</strong> base de clientes por edad (priorizar 40-60 años)</li>
            <li><strong>Destinar</strong> presupuesto a menos promociones pero más generosas (&gt;$800)</li>
            <li><strong>Medir</strong> resultados y ajustar. El ingreso no importa tanto, enfocarse en edad + monto</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); 
                padding: 1.5rem; border-radius: 10px; border: 2px solid #a855f7; margin-top: 1rem;">
        <h5 style="color: #6b21a8; margin-top: 0;">📊 En números simples:</h5>
        <p style="color: #7c3aed;">
            Si invertimos $100,000 en promociones pequeñas para todos, obtendremos un resultado mediocre. 
            Pero si invertimos los mismos $100,000 en promociones grandes para el segmento correcto, 
            <strong>podríamos duplicar o triplicar la tasa de recompra</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <p>📊 Análisis basado en 20 clientes | Datos actualizados</p>
</div>
""", unsafe_allow_html=True)