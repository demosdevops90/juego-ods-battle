import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation Battle", layout="wide")

# Estilos CSS corregidos para visibilidad total y centrado en móvil
st.markdown("""
    <style>
    /* Forzar ancho y eliminar scroll innecesario */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 98% !important;
        padding: 0.5rem !important;
        margin: auto !important;
    }

    .stApp { background-color: #F4F7F9; }

    /* Texto del Sidebar (QR) siempre visible */
    [data-testid="stSidebar"] * { color: white !important; }

    /* Título compacto */
    .main-title {
        font-size: 1.4rem;
        font-weight: bold;
        text-align: center;
        color: #1E1E1E;
        margin-bottom: 5px;
    }

    /* Caja de Ronda/Criterio - TEXTO NEGRO GARANTIZADO */
    .criterio-box {
        background-color: #FFFFFF;
        padding: 8px;
        border-radius: 10px;
        border-left: 6px solid #FF4B4B;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        text-align: center;
    }
    .criterio-box h2 { color: #1E1E1E !important; font-size: 1rem !important; margin: 0; }
    .criterio-box p { color: #444444 !important; font-size: 0.85rem !important; margin: 0; }

    /* Estructura de duelo para que no se rompa en móvil */
    .battle-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 5px;
        width: 100%;
    }

    /* Botón personalizado vía Streamlit */
    .stButton > button {
        width: 100% !important;
        height: 100px !important;
        background-color: #FFFFFF !important;
        color: #4B90FF !important;
        font-size: 0.9rem !important;
        font-weight: bold !important;
        border: 3px solid #4B90FF !important;
        border-radius: 12px !important;
        line-height: 1.1 !important;
        padding: 5px !important;
    }

    .vs-text {
        font-size: 1.5rem;
        font-weight: 900;
        color: #FF4B4B !important;
        text-align: center;
    }

    .desc-small {
        font-size: 0.75rem;
        color: #666;
        text-align: center;
        min-height: 35px;
        line-height: 1;
        margin-bottom: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## Menú")
    if st.button("⚠️ Reiniciar juego"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    st.markdown("### 📢 Invita a jugar")
    url = "https://tu-app.streamlit.app" 
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=True)

# 2. Lógica y Base de Datos
if 'competidores' not in st.session_state:
    PROBLEMAS = [
        {"nombre": "Pobreza menstrual", "desc": "Falta de acceso a higiene."},
        {"nombre": "Desnutrición oculta", "desc": "Carencia de vitaminas."},
        {"nombre": "Brecha digital rural", "desc": "Falta de internet en campo."},
        {"nombre": "Acceso a agua limpia", "desc": "Agua contaminada."},
        {"nombre": "Moda rápida", "desc": "Desecho masivo de ropa."},
        {"nombre": "Calidad del aire", "desc": "Humo cerca de escuelas."},
        {"nombre": "Protección de abejas", "desc": "Uso de pesticidas."},
        {"nombre": "Desperdicio energía", "desc": "Luces encendidas sin uso."},
        {"nombre": "Acoso y grooming", "desc": "Riesgos para menores."},
        {"nombre": "Transporte seguro", "desc": "Acoso en buses."},
        {"nombre": "Alertas de desastre", "desc": "Avisos de emergencia."},
        {"nombre": "Ciberestafas", "desc": "Robos a abuelos online."},
        {"nombre": "Salud mental joven", "desc": "Ansiedad por redes."},
        {"nombre": "Inclusión laboral", "desc": "Barreras trabajo."},
        {"nombre": "Huella carbono", "desc": "Impacto personal."},
        {"nombre": "Comercio local", "desc": "Tiendas de barrio."}
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

# --- UI ---
st.markdown('<p class="main-title">🏆 Technovation Battle</p>', unsafe_allow_html=True)

if st.session_state.ronda_nombre == "¡Ganador!":
    ganador = st.session_state.ganadores_ronda_actual[0]
    st.balloons()
    st.markdown(f"<div style='text-align:center; color:black;'><h2>¡Ganador!</h2><h1>{ganador['nombre']}</h1></div>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.clear()
        st.rerun()
else:
    info = CRITERIOS.get(st.session_state.ronda_nombre, CRITERIOS["Octavos de final"])
    st.markdown(f'''
        <div class="criterio-box">
            <h2>{info["t"]}</h2>
            <p>{info["p"]}</p>
        </div>
    ''', unsafe_allow_html=True)

    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]

    # Usamos columnas fijas de Streamlit pero con el CSS de arriba forzamos que no se apilen
    col1, col_v, col2 = st.columns([10, 3, 10])
    
    with col1:
        st.markdown(f"<p class='desc-small'>{p1['desc']}</p>", unsafe_allow_html=True)
        if st.button(p1['nombre'], key=f"btn_{i}"):
            elegir_ganador(p1)
            st.rerun()

    with col_v:
        st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<p class='desc-small'>{p2['desc']}</p>", unsafe_allow_html=True)
        if st.button(p2['nombre'], key=f"btn_{i+1}"):
            elegir_ganador(p2)
            st.rerun()

    st.progress((int(i/2) + 1) / (len(st.session_state.competidores)/2))
