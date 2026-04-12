import streamlit as st
import random

# ---- DATOS EXTRAÍDOS DEL CUADERNO "EL PLAN MAESTRO DE HYROX" ----

EJERCICIOS_FUERZA = [
    {"nombre": "SkiErg", "detalle": "1000m en ergómetro de esquí", "peso": "N/A"},
    {"nombre": "Sled Push", "detalle": "Empuje de trineo x 50m (4x12.5m)", "peso": "Pesado (ej. 152kg H / 102kg M)"},
    {"nombre": "Sled Pull", "detalle": "Tirón de trineo con cuerda x 50m", "peso": "Pesado (ej. 103kg H / 78kg M)"},
    {"nombre": "Burpee Broad Jumps", "detalle": "Burpees con salto de longitud x 80m", "peso": "Peso corporal"},
    {"nombre": "Rowing", "detalle": "1000m en ergómetro de remo", "peso": "N/A"},
    {"nombre": "Farmer's Carry", "detalle": "Paseo del granjero con pesas rusas x 200m", "peso": "2x24kg H / 2x16kg M"},
    {"nombre": "Sandbag Lunges", "detalle": "Zancadas con saco de arena x 100m", "peso": "20kg H / 10kg M"},
    {"nombre": "Wall Balls", "detalle": "Lanzamiento de balón medicinal", "peso": "100 reps (6kg H / 4kg M)"}
]

BLOQUES_CARRERA = [
    "1 km a ritmo de carrera estándar",
    "Carrera comprometida 800m (correr rápido bajo fatiga después de un ejercicio pesado)",
    "Run Shuttle: 4 x 200m (con 30s de descanso)",
    "Sprints repetidos: 10 x 50m",
    "Run Tempo: 2 x 400m a un 85% de capacidad"
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

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    tiempo_sesion = st.selectbox("⏳ Tiempo total disponible:", ["30 minutos", "45 minutos", "60 minutos"])
    btn_generar = st.button("GENERAR SESIÓN")

# ---- LÓGICA DE GENERACIÓN ----

def generar_bloque_principal(tiempo_str):
    # Determinar variables en función del tiempo
    if tiempo_str == "30 minutos":
        formato = "AMRAP"
        tiempo_main = 20
        num_ejercicios = 3
        num_carreras = 1
        explicacion = "El AMRAP es ideal para sesiones cortas, exprimiendo la intensidad máxima sin pensar en el fin de las rondas."
    elif tiempo_str == "45 minutos":
        formato = "FOR TIME"
        tiempo_main = 30
        num_ejercicios = 4
        num_carreras = 2
        explicacion = "El FOR TIME permite enfocarse en dominar un volumen concreto de trabajo a un ritmo sostenido, perfecto para media distancia."
    else: # 60 min
        formato = "MIXTO"
        tiempo_main = 40
        num_ejercicios = 6
        num_carreras = 3
        explicacion = "El formato MIXTO simula los cambios de desgaste en carrera: te empuja y luego te exige soportar repeticiones."
        
    ejercicios_seleccionados = random.sample(EJERCICIOS_FUERZA, num_ejercicios)
    carreras_seleccionadas = random.choices(BLOQUES_CARRERA, k=num_carreras)
    
    if formato == "AMRAP":
        titulo_formato = f"🔥 Formato: AMRAP ({tiempo_main} MIN)"
        desc_formato = f"**Por qué este formato:** {explicacion}\n\n**Instrucciones:** Haz la máxima cantidad de rondas posibles del siguiente circuito en {tiempo_main} minutos."
    elif formato == "FOR TIME":
        titulo_formato = f"⏱️ Formato: FOR TIME (Cap: {tiempo_main} mins)"
        desc_formato = f"**Por qué este formato:** {explicacion}\n\n**Instrucciones:** Completa 4 rondas del siguiente circuito en el menor tiempo posible (Límite: {tiempo_main} min)."
    else: # MIXTO
        titulo_formato = f"🌪️ Formato: MIXTO (Cap: {tiempo_main} mins)"
        desc_formato = f"**Por qué este formato:** {explicacion}\n\n**Instrucciones:** Completa primero todas las carreras enumeradas lo más rápido que puedas (FOR TIME). Con el tiempo restante de los {tiempo_main} min, realiza un AMRAP con los ejercicios de fuerza indicados."
        
    return titulo_formato, desc_formato, ejercicios_seleccionados, carreras_seleccionadas

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
    titulo_fmt, desc_fmt, ej_fuerza, ej_carrera = generar_bloque_principal(tiempo_sesion)
    
    st.subheader(titulo_fmt)
    st.write(desc_fmt)
    
    st.markdown("**Circuito propuesto:**")
    for carrera in ej_carrera:
        st.markdown(f"<div class='card-box'>👟 <strong>Carrera:</strong> {carrera}</div>", unsafe_allow_html=True)
        
    for i, ej in enumerate(ej_fuerza, 1):
        # Ajustamos aleatoriamente repeticiones o distancias si no tienen métricas fijas estandar para no aburrir
        detalle = ej['detalle']
        if "100 reps" in detalle:
            detalle = "30-50 reps (Escala para el circuito)" if "AMRAP" in titulo_fmt else detalle
        elif "1000m" in detalle:
            detalle = "250m - 500m (Escala corta para circuitos)" if tiempo_sesion == "30 minutos" else detalle
            
        st.markdown(f"<div class='card-box'>🏋️ <strong>Estación {i}:</strong> {ej['nombre']} <br> <em>{detalle}</em> <br> <small>Peso: {ej['peso']}</small></div>", unsafe_allow_html=True)
        
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
