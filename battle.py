import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation Battle", layout="wide", initial_sidebar_state="collapsed")

# 2. Inyección de estilos (Tailwind + Custom CSS)
st.markdown("""
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100..700,0..1&display=swap" rel="stylesheet"/>

<style>
    /* Forzar fuentes y fondo general */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background-color: #181c26;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Ocultar elementos innecesarios de Streamlit */
    header, footer {visibility: hidden;}
    [data-testid="stHeader"] {background: rgba(0,0,0,0);}
    
    /* Contenedor principal */
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 2rem !important;
        max-width: 800px !important;
    }

    /* Estilos Glassmorphism del Header */
    .glass-header {
        background: rgba(24, 28, 38, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 1rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* VS Icon */
    .vs-badge {
        display: flex;
        width: 50px;
        height: 50px;
        align-items: center;
        justify-content: center;
        border-radius: 9999px;
        background-color: #181c26;
        border: 4px solid #EE40DA;
        box-shadow: 0 0 15px rgba(238, 64, 218, 0.6);
        color: #EE40DA;
        font-weight: 900;
        font-style: italic;
        margin: auto;
        z-index: 10;
    }

    /* Estilo de los botones (Cards) */
    div.stButton > button {
        background-color: #272D3A !important;
        color: white !important;
        border-radius: 1rem !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        padding: 2rem 1rem !important;
        width: 100% !important;
        min-height: 250px !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: normal !important;
    }

    /* Card A (Primary - Teal) */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        border: 2px solid #00bdc7 !important;
        box-shadow: 0 0 15px rgba(0, 189, 199, 0.2) !important;
    }

    /* Card B (Challenger - Pink/White) */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button:hover {
        border: 2px solid #EE40DA !important;
        box-shadow: 0 0 15px rgba(238, 64, 218, 0.2) !important;
    }

    .card-title {
        font-size: 1.5rem;
        font-weight: 800;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
        color: white;
    }

    .card-desc {
        font-size: 0.85rem;
        color: #9ababc;
        line-height: 1.4;
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #00bdc7 !important;
        box-shadow: 0 0 8px #00bdc7;
    }

    /* Sidebar Dark */
    [data-testid="stSidebar"] {
        background-color: #11141d !important;
    }
</style>
""", unsafe_allow_html=True)

# --- INICIO LÓGICA ---
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

# Header Estilo Glass
info = CRITERIOS.get(st.session_state.ronda_nombre, CRITERIOS["Octavos de final"])
st.markdown(f"""
    <div class="glass-header">
        <span style="color:#00bdc7; font-size:10px; text-transform:uppercase; letter-spacing:0.2em; font-weight:bold;">Tournament</span>
        <h2 style="color:white; font-size:1.5rem; font-weight:bold; margin:0;">{st.session_state.ronda_nombre}: {info['t']}</h2>
        <p style="color:#9ababc; font-size:0.9rem; margin-top:5px;">{info['p']}</p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.ronda_nombre == "¡Ganador!":
    ganador = st.session_state.ganadores_ronda_actual[0]
    st.balloons()
    st.markdown(f"""
        <div class="glass-header" style="border: 2px solid #00bdc7;">
            <h1 style="color:#00bdc7; font-size:3rem; font-weight:900;">🏆</h1>
            <h2 style="color:white;">EL GANADOR ES:</h2>
            <h1 style="color:white; font-size:2.5rem; text-transform:uppercase;">{ganador['nombre']}</h1>
        </div>
    """, unsafe_allow_html=True)
    if st.button("JUGAR DE NUEVO"):
        st.session_state.clear()
        st.rerun()
else:
    # Battle Arena
    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]
    
    # Texto de batalla
    st.markdown(f'<p style="text-align:center; color:#00bdc7; font-weight:bold; letter-spacing:0.2em; font-size:12px; margin-bottom:20px;">BATTLE {int(i/2)+1} OF {int(len(st.session_state.competidores)/2)}</p>', unsafe_allow_html=True)

    col1, col_v, col2 = st.columns([10, 3, 10])
    
    with col1:
        content1 = f"<div class='card-title'>{p1['nombre']}</div><div class='card-desc'>{p1['desc']}</div>"
        if st.button(p1['nombre'], key=f"btn_{i}", help=p1['desc']):
            elegir_ganador(p1)
            st.rerun()
        st.markdown(f"<div style='text-align:center; color:#9ababc; font-size:0.8rem; margin-top:-30px;'>{p1['desc']}</div>", unsafe_allow_html=True)

    with col_v:
        st.markdown('<div style="height:100px"></div><div class="vs-badge">VS</div>', unsafe_allow_html=True)

    with col2:
        if st.button(p2['nombre'], key=f"btn_{i+1}", help=p2['desc']):
            elegir_ganador(p2)
            st.rerun()
        st.markdown(f"<div style='text-align:center; color:#9ababc; font-size:0.8rem; margin-top:-30px;'>{p2['desc']}</div>", unsafe_allow_html=True)

    # Footer con Progreso
    st.markdown("<br><br>", unsafe_allow_html=True)
    progreso = (int(i/2) + 1) / (len(st.session_state.competidores)/2)
    st.progress(progreso)
    st.markdown(f'<p style="text-align:right; color:#00bdc7; font-size:10px; font-weight:bold;">{int(progreso*100)}% COMPLETADO</p>', unsafe_allow_html=True)

# Sidebar para QR y Reset
with st.sidebar:
    st.markdown("<h2 style='color:white;'>OPCIONES</h2>", unsafe_allow_html=True)
    if st.button("REINICIAR TODO"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    url = "https://tu-app.streamlit.app" 
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="¡Invita a otros!")
