import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation Battle", layout="wide")

st.markdown("""
    <style>
    /* FORZAR ANCHO REAL AL 95% */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 95% !important;
        padding-left: 2% !important;
        padding-right: 2% !important;
        padding-top: 1rem !important;
        margin: auto !important;
    }

    /* Fondo y visibilidad */
    .stApp { background-color: #F4F7F9; }
    
    /* Título compacto */
    h1 {
        font-size: 1.6rem !important;
        text-align: center;
        margin: 0 !important;
        padding: 0 0 10px 0 !important;
        color: #1E1E1E !important;
    }

    /* Criterio centrado y compacto */
    .criterio-box { 
        background-color: #FFFFFF; 
        padding: 10px; 
        border-radius: 10px; 
        border-left: 8px solid #FF4B4B; 
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        text-align: center;
    }

    /* BOTONES DE DUELO: Forzar que ocupen el ancho */
    .stButton > button { 
        width: 100% !important; 
        height: 85px !important;
        background-color: #FFFFFF !important;
        color: #4B90FF !important;
        font-size: 1.2rem !important; 
        font-weight: bold !important; 
        border: 4px solid #4B90FF !important;
        border-radius: 15px !important;
        white-space: normal !important; /* Permite que el texto salte de línea */
    }
    
    .stButton > button:hover {
        background-color: #4B90FF !important;
        color: white !important;
    }
    
    .vs-text { 
        text-align: center; 
        font-size: 30px; 
        font-weight: 900; 
        color: #FF4B4B !important; 
        line-height: 85px; /* Alinea con el centro de los botones */
        margin: 0 !important;
    }

    .desc-text {
        text-align: center;
        font-size: 0.9rem;
        min-height: 35px;
        margin-bottom: 5px;
        color: #444 !important;
    }

    .cat-label {
        text-align: center;
        font-size: 0.75rem;
        font-weight: bold;
        color: #888 !important;
        margin-bottom: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (QR Y MENÚ) ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Configuración</h2>", unsafe_allow_html=True)
    if st.button("⚠️ Reiniciar partida"):
        st.session_state.clear()
        st.rerun()
    
    st.divider()
    
    # Texto con color forzado para que se vea sí o sí
    st.markdown("<h3 style='color:white !important; background-color:transparent;'>📢 Invita a jugar</h3>", unsafe_allow_html=True)
    
    # Cambia esta URL por la tuya
    url = "https://juego-ods-battle.streamlit.app/" 
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=True)

# 2. Base de datos corregida (Natural)
PROBLEMAS = [
    {"nombre": "Pobreza menstrual", "cat": "Derechos humanos", "desc": "Falta de acceso a productos de higiene."},
    {"nombre": "Desnutrición oculta", "cat": "Necesidades básicas", "desc": "Carencia de vitaminas críticas."},
    {"nombre": "Brecha digital rural", "cat": "Derechos humanos", "desc": "Falta de internet en el campo."},
    {"nombre": "Acceso a agua limpia", "cat": "Necesidades básicas", "desc": "Contaminación de fuentes locales."},
    {"nombre": "Moda rápida", "cat": "Medio ambiente", "desc": "Contaminación por descarte masivo de ropa."},
    {"nombre": "Calidad del aire", "cat": "Medio ambiente", "desc": "Polución cerca de las escuelas."},
    {"nombre": "Protección de abejas", "cat": "Medio ambiente", "desc": "Uso de pesticidas peligrosos."},
    {"nombre": "Desperdicio de energía", "cat": "Medio ambiente", "desc": "Consumo en edificios vacíos."},
    {"nombre": "Acoso y grooming", "cat": "Seguridad", "desc": "Riesgos para menores en internet."},
    {"nombre": "Transporte seguro", "cat": "Seguridad", "desc": "Acoso en paradas y buses."},
    {"nombre": "Alertas de desastre", "cat": "Seguridad", "desc": "Sistemas de aviso ineficientes."},
    {"nombre": "Ciberestafas", "cat": "Seguridad", "desc": "Robos a personas mayores online."},
    {"nombre": "Salud mental joven", "cat": "Social", "desc": "Ansiedad por redes sociales."},
    {"nombre": "Inclusión laboral", "cat": "Social", "desc": "Falta de empleo para discapacitados."},
    {"nombre": "Huella de carbono", "cat": "Acción individual", "desc": "Dificultad para medir el impacto personal."},
    {"nombre": "Comercio local", "cat": "Acción individual", "desc": "Desventaja frente a grandes tiendas."}
]

if 'competidores' not in st.session_state:
    random.shuffle(PROBLEMAS)
    st.session_state.competidores = PROBLEMAS
    st.session_state.ganadores_ronda_actual = []
    st.session_state.indice_duelo = 0
    st.session_state.ronda_nombre = "Octavos de final"

CRITERIOS = {
    "Octavos de final": {"t": "📍 Ronda 1: Impacto", "p": "¿Cuál es más urgente?"},
    "Cuartos de final": {"t": "💻 Ronda 2: Viabilidad", "p": "¿Cuál es más fácil de resolver?"},
    "Semifinal": {"t": "👤 Ronda 3: Usuario", "p": "¿Cuál tiene usuarios claros?"},
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
st.markdown("<h1>🏆 Technovation Battle</h1>", unsafe_allow_html=True)

if st.session_state.ronda_nombre == "¡Ganador!":
    ganador = st.session_state.ganadores_ronda_actual[0]
    st.balloons()
    st.markdown(f"<div style='text-align:center;'><h2>¡Ganador!</h2><h1 style='color:#FF4B4B !important; font-size:3rem !important;'>{ganador['nombre']}</h1></div>", unsafe_allow_html=True)
    if st.button("Reiniciar todo"):
        st.session_state.clear()
        st.rerun()
else:
    info = CRITERIOS.get(st.session_state.ronda_nombre, CRITERIOS["Octavos de final"])
    st.markdown(f'''
        <div class="criterio-box">
            <h2 style="margin:0; font-size:1.1rem;">{info["t"]}</h2>
            <p style="margin:0; font-size:0.9rem;">{info["p"]}</p>
        </div>
    ''', unsafe_allow_html=True)

    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]

    # PROPORCIÓN PARA QUE LOS BOTONES SEAN ANCHOS
    col_izq, col_vs, col_der = st.columns([12, 3, 12])
    
    with col_izq:
        st.markdown(f"<p class='cat-label'>{p1['cat']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='desc-text'>{p1['desc']}</p>", unsafe_allow_html=True)
        if st.button(p1['nombre'], key=f"b{i}"): 
            elegir_ganador(p1); st.rerun()

    with col_vs:
        st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)

    with col_der:
        st.markdown(f"<p class='cat-label'>{p2['cat']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='desc-text'>{p2['desc']}</p>", unsafe_allow_html=True)
        if st.button(p2['nombre'], key=f"b{i+1}"): 
            elegir_ganador(p2); st.rerun()

    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    st.progress((int(i/2) + 1) / (len(st.session_state.competidores)/2))
