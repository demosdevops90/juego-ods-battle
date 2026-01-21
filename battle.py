import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation Battle", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS para forzar Layout Horizontal "Side-by-Side"
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Reset de visualización */
    html, body, [data-testid="stAppViewBlockContainer"] {
        max-height: 100vh;
        overflow: hidden !important;
        font-family: 'Space Grotesk', sans-serif;
        background-color: #181c26;
    }

    .stApp { background-color: #181c26; }
    header, footer {visibility: hidden;}

    /* Contenedor principal centrado al 95% */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 95% !important;
        margin: auto !important;
        padding: 1rem 0.5rem !important;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* FORZAR FILA HORIZONTAL EN CUALQUIER PANTALLA */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important; /* Siempre horizontal */
        flex-wrap: nowrap !important;  /* No permite saltar de línea */
        align-items: center !important;
        justify-content: center !important;
        gap: 2px !important; /* Espacio mínimo */
        width: 100% !important;
    }

    /* Ajuste de columnas para que no se colapsen */
    [data-testid="column"] {
        width: 45% !important;
        min-width: 45% !important;
        flex: 1 1 auto !important;
    }
    
    /* Columna del VS (estrecha) */
    [data-testid="column"]:nth-of-type(2) {
        width: 10% !important;
        min-width: 40px !important;
        flex: 0 0 auto !important;
        display: flex;
        justify-content: center;
    }

    /* BOTONES AL 15% DE ALTO */
    div.stButton > button {
        width: 100% !important;
        height: 15vh !important;
        min-height: 15vh !important;
        background-color: #272D3A !important;
        color: white !important;
        border-radius: 0.8rem !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        padding: 0.5rem !important;
        font-size: 0.8rem !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }

    /* Decoración de bordes */
    [data-testid="column"]:nth-of-type(1) button { border-color: #00bdc7 !important; }
    [data-testid="column"]:nth-of-type(3) button { border-color: #EE40DA !important; }

    /* VS CIRCLE */
    .vs-circle {
        width: 35px;
        height: 35px;
        background: #181c26;
        border: 2px solid #EE40DA;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #EE40DA;
        font-weight: 900;
        font-size: 0.7rem;
        box-shadow: 0 0 10px rgba(238, 64, 218, 0.5);
    }

    .glass-header {
        background: rgba(24, 28, 38, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 0.5rem;
        text-align: center;
        width: 100%;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
if 'competidores' not in st.session_state:
    PROBLEMAS = [
        {"nombre": "Pobreza menstrual", "desc": "Acceso a higiene"},
        {"nombre": "Desnutrición", "desc": "Carencia vitaminas"},
        {"nombre": "Brecha digital", "desc": "Internet rural"},
        {"nombre": "Agua limpia", "desc": "Agua contaminada"},
        {"nombre": "Moda rápida", "desc": "Descarte ropa"},
        {"nombre": "Calidad aire", "desc": "Humo en escuelas"},
        {"nombre": "Acoso online", "desc": "Grooming"},
        {"nombre": "Transporte", "desc": "Acoso en buses"}
    ]
    random.shuffle(PROBLEMAS)
    st.session_state.competidores = PROBLEMAS
    st.session_state.ganadores_ronda_actual = []
    st.session_state.indice_duelo = 0
    st.session_state.ronda_nombre = "Octavos de final"

CRITERIOS = {
    "Octavos de final": {"t": "📍 Ronda 1: Impacto", "p": "¿Cuál es más urgente?"},
    "Cuartos de final": {"t": "💻 Ronda 2: Viabilidad", "p": "¿Cuál es más fácil?"},
    "Semifinal": {"t": "👤 Ronda 3: Usuario", "p": "¿Quién tiene usuarios?"},
    "Gran final": {"t": "❤️ Final: Pasión", "p": "¿Cuál motiva más?"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## MENÚ")
    if st.button("REINICIAR PARTIDA"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    url = "https://tu-app.streamlit.app/"
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=True)

# --- UI ---
info = CRITERIOS.get(st.session_state.ronda_nombre, CRITERIOS["Octavos de final"])

st.markdown(f'<div class="glass-header"><h2 style="color:white; margin:0; font-size:1rem;">{info["t"]}</h2><p style="color:#9ababc; margin:0; font-size:0.8rem;">{info["p"]}</p></div>', unsafe_allow_html=True)

if st.session_state.ronda_nombre == "¡Ganador!":
    st.balloons()
    st.markdown(f'<h1 style="color:white; text-align:center;">🏆 {st.session_state.ganadores_ronda_actual[0]["nombre"]}</h1>', unsafe_allow_html=True)
else:
    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]
    
    # Render de Batalla
    col1, col_v, col2 = st.columns([10, 2, 10])
    
    with col1:
        if st.button(f"**{p1['nombre']}**\n\n{p1['desc']}", key=f"btn_{i}"):
            st.session_state.ganadores_ronda_actual.append(p1)
            st.session_state.indice_duelo += 2
            st.rerun()

    with col_v:
        st.markdown('<div class="vs-circle">VS</div>', unsafe_allow_html=True)

    with col2:
        if st.button(f"**{p2['nombre']}**\n\n{p2['desc']}", key=f"btn_{i+1}"):
            st.session_state.ganadores_ronda_actual.append(p2)
            st.session_state.indice_duelo += 2
            st.rerun()

    # Barra inferior
    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    progreso = (int(i/2) + 1) / (len(st.session_state.competidores)/2)
    st.progress(progreso)
