import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="¿Qué Tipo de Gato Eres?",
    page_icon="🐱",
    layout="centered"
)

# Estilos CSS para un diseño atractivo con tema felino
st.markdown("""
<style>
    body {
        background-color: #f8f0e6;
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #FFE0B2 0%, #FFF3E0 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stTitle {
        color: #FF9800;
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .stMarkdown {
        color: #5D4037;
        font-size: 1.1em;
        text-align: center;
    }
    .stTextInput > label {
        color: #FF9800;
        font-weight: bold;
        font-size: 1.2em;
    }
    .stTextInput > div > input {
        border: 2px solid #FFB74D;
        border-radius: 10px;
        padding: 10px;
        font-size: 1em;
        background-color: #FFF8E1;
    }
    .stRadio > label {
        color: #FF9800;
        font-weight: bold;
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    .stRadio > div > label {
        background-color: #FFF8E1;
        padding: 12px;
        border-radius: 10px;
        margin: 5px 0;
        color: #5D4037;
        font-size: 1em;
        transition: all 0.3s ease;
        border-left: 4px solid #FFB74D;
    }
    .stRadio > div > label:hover {
        background-color: #FFE0B2;
        transform: translateX(5px);
        cursor: pointer;
    }
    .stButton > button {
        background-color: #FF9800;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 1.1em;
        font-weight: bold;
        transition: all 0.3s ease;
        border: none;
    }
    .stButton > button:hover {
        background-color: #F57C00;
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .stButton > button:disabled {
        background-color: #E0E0E0;
        color: #9E9E9E;
    }
    .stProgress .st-bo {
        background-color: #FFE0B2;
    }
    .stProgress .st-bo > div {
        background-color: #FF9800;
    }
    .cat-image {
        text-align: center;
        margin: 20px 0;
        font-size: 4em;
    }
    .result-card {
        background-color: #FFF8E1;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #FF9800;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .cat-traits {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    .trait-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px;
        text-align: center;
        flex: 1;
        min-width: 120px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .purr-fect {
        text-align: center;
        font-size: 1.5em;
        color: #FF9800;
        margin: 20px 0;
    }
    .question-category {
        background-color: #FFB74D;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 0.8em;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Título e introducción
st.title("🐱 Test de Personalidad: ¿Qué Tipo de Gato Eres?")
st.markdown("""
Descubre qué tipo de gato refleja mejor tu esencia interior con este test único.  
Responde honestamente y conoce tu alter ego felino basado en tu forma de ser.
""")

# Inicializar el estado de la sesión
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = []
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 0
if 'nombre' not in st.session_state:
    st.session_state.nombre = ""

# Preguntar el nombre al usuario
if not st.session_state.nombre:
    st.session_state.nombre = st.text_input("Antes de comenzar, ¿cómo te llamas?", max_chars=30)
    if st.session_state.nombre:
        st.success(f"¡Perfecto, {st.session_state.nombre}! Prepara tus bigotes para el test.")
        st.rerun()
    st.stop()

# Preguntas completamente diferentes y originales
preguntas = [
    {
        "pregunta": "1. Si tuvieras un superpoder, ¿cuál elegirías?",
        "categoria": "Esencia",
        "opciones": [
            "Leer la mente de las personas",
            "Ser invisible cuando quisiera",
            "Tener una fuerza sobrehumana",
            "Poder volar a cualquier lugar"
        ]
    },
    {
        "pregunta": "2. ¿Qué tipo de paisaje te relaja más?",
        "categoria": "Ambiente",
        "opciones": [
            "Una biblioteca tranquila y ordenada",
            "Un bosque misterioso y profundo",
            "Una playa con olas fuertes",
            "Un jardín lleno de flores coloridas"
        ]
    },
    {
        "pregunta": "3. Cuando enfrentas un problema, tu primera reacción es:",
        "categoria": "Resolución",
        "opciones": [
            "Analizarlo desde todos los ángulos posibles",
            "Seguir tu intuición y corazonada",
            "Pedir ayuda y opiniones a otros",
            "Actuar rápido y ajustar sobre la marcha"
        ]
    },
    {
        "pregunta": "4. ¿Cómo describes tu estilo de aprendizaje?",
        "categoria": "Conocimiento",
        "opciones": [
            "Metódico: paso a paso con mucha práctica",
            "Curioso: explorando y experimentando",
            "Social: aprendo mejor en grupo",
            "Intuitivo: sigo mi instinto natural"
        ]
    },
    {
        "pregunta": "5. En una fiesta, ¿qué rol sueles tomar?",
        "categoria": "Social",
        "opciones": [
            "El animador que conoce a todos",
            "El observador que disfruta desde la distancia",
            "El confidente que tiene conversaciones profundas",
            "El aventurero que prueba todo primero"
        ]
    },
    {
        "pregunta": "6. ¿Qué cualidad valoras más en un amigo?",
        "categoria": "Valores",
        "opciones": [
            "La lealtad y confiabilidad",
            "La creatividad e imaginación",
            "La honestidad y directitud",
            "La empatía y comprensión"
        ]
    },
    {
        "pregunta": "7. Tu idea de un día perfecto incluye:",
        "categoria": "Estilo de Vida",
        "opciones": [
            "Una agenda llena de actividades planificadas",
            "Improvisar y dejarse llevar por el momento",
            "Tiempo solo para hobbies y reflexión",
            "Reunirse con amigos y familia"
        ]
    },
    {
        "pregunta": "8. ¿Cómo te describes en una crisis?",
        "categoria": "Emergencia",
        "opciones": [
            "Calmado y racional, busco soluciones lógicas",
            "Emocional y empático, apoyo a los afectados",
            "Activo y práctico, actúo inmediatamente",
            "Estratégico, pienso en el largo plazo"
        ]
    },
    {
        "pregunta": "9. ¿Qué tipo de música prefieres?",
        "categoria": "Expresión",
        "opciones": [
            "Clásica o instrumental, bien estructurada",
            "Rock o electrónica, llena de energía",
            "Jazz o blues, espontánea y emotiva",
            "Pop o folk, social y relatable"
        ]
    },
    {
        "pregunta": "10. Al elegir un libro, te inclinas por:",
        "categoria": "Literatura",
        "opciones": [
            "No-ficción: biografías, ciencia, historia",
            "Fantasía o ciencia ficción épica",
            "Romance o dramas humanos profundos",
            "Misterio o thrillers con giros inesperados"
        ]
    },
    {
        "pregunta": "11. ¿Cómo manejas los cambios inesperados?",
        "categoria": "Adaptabilidad",
        "opciones": [
            "Me estreso pero creo un nuevo plan rápido",
            "Los disfruto como aventuras emocionantes",
            "Necesito tiempo para procesarlos en soledad",
            "Busco apoyo en mi círculo cercano"
        ]
    },
    {
        "pregunta": "12. Tu fortaleza secreta es:",
        "categoria": "Personalidad",
        "opciones": [
            "Paciencia infinita y perseverancia",
            "Creatividad e ideas innovadoras",
            "Habilidad para conectar con las personas",
            "Capacidad de liderazgo natural"
        ]
    }
]

# Sistema de puntuación disfrazado - las opciones mapean a dimensiones MBTI de manera no obvia
letras_mbti = [
    # Pregunta 1: Superpoder
    ["N", "I", "S", "E"],  # Leer mente (N), Invisibilidad (I), Fuerza (S), Volar (E)

    # Pregunta 2: Paisaje
    ["J", "N", "P", "F"],  # Biblioteca (J), Bosque (N), Playa (P), Jardín (F)

    # Pregunta 3: Problemas
    ["T", "F", "E", "P"],  # Analizar (T), Intuición (F), Pedir ayuda (E), Actuar rápido (P)

    # Pregunta 4: Aprendizaje
    ["S", "P", "E", "N"],  # Metódico (S), Curioso (P), Social (E), Intuitivo (N)

    # Pregunta 5: Fiesta
    ["E", "I", "F", "P"],  # Animador (E), Observador (I), Confidente (F), Aventurero (P)

    # Pregunta 6: Amistad
    ["S", "N", "T", "F"],  # Lealtad (S), Creatividad (N), Honestidad (T), Empatía (F)

    # Pregunta 7: Día perfecto
    ["J", "P", "I", "E"],  # Planificado (J), Improvisar (P), Solo (I), Social (E)

    # Pregunta 8: Crisis
    ["T", "F", "S", "N"],  # Racional (T), Emocional (F), Activo (S), Estratégico (N)

    # Pregunta 9: Música
    ["J", "E", "F", "P"],  # Estructurada (J), Energética (E), Emotiva (F), Espontánea (P)

    # Pregunta 10: Libros
    ["S", "N", "F", "T"],  # No-ficción (S), Fantasía (N), Romance (F), Misterio (T)

    # Pregunta 11: Cambios
    ["J", "P", "I", "E"],  # Nuevo plan (J), Aventura (P), Soledad (I), Apoyo (E)

    # Pregunta 12: Fortaleza
    ["S", "N", "F", "T"]  # Paciencia (S), Creatividad (N), Conexión (F), Liderazgo (T)
]

# Tipos de gatos (igual que antes pero con preguntas diferentes)
tipos_gato = {
    "ISTJ": {
        "nombre": "Gato Británico de Pelo Corto 🐱",
        "descripcion": "Eres confiable, elegante y con una dignidad natural. Como el Británico de Pelo Corto, valoras la tradición y la estabilidad.",
        "analogia": "Tu lealtad y sentido del deber te hacen el pilar confiable de cualquier grupo.",
        "fortalezas": "Responsable, organizado, metódico",
        "caracteristicas": ["Amable pero independiente", "Observador silencioso", "Amante de la rutina"],
        "emoji": "🐱"
    },
    "ISFJ": {
        "nombre": "Gato Ragdoll 🐈",
        "descripcion": "Eres dulce, protector y siempre estás pendiente del bienestar de los demás. Como el Ragdoll, tu suavidad es tu mayor fortaleza.",
        "analogia": "Tu naturaleza cuidadora te hace el compañero perfecto para quienes te rodean.",
        "fortalezas": "Empático, dedicado, cuidadoso",
        "caracteristicas": ["Extremadamente leal", "Suave y gentil", "Protector nato"],
        "emoji": "🐈"
    },
    "INFJ": {
        "nombre": "Gato Siamés Traditional 🐈‍⬛",
        "descripcion": "Eres misterioso, intuitivo y con una profundidad que pocos comprenden. Como el Siamés, tienes una conexión especial con el mundo espiritual.",
        "analogia": "Tu sabiduría interior te guía en ayudar a los demás de maneras únicas.",
        "fortalezas": "Intuitivo, idealista, perspicaz",
        "caracteristicas": ["Comunicativo y expresivo", "Muy inteligente", "Reservado pero profundo"],
        "emoji": "🐈‍⬛"
    },
    "INTJ": {
        "nombre": "Gato Bengalí 🐆",
        "descripcion": "Eres estratégico, independiente y siempre varios pasos adelante. Como el Bengalí, tu mente aguda es tu mejor arma.",
        "analogia": "Tu capacidad para ver patrones invisibles te hace un visionario natural.",
        "fortalezas": "Estratégico, independiente, visionario",
        "caracteristicas": ["Curioso e investigador", "Amante de los desafíos", "Pensador profundo"],
        "emoji": "🐆"
    },
    "ISTP": {
        "nombre": "Gato Abisinio 🐅",
        "descripcion": "Eres práctico, aventurero y maestro de la improvisación. Como el Abisinio, amas explorar y entender cómo funcionan las cosas.",
        "analogia": "Tu habilidad para resolver problemas en el momento te hace invaluable.",
        "fortalezas": "Adaptable, práctico, observador",
        "caracteristicas": ["Energético y juguetón", "Muy curioso", "Ágil y resourceful"],
        "emoji": "🐅"
    },
    "ISFP": {
        "nombre": "Gato Maine Coon 🦁",
        "descripcion": "Eres gentil, artístico y con una conexión profunda con la belleza. Como el Maine Coon, tu grandeza está en tu suavidad.",
        "analogia": "Tu sensibilidad artística te permite ver belleza donde otros no la ven.",
        "fortalezas": "Artístico, auténtico, compasivo",
        "caracteristicas": ["Gentil y paciente", "Amante de la naturaleza", "Espíritu libre"],
        "emoji": "🦁"
    },
    "INFP": {
        "nombre": "Gato Angora Turco 🐇",
        "descripcion": "Eres soñador, idealista y con un corazón que busca hacer del mundo un lugar mejor. Como el Angora, tu elegancia es natural.",
        "analogia": "Tu imaginación y valores te guían en crear un impacto positivo.",
        "fortalezas": "Creativo, idealista, auténtico",
        "caracteristicas": ["Soñador y poético", "Muy intuitivo", "Defensor de causas"],
        "emoji": "🐇"
    },
    "INTP": {
        "nombre": "Gato Savannah 🐆",
        "descripcion": "Eres analítico, curioso y siempre cuestionando lo establecido. Como el Savannah, tu mente no conoce límites.",
        "analogia": "Tu sed de conocimiento te lleva a descubrimientos fascinantes.",
        "fortalezas": "Analítico, original, innovador",
        "caracteristicas": ["Pensador abstracto", "Amante de los debates", "Innovador natural"],
        "emoji": "🐆"
    },
    "ESTP": {
        "nombre": "Gato Sphynx 🐘",
        "descripcion": "Eres energético, carismático y el alma de cualquier reunión. Como el Sphynx, rompes moldes con estilo.",
        "analogia": "Tu capacidad para vivir el momento te hace irresistiblemente auténtico.",
        "fortalezas": "Energético, práctico, carismático",
        "caracteristicas": ["Extrovertido y social", "Amante del riesgo", "Espontáneo y divertido"],
        "emoji": "🐘"
    },
    "ESFP": {
        "nombre": "Gato Exótico de Pelo Corto 🐻",
        "descripcion": "Eres juguetón, expresivo y traes alegría a donde vayas. Como el Exótico, tu dulzura es contagiosa.",
        "analogia": "Tu talento para hacer que todos se sientan incluidos es tu superpoder.",
        "fortalezas": "Energético, divertido, empático",
        "caracteristicas": ["Optimista y positivo", "Amante de la diversión", "Conector social"],
        "emoji": "🐻"
    },
    "ENFP": {
        "nombre": "Gato Oriental de Pelo Corto 🐈",
        "descripcion": "Eres entusiasta, creativo y lleno de ideas brillantes. Como el Oriental, siempre tienes algo interesante que compartir.",
        "analogia": "Tu capacidad para inspirar a otros te hace un líder natural.",
        "fortalezas": "Entusiasta, creativo, inspirador",
        "caracteristicas": ["Comunicador nato", "Ideas infinitas", "Optimista contagioso"],
        "emoji": "🐈"
    },
    "ENTP": {
        "nombre": "Gato Van Turco 🏊",
        "descripcion": "Eres innovador, debatidor y siempre buscando nuevos desafíos. Como el Van Turco, amas romper las reglas con inteligencia.",
        "analogia": "Tu mente rápida y aguda te hace excelente resolviendo problemas complejos.",
        "fortalezas": "Innovador, estratégico, persuasivo",
        "caracteristicas": ["Amante del debate", "Solucionador de problemas", "Emprendedor nato"],
        "emoji": "🏊"
    },
    "ESTJ": {
        "nombre": "Gato Chartreux 🐺",
        "descripcion": "Eres organizado, eficiente y un líder natural. Como el Chartreux, tu presencia impone respeto.",
        "analogia": "Tu talento para crear orden del caos te hace invaluable.",
        "fortalezas": "Organizado, decisivo, confiable",
        "caracteristicas": ["Líder natural", "Amante de la eficiencia", "Practical y directo"],
        "emoji": "🐺"
    },
    "ESFJ": {
        "nombre": "Gato Persa 👑",
        "descripcion": "Eres sociable, armonioso y el perfecto anfitrión. Como el Persa, traes elegancia y calma a cualquier situación.",
        "analogia": "Tu capacidad para crear conexiones significativas es tu don especial.",
        "fortalezas": "Sociable, leal, armonioso",
        "caracteristicas": ["Anfitrión perfecto", "Empático y comprensivo", "Creador de comunidad"],
        "emoji": "👑"
    },
    "ENFJ": {
        "nombre": "Gato Birmano 🙏",
        "descripcion": "Eres carismático, inspirador y con un don para guiar a otros. Como el Birmano, tu presencia es casi mágica.",
        "analogia": "Tu capacidad para ver el potencial en otros te hace un mentor excepcional.",
        "fortalezas": "Inspirador, empático, carismático",
        "caracteristicas": ["Líder servicial", "Comunicador inspirador", "Armonizador natural"],
        "emoji": "🙏"
    },
    "ENTJ": {
        "nombre": "Gato Savannah F1 🐆",
        "descripcion": "Eres estratégico, ambicioso y nacido para liderar. Como el Savannah, tu presencia demanda atención y respeto.",
        "analogia": "Tu visión clara y determinación te llevan a lograr grandes cosas.",
        "fortalezas": "Estratégico, decisivo, visionario",
        "caracteristicas": ["Líder nato", "Pensamiento estratégico", "Implementador eficaz"],
        "emoji": "🐆"
    }
}


# Función para calcular el resultado MBTI
def calcular_mbti(respuestas):
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    for i, respuesta in enumerate(respuestas):
        if i < len(letras_mbti) and respuesta < len(letras_mbti[i]):
            letra = letras_mbti[i][respuesta]
            scores[letra] += 1

    mbti = ""
    mbti += "E" if scores["E"] > scores["I"] else "I"
    mbti += "S" if scores["S"] > scores["N"] else "N"
    mbti += "T" if scores["T"] > scores["F"] else "F"
    mbti += "J" if scores["J"] > scores["P"] else "P"

    return mbti


# Función para mostrar la pregunta actual
def mostrar_pregunta(num_pregunta):
    st.progress((num_pregunta + 1) / len(preguntas))
    st.caption(f"Pregunta {num_pregunta + 1} de {len(preguntas)}")

    # Mostrar categoría con estilo especial
    st.markdown(f'<div class="question-category">{preguntas[num_pregunta]["categoria"]}</div>', unsafe_allow_html=True)

    st.subheader(preguntas[num_pregunta]["pregunta"])

    opcion_seleccionada = st.radio(
        "Selecciona la opción que más se identifique contigo:",
        preguntas[num_pregunta]["opciones"],
        key=f"pregunta_{num_pregunta}",
        index=None
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if num_pregunta > 0:
            if st.button("← Anterior"):
                st.session_state.pagina_actual -= 1
                st.rerun()
    with col2:
        if opcion_seleccionada:
            if st.button("Siguiente →" if num_pregunta < len(preguntas) - 1 else "🐾 Descubrir mi gato"):
                indice_seleccionado = preguntas[num_pregunta]["opciones"].index(opcion_seleccionada)
                if len(st.session_state.respuestas) <= num_pregunta:
                    st.session_state.respuestas.append(indice_seleccionado)
                else:
                    st.session_state.respuestas[num_pregunta] = indice_seleccionado

                if num_pregunta < len(preguntas) - 1:
                    st.session_state.pagina_actual += 1
                    st.rerun()
                else:
                    st.session_state.pagina_actual = len(preguntas)
                    st.rerun()
        else:
            st.button("Siguiente →" if num_pregunta < len(preguntas) - 1 else "🐾 Descubrir mi gato", disabled=True)


# Función para mostrar resultados
def mostrar_resultado():
    resultado_mbti = calcular_mbti(st.session_state.respuestas)
    gato = tipos_gato[resultado_mbti]

    st.balloons()
    st.title(f"¡{st.session_state.nombre}, eres un {gato['nombre']}!")

    # Emoji del gato grande
    st.markdown(f"<div class='cat-image'>{gato['emoji']}</div>", unsafe_allow_html=True)

    # Tarjeta de resultado principal
    st.markdown(f"""
    <div class='result-card'>
        <h3>{gato['emoji']} {gato['nombre']}</h3>
        <p><strong>Descripción:</strong> {gato['descripcion']}</p>
        <p><strong>Por qué este gato te representa:</strong> {gato['analogia']}</p>
        <p><strong>Tus fortalezas felinas:</strong> {gato['fortalezas']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Características del gato
    st.subheader("🐾 Rasgos de tu personalidad gatuna:")
    for caracteristica in gato['caracteristicas']:
        st.markdown(f"• **{caracteristica}**")

    # Mensaje especial
    st.markdown(f'<div class="purr-fect">¡Purr-fect! Has descubierto tu esencia felina</div>', unsafe_allow_html=True)

    # Datos curiosos
    with st.expander("🔍 Curiosidades sobre tu tipo de gato"):
        st.markdown(f"""
        **Datos interesantes sobre tu personalidad:**

        - **Tu estilo de comunicación**: {'Directo y claro' if resultado_mbti[2] == 'T' else 'Empático y armonioso'}
        - **Tu energía social**: {'Extravertida y expansiva' if resultado_mbti[0] == 'E' else 'Introvertida y selectiva'}
        - **Tu enfoque de vida**: {'Estructurado y planificado' if resultado_mbti[3] == 'J' else 'Flexible y espontáneo'}
        - **Tu forma de procesar información**: {'Práctica y concreta' if resultado_mbti[1] == 'S' else 'Intuitiva y abstracta'}

        **Compatibilidad gatuna**: Te llevas mejor con gatos {['tranquilos', 'aventureros', 'juguetones', 'misteriosos'][hash(resultado_mbti) % 4]}
        """)

    # Botón para reiniciar
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Volver a hacer el test", use_container_width=True):
            st.session_state.respuestas = []
            st.session_state.pagina_actual = 0
            st.session_state.nombre = ""
            st.rerun()


# Lógica principal
if st.session_state.pagina_actual < len(preguntas):
    mostrar_pregunta(st.session_state.pagina_actual)
else:
    mostrar_resultado()

# Nota al pie
st.markdown("---")
st.caption("✨ Test creado con mucho cariño felino - Descubre tu espíritu animal interior")