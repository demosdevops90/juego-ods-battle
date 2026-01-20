import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation Battle", layout="wide")

st.markdown("""
    <style>
    /* 1. CONTENEDOR TOTAL AL 95% */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 95% !important;
        padding: 1rem !important;
        margin: auto !important;
    }
    .stApp { background-color: #F4F7F9; }

    /* 2. ESTILO UNIFICADO DE TARJETAS (ROJA Y AZULES) */
    .criterio-box, .stButton > button {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
        width: 100% !important;
        margin-bottom: 10px !important;
        display: block !important;
        text-align: center !important;
    }

    /* Tarjeta Roja (Ronda) */
    .criterio-box {
        padding: 15px;
        border-left: 10px solid #FF4B4B !important;
    }
    .criterio-box h2 { color: #1E1E1E !important; font-size: 1.2rem !important; margin: 0; }
    .criterio-box p { color: #444 !important; font-size: 1rem !important; margin: 5px 0 0 0; }

    /* Tarjetas Azules (Problemas) */
    .stButton > button {
        height: auto !important;
        min-height: 110px !important;
        padding: 15px !important;
        border-left: 10px solid #4B90FF !important;
        border-top: none !important;
        border-right: none !important;
        border-bottom: none !important;
        transition: transform 0.2s ease;
        white-space: normal !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        background-color: #F0F7FF !important;
    }

    /* 3. VS CENTRADO Y ESTILIZADO */
    .vs-divider {
        text-align: center;
        font-size: 1.8rem;
        font-weight: 900;
        color: #FF4B4B;
        margin: 10px 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .vs-divider::before, .vs-divider::after {
        content: "";
        flex: 1;
        border-bottom: 2px solid #DDD;
        margin: 0 15px;
    }

    /* 4. SIDEBAR (FONDO OSCURO Y BOTÓN ROJO) */
    [data-testid="stSidebar"] { background-color: #1E1E1E !important; }
    [data-testid="stSidebar"] * { color: white !important; }
    
    [data-testid="stSidebar"] .stButton > button {
        background-color: #FF4B4B !important;
        color: white !important;
        border: none !important;
        height: 50px !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        margin-top: 10px !important;
    }

    /* Ocultar elementos de Streamlit que sobran */
    header, footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("## MENÚ")
    if st.button("REINICIAR JUEGO"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    st.markdown("<p style='text-align:center;'>📢 Invita a jugar</p>", unsafe_allow_html=True)
    url = "https://juego-ods-battle.streamlit.app/" 
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=True)

# 2. Inicialización de datos
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
    "Cuartos de final": {"t": "💻 Ronda 2: Viabilidad", "p": "¿Cuál es más fácil de resolver?"},
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

# --- INTERFAZ PRINCIPAL ---
st.markdown("<h1 style='text-align:center; color:#1E1E1E; margin-bottom:10px;'>🏆 ODS BATTLE</h1>", unsafe_allow_html=True)

if st.session_state.ronda_nombre == "¡Ganador!":
    ganador = st.session_state.ganadores_ronda_actual[0]
    st.balloons()
    st.markdown(f"<div class='criterio-box' style='padding:40px;'><h2>🏆 ¡GANADOR! 🏆</h2><h1 style='color:#FF4B4B !important; font-size:2.5rem !important;'>{ganador['nombre']}</h1></div>", unsafe_allow_html=True)
    if st.button("JUGAR DE NUEVO"):
        st.session_state.clear()
        st.rerun()
else:
    # Mostrar Ronda
    info = CRITERIOS.get(st.session_state.ronda_nombre, CRITERIOS["Octavos de final"])
    st.markdown(f'<div class="criterio-box"><h2>{info["t"]}</h2><p>{info["p"]}</p></div>', unsafe_allow_html=True)

    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]

    # OPCIÓN 1
    # Usamos saltos de línea para separar descripción de nombre dentro del botón
    if st.button(f"{p1['desc'].upper()}\n\n{p1['nombre']}", key=f"p1_{i}"):
        elegir_ganador(p1)
        st.rerun()

    # SEPARADOR VS
    st.markdown('<div class="vs-divider">VS</div>', unsafe_allow_html=True)

    # OPCIÓN 2
    if st.button(f"{p2['desc'].upper()}\n\n{p2['nombre']}", key=p2_f"{i}"):
        elegir_ganador(p2)
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.progress((int(i/2) + 1) / (len(st.session_state.competidores)/2))
