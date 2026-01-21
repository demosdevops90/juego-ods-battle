import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation Battle", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS "Rompe-Contenedores" para forzar el ancho completo
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* 1. Forzar el contenedor raíz a ocupar todo el ancho */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        width: 100% !important;
        padding: 1rem !important;
        margin: 0 !important;
    }

    /* 2. Quitar el límite de ancho de los bloques verticales internos */
    [data-testid="stVerticalBlock"] {
        width: 100% !important;
        align-items: center !important;
    }

    /* 3. FORZAR FILA HORIZONTAL PURA (Evita que se pongan uno encima de otro) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* Prohibido bajar de línea */
        width: 100% !important;
        gap: 2px !important;
        justify-content: center !important;
    }

    /* 4. Ajuste de columnas para que no se achiquen */
    [data-testid="column"] {
        flex: 1 1 45% !important; /* Cada botón toma el 45% */
        min-width: 45% !important;
        max-width: 48% !important;
    }
    
    [data-testid="column"]:nth-of-type(2) {
        flex: 0 0 auto !important;
        min-width: 40px !important;
        width: 40px !important;
    }

    /* 5. DISEÑO DE BOTONES AL 15% DE ALTO */
    div.stButton > button {
        width: 100% !important;
        height: 15vh !important;
        background-color: #272D3A !important;
        color: white !important;
        border-radius: 0.8rem !important;
        border: 2px solid #00bdc7 !important; /* Borde visible para depurar */
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 5px !important;
    }

    /* Diferenciar colores */
    [data-testid="column"]:nth-of-type(3) button {
        border-color: #EE40DA !important;
    }

    /* VS Circle */
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
        font-size: 0.7rem;
        box-shadow: 0 0 10px rgba(238, 64, 218, 0.5);
    }

    .glass-header {
        background: rgba(24, 28, 38, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 0.5rem;
        text-align: center;
        width: 95%;
        margin-bottom: 1rem;
    }

    header, footer {visibility: hidden;}
    .stApp { background-color: #181c26; }
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
    
    # RENDER DE BATALLA
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

    st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
    progreso = (int(i/2) + 1) / (len(st.session_state.competidores)/2)
    st.progress(progreso)
