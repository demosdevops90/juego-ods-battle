import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation ODS Battle", layout="wide")

st.markdown("""
    <style>
    /* FORZAR ANCHO DEL 90% Y CENTRADO */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 95% !important;
        padding-top: 1rem !important;
        padding-left: 5% !important;
        padding-right: 5% !important;
        margin: 0 auto !important;
    }

    /* Fondo y colores globales */
    .stApp { background-color: #F4F7F9; }
    h1, h2, h3, p, span { color: #1E1E1E !important; }
    
    /* Título compacto para evitar scroll */
    h1 {
        font-size: 1.8rem !important;
        text-align: center;
        margin: 0px 0px 10px 0px !important;
        padding: 0px !important;
    }

    /* Caja de criterios más compacta */
    .criterio-box { 
        background-color: #FFFFFF; 
        padding: 10px 20px; 
        border-radius: 12px; 
        border-left: 8px solid #FF4B4B; 
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        text-align: center;
    }

    /* Texto de descripción compacto */
    .desc-text {
        font-size: 1rem;
        margin-bottom: 8px;
        min-height: 40px;
        text-align: center;
        line-height: 1.2;
    }

    /* BOTONES GRANDES Y CENTRADOS */
    .stButton > button { 
        width: 100% !important; 
        height: 90px !important; /* Altura reducida para evitar scroll */
        background-color: #FFFFFF !important;
        color: #4B90FF !important;
        font-size: 1.4rem !important; 
        font-weight: bold !important; 
        border: 4px solid #4B90FF !important;
        border-radius: 15px !important;
    }
    
    .stButton > button:hover {
        background-color: #4B90FF !important;
        color: white !important;
    }
    
    /* VS centrado verticalmente */
    .vs-text { 
        text-align: center; 
        font-size: 35px; 
        font-weight: 900; 
        color: #FF4B4B; 
        margin-top: 45px;
    }

    .cat-label {
        text-align: center;
        font-size: 0.8rem;
        font-weight: 700;
        color: #888 !important;
        margin-bottom: 2px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("Menú")
    if st.button("⚠️ Reiniciar juego"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    st.markdown("📢 **Invita a jugar**")
    url = "https://juego-ods-battle.streamlit.app/" 
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=True)

# 2. Base de datos (Redacción natural)
PROBLEMAS = [
    {"nombre": "Pobreza menstrual", "cat": "Derechos humanos", "desc": "Falta de acceso a productos de higiene y educación básica."},
    {"nombre": "Desnutrición oculta", "cat": "Necesidades básicas", "desc": "Dietas con carencia de vitaminas y minerales críticos."},
    {"nombre": "Brecha digital rural", "cat": "Derechos humanos", "desc": "Falta de conexión a internet y equipos en el campo."},
    {"nombre": "Acceso a agua limpia", "cat": "Necesidades básicas", "desc": "Contaminación de pozos y fuentes de agua locales."},
    {"nombre": "Moda rápida", "cat": "Medio ambiente", "desc": "Impacto ambiental por el descarte masivo de ropa barata."},
    {"nombre": "Calidad del aire", "cat": "Medio ambiente", "desc": "Presencia de humos y polución cerca de las escuelas."},
    {"nombre": "Protección de abejas", "cat": "Medio ambiente", "desc": "Uso de pesticidas que afectan a los polinizadores."},
    {"nombre": "Desperdicio de energía", "cat": "Medio ambiente", "desc": "Consumo innecesario en edificios públicos vacíos."},
    {"nombre": "Acoso y grooming", "cat": "Seguridad", "desc": "Riesgos de engaños de adultos a menores en internet."},
    {"nombre": "Transporte seguro", "cat": "Seguridad", "desc": "Prevención del acoso en paradas y transporte público."},
    {"nombre": "Alertas de desastre", "cat": "Seguridad", "desc": "Sistemas deficientes de aviso ante emergencias naturales."},
    {"nombre": "Ciberestafas", "cat": "Seguridad", "desc": "Robo de datos y ahorros enfocado en personas mayores."},
    {"nombre": "Salud mental joven", "cat": "Social", "desc": "Aumento de ansiedad ligada al uso de redes sociales."},
    {"nombre": "Inclusión laboral", "cat": "Social", "desc": "Barreras para el trabajo de personas con discapacidad."},
    {"nombre": "Huella de carbono", "cat": "Acción individual", "desc": "Dificultad para medir el impacto ambiental personal."},
    {"nombre": "Comercio local", "cat": "Acción individual", "desc": "Desventaja de tiendas de barrio frente a grandes plataformas."}
]

# Inicialización
if 'competidores' not in st.session_state:
    random.shuffle(PROBLEMAS)
    st.session_state.competidores = PROBLEMAS
    st.session_state.ganadores_ronda_actual = []
    st.session_state.indice_duelo = 0
    st.session_state.ronda_nombre = "Octavos de final"

CRITERIOS = {
    "Octavos de final": {"t": "📍 Ronda 1: Impacto", "p": "¿Cuál es más urgente en tu comunidad?"},
    "Cuartos de final": {"t": "💻 Ronda 2: Viabilidad", "p": "¿Cuál es más fácil de resolver con una app?"},
    "Semifinal": {"t": "👤 Ronda 3: Usuario", "p": "¿Cuál tiene un grupo de usuarios más claro?"},
    "Gran final": {"t": "❤️ Final: Pasión", "p": "¿Cuál les motiva más para trabajar?"}
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
    st.markdown(f"<div style='text-align:center; padding: 20px;'><h2>El proyecto ganador es:</h2><h1 style='font-size:3.5rem !important; color:#FF4B4B !important;'>{ganador['nombre']}</h1></div>", unsafe_allow_html=True)
    if st.button("Nueva partida"):
        st.session_state.clear()
        st.rerun()
else:
    info = CRITERIOS.get(st.session_state.ronda_nombre, CRITERIOS["Octavos de final"])
    st.markdown(f'''
        <div class="criterio-box">
            <h2 style="margin:0; font-size:1.2rem;">{info["t"]}</h2>
            <p style="margin:0; font-size:1rem; color:#555 !important;">{info["p"]}</p>
        </div>
    ''', unsafe_allow_html=True)

    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]

    # CONTENEDOR DE DUELO AL 90%
    col_izq, col_vs, col_der = st.columns([10, 2, 10])
    
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

    st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
    progreso = (int(i/2) + 1) / (len(st.session_state.competidores)/2)
    st.progress(progreso)
