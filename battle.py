import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation Battle", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS Restaurado y Ajustado (Alto 15vh y Menú lateral)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewBlockContainer"] {
        max-height: 100vh;
        overflow: hidden !important;
        font-family: 'Space Grotesk', sans-serif;
        background-color: #181c26;
    }

    .stApp {
        background-color: #181c26;
        background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0);
        background-size: 24px 24px;
    }

    header, footer {visibility: hidden;}

    [data-testid="stAppViewBlockContainer"] {
        max-width: 950px !important;
        padding: 1rem !important;
    }

    /* Separación mínima entre columnas */
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
    }

    /* Sidebar Estilo Dark */
    [data-testid="stSidebar"] {
        background-color: #11141d !important;
        color: white !important;
    }

    .glass-header {
        background: rgba(24, 28, 38, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 0.8rem;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* ALTO AL 15% DE LA PANTALLA */
    div.stButton > button {
        width: 100% !important;
        height: 15vh !important;
        min-height: 15vh !important;
        background-color: #272D3A !important;
        color: white !important;
        border-radius: 1rem !important;
        padding: 0.5rem !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        transition: all 0.2s ease;
        line-height: 1.2 !important;
    }

    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        border-color: #00bdc7 !important;
        box-shadow: 0 0 10px rgba(0, 189, 199, 0.1) !important;
        margin-right: -5px !important;
    }

    div[data-testid="column"]:nth-of-type(3) div.stButton > button {
        margin-left: -5px !important;
    }

    div[data-testid="column"]:nth-of-type(3) div.stButton > button:hover {
        border-color: #EE40DA !important;
        box-shadow: 0 0 10px rgba(238, 64, 218, 0.2) !important;
    }

    /* VS Ultra pegado */
    .vs-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 15vh;
        z-index: 10;
    }
    .vs-circle {
        width: 38px;
        height: 38px;
        background: #181c26;
        border: 2px solid #EE40DA;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #EE40DA;
        font-weight: 900;
        font-size: 0.8rem;
        box-shadow: 0 0 10px rgba(238, 64, 218, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA Y DATOS (RESTAURADOS) ---
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
    "Octavos de final": {"t": "📍 Ronda 1: Impacto", "p": "¿Cuál es más urgente?"},
    "Cuartos de final": {"t": "💻 Ronda 2: Viabilidad", "p": "¿Cuál es más fácil?"},
    "Semifinal": {"t": "👤 Ronda 3: Usuario", "p": "¿Quién tiene usuarios claros?"},
    "Gran final": {"t": "❤️ Final: Pasión", "p": "¿Cuál les motiva más?"}
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
            st.session_state.ronda_nombre = etapas.get(len(st.session_state.competidores), "Final")

# --- SIDEBAR (RESTAURADO) ---
with st.sidebar:
    st.markdown("## MENÚ")
    if st.button("REINICIAR PARTIDA"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    st.markdown("<p style='color:white;'>📢 Invita a jugar</p>", unsafe_allow_html=True)
    url = "https://tu-app.streamlit.app/" # Cambia por tu URL
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=True)

# --- UI PRINCIPAL ---
if st.session_state.ronda_nombre == "¡Ganador!":
    ganador = st.session_state.ganadores_ronda_actual[0]
    st.balloons()
    st.markdown(f'<div class="glass-header"><h2 style="color:#00bdc7">¡Ganador!</h2><h1 style="color:white">{ganador["nombre"]}</h1></div>', unsafe_allow_html=True)
else:
    info = CRITERIOS.get(st.session_state.ronda_nombre, CRITERIOS["Octavos de final"])
    st.markdown(f'<div class="glass-header"><h2 style="color:white; margin:0; font-size:1.1rem;">{info["t"]}</h2><p style="color:#9ababc; margin:0; font-size:0.8rem;">{info["p"]}</p></div>', unsafe_allow_html=True)

    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]
    
    st.markdown(f'<p style="text-align:center; color:#00bdc7; font-size:0.7rem; font-weight:bold; letter-spacing:0.1em; margin-bottom:5px;">BATALLA {int(i/2)+1} / {int(len(st.session_state.competidores)/2)}</p>', unsafe_allow_html=True)

    col1, col_v, col2 = st.columns([10, 1.2, 10])
    
    with col1:
        if st.button(f"**{p1['nombre']}**\n\n{p1['desc']}", key=f"btn_{i}"):
            elegir_ganador(p1)
            st.rerun()

    with col_v:
        st.markdown('<div class="vs-container"><div class="vs-circle">VS</div></div>', unsafe_allow_html=True)

    with col2:
        if st.button(f"**{p2['nombre']}**\n\n{p2['desc']}", key=f"btn_{i+1}"):
            elegir_ganador(p2)
            st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    progreso = (int(i/2) + 1) / (len(st.session_state.competidores)/2)
    st.progress(progreso)
