import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="¿Qué Tipo de Café Eres?",
    page_icon="☕",
    layout="centered"
)

# Estilos CSS para un diseño atractivo
st.markdown("""
<style>
    body {
        background-color: #f8f0e6;
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background-color: #C4DFFF;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stTitle {
        color: #e65100;
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stMarkdown {
        color: #4a4a4a;
        font-size: 1.1em;
        text-align: center;
    }
    .stTextInput > label {
        color: #e65100;
        font-weight: bold;
        font-size: 1.2em;
    }
    .stTextInput > div > input {
        border: 2px solid #ffcc80;
        border-radius: 10px;
        padding: 10px;
        font-size: 1em;
    }
    .stRadio > label {
        color: #e65100;
        font-weight: bold;
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    .stRadio > div > label {
        background-color: #F2F8FF;
        padding: 12px;
        border-radius: 10px;
        margin: 5px 0;
        color: #4a4a4a;
        font-size: 1em;
        transition: all 0.3s ease;
    }
    .stRadio > div > label:hover {
        background-color: #ffcc80;
        cursor: pointer;
    }
    .stButton > button {
        background-color: #e65100;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 1.1em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #bf360c;
        transform: scale(1.05);
    }
    .stButton > button:disabled {
        background-color: #e0e0e0;
        color: #9e9e9e;
    }
    .stProgress .st-bo {
        background-color: #ffcc80;
    }
    .stProgress .st-bo > div {
        background-color: #e65100;
    }
    .stSuccess {
        background-color: #fff3e0;
        padding: 15px;
        border-radius: 10px;
        color: #e65100;
        font-size: 1.2em;
        font-weight: bold;
        text-align: center;
    }
    .stCaption {
        color: #757575;
        font-style: italic;
        text-align: center;
    }
    .stBarChart {
        background-color: #fff8ee;
        padding: 10px;
        border-radius: 10px;
    }
    .coffee-image {
        text-align: center;
        margin: 20px 0;
    }
    .result-card {
        background-color: #fff8ee;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #e65100;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Título e introducción
st.title("☕ Test de Personalidad: ¿Qué Tipo de Café Eres?")
st.markdown("""
Descubre qué tipo de café refleja mejor tu personalidad con este test psicológico.  
Responde las 12 preguntas y conoce tu café ideal basado en tu forma de ser.
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
        st.success(f"¡Perfecto, {st.session_state.nombre}! Ahora comencemos con el test.")
        st.rerun()
    st.stop()

# Preguntas de personalidad general (no relacionadas con café)
preguntas = [
    # Dimensión 1: Energía (Extraversión/Introversión)
    {
        "pregunta": "1. ¿Cómo recargas energías después de un día agotador?",
        "dimension": "Energía",
        "opciones": [
            "Salgo con amigos o familia, necesito interactuar y compartir experiencias",
            "Me quedo en casa solo o con alguien cercano, necesito tranquilidad",
            "Planifico actividades relajantes como leer o ver una película",
            "Hago ejercicio o alguna actividad física que me active"
        ]
    },
    {
        "pregunta": "2. En una fiesta, ¿cómo sueles comportarte?",
        "dimension": "Energía",
        "opciones": [
            "Soy el alma de la fiesta, conozco a todo el mundo",
            "Prefiero conversaciones profundas con pocas personas",
            "Me muevo por grupos, alternando entre socializar y observar",
            "Busco un rincón tranquilo y espero que alguien se me acerque"
        ]
    },
    {
        "pregunta": "3. ¿Cómo manejas los problemas importantes?",
        "dimension": "Energía",
        "opciones": [
            "Los discuto con varias personas para tener diferentes perspectivas",
            "Reflexiono solo antes de tomar una decisión",
            "Analizo los pros y contras de manera sistemática",
            "Sigo mi intuición y lo que me hace sentir bien"
        ]
    },

    # Dimensión 2: Percepción (Sensación/Intuición)
    {
        "pregunta": "4. ¿Cómo describes tu forma de pensar?",
        "dimension": "Percepción",
        "opciones": [
            "Práctica y concreta, me baso en hechos y experiencias",
            "Creativa e imaginativa, veo posibilidades donde otros no",
            "Analítica y detallada, todo debe tener lógica",
            "Empática e intuitiva, confío en mis corazonadas"
        ]
    },
    {
        "pregunta": "5. Al aprender algo nuevo, prefieres:",
        "dimension": "Percepción",
        "opciones": [
            "Instrucciones paso a paso y ejemplos concretos",
            "Explorar libremente y descubrir por mí mismo",
            "Entender la teoría detrás antes de practicar",
            "Aprender haciendo y experimentando en el momento"
        ]
    },
    {
        "pregunta": "6. ¿Qué tipo de películas o libros prefieres?",
        "dimension": "Percepción",
        "opciones": [
            "Basados en hechos reales o documentales",
            "Ciencia ficción o fantasía con mundos imaginativos",
            "Thrillers o misterios que requieran resolver acertijos",
            "Dramas humanos con emociones profundas"
        ]
    },

    # Dimensión 3: Toma de decisiones (Pensamiento/Sentimiento)
    {
        "pregunta": "7. Al tomar decisiones importantes, priorizas:",
        "dimension": "Decisiones",
        "opciones": [
            "La lógica y los datos objetivos",
            "Los sentimientos y valores personales",
            "El impacto en las relaciones humanas",
            "La eficiencia y los resultados prácticos"
        ]
    },
    {
        "pregunta": "8. En el trabajo, tu mayor fortaleza es:",
        "dimension": "Decisiones",
        "opciones": [
            "Resolver problemas complejos con razonamiento",
            "Motivar y conectar emocionalmente con el equipo",
            "Organizar y planificar meticulosamente",
            "Adaptarte rápidamente a los cambios"
        ]
    },
    {
        "pregunta": "9. Cuando alguien está en desacuerdo contigo:",
        "dimension": "Decisiones",
        "opciones": [
            "Presento argumentos lógicos para persuadir",
            "Busco un punto medio que satisfaga a todos",
            "Escucho su perspectiva y trato de entender",
            "Defiendo mi posición con convicción"
        ]
    },

    # Dimensión 4: Estilo de vida (Juicio/Percepción)
    {
        "pregunta": "10. ¿Cómo organizas tu tiempo?",
        "dimension": "Estilo de Vida",
        "opciones": [
            "Con horarios estrictos y listas de tareas",
            "De manera flexible, según cómo me sienta",
            "Planifico pero dejo espacio para improvisar",
            "Voy resolviendo las cosas según surgen"
        ]
    },
    {
        "pregunta": "11. Ante un proyecto nuevo, tu enfoque es:",
        "dimension": "Estilo de Vida",
        "opciones": [
            "Investigar todo antes de comenzar",
            "Lanzarme y aprender en el proceso",
            "Establecer metas claras y plazos",
            "Improvisar y ajustar sobre la marcha"
        ]
    },
    {
        "pregunta": "12. ¿Cómo describes tu ambiente ideal?",
        "dimension": "Estilo de Vida",
        "opciones": [
            "Ordenado y predecible",
            "Estimulante y lleno de posibilidades",
            "Armonioso y acogedor",
            "Dinámico y con desafíos constantes"
        ]
    }
]

# Sistema de puntuación MBTI mejorado
letras_mbti = [
    # Preguntas 0-2: E/I
    ["E", "I", "E", "I"],  # Más opciones para matices
    ["E", "I", "E", "I"],
    ["E", "I", "T", "F"],
    # Preguntas 3-5: S/N
    ["S", "N", "T", "F"],
    ["S", "N", "T", "F"],
    ["S", "N", "T", "F"],
    # Preguntas 6-8: T/F
    ["T", "F", "F", "T"],
    ["T", "F", "J", "P"],
    ["T", "F", "F", "T"],
    # Preguntas 9-11: J/P
    ["J", "P", "J", "P"],
    ["J", "P", "J", "P"],
    ["J", "P", "F", "E"]
]

# Tipos de café con descripciones mejoradas
tipos_cafe = {
    "ISTJ": {
        "nombre": "Americano Clásico",
        "descripcion": "Eres confiable, estructurado y sin complicaciones. Como el Americano, eres directo y efectivo. Tu enfoque práctico y tu lealtad te hacen la base confiable de cualquier grupo.",
        "analogia": "Así como el Americano es esencial y siempre satisface, tú eres la persona en quien todos confían.",
        "fortalezas": "Responsable, organizado, práctico"
    },
    "ISFJ": {
        "nombre": "Latte Vainilla",
        "descripcion": "Eres cálido, reconfortante y siempre estás cuidando de los demás. Como el Latte Vainilla, aportas dulzura y comfort a la vida de quienes te rodean.",
        "analogia": "Tu naturaleza protectora y tu atención a los detalles te hacen indispensable para tu círculo cercano.",
        "fortalezas": "Empático, leal, servicial"
    },
    "INFJ": {
        "nombre": "Café de Filtro (Pour Over)",
        "descripcion": "Eres profundo, intuitivo y con capas de complejidad que se revelan con el tiempo. Como el café de filtro, requieres paciencia para ser apreciado completamente.",
        "analogia": "Tu sabiduría interior y tu comprensión de las emociones humanas te hacen un consejero natural.",
        "fortalezas": "Visionario, empático, perspicaz"
    },
    "INTJ": {
        "nombre": "Espresso Doble",
        "descripcion": "Eres intenso, estratégico y vas directo al grano. Como el espresso doble, eres concentrado y potente, con una claridad que impresiona.",
        "analogia": "Tu mente analítica y tu capacidad para ver el panorama general te hacen un estratega excepcional.",
        "fortalezas": "Estratégico, independiente, decidido"
    },
    "ISTP": {
        "nombre": "Cold Brew Nitro",
        "descripcion": "Eres práctico, innovador y con un toque de frescura. Como el cold brew nitro, combinas técnica con un estilo único y refrescante.",
        "analogia": "Tu habilidad para resolver problemas en el momento y tu adaptabilidad te hacen invaluable en crisis.",
        "fortalezas": "Adaptable, lógico, hábil"
    },
    "ISFP": {
        "nombre": "Mocha",
        "descripcion": "Eres artístico, sensible y con un dulce equilibrio entre practicidad y creatividad. Como el mocha, armonizas diferentes elementos con gracia.",
        "analogia": "Tu aprecio por la belleza y tu autenticidad te hacen una presencia calmante y inspiradora.",
        "fortalezas": "Artístico, auténtico, compasivo"
    },
    "INFP": {
        "nombre": "Café Etíope Yirgacheffe",
        "descripcion": "Eres idealista, con profundidad emocional y notas de creatividad única. Como este café especial, tienes matices que sorprenden y inspiran.",
        "analogia": "Tu pasión por tus valores y tu capacidad para ver lo mejor en las personas te hacen un idealista práctico.",
        "fortalezas": "Creativo, idealista, auténtico"
    },
    "INTP": {
        "nombre": "Chemex",
        "descripcion": "Eres analítico, curioso y siempre buscando la perfección teórica. Como la chemex, aprecias la elegancia de los sistemas bien diseñados.",
        "analogia": "Tu sed de conocimiento y tu pensamiento original te hacen un innovador natural.",
        "fortalezas": "Analítico, original, lógico"
    },
    "ESTP": {
        "nombre": "Cortado",
        "descripcion": "Eres energético, práctico y te adaptas rápidamente. Como el cortado, eres equilibrado y efectivo, perfecto para la acción.",
        "analogia": "Tu carisma natural y tu capacidad para pensar rápido te hacen destacar en situaciones dinámicas.",
        "fortalezas": "Energético, práctico, persuasivo"
    },
    "ESFP": {
        "nombre": "Frappé",
        "descripcion": "Eres vibrante, espontáneo y la vida de la fiesta. Como el frappé, traes frescura y diversión a cualquier situación.",
        "analogia": "Tu entusiasmo contagioso y tu capacidad para vivir el momento te hacen irresistible.",
        "fortalezas": "Energético, divertido, práctico"
    },
    "ENFP": {
        "nombre": "Cold Brew con Infusión Exótica",
        "descripcion": "Eres entusiasta, creativo y lleno de posibilidades. Como este café innovador, siempre traes nuevas ideas y energía.",
        "analogia": "Tu capacidad para conectar ideas y personas te hace un catalizador de creatividad.",
        "fortalezas": "Entusiasta, creativo, sociable"
    },
    "ENTP": {
        "nombre": "Café Turco",
        "descripcion": "Eres innovador, debatidor y poco convencional. Como el café turco, tienes un método único y una intensidad que desafía lo establecido.",
        "analogia": "Tu ingenio rápido y tu amor por el debate te hacen un pensador provocador e inspirador.",
        "fortalezas": "Innovador, estratégico, energético"
    },
    "ESTJ": {
        "nombre": "Macchiato",
        "descripcion": "Eres organizado, decisivo y con un claro sentido del deber. Como el macchiato, eres estructurado pero con un toque de sofisticación.",
        "analogia": "Tu capacidad para implementar sistemas eficientes te hace un líder natural.",
        "fortalezas": "Organizado, decisivo, práctico"
    },
    "ESFJ": {
        "nombre": "Cappuccino Clásico",
        "descripcion": "Eres sociable, armonioso y siempre cuidando del bienestar del grupo. Como el cappuccino, eres equilibrado y siempre bien recibido.",
        "analogia": "Tu talento para crear armonía y tu calidez te hacen el corazón de tu comunidad.",
        "fortalezas": "Sociable, leal, organizado"
    },
    "ENFJ": {
        "nombre": "Café Cubano",
        "descripcion": "Eres carismático, inspirador y con un toque dulce que une a las personas. Como el café cubano, tienes una intensidad que motiva.",
        "analogia": "Tu capacidad para entender y motivar a otros te hace un líder natural y empático.",
        "fortalezas": "Inspirador, empático, estratégico"
    },
    "ENTJ": {
        "nombre": "Ristretto",
        "descripcion": "Eres estratégico, decisivo y con una intensidad enfocada. Como el ristretto, vas directo al grano con máxima eficiencia.",
        "analogia": "Tu visión de largo plazo y tu capacidad de liderazgo te hacen un comandante natural.",
        "fortalezas": "Estratégico, decisivo, visionario"
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
    st.subheader(preguntas[num_pregunta]["pregunta"])
    st.caption(f"Dimensión: {preguntas[num_pregunta]['dimension']}")

    opcion_seleccionada = st.radio(
        "Selecciona la opción que mejor te describa:",
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
            if st.button("Siguiente →" if num_pregunta < len(preguntas) - 1 else "☕ Ver resultado"):
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
            st.button("Siguiente →" if num_pregunta < len(preguntas) - 1 else "☕ Ver resultado", disabled=True)


# Función para mostrar resultados
def mostrar_resultado():
    resultado_mbti = calcular_mbti(st.session_state.respuestas)
    cafe = tipos_cafe[resultado_mbti]

    st.balloons()
    st.title(f"¡{st.session_state.nombre}, eres un {cafe['nombre']}!")

    # Tarjeta de resultado principal
    st.markdown(f"""
    <div class='result-card'>
        <h3>☕ {cafe['nombre']} - {resultado_mbti}</h3>
        <p><strong>Descripción:</strong> {cafe['descripcion']}</p>
        <p><strong>Analogía:</strong> {cafe['analogia']}</p>
        <p><strong>Fortalezas principales:</strong> {cafe['fortalezas']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Emoji del café
    st.markdown("<div class='coffee-image' style='font-size: 4em;'>☕</div>", unsafe_allow_html=True)

    # Explicación detallada
    with st.expander("📖 Ver análisis detallado de tu personalidad-café"):
        st.subheader("¿Por qué este café representa tu personalidad?")
        st.markdown(f"""
        Tu tipo de personalidad **{resultado_mbti}** se caracteriza por:
        - **{resultado_mbti[0]}** ({'Extraversión' if resultado_mbti[0] == 'E' else 'Introversión'}): {'Obtienes energía del mundo exterior' if resultado_mbti[0] == 'E' else 'Recargas energía en la introspección'}
        - **{resultado_mbti[1]}** ({'Sensación' if resultado_mbti[1] == 'S' else 'Intuición'}): {'Te enfocas en hechos y detalles concretos' if resultado_mbti[1] == 'S' else 'Ves patrones y posibilidades futuras'}
        - **{resultado_mbti[2]}** ({'Pensamiento' if resultado_mbti[2] == 'T' else 'Sentimiento'}): {'Decides basado en lógica y objetividad' if resultado_mbti[2] == 'T' else 'Priorizas valores y armonía'}
        - **{resultado_mbti[3]}** ({'Juicio' if resultado_mbti[3] == 'J' else 'Percepción'}): {'Prefieres estructura y planificación' if resultado_mbti[3] == 'J' else 'Eres flexible y espontáneo'}

        **El {cafe['nombre'].lower()}** refleja perfectamente esta combinación única de características.
        """)

    # Botón para reiniciar
    st.markdown("---")
    if st.button("🔄 Volver a hacer el test"):
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
st.caption("¡Descubre tu esencia en cada taza! Este test se basa en principios psicológicos similares al MBTI")