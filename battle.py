import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation Battle", layout="wide")

st.markdown("""
    <style>
    /* 1. ELIMINAR ESPACIOS Y BARRAS DE STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        max-width: 98% !important;
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        margin: auto;
    }

    /* 2. COLORES Y FUENTES */
    .stApp { background-color: #F4F7F9; }
    
    /* Forzar visibilidad del texto en el Sidebar (QR) */
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important; /* Texto blanco para fondo oscuro del sidebar */
    }
    
    h1 {
        font-size: 1.4rem !important; /* Título muy pequeño para ahorrar alto */
        text-align: center;
        margin: 0 !important;
        padding: 5px 0 !important;
        color: #1E1E1E !important;
    }

    /* 3. CONTENEDORES COMPACTOS */
    .criterio-box { 
        background-color: #FFFFFF; 
        padding: 8px 15px; 
        border-radius: 10px; 
        border-left: 5px solid #FF4B4B; 
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    
    .criterio-box h2 { font-size: 1rem !important; margin:0 !important; color: #1E1E1E !important;}
    .criterio-box p { font-size: 0.85rem !important; margin:0 !important; color: #444 !important;}

    .desc-text {
        color: #444 !important;
        font-size: 0.85rem;
        margin-bottom: 4px;
        min-height: 30px;
        text-align: center;
        line-height: 1.1;
    }

    /* 4. BOTONES ULTRA-COMPACTOS (SIN SCROLL) */
    .stButton > button { 
        width: 100% !important; 
        height: 75px !important; /* Altura mínima funcional */
        background-color: #FFFFFF !important;
        color: #4B90FF !important;
        font-size: 1.1rem !important; 
        font-weight: bold !important; 
        border: 3px solid #4B90FF !important;
        border-radius: 12px !important;
        line-height: 1.2 !important;
    }
    
    .vs-text { 
        text-align: center; 
        font-size: 24px; 
        font-weight: 900; 
        color: #FF4B4B !important; 
        margin-top: 35px;
    }

    .cat-label {
        text-align: center;
        font-size: 0.7rem;
        font-weight: 700;
        color: #777 !important;
        margin-bottom: 0px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (QR) ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>Menú</h2>", unsafe_allow_html=True)
    if st.button("⚠️ Reiniciar juego"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    # Texto forzado en blanco para que se vea en el fondo oscuro del móvil
    st.markdown("<h3 style='color:white; font-size:1.1rem;'>📢 Invita a jugar</h3>", unsafe_allow_html=True)
    
    url = "https://juego-ods-battle.streamlit.app/" 
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=True)

# 2. Base de datos
PROBLEMAS = [
    {"nombre": "Pobreza menstrual", "cat": "Derechos humanos", "desc": "Falta de acceso a productos de higiene."},
    {"nombre": "Desnutrición oculta", "cat": "Necesidades básicas", "desc": "Dietas sin vitaminas críticas."},
    {"nombre": "Brecha digital rural", "cat": "Derechos humanos", "desc": "Falta de internet en el campo."},
    {"nombre": "Acceso a agua limpia", "cat": "Necesidades básicas", "desc": "Contaminación de fuentes locales."},
    {"nombre": "Moda rápida", "cat": "Medio ambiente", "desc": "Contaminación por descarte de ropa."},
    {"nombre": "Calidad del aire", "cat": "Medio ambiente", "desc": "Polución cerca de las escuelas."},
    {"nombre": "Protección de abejas", "cat": "Medio ambiente", "desc": "Uso de pesticidas peligrosos."},
    {"nombre": "Desperdicio de energía", "cat": "Medio ambiente", "desc": "Luces encendidas en edificios vacíos."},
    {"nombre": "Acoso y grooming", "cat": "Seguridad", "desc": "Engaños de adultos a menores online."},
    {"nombre": "Transporte seguro", "cat": "Seguridad", "desc": "Prevención del acoso en buses."},
    {"nombre": "Alertas de desastre", "cat": "Seguridad", "desc": "Sistemas de aviso ineficientes."},
    {"nombre": "Ciberestafas", "cat": "Seguridad", "desc": "Robos enfocados en adultos mayores."},
    {"nombre": "Salud mental joven", "cat": "Social", "desc": "Ansiedad por redes sociales."},
    {"nombre": "Inclusión laboral", "cat": "Social", "desc": "Falta de empleo para discapacitados."},
    {"nombre": "Huella de carbono", "cat": "Acción individual", "desc": "Dificultad para medir el impacto personal."},
    {"nombre": "Comercio local", "cat": "Acción individual", "desc": "Desventaja frente a grandes plataformas."}
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
    "Semifinal": {"t": "👤 Ronda 3: Usuario", "p": "¿Cuál tiene usuarios más claros?"},
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
    st.markdown(f"<div style='text-align:center;'><h2>¡Ganador!</h2><h1 style='color:#FF4B4B !important;'>{ganador['nombre']}</h1></div>", unsafe_allow_html=True)
    if st.button("Nueva partida"):
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

    # Columnas con poco espacio entre ellas para aprovechar el 98% de ancho
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

    st.progress((int(i/2) + 1) / (len(st.session_state.competidores)/2))
