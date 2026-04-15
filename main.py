import streamlit as st
import random
import streamlit.components.v1 as components

# ---- DATOS EXTRAÍDOS DEL CUADERNO "EL PLAN MAESTRO DE HYROX" ----

EJERCICIOS_FUERZA = [
    {"nombre": "SkiErg", "detalle": "1000m en ergómetro de esquí", "peso": {
        "Iniciación": "N/A", "Open": "N/A", "Pro": "N/A"
    }, "foco": "Aeróbico"},
    {"nombre": "Sled Push", "detalle": "Empuje de trineo x 50m (4x12.5m)", "peso": {
        "Iniciación": "102kg H / 52kg M", 
        "Open": "152kg H / 102kg M", 
        "Pro": "175kg H / 152kg M"
    }, "foco": "Fuerza-Resistencia"},
    {"nombre": "Sled Pull", "detalle": "Tirón de trineo con cuerda x 50m", "peso": {
        "Iniciación": "78kg H / 53kg M", 
        "Open": "103kg H / 78kg M", 
        "Pro": "153kg H / 103kg M"
    }, "foco": "Fuerza-Resistencia"},
    {"nombre": "Burpee Broad Jumps", "detalle": "Burpees con salto de longitud x 80m", "peso": {
        "Iniciación": "Peso corporal", "Open": "Peso corporal", "Pro": "Peso corporal"
    }, "foco": "Umbral"},
    {"nombre": "Rowing", "detalle": "1000m en ergómetro de remo", "peso": {
        "Iniciación": "N/A", "Open": "N/A", "Pro": "N/A"
    }, "foco": "Aeróbico"},
    {"nombre": "Farmer's Carry", "detalle": "Paseo del granjero con pesas rusas x 200m", "peso": {
        "Iniciación": "2x16kg H / 2x12kg M", 
        "Open": "2x24kg H / 2x16kg M", 
        "Pro": "2x32kg H / 2x24kg M"
    }, "foco": "Fuerza-Resistencia"},
    {"nombre": "Sandbag Lunges", "detalle": "Zancadas con saco de arena x 100m", "peso": {
        "Iniciación": "10kg H / 10kg M", 
        "Open": "20kg H / 10kg M", 
        "Pro": "30kg H / 20kg M"
    }, "foco": "Fuerza-Resistencia"},
    {"nombre": "Wall Balls", "detalle": "Lanzamiento de balón medicinal", "peso": {
        "Iniciación": "75 reps (4kg H / 4kg M)", 
        "Open": "100 reps (6kg H) / 75 reps (4kg M)", 
        "Pro": "100 reps (9kg H / 6kg M)"
    }, "foco": "Aeróbico"}
]

BLOQUES_CARRERA = [
    {"nombre": "1 km a ritmo de carrera estándar", "foco": "Aeróbico"},
    {"nombre": "Carrera comprometida 800m (correr rápido bajo fatiga después de un ejercicio pesado)", "foco": "Fuerza-Resistencia"},
    {"nombre": "Run Shuttle: 4 x 200m (con 30s de descanso)", "foco": "Umbral"},
    {"nombre": "Sprints repetidos: 10 x 50m", "foco": "Umbral"},
    {"nombre": "Run Tempo: 2 x 400m a un 85% de capacidad", "foco": "Fuerza-Resistencia"}
]

METODOS_RECUPERACION = [
    "Recuperación activa: 10-15 minutos de trote o bicicleta muy suave (40-60% FC max)",
    "Liberación miofascial: Uso de foam roller en piernas y espalda",
    "Inmersión en agua fría (baño de hielo) durante unos minutos",
    "Terapia de compresión para drenaje en extremidades inferiores",
    "Estiramientos profundos y focalización en la respiración"
]

CALENTAMIENTOS = [
    "5 min movilidad articular general + 3 min SkiErg o Remo suave + 2 rondas de (10 sentadillas, 5 flexiones, 10 zancadas)",
    "8 min de trote suave incrementando ritmo + estiramientos dinámicos (High knees, butt kicks, lunges con rotación)",
    "10 min alternando: 1 min salto de comba, 1 min movilidad activa (gateo de oso, inchworms) x 5 rondas"
]

# ---- CONFIGURACIÓN DE PÁGINA Y CSS (INSPIRADO EN LA IMAGEN) ----
st.set_page_config(page_title="Hyrox Session Generator", page_icon="💪", layout="centered")

# ---- STATE INIT Y MODO ENTRENAMIENTO ----
if 'entrenando' not in st.session_state:
    st.session_state.entrenando = False

def iniciar_entrenamiento():
    st.session_state.entrenando = True

def finalizar_entrenamiento():
    st.session_state.entrenando = False

if st.session_state.entrenando:
    st.markdown("""
        <style>
        .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
        .stMarkdown p, .stMarkdown li, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stText { color: #FFFFFF !important; }
        h1 { color: #FFE32E !important; font-size: 2.5rem !important; text-align: center; margin-bottom: 0px; }
        .workout-text { font-size: 1.4rem; line-height: 1.6; padding: 25px; border-radius: 12px; background-color: #111; border: 2px solid #3BCB8B; margin-top: 10px; }
        .workout-text strong { color: #FFE32E !important; }
        .stButton>button { background-color: #FF4B4B !important; color: white !important; border: none !important; padding: 15px 24px !important; font-weight: bold !important; border-radius: 10px !important; width: 100% !important; font-size:1.5rem !important; }
        .stButton>button:hover { background-color: #FF0000 !important; color: white !important; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>🔥 ACTIVE WORKOUT 🔥</h1>", unsafe_allow_html=True)
    
    minutos = st.session_state.get('minutos_timer', 30)
    timer_html = f'''
    <div style="font-size: 6rem; font-weight: 800; text-align: center; color: #FFE32E; font-family: monospace; line-height: 1.2;">
        <span id="timer">--:--</span>
    </div>
    <script>
        var time = {minutos} * 60;
        var display = document.getElementById('timer');
        var timerInterval = setInterval(function () {{
            if (time < 0) {{
                clearInterval(timerInterval);
                display.innerHTML = "00:00";
                display.style.color = "#FF4B4B";
                return;
            }}
            var m = parseInt(time / 60, 10);
            var s = parseInt(time % 60, 10);
            m = m < 10 ? "0" + m : m;
            s = s < 10 ? "0" + s : s;
            display.innerHTML = m + ":" + s;
            time--;
        }}, 1000);
    </script>
    '''
    components.html(timer_html, height=140)
    
    st.markdown(f"<div class='workout-text'>{st.session_state.get('rutina_texto', '')}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        st.button("🛑 FINALIZAR", on_click=finalizar_entrenamiento)
    
    st.stop()

# Colores de la imagen:
# Verde pálido/esmeralda: #3BCB8B (Mint)
# Amarillo mostaza/melón: #DBAF55
CUSTOM_CSS = """
<style>
    /* Gradient Background */
    .stApp {
        background-color: #f6f8fa;
        font-family: 'Inter', sans-serif;
    }
    
    /* Fix text colors for dark mode browsers overriding light backgrounds */
    .stMarkdown p, .stMarkdown li, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stText {
        color: #2b3138 !important;
    }
    
    /* Title styling */
    h1 {
        color: #2e3b4e;
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #7b8a9e;
        font-size: 1.1em;
        margin-bottom: 30px;
    }

    /* Primary buttons (Melon/Mustard color) */
    .stButton>button {
        background-color: #DBAF55;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 700;
        font-size: 1.2em;
        transition: 0.3s all ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #c99d45;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Headers and cards (Mint Green touches) */
    .section-header {
        color: white;
        background-color: #3BCB8B;
        padding: 10px 15px;
        border-radius: 8px;
        margin-top: 20px;
        font-weight: bold;
        font-size: 1.2em;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .card-box {
        background-color: white;
        color: black !important;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #DBAF55;
        margin-top: 10px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    hr {
        border-top: 2px dashed #DBAF55;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---- UI PRINCIPAL ----

st.title("⚡ Generador de Rutinas HYROX")
st.markdown("<div class='subtitle'>Selecciona tu tiempo disponible y genera un WOD estratégico (AMRAP / FOR TIME) basado en The Master Plan.</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    foco_usuario = st.selectbox("🎯 Foco:", ["Aeróbico", "Fuerza-Resistencia", "Umbral"])
with col2:
    nivel_usuario = st.selectbox("🏅 Nivel:", ["Iniciación", "Open", "Pro"], index=1)
with col3:
    tiempo_sesion = st.selectbox("⏳ Tiempo:", ["30 minutos", "45 minutos", "60 minutos"])

st.markdown("<br>", unsafe_allow_html=True)
colBtnA, colBtnB, colBtnC = st.columns([1, 2, 1])
with colBtnB:
    btn_generar = st.button("GENERAR SESIÓN")

# ---- LÓGICA DE GENERACIÓN ----

def generar_bloque_principal(tiempo_str, nivel_str, foco_str):
    def get_fuerza():
        filtrados = [ej for ej in EJERCICIOS_FUERZA if ej.get('foco') == foco_str]
        if not filtrados:
            filtrados = [EJERCICIOS_FUERZA[0]]
        ej = random.choice(filtrados)
        peso_str = ej['peso'][nivel_str]
        return f"{ej['nombre']} ({ej['detalle']} - {peso_str})"

    def get_carrera():
        filtrados = [c for c in BLOQUES_CARRERA if c.get('foco') == foco_str]
        if not filtrados:
            filtrados = [BLOQUES_CARRERA[0]]
        return random.choice(filtrados)['nombre']

    # Determinamos la rutina de "Carrera bajo fatiga" según el tiempo
    if tiempo_str == "30 minutos":
        tiempo_main = 20
        explicacion = "El objetivo es sostener intensidad en periodos cortos con alta interferencia muscular (Carrera bajo fatiga)."
        
        rutina_seleccionada = f"<strong>AMRAP Loop (Repetir sin pausa por {tiempo_main} minutos):</strong><br><br>" \
                              f"1. 🏃 {get_carrera()}<br>" \
                              f"2. 🏋️ {get_fuerza()}<br>" \
                              f"3. 🏃 {get_carrera()}<br>" \
                              f"4. 🏋️ {get_fuerza()}"
        titulo_formato = f"🔥 Formato: AMRAP - Carrera Bajo Fatiga ({tiempo_main} MIN)"
        desc_formato = f"**Por qué este formato:** {explicacion}\n\n**Instrucciones:** Haz la máxima cantidad de rondas posibles de la siguiente estructura en {tiempo_main} minutos."
        
    elif tiempo_str == "45 minutos":
        tiempo_main = 30
        explicacion = "Enfoque en resistencia muscular y transiciones (Carrera bajo fatiga). Correr largo con pausas activas duras."
        
        rutina_seleccionada = f"<strong>Completar lo más rápido posible (Rondas intercaladas):</strong><br><br>" \
                              f"&bull; <strong>Estación 1:</strong><br>🏃 {get_carrera()}<br>🏋️ {get_fuerza()}<br><br>" \
                              f"&bull; <strong>Estación 2:</strong><br>🏃 {get_carrera()}<br>🏋️ {get_fuerza()}<br><br>" \
                              f"&bull; <strong>Estación 3:</strong><br>🏃 {get_carrera()}<br>🏋️ {get_fuerza()}<br><br>" \
                              f"&bull; <strong>Estación 4:</strong><br>🏃 {get_carrera()}<br>🏋️ {get_fuerza()}"
        titulo_formato = f"⏱️ Formato: FOR TIME - Carrera Bajo Fatiga (Cap: {tiempo_main} mins)"
        desc_formato = f"**Por qué este formato:** {explicacion}\n\n**Instrucciones:** Completa toda la estructura en el menor tiempo posible, manteniendo un ritmo de carrera sólido a pesar del trabajo de fuerza."
        
    else: # 60 min
        tiempo_main = 40
        explicacion = "Simulación real de la carrera bajo fatiga. Intercalar el ritmo con bloques de fuerza largos y pesados."
        
        rutina_seleccionada = f"<strong>Simulación HYROX Larga (Completar con consistencia):</strong><br><br>" \
                              f"&bull; <strong>Estación 1:</strong><br>🏃 {get_carrera()}<br>🏋️ {get_fuerza()}<br><br>" \
                              f"&bull; <strong>Estación 2:</strong><br>🏃 {get_carrera()}<br>🏋️ {get_fuerza()}<br><br>" \
                              f"&bull; <strong>Estación 3:</strong><br>🏃 {get_carrera()}<br>🏋️ {get_fuerza()}<br><br>" \
                              f"&bull; <strong>Estación 4:</strong><br>🏃 {get_carrera()}<br>🏋️ {get_fuerza()}<br><br>" \
                              f"&bull; <strong>Estación 5:</strong><br>🏃 {get_carrera()}<br>🏋️ {get_fuerza()}<br><br>" \
                              f"&bull; <strong>Estación 6:</strong><br>🏃 {get_carrera()}<br>🏋️ {get_fuerza()}"
        titulo_formato = f"🌪️ Formato: MIXTO - Carrera Bajo Fatiga (Cap: {tiempo_main} mins)"
        desc_formato = f"**Por qué este formato:** {explicacion}\n\n**Instrucciones:** Realiza el bloque principal buscando mantener una velocidad de carrera consistente en cada estación, tal como lo harías en un evento HYROX."

    return titulo_formato, desc_formato, rutina_seleccionada

if btn_generar:
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 1. CALENTAMIENTO
    st.markdown("<div class='section-header'>1️⃣ WARM-UP (Calentamiento)</div>", unsafe_allow_html=True)
    warmup_text = random.choice(CALENTAMIENTOS)
    if tiempo_sesion == "30 minutos":
        st.info("🕒 Duración sugerida: 5 minutos")
    elif tiempo_sesion == "45 minutos":
        st.info("🕒 Duración sugerida: 8 minutos")
    else:
        st.info("🕒 Duración sugerida: 10 minutos")
    st.markdown(f"<div class='card-box'>🏃‍♂️ <strong>Estructura:</strong> {warmup_text}</div>", unsafe_allow_html=True)
    
    # 2. BLOQUE PRINCIPAL
    st.markdown("<div class='section-header'>2️⃣ MAIN WORKOUT (Bloque Principal)</div>", unsafe_allow_html=True)
    titulo_fmt, desc_fmt, rutina_seleccionada = generar_bloque_principal(tiempo_sesion, nivel_usuario, foco_usuario)
    
    st.subheader(titulo_fmt)
    st.write(desc_fmt)
    
    st.markdown("**Estructura de la sesión (Carrera bajo fatiga):**")
    st.markdown(f"<div class='card-box' style='font-weight: 500; font-size: 1.1em;'>🏃‍♂️💥 <strong>Trabajo Específico:</strong><br><br>{rutina_seleccionada}</div>", unsafe_allow_html=True)
        
    # 3. VUELTA A LA CALMA
    st.markdown("<div class='section-header'>3️⃣ COOL-DOWN (Recuperación)</div>", unsafe_allow_html=True)
    if tiempo_sesion == "30 minutos":
        st.info("🕒 Duración sugerida: 5 minutos")
    elif tiempo_sesion == "45 minutos":
        st.info("🕒 Duración sugerida: 7 minutos")
    else:
        st.info("🕒 Duración sugerida: 10 minutos")
        
    metodo_rec = random.choice(METODOS_RECUPERACION)
    st.markdown(f"<div class='card-box'>🧘 <strong>Método:</strong> {metodo_rec}</div>", unsafe_allow_html=True)
    
    st.success("¡Sesión generada con éxito! A por todas.")
    
    # Guardar en estado para el modo entrenamiento
    st.session_state['minutos_timer'] = int(tiempo_sesion.split()[0])
    st.session_state['rutina_texto'] = f"<div style='margin-bottom: 15px;'><strong>1️⃣ CALENTAMIENTO:</strong><br>{warmup_text}</div>" \
                                       f"<div style='margin-bottom: 15px;'><strong>2️⃣ BLOQUE PRINCIPAL:</strong><br>{titulo_fmt}<br><br>{rutina_seleccionada}</div>" \
                                       f"<div><strong>3️⃣ VUELTA A LA CALMA:</strong><br>{metodo_rec}</div>"
    
    st.markdown("<br>", unsafe_allow_html=True)
    colStartX, colStartY, colStartZ = st.columns([1, 2, 1])
    with colStartY:
        st.button("🚀 INICIAR ENTRENAMIENTO", on_click=iniciar_entrenamiento, use_container_width=True)
