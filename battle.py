import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página (IMPORTANTE: Esto debe ir primero)
st.set_page_config(page_title="Technovation Battle", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* 1. FORZAR ANCHO TOTAL Y ELIMINAR MÁRGENES LATERALES */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
        margin: 0 auto !important;
    }

    /* 2. DISEÑO DE TARJETAS UNIFICADO (Ronda y Problemas) */
    /* Caja de Ronda (Roja) */
    .criterio-box {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 12px;
        border-left: 10px solid #FF4B4B;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
        width: 100%;
    }
    .criterio-box h2 { color: #1E1E1E !important; font-size: 1.2rem !important; margin: 0; }
    .criterio-box p { color: #444 !important; font-size: 1rem !important; margin-top: 5px; }

    /* 3. BOTONES QUE SON LA TARJETA (Azules) */
    /* Estilizamos el botón para que parezca la tarjeta de la ronda */
    .stButton > button {
        width: 100% !important;
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        border-left: 10px solid #4B90FF !important; /* Borde azul igual al rojo de arriba */
        border-top: none !important;
        border-right: none !important;
        border-bottom: none !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
        padding: 20px !important;
        height: auto !important;
        min-height: 120px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: normal !important;
        color: #1E1E1E !important;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #F0F7FF !important;
        transform: translateY(-2px);
    }

    /* 4. VS CENTRADO Y ESTILIZADO */
    .vs-divider {
        text-align: center;
        font-size: 2rem;
        font-weight: 900;
        color: #FF4B4B;
        margin: 15px 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }

    /* 5. SIDEBAR (Recuperar visibilidad y estilo) */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    /* Botón de reinicio en Sidebar */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #FF4B4B !important;
        border: none !important;
        height: 50px !important;
        min-height: 50px !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        color: white !important;
    }

    /* Ocultar basura de Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>MENÚ</h2>", unsafe_allow_html=True)
    if st.button("REINICIAR PARTIDA"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    st.markdown("<p style='text-align:center; font-weight:bold;'>📢 Invita a jugar</p>", unsafe_allow_html=True)
    
    url = "https://juego-ods-battle.streamlit.app/" 
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=True)

# 2. Datos y Lógica
if 'competidores' not in st.session_state:
    PROBLEMAS = [
        {"nombre": "Comercio local", "desc": "Tiendas de barrio"},
        {"nombre": "Salud mental joven", "desc": "Ansiedad por redes"},
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
        {"nombre": "Ciberestafas", "desc": "Robos a abuelos"},
        {"nombre": "Inclusión laboral", "desc": "Barreras trabajo"},
        {"nombre": "Huella carbono", "desc": "Impacto personal"}
    ]
    random.shuffle(PROBLEMAS)
    st.session_state.competidores = PROBLEMS
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

# --- UI PRINCIPAL ---
st.markdown("<h1 style='text-align:center; color:#1E1E1E; margin-bottom:5px;'>🏆 ODS BATTLE</h1>", unsafe_allow_html=True)

if st.session_state.ronda_nombre == "¡Ganador!":
    ganador = st.session_state.ganadores_ronda_actual[0]
    st.balloons()
    st.markdown(f"<div class='criterio-box' style='padding:40px;'><h2>🏆 ¡GANADOR! 🏆</h2><h1 style='color:#FF4B4B !important; font-size:2.5rem !important;'>{ganador['nombre']}</h1></div>", unsafe_allow_html=True)
    if st.button("JUGAR DE NUEVO"):
        st.session_state.clear()
        st.rerun()
else:
    info = CRITERIOS.get(st.session_state.ronda_nombre, CRITERIOS["Octavos de final"])
    st.markdown(f'<div class="criterio-box"><h2>{info["t"]}</h2><p>{info["p"]}</p></div>', unsafe_allow_html=True)

    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]

    # Tarjeta 1 (Botón que contiene descripción y nombre)
    if st.button(f"{p1['desc']}\n\n{p1['nombre']}", key=f"btn_p1_{i}"):
        elegir_ganador(p1)
        st.rerun()

    st.markdown('<div class="vs-divider">VS</div>', unsafe_allow_html=True)

    # Tarjeta 2
    if st.button(f"{p2['desc']}\n\n{p2['nombre']}", key=f"btn_p2_{i}"):
        elegir_ganador(p2)
        st.rerun()

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    st.progress((int(i/2) + 1) / (len(st.session_state.competidores)/2))
