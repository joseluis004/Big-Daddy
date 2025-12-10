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
from io import StringIO

warnings.filterwarnings("ignore")

# Configuración de la página PRINCIPAL para Cloud
st.set_page_config(
    page_title="Risk Analytics Dashboard",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS PERSONALIZADO OPTIMIZADO PARA CLOUD
# ==========================================
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit (Cloud-safe) */
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stAppViewContainer"] {background-color: #0f172a !important;}
    
    /* Fondo principal - IMPORTANTE para Cloud */
    .stApp {
        background: #0f172a !important;
        padding: 0px !important;
        margin: 0px !important;
    }
    
    /* Ajustar el contenedor principal */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    /* Título principal */
    .risk-title {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin-bottom: 0.5rem !important;
        text-align: center !important;
        letter-spacing: 2px !important;
        padding-top: 0.5rem !important;
    }
    
    /* Subtítulo de Riesgo */
    .risk-subtitle {
        color: #94a3b8 !important;
        font-size: 14px !important;
        letter-spacing: 4px !important;
        text-align: center !important;
        margin-bottom: 2rem !important;
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
        padding-left: 0.5rem !important;
        border-left: 4px solid #00ffff !important;
        padding-left: 1rem !important;
    }
    
    /* Gráficos - HEIGHT FIJADO para evitar cambios en Cloud */
    [data-testid="stPlotlyChart"] {
        border-radius: 12px !important;
        background-color: #0b1228 !important;
        padding: 15px !important;
        margin-bottom: 1.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        height: 320px !important;
    }
    
    /* Asegurar que los gráficos de Plotly mantengan tamaño */
    .js-plotly-plot {
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
    .divider {
        margin: 2.5rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.3), transparent) !important;
    }
    
    /* Upload box */
    .upload-box {
        background-color: #1e293b !important;
        border: 2px dashed #00ffff !important;
        border-radius: 12px !important;
        padding: 2.5rem !important;
        text-align: center !important;
        margin: 1rem auto 2rem auto !important;
        transition: all 0.3s ease !important;
        max-width: 600px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* Footer */
    .dashboard-footer {
        text-align: center !important;
        margin-top: 3rem !important;
        padding: 2rem !important;
        color: #64748b !important;
        font-size: 14px !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Ajustes para tablas en Cloud */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Botones */
    [data-testid="baseButton-secondary"] {
        background: linear-gradient(135deg, #0b1228 0%, #101f3d 100%) !important;
        color: #00ffff !important;
        border: 1px solid #00ffff !important;
    }
    
    /* Contenedor del iframe */
    iframe {
        width: 100% !important;
        height: 100vh !important;
        border: none !important;
        background: #000000 !important;
    }
    
    /* Ajustes específicos para Cloud */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        .metric-card-risk {
            padding: 1rem !important;
        }
        
        [data-testid="stPlotlyChart"] {
            height: 280px !important;
        }
        
        .js-plotly-plot {
            height: 280px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PORTADA THREE.JS - VERSIÓN CLOUD OPTIMIZADA
# ==========================================
def get_threejs_portal():
    """Genera el HTML del portal Three.js optimizado para Cloud"""
    return """
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
        
        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #000000;
        }
        
        #three-container {
            width: 100%;
            height: 100%;
            position: fixed;
            top: 0;
            left: 0;
            background: #000000;
        }
        
        canvas {
            display: block;
            width: 100% !important;
            height: 100% !important;
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
            font-family: 'Arial', sans-serif;
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
        
        #toggleButton {
            padding: 15px 40px;
            cursor: pointer;
            background-color: #00ffff;
            color: #000000;
            border: none;
            border-radius: 30px;
            font-weight: bold;
            font-size: 18px;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        }
        
        #toggleButton:hover {
            background-color: #00e6e6;
            transform: scale(1.05);
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.8);
        }
        
        .loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #00ffff;
            font-size: 18px;
            z-index: 5;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/FontLoader.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/math/MeshSurfaceSampler.min.js"></script>
</head>
<body>
    <div id="three-container">
        <div class="title">FIN PLUS PORTAL</div>
        <div class="loading" id="loadingText">Cargando sistema de partículas...</div>
        <div class="controls">
            <button id="toggleButton">ENTRAR</button>
        </div>
    </div>
    
<script>
// Script Three.js simplificado y optimizado para Cloud
let scene, camera, renderer, particles;
const totalParticles = 8000; // Reducido para mejor performance en Cloud
const SPHERE_RADIUS = 4;
const particleSize = 0.03;
const ROTATION_SPEED = 0.003;

function initThreeJS() {
    // Crear escena
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);
    
    // Configurar cámara
    const width = window.innerWidth;
    const height = window.innerHeight;
    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 10;
    
    // Configurar renderer
    renderer = new THREE.WebGLRenderer({ 
        antialias: true,
        alpha: false,
        powerPreference: "high-performance"
    });
    renderer.setSize(width, height);
    document.getElementById('three-container').appendChild(renderer.domElement);
    
    // Luces
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0x00ffff, 0.8);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);
    
    // Crear partículas en esfera
    createSphereParticles();
    
    // Ocultar texto de carga
    document.getElementById('loadingText').style.display = 'none';
    
    // Animación
    animate();
    
    // Configurar botón
    document.getElementById('toggleButton').addEventListener('click', function() {
        this.textContent = 'CARGANDO DASHBOARD...';
        this.disabled = true;
        
        // Transición a dashboard
        setTimeout(function() {
            window.parent.postMessage('ENTER_DASHBOARD', '*');
        }, 1000);
    });
}

function createSphereParticles() {
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(totalParticles * 3);
    const colors = new Float32Array(totalParticles * 3);
    
    for (let i = 0; i < totalParticles * 3; i += 3) {
        const phi = Math.random() * Math.PI * 2;
        const theta = Math.acos(Math.random() * 2 - 1);
        
        positions[i] = SPHERE_RADIUS * Math.sin(theta) * Math.cos(phi);
        positions[i + 1] = SPHERE_RADIUS * Math.sin(theta) * Math.sin(phi);
        positions[i + 2] = SPHERE_RADIUS * Math.cos(theta);
        
        // Colores cian
        colors[i] = 0.0;
        colors[i + 1] = 1.0;
        colors[i + 2] = 1.0;
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
    
    if (particles) {
        particles.rotation.y += ROTATION_SPEED;
    }
    
    renderer.render(scene, camera);
}

// Manejar resize
window.addEventListener('resize', function() {
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
});

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initThreeJS, 100);
});

// Comunicación con Streamlit
window.addEventListener('message', function(event) {
    if (event.data === 'START_ANIMATION') {
        initThreeJS();
    }
});
</script>
</body>
</html>
"""

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
# DASHBOARD PRINCIPAL - OPTIMIZADO PARA CLOUD
# ==========================================

def create_dashboard():
    """Dashboard optimizado para Streamlit Cloud"""
    
    # Título principal
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div class="risk-title">⚠️ Risk Analytics Platform</div>
        <div class="risk-subtitle">MODELO DE RIESGO CREDITICIO</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # --- SECCIÓN DE CARGA DE DATOS ---
    st.markdown("""
    <div class="upload-title" style="text-align: center; color: #00ffff; font-size: 20px; margin-bottom: 1rem;">
        📁 CARGAR DATOS DE CLIENTES (CSV)
    </div>
    """, unsafe_allow_html=True)
    
    # Contenedor para upload
    col_upload = st.columns([1, 2, 1])
    with col_upload[1]:
        uploaded_file = st.file_uploader(
            "Seleccionar archivo CSV", 
            type="csv",
            help="Sube un archivo CSV con datos de clientes",
            label_visibility="collapsed"
        )
    
    # Inicializar con datos simulados
    results, scaled, df_importance, feature_names = simulate_risk_data()
    
    # Procesar archivo subido
    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            new_results, new_scaled = process_data_and_predict(df_uploaded.copy())
            
            if not new_results.empty:
                results = new_results
                scaled = new_scaled
                st.success(f"✅ Datos cargados correctamente: **{len(results)}** registros procesados")
        except Exception as e:
            st.error(f"❌ Error al procesar archivo: {e}")
    
    # --- CÁLCULOS ---
    alto_riesgo_count = sum(results.PREDICCION)
    total_count = len(results)
    prob_promedio = results['PROBABILIDAD_NON_COMPLIANT'].mean() * 100
    
    # Configuración Plotly FIJA para evitar cambios en Cloud
    PLOTLY_LAYOUT = {
        'template': "plotly_dark",
        'margin': dict(l=10, r=10, t=30, b=10),
        'height': 300,  # ALTURA FIJA
        'plot_bgcolor': '#0b1228',
        'paper_bgcolor': '#0b1228',
        'font': {'color': '#ffffff', 'size': 12},
        'hovermode': 'closest',
        'autosize': False  # IMPORTANTE: Desactivar autosize
    }
    
    # --- Fila 1: Indicadores Clave ---
    st.markdown('<div class="section-title">🔑 Métricas Clave del Modelo</div>', unsafe_allow_html=True)
    
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
    
    rate = f"{alto_riesgo_count/total_count:.1%}" if total_count > 0 else "0%"
    
    metric_card(col1, "TOTAL CLIENTES", f"{total_count:,}", "#00ffff", "👥")
    metric_card(col2, "TASA ALTO RIESGO", rate, "#ff4b4b", "⚠️")
    metric_card(col3, "ALTO RIESGO", f"{alto_riesgo_count:,}", "#ff4b4b", "🔴")
    metric_card(col4, "PROBABILIDAD MEDIA", f"{prob_promedio:.2f}%", "#fdb400", "📈")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # --- Fila 2: Visualizaciones con ALTURAS FIJAS ---
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
                textinfo='percent+label'
            )
            pie_fig.update_layout(
                **PLOTLY_LAYOUT,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            # Forzar altura fija
            pie_fig.update_layout(height=300, autosize=False)
            st.plotly_chart(pie_fig, use_container_width=True, config={'responsive': False})
    
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
            density_fig.update_layout(**PLOTLY_LAYOUT)
            density_fig.update_layout(height=300, autosize=False)
            st.plotly_chart(density_fig, use_container_width=True, config={'responsive': False})
    
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
                pca_plot.update_layout(**PLOTLY_LAYOUT)
                pca_plot.update_layout(height=300, autosize=False)
                st.plotly_chart(pca_plot, use_container_width=True, config={'responsive': False})
            else:
                st.info("📊 Datos insuficientes para análisis PCA")
        except Exception as e:
            st.info("📊 Error en análisis PCA")
    
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
                textposition='outside'
            )
            importance_fig.update_layout(**PLOTLY_LAYOUT)
            importance_fig.update_layout(height=300, autosize=False)
            st.plotly_chart(importance_fig, use_container_width=True, config={'responsive': False})
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # --- Fila 3: Tabla y Exportación ---
    st.markdown('<div class="section-title">📋 Resultados y Exportación</div>', unsafe_allow_html=True)
    
    col_data, col_export = st.columns([3, 1])
    
    with col_data:
        st.markdown("#### 📜 Resultados de Predicción")
        if total_count > 0:
            df_display = results[['CLIENT_ID', 'PROBABILIDAD_NON_COMPLIANT', 'Nivel_Riesgo']].copy()
            df_display['PROBABILIDAD_NON_COMPLIANT'] = df_display['PROBABILIDAD_NON_COMPLIANT'].apply(lambda x: f"{x:.2%}")
            df_display = df_display.rename(columns={
                'CLIENT_ID': 'ID Cliente',
                'PROBABILIDAD_NON_COMPLIANT': 'Prob. Incumplimiento',
                'Nivel_Riesgo': 'Nivel de Riesgo'
            }).head(15)
            
            # Mostrar tabla
            st.dataframe(df_display, use_container_width=True, height=400)
    
    with col_export:
        st.markdown("#### 📥 Exportar Resultados")
        st.markdown("---")
        
        st.metric("Total Registros", f"{total_count:,}")
        st.metric("Alto Riesgo", f"{alto_riesgo_count:,}")
        
        if total_count > 0:
            csv_data = results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Descargar CSV",
                data=csv_data,
                file_name="predicciones_riesgo.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # Footer
    st.markdown("""
    <div class="dashboard-footer">
        <div style="font-size: 16px; font-weight: 600; margin-bottom: 0.5rem; color: #00ffff;">
            Fin Plus Analytics Platform
        </div>
        <div style="margin-bottom: 1rem;">Modelo predictivo de riesgo crediticio • Versión 2.0</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botón para regresar
    st.markdown("---")
    if st.button("🔄 Regresar al Portal", type="secondary", use_container_width=True):
        st.session_state.portal_complete = False
        st.rerun()

# ==========================================
# LÓGICA PRINCIPAL - OPTIMIZADA PARA CLOUD
# ==========================================

# Inicializar estado de sesión
if 'portal_complete' not in st.session_state:
    st.session_state.portal_complete = False

# Manejar mensajes del iframe
def handle_iframe_message():
    """Manejar comunicación desde el iframe Three.js"""
    js_code = """
    <script>
    window.addEventListener('message', function(event) {
        if (event.data === 'ENTER_DASHBOARD') {
            window.parent.streamlitWindow.setComponentValue('ENTER_DASHBOARD');
        }
    });
    
    // Iniciar animación cuando el iframe esté listo
    window.dispatchEvent(new Event('START_ANIMATION'));
    </script>
    """
    return js_code

# Botón oculto para manejar la transición
if st.button("ENTRAR_AL_DASHBOARD", key="hidden_btn", help="", type="primary", visible=False):
    st.session_state.portal_complete = True
    st.rerun()

# Renderizar portal o dashboard
if not st.session_state.portal_complete:
    # Mostrar portal Three.js
    components.html(
        get_threejs_portal(), 
        height=700,  # Altura fija
        scrolling=False
    )
    
    # Inyectar código JavaScript para comunicación
    components.html(handle_iframe_message(), height=0)
    
    # Verificar si se recibió el mensaje
    if st.experimental_get_query_params().get('enter', False):
        st.session_state.portal_complete = True
        st.rerun()
else:
    # Mostrar dashboard
    create_dashboard()