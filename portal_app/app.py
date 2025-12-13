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
import joblib
import pickle
import os

warnings.filterwarnings("ignore")

# Configuración de la página
st.set_page_config(
    page_title="Risk Analytics Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CARGAR EL MODELO XGBOOST ENTRENADO
# ==========================================

@st.cache_resource
def load_xgboost_model():
    """Carga el modelo XGBoost entrenado"""
    try:
        # Cargar el pipeline entrenado
        model_path = "C:/Users/PcVip/Downloads/xgb_pipeline_no_earlystop.joblib"
        
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            st.success("✅ Modelo XGBoost cargado correctamente")
            return model
        else:
            st.warning("⚠️ Archivo del modelo no encontrado. Usando modelo simulado.")
            return None
    except Exception as e:
        st.error(f"❌ Error al cargar el modelo: {str(e)}")
        return None

# Cargar el modelo al inicio
xgboost_model = load_xgboost_model()

# ==========================================
# CSS PERSONALIZADO (ACTUALIZADO MÁS AGRESIVAMENTE)
# ==========================================
st.markdown("""
<style>
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Eliminar márgenes y paddings para fondo completo - MÁS AGRESIVO */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
        margin-top: -70px !important;
    }
    
    /* Fondo del dashboard - MODIFICADO: -70px en lugar de -80px */
    .stApp {
        margin-top: -70px !important;
        background: #0f172a !important;
        min-height: 100vh !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Contenedor principal del dashboard - AJUSTADO */
    .main-content {
        background: #0f172a;
        padding: 0rem 1.5rem;
        margin: 0 auto;
        max-width: 100%;
        margin-top: 0px !important;
    }
    
    /* Título principal de Riesgo - REDUCIDO padding-top */
    .risk-title {
        font-size: 32px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin-bottom: 0.5rem !important;
        text-align: center !important;
        letter-spacing: 2px !important;
        padding-top: 0.5rem !important;
    }
    
    /* Subtítulo de Riesgo - MÁS GRANDE */
    .risk-subtitle {
        color: #94a3b8 !important;
        font-size: 14px !important;
        letter-spacing: 4px !important;
        text-align: center !important;
        margin-bottom: 2.5rem !important;
        text-transform: uppercase !important;
    }
    
    /* Tarjetas de métricas - MÁS GRANDES CON MÁRGENES */
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
    
    /* Títulos de secciones - MÁS GRANDES Y ESPACIADOS */
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
    
    /* Gráficos más grandes y mejor espaciados */
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
    
    /* Separadores con más espacio */
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
    
    /* Botones más grandes */
    .stButton > button {
        width: 100% !important;
        height: 48px !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    /* Tabla con mejor formato */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Upload box más grande y CENTRADO - ESTILO SIMPLIFICADO */
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
    
    /* Contenedor del iframe de Three.js */
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
        background: #000000 !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
    }
    
    /* TRUCO DEL BOTÓN FANTASMA */
    .ghost-button-container {
        display: none !important;
    }
    
    /* Footer mejor espaciado */
    .dashboard-footer {
        text-align: center !important;
        margin-top: 4rem !important;
        padding: 2rem !important;
        color: #64748b !important;
        font-size: 14px !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Ajustes responsive para pantallas grandes */
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
    
    /* Ajustes para pantallas muy grandes */
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
# PORTADA THREE.JS (MODIFICADA - QUITADO EL TEXTO)
# ==========================================

threejs_portal = """
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
            width: 100vw;
            height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
        }
        
        #three-container {
            width: 100vw;
            height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            background: #000000 !important;
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
        
        button { 
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
            margin-top: 20px; 
        }
        
        button:hover { 
            background-color: #00e6e6; 
            transform: scale(1.05); 
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.8); 
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
        
        /* QUITADO EL SUBTITLE */
        
        .fullscreen-container {
            width: 100vw;
            height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            background: #000000 !important;
            overflow: hidden;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://unpkg.com/three@0.128.0/examples/js/loaders/FontLoader.js"></script>
    <script src="https://unpkg.com/three@0.128.0/examples/js/math/MeshSurfaceSampler.js"></script>
</head>
<body>
    <div id="three-container" class="fullscreen-container">
        <div class="title">FIN PLUS PORTAL</div>
        <!-- QUITADO EL TEXTO "Interactive Particle System • Click ENTRAR to Continue" -->
        <div class="controls">
            <button id="toggleButton">ENTRAR</button>
        </div>
    </div>
    
<script>
let scene, camera, renderer, particles;
const totalParticles = 10000;
const SPHERE_RADIUS = 4;
const particleSize = 0.03;
const ROTATION_SPEED = 0.004;
const FONT_URL = 'https://threejs.org/examples/fonts/helvetiker_bold.typeface.json';
const TEXT = "FinPlus";

let sphereTargetPositions = new Float32Array(totalParticles * 3);
let textTargetPositions = null; 
let currentPositions;
let targetPositions = null;
let isAnimatingToText = false; 
let isTransitioning = false;
const transitionSpeed = 0.01; 
const epsilon = 0.001;

function setupRenderer() {
    const container = document.getElementById('three-container');
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    renderer.setSize(width, height);
    renderer.domElement.style.width = '100%';
    renderer.domElement.style.height = '100%';
    renderer.domElement.style.position = 'absolute';
    renderer.domElement.style.top = '0';
    renderer.domElement.style.left = '0';
    renderer.domElement.style.background = '#000000';
}

function triggerStreamlitTransition() {
    try {
        const buttons = window.parent.document.getElementsByTagName('button');
        for (let i = 0; i < buttons.length; i++) {
            if (buttons[i].innerText === "ENTRAR_AL_DASHBOARD_TRIGGER") {
                buttons[i].click(); 
                return;
            }
        }
    } catch (e) { console.error(e); }
}

function setupScene() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000);
    
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ 
        antialias: true, 
        alpha: false,
        powerPreference: "high-performance"
    });
    
    setupRenderer();
    document.getElementById('three-container').appendChild(renderer.domElement);
    
    camera.position.z = 10;
    scene.add(new THREE.AmbientLight(0xffffff, 0.5));
    const dl = new THREE.DirectionalLight(0x00ffff, 0.8);
    dl.position.set(5, 5, 5);
    scene.add(dl);
}

function createParticles() {
    for (let i = 0; i < totalParticles * 3; i += 3) {
        const phi = Math.random() * Math.PI * 2;
        const theta = Math.acos(Math.random() * 2 - 1);
        sphereTargetPositions[i] = SPHERE_RADIUS * Math.sin(theta) * Math.cos(phi);
        sphereTargetPositions[i + 1] = SPHERE_RADIUS * Math.sin(theta) * Math.sin(phi);
        sphereTargetPositions[i + 2] = SPHERE_RADIUS * Math.cos(theta);
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(sphereTargetPositions.slice(), 3));
    currentPositions = geometry.getAttribute('position');
    const material = new THREE.PointsMaterial({ 
        size: particleSize, 
        color: 0x00ffff, 
        sizeAttenuation: true, 
        transparent: true, 
        opacity: 0.9 
    });
    particles = new THREE.Points(geometry, material);
    scene.add(particles);
}

function createTextPoints() {
    return new Promise((resolve) => {
        const loader = new THREE.FontLoader();
        loader.load(FONT_URL, function (font) {
            const textGeometry = new THREE.TextGeometry(TEXT, {
                font: font, 
                size: 3.0, 
                height: 0.5, 
                curveSegments: 24,
                bevelEnabled: true, 
                bevelThickness: 0.1, 
                bevelSize: 0.05, 
                bevelSegments: 3
            });
            textGeometry.computeBoundingBox();
            const centerOffset_x = -0.5 * (textGeometry.boundingBox.max.x - textGeometry.boundingBox.min.x);
            const centerOffset_y = -0.5 * (textGeometry.boundingBox.max.y - textGeometry.boundingBox.min.y);
            textGeometry.translate(centerOffset_x, centerOffset_y, 0);
            textGeometry.scale(1.2, 1.2, 1.2);
            
            const mesh = new THREE.Mesh(textGeometry, new THREE.MeshBasicMaterial());
            const sampler = new THREE.MeshSurfaceSampler(mesh).build();
            
            let targetPositions = new Float32Array(totalParticles * 3);
            const tempPosition = new THREE.Vector3();
            
            for (let i = 0; i < totalParticles; i++) {
                sampler.sample(tempPosition);
                targetPositions[i * 3] = tempPosition.x + (Math.random() - 0.5) * 0.02;
                targetPositions[i * 3 + 1] = tempPosition.y + (Math.random() - 0.5) * 0.02;
                targetPositions[i * 3 + 2] = tempPosition.z + (Math.random() - 0.5) * 0.02;
            }
            resolve(targetPositions);
        });
    });
}

function animate() {
    requestAnimationFrame(animate);
    
    if (targetPositions && currentPositions) {
        let positionsChanged = false;
        
        for (let i = 0; i < totalParticles * 3; i += 3) {
            const cx = currentPositions.array[i];
            const cy = currentPositions.array[i + 1];
            const cz = currentPositions.array[i + 2];
            const tx = targetPositions[i];
            const ty = targetPositions[i + 1];
            const tz = targetPositions[i + 2];
            
            currentPositions.array[i] = THREE.MathUtils.lerp(cx, tx, transitionSpeed);
            currentPositions.array[i + 1] = THREE.MathUtils.lerp(cy, ty, transitionSpeed);
            currentPositions.array[i + 2] = THREE.MathUtils.lerp(cz, tz, transitionSpeed);
            
            if (!positionsChanged) {
                if (Math.abs(cx - tx) > epsilon || Math.abs(cy - ty) > epsilon || Math.abs(cz - tz) > epsilon) {
                    positionsChanged = true;
                }
            }
        }
        currentPositions.needsUpdate = true;
        
        if (isTransitioning && !positionsChanged) {
            isTransitioning = false;
            if (isAnimatingToText) {
                particles.rotation.y = 0;
                setTimeout(triggerStreamlitTransition, 2000);
            } 
        }
    }
    
    if (particles && !isAnimatingToText) {
        particles.rotation.y += ROTATION_SPEED;
    }
    
    renderer.render(scene, camera);
}

async function toggleShape() {
    if (isTransitioning || isAnimatingToText) return; 
    isAnimatingToText = true; 
    isTransitioning = true;
    
    if (!textTargetPositions) {
        textTargetPositions = await createTextPoints();
    }
    
    targetPositions = textTargetPositions;
    
    const button = document.getElementById('toggleButton');
    if (button) {
        button.textContent = 'TRANSITIONING...';
        button.style.opacity = '0.7';
        button.style.cursor = 'wait';
    }
    
    particles.rotation.y = 0;
}

async function init() {
    setupScene();
    createParticles(); 
    textTargetPositions = await createTextPoints();
    targetPositions = sphereTargetPositions;
    
    const button = document.getElementById('toggleButton');
    if (button) {
        button.addEventListener('click', toggleShape);
    }
    
    animate(); 
}

window.addEventListener('DOMContentLoaded', init);

window.addEventListener('resize', function() {
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
});

document.body.style.backgroundColor = '#000000';
document.body.style.overflow = 'hidden';
</script>
</body>
</html>
"""

# ==========================================
# LÓGICA DE DATOS (ACTUALIZADA CON TODAS LAS CARACTERÍSTICAS)
# ==========================================

# Lista completa de características que espera el modelo XGBoost
XGBOOST_FEATURES = [
    'TOTAL_INCOME', 'AMOUNT_PRODUCT', 'INSTALLMENT', 'REGION_SCORE', 
    'AGE_IN_YEARS', 'JOB_SENIORITY', 'HOME_SENIORITY', 'LAST_UPDATE', 
    'CAR_AGE', 'FAMILY_SIZE', 'REACTIVE_SCORING', 'PROACTIVE_SCORING', 
    'BEHAVIORAL_SCORING', 'DAYS_LAST_INFO_CHANGE', 'NUMBER_OF_PRODUCTS', 
    'DIGITAL_CLIENT', 'NUM_PREVIOUS_LOAN_APP', 'LOAN_ANNUITY_PAYMENT_SUM', 
    'LOAN_APPLICATION_AMOUNT_SUM', 'LOAN_CREDIT_GRANTED_SUM', 'NUM_STATUS_ANNULLED', 
    'NUM_STATUS_AUTHORIZED', 'NUM_STATUS_DENIED', 'NUM_STATUS_NOT_USED', 
    'NUM_FLAG_INSURED', 'CREDICT_CARD_BALANCE', 'CREDIT_CARD_LIMIT', 
    'CREDIT_CARD_PAYMENT', 'NUMBER_DRAWINGS_ATM', 'NUMBER_DRAWINGS', 
    'NUMBER_INSTALMENTS', 'KPI_DAYS_LAST_MOV', 'KPI_TOTAL_SPEND', 
    'KPI_DEBT_RATIO', 'KPI_LOAN_VOLATILITY', 'KPI_APPROVAL_RATIO', 
    'KPI_DENIAL_RATE', 'NAME_PRODUCT_TYPE_IDX', 'GENDER_IDX', 
    'EDUCATION_IDX', 'MARITAL_STATUS_IDX', 'HOME_SITUATION_IDX', 
    'OWN_INSURANCE_CAR_IDX', 'OCCUPATION_IDX', 'HOME_OWNER_IDX', 
    'EMPLOYER_ORGANIZATION_TYPE_IDX', 'KPI_AGE_GROUP_IDX'
]

# Características mínimas requeridas para la simulación
REQUIRED_FEATURES_SIMULATED = ['TOTAL_INCOME', 'AGE_IN_YEARS', 'AMOUNT_PRODUCT']

@st.cache_data
def simulate_risk_data():
    """Simula datos de riesgo con todas las características del modelo XGBoost"""
    np.random.seed(42)
    N = 1000
    
    # Crear DataFrame con todas las características necesarias
    data = {
        'CLIENT_ID': range(1000, 1000 + N),
    }
    
    # Generar valores para todas las características
    for feature in XGBOOST_FEATURES:
        if feature in ['TOTAL_INCOME', 'AMOUNT_PRODUCT', 'INSTALLMENT', 'LOAN_ANNUITY_PAYMENT_SUM',
                      'LOAN_APPLICATION_AMOUNT_SUM', 'LOAN_CREDIT_GRANTED_SUM', 'CREDICT_CARD_BALANCE',
                      'CREDIT_CARD_LIMIT', 'CREDIT_CARD_PAYMENT']:
            data[feature] = np.random.rand(N) * 50000 + 1000
        elif feature in ['AGE_IN_YEARS']:
            data[feature] = np.random.randint(20, 70, N)
        elif feature in ['JOB_SENIORITY', 'HOME_SENIORITY', 'CAR_AGE', 'FAMILY_SIZE']:
            data[feature] = np.random.randint(0, 30, N)
        elif feature in ['REGION_SCORE', 'REACTIVE_SCORING', 'PROACTIVE_SCORING', 'BEHAVIORAL_SCORING']:
            data[feature] = np.random.rand(N) * 100
        elif feature in ['LAST_UPDATE', 'DAYS_LAST_INFO_CHANGE', 'KPI_DAYS_LAST_MOV']:
            data[feature] = np.random.randint(0, 365, N)
        elif feature in ['NUMBER_OF_PRODUCTS', 'NUM_PREVIOUS_LOAN_APP', 'NUMBER_DRAWINGS_ATM',
                        'NUMBER_DRAWINGS', 'NUMBER_INSTALMENTS']:
            data[feature] = np.random.randint(0, 20, N)
        elif feature in ['DIGITAL_CLIENT', 'NUM_FLAG_INSURED']:
            data[feature] = np.random.randint(0, 2, N)
        elif feature in ['NUM_STATUS_ANNULLED', 'NUM_STATUS_AUTHORIZED', 'NUM_STATUS_DENIED',
                        'NUM_STATUS_NOT_USED']:
            data[feature] = np.random.randint(0, 10, N)
        elif feature in ['KPI_TOTAL_SPEND', 'KPI_DEBT_RATIO', 'KPI_LOAN_VOLATILITY',
                        'KPI_APPROVAL_RATIO', 'KPI_DENIAL_RATE']:
            data[feature] = np.random.rand(N)
        elif feature.endswith('_IDX'):
            data[feature] = np.random.randint(0, 10, N)
        else:
            data[feature] = np.random.rand(N)
    
    df = pd.DataFrame(data)
    
    # Usar el modelo XGBoost si está disponible, de lo contrario usar simulación
    if xgboost_model is not None:
        try:
            # Preparar datos para el modelo
            X = df[XGBOOST_FEATURES]
            probs = xgboost_model.predict_proba(X)[:, 1]
            preds = (probs >= 0.5).astype(int)
        except Exception as e:
            st.warning(f"Error usando modelo XGBoost: {str(e)}. Usando simulación.")
            # Simulación simple basada en características principales
            probs = 0.1 + (df['TOTAL_INCOME'] < 30000) * 0.3 + (df['AMOUNT_PRODUCT'] > 20000) * 0.3
            probs = np.clip(probs + np.random.normal(0, 0.1, len(df)), 0.01, 0.99)
            preds = (probs >= 0.5).astype(int)
    else:
        # Simulación simple
        probs = 0.1 + (df['TOTAL_INCOME'] < 30000) * 0.3 + (df['AMOUNT_PRODUCT'] > 20000) * 0.3
        probs = np.clip(probs + np.random.normal(0, 0.1, len(df)), 0.01, 0.99)
        preds = (probs >= 0.5).astype(int)
    
    # Crear DataFrame de importancia de características (simulado)
    importances = np.random.rand(len(XGBOOST_FEATURES[:10]))  # Solo mostrar top 10
    importances = importances / importances.sum()
    df_importance = pd.DataFrame({
        'Feature': XGBOOST_FEATURES[:10],
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    df_importance['Importance_Norm'] = (df_importance['Importance'] / df_importance['Importance'].sum()) * 100

    results = pd.DataFrame({
        'CLIENT_ID': df['CLIENT_ID'].values,
        'PROBABILIDAD_NON_COMPLIANT': probs,
        'PREDICCION': preds
    })
    results['Nivel_Riesgo'] = results['PREDICCION'].map({0:'BAJO RIESGO',1:'ALTO RIESGO'})
    
    # Para PCA, usar solo algunas características principales
    scaled_data = df[['TOTAL_INCOME', 'AGE_IN_YEARS', 'AMOUNT_PRODUCT']].apply(
        lambda x: (x - x.mean()) / x.std() if x.std() > 0 else 0, axis=0
    ).values
    
    return results, scaled_data, df_importance, XGBOOST_FEATURES[:10]

@st.cache_data(show_spinner="Calculando predicciones de riesgo...")
def process_data_and_predict(df_input: pd.DataFrame):
    """Procesa datos y realiza predicciones usando el modelo XGBoost"""
    
    # Verificar características mínimas requeridas
    min_features = ['TOTAL_INCOME', 'AGE_IN_YEARS', 'AMOUNT_PRODUCT']
    for feature in min_features:
        if feature not in df_input.columns:
            st.error(f"Falta la columna requerida: **{feature}**.")
            return pd.DataFrame(), np.array([])
    
    # Asignar ID de cliente si no existe
    if 'CLIENT_ID' not in df_input.columns:
        df_input['CLIENT_ID'] = range(1000, 1000 + len(df_input))
    
    # Generar características faltantes para el modelo XGBoost si es necesario
    for feature in XGBOOST_FEATURES:
        if feature not in df_input.columns:
            # Generar valores aleatorios según el tipo de característica
            if feature in ['TOTAL_INCOME', 'AMOUNT_PRODUCT', 'INSTALLMENT', 'LOAN_ANNUITY_PAYMENT_SUM',
                          'LOAN_APPLICATION_AMOUNT_SUM', 'LOAN_CREDIT_GRANTED_SUM', 'CREDICT_CARD_BALANCE',
                          'CREDIT_CARD_LIMIT', 'CREDIT_CARD_PAYMENT']:
                df_input[feature] = np.random.rand(len(df_input)) * 50000 + 1000
            elif feature in ['AGE_IN_YEARS']:
                df_input[feature] = np.random.randint(20, 70, len(df_input))
            elif feature in ['JOB_SENIORITY', 'HOME_SENIORITY', 'CAR_AGE', 'FAMILY_SIZE']:
                df_input[feature] = np.random.randint(0, 30, len(df_input))
            elif feature in ['REGION_SCORE', 'REACTIVE_SCORING', 'PROACTIVE_SCORING', 'BEHAVIORAL_SCORING']:
                df_input[feature] = np.random.rand(len(df_input)) * 100
            elif feature in ['LAST_UPDATE', 'DAYS_LAST_INFO_CHANGE', 'KPI_DAYS_LAST_MOV']:
                df_input[feature] = np.random.randint(0, 365, len(df_input))
            elif feature in ['NUMBER_OF_PRODUCTS', 'NUM_PREVIOUS_LOAN_APP', 'NUMBER_DRAWINGS_ATM',
                            'NUMBER_DRAWINGS', 'NUMBER_INSTALMENTS']:
                df_input[feature] = np.random.randint(0, 20, len(df_input))
            elif feature in ['DIGITAL_CLIENT', 'NUM_FLAG_INSURED']:
                df_input[feature] = np.random.randint(0, 2, len(df_input))
            elif feature in ['NUM_STATUS_ANNULLED', 'NUM_STATUS_AUTHORIZED', 'NUM_STATUS_DENIED',
                            'NUM_STATUS_NOT_USED']:
                df_input[feature] = np.random.randint(0, 10, len(df_input))
            elif feature in ['KPI_TOTAL_SPEND', 'KPI_DEBT_RATIO', 'KPI_LOAN_VOLATILITY',
                            'KPI_APPROVAL_RATIO', 'KPI_DENIAL_RATE']:
                df_input[feature] = np.random.rand(len(df_input))
            elif feature.endswith('_IDX'):
                df_input[feature] = np.random.randint(0, 10, len(df_input))
            else:
                df_input[feature] = np.random.rand(len(df_input))
    
    # Usar el modelo XGBoost si está disponible
    if xgboost_model is not None:
        try:
            # Preparar datos para el modelo
            X = df_input[XGBOOST_FEATURES]
            probs = xgboost_model.predict_proba(X)[:, 1]
            preds = (probs >= 0.5).astype(int)
        except Exception as e:
            st.warning(f"Error usando modelo XGBoost: {str(e)}. Usando simulación.")
            probs = 0.1 + (df_input['TOTAL_INCOME'] < 30000) * 0.3 + (df_input['AMOUNT_PRODUCT'] > 20000) * 0.3
            probs = np.clip(probs + np.random.normal(0, 0.1, len(df_input)), 0.01, 0.99)
            preds = (probs >= 0.5).astype(int)
    else:
        probs = 0.1 + (df_input['TOTAL_INCOME'] < 30000) * 0.3 + (df_input['AMOUNT_PRODUCT'] > 20000) * 0.3
        probs = np.clip(probs + np.random.normal(0, 0.1, len(df_input)), 0.01, 0.99)
        preds = (probs >= 0.5).astype(int)
    
    results = pd.DataFrame({
        'CLIENT_ID': df_input['CLIENT_ID'].values,
        'PROBABILIDAD_NON_COMPLIANT': probs,
        'PREDICCION': preds
    })
    results['Nivel_Riesgo'] = results['PREDICCION'].map({0:'BAJO RIESGO',1:'ALTO RIESGO'})

    # Para PCA, usar solo algunas características principales
    scaled_data = df_input[['TOTAL_INCOME', 'AGE_IN_YEARS', 'AMOUNT_PRODUCT']].apply(
        lambda x: (x - x.mean()) / x.std() if x.std() > 0 else 0, axis=0
    ).values
    
    return results, scaled_data

# ==========================================
# FUNCIÓN DEL DASHBOARD (MODIFICADA)
# ==========================================

def create_dashboard():
    """Crea el dashboard principal con mejor distribución en pantallas grandes."""
    
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Título principal - MÁS GRANDE Y MEJOR ESPACIADO
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0;">
        <div class="risk-title">Risk Analytics Platform</div>
        <div class="risk-subtitle">MODELO DE RIESGO CREDITICIO XGBOOST</div>
        <div style="color: #00ffff; font-size: 14px; margin-top: 0.5rem;">
            {'✅ Modelo XGBoost' if xgboost_model is not None else '⚠️ Modelo Simulado'}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Separador elegante
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # --- SECCIÓN DE CARGA DE DATOS - SIMPLIFICADA (QUITADO EL CUADRADO) ---
    
    # Título intuitivo para cargar CSV
    st.markdown("""
    <div class="upload-title">
        CARGAR DATOS DE CLIENTES (CSV)
    </div>
    <div style="text-align: center; color: #94a3b8; font-size: 12px; margin-bottom: 1rem;">
        <strong>Características mínimas requeridas:</strong> TOTAL_INCOME, AGE_IN_YEARS, AMOUNT_PRODUCT<br>
        <em>Las características faltantes se generarán automáticamente</em>
    </div>
    """, unsafe_allow_html=True)
    
    # SOLO MOSTRAR EL FILE UPLOADER SIN EL CONTENEDOR CUADRADO
    uploaded_file = st.file_uploader("Seleccionar archivo CSV de datos de clientes", type="csv", 
                                     help="Sube un archivo CSV con información de clientes para analizar")
    
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
                        Datos cargados correctamente: <strong>{}</strong> registros procesados
                    </div>
                </div>
                """.format(len(results)), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al procesar archivo: {e}")
    
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
    
    def metric_card(col, label, value, color, icon=""):
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
    metric_card(col1, "TOTAL CLIENTES", f"{total_count:,}", "#00ffff")
    metric_card(col2, "TASA ALTO RIESGO", rate, "#ff4b4b" )
    metric_card(col3, "ALTO RIESGO", f"{alto_riesgo_count:,}", "#ff4b4b")
    metric_card(col4, "PROBABILIDAD MEDIA", f"{prob_promedio:.2f}%", "#fdb400")
    
    # Separador
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # --- Fila 2: Visualizaciones - MEJOR DISTRIBUIDAS ---
    st.markdown('<div class="section-title"> Visualizaciones del Modelo</div>', unsafe_allow_html=True)
    
    # Primera fila de gráficos
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        st.markdown("<h4> Distribución de Riesgo</h4>", unsafe_allow_html=True)
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
        st.markdown("<h4> Densidad de Probabilidad</h4>", unsafe_allow_html=True)
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
        st.markdown("<h4>Mapa PCA (Segmentación)</h4>", unsafe_allow_html=True)
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
                st.info(" Datos insuficientes para análisis PCA")
        except Exception as e:
            st.info(f" Error en PCA: {str(e)[:50]}...")
    
    with col_viz4:
        st.markdown("<h4>Top 5 Variables Importantes</h4>", unsafe_allow_html=True)
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
    st.markdown('<div class="section-title">Resultados y Exportación</div>', unsafe_allow_html=True)
    
    col_data, col_export = st.columns([3, 1])
    
    with col_data:
        st.markdown("####Resultados de Predicción")
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
        st.markdown("#### Exportar Resultados")
        st.markdown("---")
        
        # Estadísticas rápidas
        st.metric("Total Registros", f"{total_count:,}")
        st.metric("Alto Riesgo", f"{alto_riesgo_count:,}")
        st.metric("Tasa", f"{alto_riesgo_count/total_count:.1%}")
        
        # Botón de descarga
        if total_count > 0:
            csv_data = results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇ Descargar CSV Completo",
                data=csv_data,
                file_name="predicciones_riesgo_completo.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # Botón para reporte resumido
            if st.button(" Generar Reporte PDF", use_container_width=True):
                st.info(" Funcionalidad de PDF en desarrollo...")
    
    # Footer del dashboard
    st.markdown("""
    <div class="dashboard-footer">
        <div style="font-size: 16px; font-weight: 600; margin-bottom: 0.5rem; color: #00ffff;">
            Fin Plus Analytics Platform
        </div>
        <div style="margin-bottom: 1rem;">Modelo predictivo de riesgo crediticio XGBoost • Versión 2.0</div>
        <div style="font-size: 12px; color: #94a3b8;">
            <div>Powered by Three.js Interactive Portal • Streamlit • Plotly • XGBoost</div>
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

# ==========================================
# LÓGICA PRINCIPAL
# ==========================================

if 'portal_complete' not in st.session_state:
    st.session_state.portal_complete = False

# Solo mostrar el botón fantasma cuando NO estemos en el dashboard
if not st.session_state.portal_complete:
    st.markdown('<div class="ghost-button-container">', unsafe_allow_html=True)
    if st.button("ENTRAR_AL_DASHBOARD_TRIGGER", key="btn_trigger_hidden"):
        st.session_state.portal_complete = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Lógica de renderizado
if not st.session_state.portal_complete:
    # Mostrar portal Three.js
    components.html(threejs_portal, height=1000, scrolling=False)
    
    
else:
    # Mostrar dashboard
    create_dashboard()