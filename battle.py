import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation Battle", layout="wide")

st.markdown("""
    <style>
    /* 1. ESTRUCTURA Y FONDO */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 98% !important;
        padding: 0.5rem !important;
        margin: auto !important;
    }
    .stApp { background-color: #F4F7F9; }

    /* 2. DISEÑO DE TARJETAS (IGUAL QUE LA RONDA) */
    .card-style {
        background-color: #FFFFFF;
        padding: 12px;
        border-radius: 12px;
        border-left: 8px solid #4B90FF; /* Azul para las opciones */
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 10px;
    }
    
    /* Caja de la ronda (Roja) */
    .criterio-box {
        background-color: #FFFFFF;
        padding: 10px;
        border-radius: 12px;
        border-left: 8px solid #FF4B4B; /* Rojo para la ronda */
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        text-align: center;
    }

    /* 3. TEXTOS */
    h1 { font-size: 1.5rem !important; text-align: center; color: #1E1E1E !important; margin: 0 0 10px 0 !important; }
    .criterio-box h2 { color: #1E1E1E !important; font-size: 1.1rem !important; margin: 0; }
    .criterio-box p { color: #444 !important; font-size: 0.9rem !important; margin: 0; }
    .desc-text { color: #555 !important; font-size: 0.85rem; margin-bottom: 8px; min-height: 35px; line-height: 1.2; }

    /* 4. BOTONES DENTRO DE TARJETAS */
    .stButton > button {
        width: 100% !important;
        height: 60px !important;
        background-color: #4B90FF !important; /* Botón sólido para que resalte */
        color: white !important;
        font-size: 1rem !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        text-transform: none !important;
    }
    
    /* 5. BOTÓN REINICIAR (SIDEBAR) */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #FF4B4B !important;
        color: white !important;
        font-size: 1.1rem !important;
        height: 50px !important;
        border: 2px solid white !important;
    }

    /* Forzar que las columnas no se apilen en móvil */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 8px !important;
        align-items: flex-end !important;
    }
    
    .vs-text {
        font-size: 1.4rem;
        font-weight: 900;
        color: #FF4B4B;
        padding-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Menú</h2>", unsafe_allow_html=True)
    if st.button("REINICIAR PARTIDA"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    st.markdown("<h3 style='color:white;'>📢 Invita a jugar</h3>", unsafe_allow_html=True)
    url = "https://juego-ods-battle.streamlit.app/" 
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=True)

# 2. Lógica de juego
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

# --- UI ---
st.markdown("<h1>🏆 Technovation Battle</h1>", unsafe_allow_html=True)

if st.session_state.ronda_nombre == "¡Ganador!":
    ganador = st.session_state.ganadores_ronda_actual[0]
    st.balloons()
    st.markdown(f"<div class='card-style' style='border-left-color:#FF4B4B;'><h2>¡Ganador!</h2><h1 style='color:#FF4B4B !important;'>{ganador['nombre']}</h1></div>", unsafe_allow_html=True)
    if st.button("NUEVA PARTIDA"):
        st.session_state.clear()
        st.rerun()
else:
    info = CRITERIOS.get(st.session_state.ronda_nombre, CRITERIOS["Octavos de final"])
    st.markdown(f'<div class="criterio-box"><h2>{info["t"]}</h2><p>{info["p"]}</p></div>', unsafe_allow_html=True)

    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]

    col1, col_v, col2 = st.columns([10, 2, 10])
    
    with col1:
        st.markdown(f'''<div class="card-style">
            <p class="desc-text">{p1['desc']}</p>
        </div>''', unsafe_allow_html=True)
        if st.button(p1['nombre'], key=f"btn_{i}"):
            elegir_ganador(p1)
            st.rerun()

    with col_v:
        st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)

    with col2:
        st.markdown(f'''<div class="card-style">
            <p class="desc-text">{p2['desc']}</p>
        </div>''', unsafe_allow_html=True)
        if st.button(p2['nombre'], key=f"btn_{i+1}"):
            elegir_ganador(p2)
            st.rerun()

    st.progress((int(i/2) + 1) / (len(st.session_state.competidores)/2))
