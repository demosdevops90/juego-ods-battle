import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página y Estilos de alto contraste
st.set_page_config(page_title="Technovation ODS Battle", layout="centered")

st.markdown("""
    <style>
    /* Forzamos colores oscuros para los textos sobre fondo claro */
    .stApp { background-color: #F4F7F9; }
    h1, h2, h3, span, p, div { color: #1E1E1E !important; }
    
    /* Caja de Criterios */
    .criterio-box { 
        background-color: #FFFFFF; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 10px solid #FF4B4B; 
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Descripción del problema */
    .desc-text {
        color: #444444 !important;
        font-size: 16px;
        margin-bottom: 10px;
        min-height: 40px;
    }

    /* Botones de Duelo */
    .stButton>button { 
        width: 100%; 
        height: 120px; 
        background-color: #FFFFFF !important;
        color: #4B90FF !important;
        font-size: 20px !important; 
        font-weight: bold !important; 
        border: 3px solid #4B90FF !important;
        border-radius: 15px !important;
    }
    
    .vs-text { text-align: center; font-size: 40px; font-weight: 900; color: #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL CON QR ---
with st.sidebar:
    st.header("Menú")
    if st.button("⚠️ Reiniciar Juego"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    st.write("📢 **Invita a jugar**")
    # Sustituye esta URL por la URL real de tu app cuando la publiques
    url = "https://juego-ods-battlegit-9vfpqcmbe4scvs3oj8okos.streamlit.app/" 
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="Escanea para unirte")

# 2. Base de datos
PROBLEMAS = [
    {"nombre": "Pobreza Menstrual", "cat": "Derechos Humanos", "desc": "Falta de acceso a productos y educación."},
    {"nombre": "Desnutrición Oculta", "cat": "Necesidades Básicas", "desc": "Dietas pobres en vitaminas críticas."},
    {"nombre": "Brecha Digital Rural", "cat": "Derechos Humanos", "desc": "Falta de internet y equipo en el campo."},
    {"nombre": "Acceso a Agua Limpia", "cat": "Necesidades Básicas", "desc": "Contaminación de pozos y ríos locales."},
    {"nombre": "Fast Fashion", "cat": "Medio Ambiente", "desc": "Contaminación por descarte masivo de ropa."},
    {"nombre": "Calidad del Aire", "cat": "Medio Ambiente", "desc": "Humos y polución cerca de las escuelas."},
    {"nombre": "Protección de Abejas", "cat": "Medio Ambiente", "desc": "Uso de pesticidas que matan polinizadores."},
    {"nombre": "Desperdicio Energía", "cat": "Medio Ambiente", "desc": "Luces encendidas en edificios vacíos."},
    {"nombre": "Grooming y Acoso", "cat": "Seguridad", "desc": "Engaños de adultos a menores online."},
    {"nombre": "Transporte Seguro", "cat": "Seguridad", "desc": "Acoso en autobuses y paradas."},
    {"nombre": "Alertas de Desastre", "cat": "Seguridad", "desc": "Falta de aviso ante inundaciones."},
    {"nombre": "Ciber-estafas", "cat": "Seguridad", "desc": "Robo de ahorros a adultos mayores."},
    {"nombre": "Salud Mental", "cat": "Social", "desc": "Ansiedad y depresión por redes sociales."},
    {"nombre": "Inclusión Laboral", "cat": "Social", "desc": "Falta de trabajo para discapacitados."},
    {"nombre": "Huella Carbono", "cat": "Acción Individual", "desc": "Dificultad para medir el impacto personal."},
    {"nombre": "Comercio Local", "cat": "Acción Individual", "desc": "Dificultad de competir con grandes tiendas."}
]

# Inicialización
if 'competidores' not in st.session_state:
    random.shuffle(PROBLEMAS)
    st.session_state.competidores = PROBLEMAS
    st.session_state.ganadores_ronda_actual = []
    st.session_state.indice_duelo = 0
    st.session_state.ronda_nombre = "Octavos de Final"

CRITERIOS = {
    "Octavos de Final": {"t": "📍 RONDA 1: IMPACTO", "p": "¿Cuál es más URGENTE en tu ciudad?"},
    "Cuartos de Final": {"t": "💻 RONDA 2: VIABILIDAD", "p": "¿Cuál es más fácil de resolver con una APP?"},
    "Semifinal": {"t": "👤 RONDA 3: USUARIO", "p": "¿Quién tiene usuarios más claros?"},
    "GRAN FINAL": {"t": "❤️ FINAL: PASIÓN", "p": "¿Cuál les motiva más para trabajar?"}
}

def elegir_ganador(elegido):
    st.session_state.ganadores_ronda_actual.append(elegido)
    st.session_state.indice_duelo += 2
    if st.session_state.indice_duelo >= len(st.session_state.competidores):
        if len(st.session_state.ganadores_ronda_actual) == 1:
            st.session_state.ronda_nombre = "¡GANADOR!"
        else:
            st.session_state.competidores = st.session_state.ganadores_ronda_actual
            st.session_state.ganadores_ronda_actual = []
            st.session_state.indice_duelo = 0
            nombres = {8: "Cuartos de Final", 4: "Semifinal", 2: "GRAN FINAL"}
            st.session_state.ronda_nombre = nombres.get(len(st.session_state.competidores), "Final")

# UI
st.title("🏆 ODS 1 vs 1")

if st.session_state.ronda_nombre == "¡GANADOR!":
    ganador = st.session_state.ganadores_ronda_actual[0]
    st.balloons()
    st.markdown(f"<h1 style='text-align:center;'>{ganador['nombre']}</h1>", unsafe_allow_html=True)
    if st.button("Reiniciar"):
        st.session_state.clear()
        st.rerun()
else:
    info = CRITERIOS[st.session_state.ronda_nombre]
    st.markdown(f'<div class="criterio-box"><h3>{info["t"]}</h3><p>{info["p"]}</p></div>', unsafe_allow_html=True)

    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]

    col1, col_vs, col2 = st.columns([5, 2, 5])
    with col1:
        st.write(f"**{p1['cat']}**")
        st.markdown(f"<p class='desc-text'>{p1['desc']}</p>", unsafe_allow_html=True)
        if st.button(p1['nombre'], key=f"b{i}"): elegir_ganador(p1); st.rerun()
    with col_vs:
        st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)
    with col2:
        st.write(f"**{p2['cat']}**")
        st.markdown(f"<p class='desc-text'>{p2['desc']}</p>", unsafe_allow_html=True)
        if st.button(p2['nombre'], key=f"b{i+1}"): elegir_ganador(p2); st.rerun()

    st.progress((int(i/2) + 1) / int(len(st.session_state.competidores)/2))
