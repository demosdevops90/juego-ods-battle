import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation Battle", layout="wide")

st.markdown("""
    <style>
    /* 1. FORZAR ANCHO Y ELIMINAR MÁRGENES EN MÓVIL */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        padding: 0.5rem !important;
        margin: 0 !important;
    }
    
    /* 2. EVITAR QUE LAS COLUMNAS SE APILEN EN MÓVIL (TRUCO FLEX) */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 5px !important;
    }
    
    [data-testid="column"] {
        width: auto !important;
        flex: 1 1 auto !important;
    }

    /* 3. TÍTULO Y TEXTOS VISIBLES */
    .stApp { background-color: #F4F7F9; }
    
    h1 {
        font-size: 1.5rem !important;
        text-align: center;
        color: #1E1E1E !important;
        margin: 0 !important;
        padding: 5px !important;
    }

    /* Caja de criterio corregida (Texto negro) */
    .criterio-box { 
        background-color: #FFFFFF; 
        padding: 10px; 
        border-radius: 10px; 
        border-left: 6px solid #FF4B4B; 
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        text-align: center;
    }
    .criterio-box h2 { color: #1E1E1E !important; font-size: 1.1rem !important; margin: 0 !important; }
    .criterio-box p { color: #444444 !important; font-size: 0.9rem !important; margin: 0 !important; }

    /* 4. BOTONES QUE OCUPAN EL ANCHO */
    .stButton > button { 
        width: 100% !important; 
        height: 80px !important;
        background-color: #FFFFFF !important;
        color: #4B90FF !important;
        font-size: 1rem !important; 
        font-weight: bold !important; 
        border: 3px solid #4B90FF !important;
        border-radius: 12px !important;
        padding: 2px !important;
    }
    
    .vs-text { 
        text-align: center; 
        font-size: 20px; 
        font-weight: 900; 
        color: #FF4B4B !important;
        margin: 0 !important;
        min-width: 30px;
    }

    .desc-text {
        text-align: center;
        font-size: 0.75rem;
        color: #555555 !important;
        line-height: 1;
        margin-bottom: 3px;
    }

    /* Texto sidebar blanco */
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("## Configuración")
    if st.button("⚠️ Reiniciar"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    st.markdown("### 📢 Invita a jugar")
    url = "https://tu-app.streamlit.app" 
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), use_container_width=True)

# 2. Base de datos
if 'competidores' not in st.session_state:
    PROBLEMAS = [
        {"nombre": "Pobreza menstrual", "cat": "Derechos humanos", "desc": "Falta de acceso a higiene."},
        {"nombre": "Desnutrición oculta", "cat": "Necesidades básicas", "desc": "Carencia de vitaminas."},
        {"nombre": "Brecha digital rural", "cat": "Derechos humanos", "desc": "Falta de internet en campo."},
        {"nombre": "Acceso a agua limpia", "cat": "Necesidades básicas", "desc": "Agua contaminada."},
        {"nombre": "Moda rápida", "cat": "Medio ambiente", "desc": "Desecho masivo de ropa."},
        {"nombre": "Calidad del aire", "cat": "Medio ambiente", "desc": "Humo cerca de escuelas."},
        {"nombre": "Protección de abejas", "cat": "Medio ambiente", "desc": "Uso de pesticidas."},
        {"nombre": "Desperdicio energía", "cat": "Medio ambiente", "desc": "Luces encendidas sin uso."},
        {"nombre": "Acoso y grooming", "cat": "Seguridad", "desc": "Riesgos para menores online."},
        {"nombre": "Transporte seguro", "cat": "Seguridad", "desc": "Acoso en buses y paradas."},
        {"nombre": "Alertas de desastre", "cat": "Seguridad", "desc": "Avisos de emergencia malos."},
        {"nombre": "Ciberestafas", "cat": "Seguridad", "desc": "Robos a abuelos online."},
        {"nombre": "Salud mental joven", "cat": "Social", "desc": "Ansiedad por redes."},
        {"nombre": "Inclusión laboral", "cat": "Social", "desc": "Barreras para discapacitados."},
        {"nombre": "Huella de carbono", "cat": "Individual", "desc": "Medir el impacto personal."},
        {"nombre": "Comercio local", "cat": "Individual", "desc": "Tiendas vs plataformas."}
    ]
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
    st.markdown(f"<div style='text-align:center;'><h2>¡Ganador!</h2><h1 style='color:#FF4B4B !important;'>{ganador['nombre']}</h1></div>", unsafe_allow_html=True)
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

    # CONTENEDOR DE DUELO
    col_izq, col_vs, col_der = st.columns([10, 2, 10])
    
    with col_izq:
        st.markdown(f"<p class='desc-text'>{p1['desc']}</p>", unsafe_allow_html=True)
        if st.button(p1['nombre'], key=f"b{i}"): 
            elegir_ganador(p1); st.rerun()

    with col_vs:
        st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)

    with col_der:
        st.markdown(f"<p class='desc-text'>{p2['desc']}</p>", unsafe_allow_html=True)
        if st.button(p2['nombre'], key=f"b{i+1}"): 
            elegir_ganador(p2); st.rerun()

    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    st.progress((int(i/2) + 1) / (len(st.session_state.competidores)/2))
