import streamlit as st
import plotly.graph_objects as go
import time
import random
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA
import warnings
import base64

warnings.filterwarnings("ignore")

# Configuración de la página
st.set_page_config(
    page_title="Risk Analytics Dashboard",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS PERSONALIZADO (OPTIMIZADO PARA COMMUNITY CLOUD)
# ==========================================
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit - VERSIÓN SEGURA */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    
    /* IMPORTANTE: Eliminar 'fixed' y 'absolute' problemáticos para Community Cloud */
    .block-container {
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
        max-width: 100% !important;
    }
    
    /* Fondo del dashboard - VERSIÓN SEGURA */
    .stApp {
        background: #0f172a !important;
        min-height: 100vh !important;
    }
    
    /* Contenedor principal - ELIMINADO position: fixed/absolute */
    .main-content {
        background: #0f172a;
        padding: 0rem 1.5rem;
        margin: 0 auto;
        max-width: 100%;
        position: relative !important; /* Cambiado de fixed a relative */
    }
    
    /* Título principal de Riesgo */
    .risk-title {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin-bottom: 0.5rem !important;
        text-align: center !important;
        letter-spacing: 2px !important;
        padding-top: 1.5rem !important;
    }
    
    /* Subtítulo de Riesgo */
    .risk-subtitle {
        color: #94a3b8 !important;
        font-size: 14px !important;
        letter-spacing: 4px !important;
        text-align: center !important;
        margin-bottom: 2.5rem !important;
        text-transform: uppercase !important;
    }
    
    /* Tarjetas de métricas */
    .metric-card-risk {
        background: linear-gradient(135deg, #0b1228 0%, #101f3d 100%) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
        height: 100% !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        margin-bottom: 1rem !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    
    .metric-card-risk:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Títulos de secciones */
    .section-title {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
        padding-left: 1rem !important;
        border-left: 4px solid #00ffff !important;
    }
    
    /* Gráficos */
    div.stPlotlyChart {
        border-radius: 12px !important;
        box-shadow: 0 6px 20px 0 rgba(0,0,0,0.3) !important;
        background-color: #0b1228 !important;
        padding: 15px !important;
        margin-bottom: 1.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        height: 320px !important;
    }
    
    /* Títulos de gráficos */
    h4 {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 1rem !important;
        text-align: center !important;
        padding: 0.5rem !important;
        background: rgba(0, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    
    /* Separadores */
    hr {
        margin: 2.5rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.3), transparent) !important;
    }
    
    /* Mejor espaciado en columnas */
    .stColumn {
        padding: 0 0.75rem !important;
    }
    
    /* Botones */
    .stButton > button {
        width: 100% !important;
        height: 48px !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    /* Tabla */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Upload box - REVISADO para Community Cloud */
    .upload-box {
        background-color: #1e293b !important;
        border: 2px dashed #00ffff !important;
        border-radius: 12px !important;
        padding: 2.5rem !important;
        text-align: center !important;
        margin: 1rem auto 2rem auto !important;
        transition: all 0.3s ease !important;
        max-width: 600px !important;
    }
    
    .upload-box:hover {
        background-color: #1e293b !important;
        border-color: #00ffff !important;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.3) !important;
    }
    
    /* Título intuitivo para cargar CSV */
    .upload-title {
        font-size: 20px !important;
        font-weight: 600 !important;
        color: #00ffff !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
        padding: 0.5rem !important;
        letter-spacing: 1px !important;
    }
    
    /* IMPORTANTE: ELIMINADO el iframe problemático para Community Cloud */
    /* Se reemplaza por un div normal */
    .threejs-container {
        width: 100% !important;
        height: 100vh !important;
        border: none !important;
        background: #000000 !important;
        position: relative !important; /* Cambiado de fixed a relative */
        top: 0 !important;
        left: 0 !important;
    }
    
    /* TRUCO DEL BOTÓN FANTASMA - MEJORADO */
    .ghost-button-container {
        position: absolute !important;
        opacity: 0 !important;
        z-index: -9999 !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
    }
    
    /* Footer */
    .dashboard-footer {
        text-align: center !important;
        margin-top: 4rem !important;
        padding: 2rem !important;
        color: #64748b !important;
        font-size: 14px !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Botón de portal mejorado */
    .portal-button {
        background: linear-gradient(135deg, #00ffff 0%, #0099cc 100%) !important;
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 18px !important;
        letter-spacing: 1px !important;
        padding: 15px 40px !important;
        border-radius: 30px !important;
        border: none !important;
        cursor: pointer !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5) !important;
        transition: all 0.3s ease !important;
        margin: 20px auto !important;
        display: block !important;
    }
    
    .portal-button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.8) !important;
    }
    
    /* Ajustes responsive */
    @media (min-width: 1200px) {
        .main-content {
            padding: 0rem 3rem !important;
        }
        
        .risk-title {
            font-size: 36px !important;
        }
        
        .metric-card-risk {
            padding: 2rem !important;
        }
        
        div.stPlotlyChart {
            height: 350px !important;
        }
    }
    
    @media (min-width: 1600px) {
        .main-content {
            padding: 0rem 4rem !important;
        }
        
        .risk-title {
            font-size: 40px !important;
        }
        
        .section-title {
            font-size: 26px !important;
        }
        
        div.stPlotlyChart {
            height: 380px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PORTADA THREE.JS SIMPLIFICADA PARA COMMUNITY CLOUD
# ==========================================

# En Community Cloud, usamos un HTML más simple sin iframes
threejs_portal_simple = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body { 
            margin: 0; 
            padding: 0;
            background-color: #000000 !important; 
            overflow: hidden; 
            font-family: sans-serif; 
            color: white; 
            width: 100%;
            height: 100%;
            position: relative;
        }
        
        #three-container {
            width: 100%;
            height: 100vh;
            position: relative;
            background: #000000 !important;
            overflow: hidden;
        }
        
        canvas { 
            display: block; 
            position: absolute;
            top: 0;
            left: 0;
            width: 100% !important;
            height: 100% !important;
            background: #000000 !important;
        }
        
        .controls { 
            position: absolute; 
            bottom: 50px; 
            z-index: 10; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            width: 100%;
        }
        
        .title { 
            position: absolute; 
            top: 30px; 
            font-size: 28px; 
            color: #00ffff; 
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.7); 
            letter-spacing: 2px; 
            z-index: 10; 
            width: 100%;
            text-align: center;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        // Versión simplificada de Three.js para Community Cloud
        let scene, camera, renderer, particles;
        const totalParticles = 5000; // Reducido para mejor performance
        const SPHERE_RADIUS = 3;
        const particleSize = 0.02;
        const ROTATION_SPEED = 0.002;
        
        function init() {
            // Crear escena
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x000000);
            
            // Configurar cámara
            const width = window.innerWidth;
            const height = window.innerHeight;
            camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
            
            // Configurar renderer
            renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(width, height);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Optimización
            
            // Añadir al DOM
            document.getElementById('three-container').appendChild(renderer.domElement);
            
            // Posicionar cámara
            camera.position.z = 8;
            
            // Crear partículas
            createParticles();
            
            // Añadir luz básica
            const light = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(light);
            
            const directionalLight = new THREE.DirectionalLight(0x00ffff, 0.8);
            directionalLight.position.set(5, 5, 5);
            scene.add(directionalLight);
            
            // Iniciar animación
            animate();
            
            // Manejar resize
            window.addEventListener('resize', onWindowResize);
        }
        
        function createParticles() {
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(totalParticles * 3);
            const colors = new Float32Array(totalParticles * 3);
            
            for (let i = 0; i < totalParticles * 3; i += 3) {
                // Crear partículas en una esfera
                const phi = Math.random() * Math.PI * 2;
                const theta = Math.acos(Math.random() * 2 - 1);
                
                positions[i] = SPHERE_RADIUS * Math.sin(theta) * Math.cos(phi);
                positions[i + 1] = SPHERE_RADIUS * Math.sin(theta) * Math.sin(phi);
                positions[i + 2] = SPHERE_RADIUS * Math.cos(theta);
                
                // Colores cian
                colors[i] = 0.0;     // R
                colors[i + 1] = 1.0; // G
                colors[i + 2] = 1.0; // B
            }
            
            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
            
            const material = new THREE.PointsMaterial({
                size: particleSize,
                vertexColors: true,
                transparent: true,
                opacity: 0.8,
                sizeAttenuation: true
            });
            
            particles = new THREE.Points(geometry, material);
            scene.add(particles);
        }
        
        function animate() {
            requestAnimationFrame(animate);
            
            // Rotación suave
            if (particles) {
                particles.rotation.y += ROTATION_SPEED;
                particles.rotation.x += ROTATION_SPEED * 0.5;
            }
            
            renderer.render(scene, camera);
        }
        
        function onWindowResize() {
            const width = window.innerWidth;
            const height = window.innerHeight;
            
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
            renderer.setSize(width, height);
        }
        
        // Iniciar cuando el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
    </script>
</head>
<body>
    <div id="three-container" class="threejs-container">
        <div class="title">FIN PLUS PORTAL</div>
    </div>
</body>
</html>
"""

# ==========================================
# PORTADA ALTERNATIVA PARA COMMUNITY CLOUD (CUANDO THREE.JS FALLE)
# ==========================================

def create_simple_portal():
    """Crea una portada alternativa si Three.js tiene problemas en Community Cloud"""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 2rem;
    ">
        <div style="
            font-size: 48px;
            font-weight: 800;
            color: #00ffff;
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.7);
            letter-spacing: 4px;
            margin-bottom: 20px;
        ">
            FIN PLUS PORTAL
        </div>
        
        <div style="
            font-size: 18px;
            color: #94a3b8;
            letter-spacing: 2px;
            margin-bottom: 60px;
            max-width: 600px;
        ">
            Interactive Risk Analytics Dashboard
        </div>
        
        <div style="
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin-bottom: 40px;
            max-width: 800px;
        ">
            <div style="
                background: rgba(0, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                width: 180px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(0, 255, 255, 0.2);
            ">
                <div style="font-size: 36px; margin-bottom: 10px;">📊</div>
                <div style="color: #ffffff; font-weight: 600;">Risk Analytics</div>
            </div>
            
            <div style="
                background: rgba(0, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                width: 180px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(0, 255, 255, 0.2);
            ">
                <div style="font-size: 36px; margin-bottom: 10px;">📈</div>
                <div style="color: #ffffff; font-weight: 600;">Real-time Metrics</div>
            </div>
            
            <div style="
                background: rgba(0, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                width: 180px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(0, 255, 255, 0.2);
            ">
                <div style="font-size: 36px; margin-bottom: 10px;">🔍</div>
                <div style="color: #ffffff; font-weight: 600;">Deep Insights</div>
            </div>
        </div>
        
        <div style="
            color: #ffffff;
            font-size: 14px;
            max-width: 500px;
            margin-top: 40px;
            padding: 20px;
            border-top: 1px solid rgba(0, 255, 255, 0.3);
        ">
            Advanced Credit Risk Assessment Platform • Powered by Machine Learning
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# LÓGICA DE DATOS (MANTENIDO IGUAL)
# ==========================================

REQUIRED_FEATURES = ['AGE', 'INCOME', 'LOAN_AMOUNT']
SIMULATED_FEATURES = ['AGE', 'INCOME', 'LOAN_AMOUNT', 'N_TRANSACCIONES', 'credit_utilization_mean']

@st.cache_data
def simulate_risk_data():
    np.random.seed(42)
    N = 1000
    df = pd.DataFrame({
        'CLIENT_ID': range(1000, 1000 + N),
        'AGE': np.random.randint(20, 70, N),
        'INCOME': np.random.rand(N) * 150000,
        'LOAN_AMOUNT': np.random.rand(N) * 50000,
        'N_TRANSACCIONES': np.random.randint(1, 500, N),
        'credit_utilization_mean': np.random.rand(N) * 0.9 + 0.1
    })
    
    importances = np.array([0.45, 0.30, 0.15, 0.07, 0.03])
    df_importance = pd.DataFrame({
        'Feature': SIMULATED_FEATURES,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    df_importance['Importance_Norm'] = (df_importance['Importance'] / df_importance['Importance'].sum()) * 100

    results, scaled_data = process_data_and_predict(df.copy())
    return results, scaled_data, df_importance, SIMULATED_FEATURES

@st.cache_data(show_spinner="Calculando predicciones de riesgo...")
def process_data_and_predict(df_input: pd.DataFrame):
    for feature in REQUIRED_FEATURES:
        if feature not in df_input.columns:
            st.error(f"Falta la columna requerida: **{feature}**.")
            return pd.DataFrame(), np.array([])
    
    if 'CLIENT_ID' not in df_input.columns:
        df_input['CLIENT_ID'] = range(1000, 1000 + len(df_input))

    probs = 0.1 + (df_input['INCOME'] < 50000) * 0.3 + (df_input['LOAN_AMOUNT'] > 30000) * 0.3
    
    if len(df_input) > 0:
        probs = np.clip(probs + np.random.normal(0, 0.1, len(df_input)), 0.01, 0.99)
    else:
        probs = np.clip(probs, 0.01, 0.99)
        
    preds = (probs >= 0.5).astype(int)
    
    results = pd.DataFrame({
        'CLIENT_ID': df_input['CLIENT_ID'].values,
        'PROBABILIDAD_NON_COMPLIANT': probs,
        'PREDICCION': preds
    })
    results['Nivel_Riesgo'] = results['PREDICCION'].map({0:'BAJO RIESGO',1:'ALTO RIESGO'})

    scaled_data = df_input[REQUIRED_FEATURES].apply(lambda x: (x - x.mean()) / x.std(), axis=0).values
    
    return results, scaled_data

# ==========================================
# FUNCIÓN DEL DASHBOARD (MANTENIDO IGUAL)
# ==========================================

def create_dashboard():
    """Crea el dashboard principal con mejor distribución en pantallas grandes."""
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Título principal - MÁS GRANDE Y MEJOR ESPACIADO
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <div class="risk-title">⚠️ Risk Analytics Platform</div>
        <div class="risk-subtitle">MODELO DE RIESGO CREDITICIO</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Separador elegante
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # --- SECCIÓN DE CARGA DE DATOS - CON NOMBRE INTUITIVO ---
    
    # Título intuitivo para cargar CSV
    st.markdown("""
    <div class="upload-title">
        📁 CARGAR DATOS DE CLIENTES (CSV)
    </div>
    """, unsafe_allow_html=True)
    
    # Contenedor centrado para el upload box
    st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%;">
        <div class="upload-box">
    """, unsafe_allow_html=True)
    
    # File uploader dentro del contenedor centrado - CON NOMBRE MÁS INTUITIVO
    uploaded_file = st.file_uploader("Seleccionar archivo CSV de datos de clientes", type="csv", 
                                     help="Sube un archivo CSV con información de clientes para analizar")
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar con datos simulados
    results, scaled, df_importance, feature_names = simulate_risk_data()
    
    # Procesar archivo subido - MANTENIDO IGUAL
    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            new_results, new_scaled = process_data_and_predict(df_uploaded.copy())
            
            if not new_results.empty:
                results = new_results
                scaled = new_scaled
                # Mostrar mensaje de éxito centrado
                st.markdown("""
                <div style="display: flex; justify-content: center; margin: 1rem 0;">
                    <div style="background-color: #10b981; color: white; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; text-align: center;">
                        ✅ Datos cargados correctamente: <strong>{}</strong> registros procesados
                    </div>
                </div>
                """.format(len(results)), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error al procesar archivo: {e}")
    
    # --- CÁLCULOS ---
    alto_riesgo_count = sum(results.PREDICCION)
    total_count = len(results)
    prob_promedio = results['PROBABILIDAD_NON_COMPLIANT'].mean() * 100
    
    # Configuración de estilo Plotly optimizada para pantallas grandes
    PLOTLY_LAYOUT = {
        'template': "plotly_dark",
        'margin': dict(l=10, r=10, t=40, b=20),
        'height': 320,
        'plot_bgcolor': '#0b1228', 
        'paper_bgcolor': '#0b1228', 
        'font': {'color': '#ffffff', 'size': 12},
        'hovermode': 'closest'
    }
    
    # --- Fila 1: Indicadores Clave (Métricas) - MÁS ESPACIADAS ---
    st.markdown('<div class="section-title">🔑 Métricas Clave del Modelo</div>', unsafe_allow_html=True)
    
    # Usar 2 filas de 2 columnas cada una para mejor distribución en pantallas grandes
    col1, col2, col3, col4 = st.columns(4)
    
    def metric_card(col, label, value, color, icon="📊"):
        col.markdown(f"""
        <div class="metric-card-risk" style="border-left: 6px solid {color};">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 24px; margin-right: 10px;">{icon}</span>
                <div style="font-size: 12px; color: #94a3b8; font-weight: 600;">{label}</div>
            </div>
            <div style="font-size: 28px; color: #ffffff; font-weight: 800; text-align: center;">{value}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Calcular métricas
    rate = f"{alto_riesgo_count/total_count:.1%}" if total_count > 0 else "0%"
    
    # Mostrar métricas
    metric_card(col1, "TOTAL CLIENTES", f"{total_count:,}", "#00ffff", "👥")
    metric_card(col2, "TASA ALTO RIESGO", rate, "#ff4b4b", "⚠️")
    metric_card(col3, "ALTO RIESGO", f"{alto_riesgo_count:,}", "#ff4b4b", "🔴")
    metric_card(col4, "PROBABILIDAD MEDIA", f"{prob_promedio:.2f}%", "#fdb400", "📈")
    
    # Separador
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # --- Fila 2: Visualizaciones - MEJOR DISTRIBUIDAS ---
    st.markdown('<div class="section-title">📊 Visualizaciones del Modelo</div>', unsafe_allow_html=True)
    
    # Primera fila de gráficos
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        st.markdown("<h4>📊 Distribución de Riesgo</h4>", unsafe_allow_html=True)
        if total_count > 0:
            pie_fig = px.pie(
                results, names="Nivel_Riesgo", title="",
                color="Nivel_Riesgo",
                color_discrete_map={'ALTO RIESGO':'#ff4b4b', 'BAJO RIESGO':'#004aad'},
                hole=0.4
            )
            pie_fig.update_traces(
                marker=dict(line=dict(color='#0c1a35', width=2)), 
                textinfo='percent+label',
                textposition='outside',
                pull=[0.1, 0]
            )
            pie_fig.update_layout(
                PLOTLY_LAYOUT,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(pie_fig, use_container_width=True)
    
    with col_viz2:
        st.markdown("<h4>📈 Densidad de Probabilidad</h4>", unsafe_allow_html=True)
        if total_count > 0:
            density_fig = go.Figure()
            density_fig.add_trace(go.Histogram(
                x=results[results['Nivel_Riesgo'] == 'ALTO RIESGO']['PROBABILIDAD_NON_COMPLIANT'],
                name='Alto Riesgo', 
                marker_color='#ff4b4b',
                nbinsx=30,
                opacity=0.8
            ))
            density_fig.add_trace(go.Histogram(
                x=results[results['Nivel_Riesgo'] == 'BAJO RIESGO']['PROBABILIDAD_NON_COMPLIANT'],
                name='Bajo Riesgo', 
                marker_color='#004aad',
                nbinsx=30,
                opacity=0.8
            ))
            density_fig.update_layout(
                barmode='overlay', 
                xaxis_title="Probabilidad de Incumplimiento",
                yaxis_title="Frecuencia",
                bargap=0.1
            )
            density_fig.update_layout(PLOTLY_LAYOUT)
            st.plotly_chart(density_fig, use_container_width=True)
    
    # Segunda fila de gráficos
    col_viz3, col_viz4 = st.columns(2)
    
    with col_viz3:
        st.markdown("<h4>🗺️ Mapa PCA (Segmentación)</h4>", unsafe_allow_html=True)
        try:
            if scaled.shape[0] > 1 and scaled.shape[1] >= 2:
                pca = PCA(min(2, scaled.shape[1]))
                coords = pca.fit_transform(scaled)
                results["Dim1"] = coords[:,0]
                results["Dim2"] = coords[:,1]
                
                pca_plot = px.scatter(
                    results, x="Dim1", y="Dim2", color="Nivel_Riesgo",
                    size="PROBABILIDAD_NON_COMPLIANT", 
                    color_discrete_map={'ALTO RIESGO':'#ff4b4b', 'BAJO RIESGO':'#004aad'},
                    hover_name="CLIENT_ID", 
                    title="",
                    size_max=15
                )
                pca_plot.update_traces(
                    marker=dict(opacity=0.7, line=dict(width=1, color='white'))
                )
                pca_plot.update_layout(
                    PLOTLY_LAYOUT,
                    showlegend=True,
                    xaxis_title="Componente Principal 1",
                    yaxis_title="Componente Principal 2"
                )
                st.plotly_chart(pca_plot, use_container_width=True)
            else:
                st.info("📊 Datos insuficientes para análisis PCA")
        except Exception as e:
            st.info(f"📊 Error en PCA: {str(e)[:50]}...")
    
    with col_viz4:
        st.markdown("<h4>🏆 Top 5 Variables Importantes</h4>", unsafe_allow_html=True)
        if not df_importance.empty:
            importance_fig = px.bar(
                df_importance.head(5), 
                x='Importance_Norm', 
                y='Feature', 
                orientation='h',
                title="", 
                text='Importance_Norm', 
                color='Importance_Norm',
                color_continuous_scale='Blues'
            )
            importance_fig.update_traces(
                texttemplate='%{text:.1f}%', 
                textposition='outside', 
                marker_line_width=0,
                opacity=0.9
            )
            importance_fig.update_layout(
                PLOTLY_LAYOUT,
                xaxis_title="Importancia Relativa (%)",
                yaxis_title="",
                xaxis_showgrid=True,
                yaxis_automargin=True,
                coloraxis_showscale=False
            )
            importance_fig.update_xaxes(range=[0, df_importance['Importance_Norm'].max() * 1.2])
            st.plotly_chart(importance_fig, use_container_width=True)
    
    # Separador
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # --- Fila 3: Tabla y Exportación - MEJOR ORGANIZADO ---
    st.markdown('<div class="section-title">📋 Resultados y Exportación</div>', unsafe_allow_html=True)
    
    col_data, col_export = st.columns([3, 1])
    
    with col_data:
        st.markdown("#### 📜 Resultados de Predicción")
        if total_count > 0:
            # Formatear mejor la tabla
            df_display = results[['CLIENT_ID', 'PROBABILIDAD_NON_COMPLIANT', 'Nivel_Riesgo']].copy()
            df_display['PROBABILIDAD_NON_COMPLIANT'] = df_display['PROBABILIDAD_NON_COMPLIANT'].apply(lambda x: f"{x:.2%}")
            df_display = df_display.rename(columns={
                'CLIENT_ID': 'ID Cliente',
                'PROBABILIDAD_NON_COMPLIANT': 'Prob. Incumplimiento',
                'Nivel_Riesgo': 'Nivel de Riesgo'
            }).head(15)  # Mostrar más filas en pantallas grandes
            
            # Función para colorear las filas
            def highlight_rows(row):
                color = '#ffcccc' if row['Nivel de Riesgo'] == 'ALTO RIESGO' else '#ccffcc'
                return ['background-color: {}'.format(color)] * len(row)
            
            # Mostrar tabla con mejor formato
            st.dataframe(
                df_display.style.apply(highlight_rows, axis=1),
                use_container_width=True,
                height=400  # Más alto para pantallas grandes
            )
    
    with col_export:
        st.markdown("#### 📥 Exportar Resultados")
        st.markdown("---")
        
        # Estadísticas rápidas
        st.metric("Total Registros", f"{total_count:,}")
        st.metric("Alto Riesgo", f"{alto_riesgo_count:,}")
        st.metric("Tasa", f"{alto_riesgo_count/total_count:.1%}")
        
        # Botón de descarga
        if total_count > 0:
            csv_data = results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Descargar CSV Completo",
                data=csv_data,
                file_name="predicciones_riesgo_completo.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # Botón para reporte resumido
            if st.button("📄 Generar Reporte PDF", use_container_width=True):
                st.info("🔄 Funcionalidad de PDF en desarrollo...")
    
    # Footer del dashboard
    st.markdown("""
    <div class="dashboard-footer">
        <div style="font-size: 16px; font-weight: 600; margin-bottom: 0.5rem; color: #00ffff;">
            Fin Plus Analytics Platform
        </div>
        <div style="margin-bottom: 1rem;">Modelo predictivo de riesgo crediticio • Versión 2.0</div>
        <div style="font-size: 12px; color: #94a3b8;">
            <div>Powered by Three.js Interactive Portal • Streamlit • Plotly</div>
            <div style="margin-top: 0.5rem;">© 2024 Fin Plus Analytics. Todos los derechos reservados.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón para regresar al portal
    st.markdown("---")
    col_return = st.columns([1, 2, 1])
    with col_return[1]:
        if st.button("🔄 Regresar al Portal Interactivo", type="secondary", use_container_width=True):
            st.session_state.portal_complete = False
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# LÓGICA PRINCIPAL MEJORADA PARA COMMUNITY CLOUD
# ==========================================

if 'portal_complete' not in st.session_state:
    st.session_state.portal_complete = False

# Botón fantasma mejorado para la transición
st.markdown("""
<div class="ghost-button-container">
    <button id="hidden-trigger-btn" style="display: none;">Hidden Trigger</button>
</div>
""", unsafe_allow_html=True)

# Inicializar estado para controlar la transición
if 'show_entrar_button' not in st.session_state:
    st.session_state.show_entrar_button = True

# Lógica de renderizado optimizada para Community Cloud
if not st.session_state.portal_complete:
    # Crear un contenedor para la portada
    with st.container():
        # Opción 1: Intentar con Three.js simplificado
        try:
            components.html(threejs_portal_simple, height=700, scrolling=False)
        except:
            # Opción 2: Si Three.js falla, mostrar portada alternativa
            create_simple_portal()
        
        # Mostrar el botón ENTRAR siempre visible
        st.markdown("""
        <div style="
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            width: 100%;
            text-align: center;
        ">
            <button class="portal-button" id="entrar-btn-visible">
                ENTRAR AL DASHBOARD
            </button>
        </div>
        
        <script>
        // Script para manejar el botón visible
        document.getElementById('entrar-btn-visible').onclick = function() {
            // Hacer clic en el botón oculto de Streamlit
            const hiddenBtn = window.parent.document.querySelector('[data-testid="baseButton-secondary"]');
            if (hiddenBtn) {
                hiddenBtn.click();
            }
        };
        </script>
        """, unsafe_allow_html=True)
        
        # Botón de Streamlit que realmente activa la transición
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("ENTRAR AL DASHBOARD", type="secondary", key="portal_enter_button"):
                st.session_state.portal_complete = True
                st.rerun()
else:
    # Mostrar dashboard
    create_dashboard()

# JavaScript adicional para mejorar la compatibilidad
st.markdown("""
<script>
// Script para mejorar compatibilidad con Community Cloud
document.addEventListener('DOMContentLoaded', function() {
    // Asegurar que el fondo sea correcto
    document.body.style.backgroundColor = '#0f172a';
    
    // Prevenir desbordamientos problemáticos
    const appContainer = document.querySelector('.stApp');
    if (appContainer) {
        appContainer.style.overflow = 'hidden';
    }
    
    // Asegurar que el contenido principal esté visible
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.style.position = 'relative';
        mainContent.style.zIndex = '1';
    }
});
</script>
""", unsafe_allow_html=True)