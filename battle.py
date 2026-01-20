import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation ODS Battle", layout="wide")

st.markdown("""
    <style>
    /* Ancho al 90% y centrado */
    .block-container {
        max-width: 90% !important;
        padding-top: 1.5rem !important;
        margin: auto;
    }

    .stApp { background-color: #F4F7F9; }
    h1, h2, h3, span, p, div { color: #1E1E1E !important; }
    
    h1 {
        font-size: 2.2rem !important;
        text-align: center;
        margin-bottom: 1rem !important;
    }

    /* Caja de criterios con redacción natural */
    .criterio-box { 
        background-color: #FFFFFF; 
        padding: 15px 25px; 
        border-radius: 15px; 
        border-left: 10px solid #FF4B4B; 
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .desc-text {
        color: #444444 !important;
        font-size: 1.1rem;
        margin-bottom: 12px;
        min-height: 45px;
        text-align: center;
        line-height: 1.4;
    }

    /* Botones de duelo */
    .stButton>button { 
        width: 100%; 
        height: 110px; 
        background-color: #FFFFFF !important;
        color: #4B90FF !important;
        font-size: 20px !important; 
        font-weight: bold !important; 
        border: 3px solid #4B90FF !important;
        border-radius: 18px !important;
        text-transform: none !important; /* Evita mayúsculas automáticas */
    }
    
    .stButton>button:hover {
        background-color: #4B90FF !important;
        color: white !important;
    }
    
    .vs-text { 
        text-align: center; 
        font-size: 40px; 
        font-weight: 900; 
        color: #FF4B4B; 
        line-height: 110px; 
    }

    .cat-label {
        text-align: center;
        font-size: 0.9rem;
        font-weight: 600;
        color: #666 !important;
        margin-bottom: 5px;
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
    st.markdown("<p style='font-weight: bold;'>📢 Invita a jugar</p>", unsafe_allow_html=True)
    
    url = "https://tu-app-technovation.streamlit.app/" 
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=True)

# 2. Base de datos con redacción corregida
PROBLEMAS = [
    {"nombre": "Pobreza menstrual", "cat": "Derechos humanos", "desc": "Falta de acceso a productos de higiene y educación básica."},
    {"nombre": "Desnutrición oculta", "cat": "Necesidades básicas", "desc": "Dietas con carencia de vitaminas y minerales críticos."},
    {"nombre": "Brecha digital rural", "cat": "Derechos humanos", "desc": "Falta de conexión a internet y equipos en zonas de campo."},
    {"nombre": "Acceso a agua limpia", "cat": "Necesidades básicas", "desc": "Contaminación de pozos y fuentes de agua locales."},
    {"nombre": "Moda rápida (Fast fashion)", "cat": "Medio ambiente", "desc": "Impacto ambiental por el descarte masivo de ropa económica."},
    {"nombre": "Calidad del aire", "cat": "Medio ambiente", "desc": "Presencia de humos y polución cerca de entornos escolares."},
    {"nombre": "Protección de abejas", "cat": "Medio ambiente", "desc": "Uso de pesticidas que afectan a los insectos polinizadores."},
    {"nombre": "Desperdicio de energía", "cat": "Medio ambiente", "desc": "Consumo innecesario en edificios públicos vacíos."},
    {"nombre": "Acoso y grooming", "cat": "Seguridad", "desc": "Riesgos de engaños y contacto de adultos con menores en internet."},
    {"nombre": "Transporte seguro", "cat": "Seguridad", "desc": "Prevención del acoso en paradas y vehículos de transporte público."},
    {"nombre": "Alertas de desastre", "cat": "Seguridad", "desc": "Sistemas deficientes de aviso ante inundaciones o sismos."},
    {"nombre": "Ciberestafas", "cat": "Seguridad", "desc": "Robo de datos y ahorros enfocado en personas mayores."},
    {"nombre": "Salud mental joven", "cat": "Social", "desc": "Aumento de ansiedad y depresión ligada al uso de redes sociales."},
    {"nombre": "Inclusión laboral", "cat": "Social", "desc": "Barreras para el acceso al trabajo de personas con discapacidad."},
    {"nombre": "Huella de carbono", "cat": "Acción individual", "desc": "Dificultad para medir y reducir el impacto ambiental personal."},
    {"nombre": "Comercio local", "cat": "Acción individual", "desc": "Desventaja de las tiendas de barrio frente a las grandes plataformas."}
]

# Inicialización
if 'competidores' not in st.session_state:
    random.shuffle(PROBLEMAS)
    st.session_state.competidores = PROBLEMS
    st.session_state.ganadores_ronda_actual = []
    st.session_state.indice_duelo = 0
    st.session_state.ronda_nombre = "Octavos de final"

CRITERIOS = {
    "Octavos de final": {"t": "📍 Ronda 1: Impacto", "p": "¿Cuál de estos problemas es más urgente en tu comunidad?"},
    "Cuartos de final": {"t": "💻 Ronda 2: Viabilidad", "p": "¿Cuál es más sencillo de resolver mediante una aplicación móvil?"},
    "Semifinal": {"t": "👤 Ronda 3: Usuario", "p": "¿Cuál de los dos tiene un grupo de usuarios más claro?"},
    "Gran final": {"t": "❤️ Final: Pasión", "p": "¿Cuál de estas causas les motiva más para trabajar?"}
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
            nombres = {8: "Cuartos de final", 4: "Semifinal", 2: "Gran final"}
            st.session_state.ronda_nombre = nombres.get(len(st.session_state.competidores), "Final")

# --- UI PRINCIPAL ---
st.title("🏆 Technovation Battle")

if st.session_state.ronda_nombre == "¡Ganador!":
    ganador = st.session_state.ganadores_ronda_actual[0]
    st.balloons()
    st.markdown(f"<div style='text-align:center; padding: 40px;'><h2>El proyecto ganador es:</h2><h1 style='font-size:3.5rem !important; color:#FF4B4B !important;'>{ganador['nombre']}</h1></div>", unsafe_allow_html=True)
    if st.button("Empezar una nueva partida"):
        st.session_state.clear()
        st.rerun()
else:
    info = CRITERIOS[st.session_state.ronda_nombre]
    st.markdown(f'''
        <div class="criterio-box">
            <h2 style="margin:0; font-size:1.4rem;">{info["t"]}</h2>
            <p style="margin:0; font-size:1.1rem; color:#444 !important;">{info["p"]}</p>
        </div>
    ''', unsafe_allow_html=True)

    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]

    col_izq, col_vs, col_der = st.columns([5, 1, 5])
    
    with col_izq:
        st.markdown(f"<p class='cat-label'>{p1['cat']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='desc-text'>{p1['desc']}</p>", unsafe_allow_html=True)
        if st.button(p1['nombre'], key=f"b{i}"): 
            elegir_ganador(p1)
            st.rerun()

    with col_vs:
        st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)

    with col_der:
        st.markdown(f"<p class='cat-label'>{p2['cat']}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='desc-text'>{p2['desc']}</p>", unsafe_allow_html=True)
        if st.button(p2['nombre'], key=f"b{i+1}"): 
            elegir_ganador(p2)
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    progreso = (int(i/2) + 1) / int(len(st.session_state.competidores)/2)
    st.progress(progreso)
