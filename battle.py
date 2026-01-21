import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página - Forzamos el modo oscuro y eliminamos espacios
st.set_page_config(page_title="Technovation Battle", layout="wide", initial_sidebar_state="collapsed")

# 2. Inyección de estilos optimizados para pantalla completa (No Scroll)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Evitar scroll en el body */
    html, body, [data-testid="stAppViewBlockContainer"] {
        max-height: 100vh;
        overflow: hidden !important;
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background-color: #181c26;
        background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0);
        background-size: 24px 24px;
    }

    /* Reducir márgenes superiores de Streamlit */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 1100px !important;
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

    header, footer {visibility: hidden;}

    /* Header más compacto */
    .glass-header {
        background: rgba(24, 28, 38, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 0.8rem 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* BOTONES TIPO CARD OPTIMIZADOS (Altura basada en pantalla) */
    div.stButton > button {
        width: 100% !important;
        height: 50vh !important; /* Ocupa exactamente el 50% de la altura visible */
        background-color: #272D3A !important;
        color: white !important;
        border-radius: 1.2rem !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* Card Izquierda */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        border: 2px solid #00bdc7 !important;
        box-shadow: 0 0 15px rgba(0, 189, 199, 0.1) !important;
    }

    /* Card Derecha */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button:hover {
        border: 2px solid #EE40DA !important;
        box-shadow: 0 0 20px rgba(238, 64, 218, 0.2) !important;
    }

    /* VS Ajustado */
    .vs-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 50vh;
    }
    .vs-circle {
        width: 50px;
        height: 50px;
        background: #181c26;
        border: 3px solid #EE40DA;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #EE40DA;
        font-weight: 900;
        font-size: 1.2rem;
        box-shadow: 0 0 15px #EE40DA;
    }

    /* Texto dentro de las Cards */
    .card-title-internal {
        font-size: clamp(1.2rem, 3vw, 1.8rem);
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .card-desc-internal {
        color: #9ababc;
        font-size: clamp(0.8rem, 1.5vw, 0.95rem);
        line-height: 1.3;
        text-align: center;
    }

    /* Progress bar pegada abajo */
    .stProgress {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE DATOS (Mantenida) ---
if 'competidores' not in st.session_state:
    PROBLEMAS = [
        {"nombre": "Pobreza menstrual", "desc": "Falta de acceso a higiene"},
        {"nombre": "Desnutrición oculta", "desc": "Carencia de vitaminas"},
        {"nombre": "Brecha digital rural", "desc": "Falta de internet en campo"},
        {"nombre": "Acceso a agua limpia", "desc": "Agua contaminada"},
        {"nombre": "Moda rápida", "desc": "Desecho masivo de ropa"},
        {"nombre": "Calidad del aire", "desc": "Humo cerca de escuelas"},
        {"nombre": "Protección de abejas", "desc": "Uso de pesticidas"},
        {"nombre": "Desperdicio energía", "desc": "Luces encendidas sin uso"},
        {"nombre": "Acoso y grooming", "desc": "Riesgos para menores"},
        {"nombre": "Transporte seguro", "desc": "Acoso en buses"},
        {"nombre": "Alertas de desastre", "desc": "Avisos de emergencia"},
        {"nombre": "Ciberestafas", "desc": "Robos a personas mayores"},
        {"nombre": "Salud mental joven", "desc": "Ansiedad por redes"},
        {"nombre": "Inclusión laboral", "desc": "Barreras trabajo"},
        {"nombre": "Huella carbono", "desc": "Impacto personal"},
        {"nombre": "Comercio local", "desc": "Tiendas de barrio"}
    ]
    random.shuffle(PROBLEMAS)
    st.session_state.competidores = PROBLEMAS
    st.session_state.ganadores_ronda_actual = []
    st.session_state.indice_duelo = 0
    st.session_state.ronda_nombre = "Octavos de final"

CRITERIOS = {
    "Octavos de final": {"t": "Impacto", "p": "¿Cuál es más urgente?"},
    "Cuartos de final": {"t": "Viabilidad", "p": "¿Cuál es más fácil?"},
    "Semifinal": {"t": "Usuario", "p": "¿Quién tiene usuarios claros?"},
    "Gran final": {"t": "Pasión", "p": "¿Cuál les motiva más?"}
}

def elegir_ganador(elegido):
    st.session_state.ganadores_ronda_actual.append(elegido)
    st.session_state.indice_duelo += 2
    if st.session_state.indice_duelo >= len(st.session_state.competidores):
        if len(st.session_state.ganadores_ronda_actual) == 1:
            st.session_state.ronda_nombre = "¡Ganador!"
        else:
            st.session_state.competidores = st.session_state.ganadores_ronda_actual
            st.session_state.ganadores_ronda_actual = []
            st.session_state.indice_duelo = 0
            etapas = {8: "Cuartos de final", 4: "Semifinal", 2: "Gran final"}
            st.session_state.ronda_nombre = etapas.get(len(st.session_state.competidores), "Gran final")

# --- UI RENDER ---

info = CRITERIOS.get(st.session_state.ronda_nombre, CRITERIOS["Octavos de final"])

# Header Compacto
st.markdown(f"""
    <div class="glass-header">
        <h2 style="color:white; margin:0; font-size:1.4rem;">{st.session_state.ronda_nombre}: {info['t']}</h2>
        <p style="color:#00bdc7; margin:0; font-size:0.9rem; font-weight:bold;">{info['p']}</p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.ronda_nombre == "¡Ganador!":
    ganador = st.session_state.ganadores_ronda_actual[0]
    st.balloons()
    st.markdown(f"<div class='glass-header' style='border:2px solid #00bdc7'><h2 style='color:#00bdc7'>GANADOR FINAL</h2><h1 style='color:white;'>{ganador['nombre']}</h1></div>", unsafe_allow_html=True)
    if st.button("NUEVA PARTIDA"):
        st.session_state.clear()
        st.rerun()
else:
    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]
    
    # Grid de Batalla
    col1, col_v, col2 = st.columns([10, 2, 10])
    
    with col1:
        # Texto formateado dentro del botón
        if st.button(f"{p1['nombre']}\n\n{p1['desc']}", key=f"btn_{i}"):
            elegir_ganador(p1)
            st.rerun()

    with col_v:
        st.markdown('<div class="vs-container"><div class="vs-circle">VS</div></div>', unsafe_allow_html=True)

    with col2:
        if st.button(f"{p2['nombre']}\n\n{p2['desc']}", key=f"btn_{i+1}"):
            elegir_ganador(p2)
            st.rerun()

    # Progreso
    progreso = (int(i/2) + 1) / (len(st.session_state.competidores)/2)
    st.progress(progreso)
    st.markdown(f'<p style="text-align:center; color:#9ababc; font-size:0.7rem; margin:0;">BATTLE {int(i/2)+1} / {int(len(st.session_state.competidores)/2)}</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    if st.button("REINICIAR"):
        st.session_state.clear()
        st.rerun()
