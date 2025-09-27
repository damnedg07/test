import streamlit as st
import pandas as pd
import uuid

# Configuración de la página
st.set_page_config(
    page_title="¿Qué Tipo de Pan Eres?",
    page_icon="🍞",
    layout="centered"
)

# Estilos CSS para un diseño atractivo
st.markdown("""
<style>
    body {
        background-color: #f8edeb;
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        background-color: #fff3e0;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .stTitle {
        color: #d81b60;
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
        color: #d81b60;
        font-weight: bold;
        font-size: 1.2em;
    }
    .stTextInput > div > input {
        border: 2px solid #ffb6c1;
        border-radius: 10px;
        padding: 10px;
        font-size: 1em;
    }
    .stRadio > label {
        color: #d81b60;
        font-weight: bold;
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    .stRadio > div > label {
        background-color: #ffebee;
        padding: 12px;
        border-radius: 10px;
        margin: 5px 0;
        color: #4a4a4a;
        font-size: 1em;
        transition: all 0.3s ease;
    }
    .stRadio > div > label:hover {
        background-color: #ffcdd2;
        cursor: pointer;
    }
    .stButton > button {
        background-color: #d81b60;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 1.1em;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #ad1457;
        transform: scale(1.05);
    }
    .stButton > button:disabled {
        background-color: #e0e0e0;
        color: #9e9e9e;
    }
    .stProgress .st-bo {
        background-color: #ffb6c1;
    }
    .stProgress .st-bo > div {
        background-color: #d81b60;
    }
    .stSuccess {
        background-color: #fce4ec;
        padding: 15px;
        border-radius: 10px;
        color: #d81b60;
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
        background-color: #fff3e0;
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Título e introducción
st.title("🍞 Test de Personalidad: ¿Qué Tipo de Pan Eres?")
st.markdown("""
Descubre qué tipo de pan refleja mejor tu personalidad con este divertido test.  
Responde las 10 preguntas y conoce tu esencia panadera, ¡personalizada solo para ti!
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

# Preguntas y opciones
preguntas = [
    {
        "pregunta": "1. ¿Cómo describes tu energía durante el día?",
        "opciones": [
            "Explosiva y llena de vitalidad desde primera hora",
            "Constante y equilibrada",
            "Me tomo mi tiempo para activarme",
            "Intensa pero breve, luego necesito recargar"
        ]
    },
    {
        "pregunta": "2. En una situación social, tú eres:",
        "opciones": [
            "El alma de la fiesta, siempre con algo que decir",
            "Alguien que une a las personas y crea armonía",
            "Observador y reservado, pero con profundidad",
            "Directo y auténtico, sin rodeos"
        ]
    },
    {
        "pregunta": "3. Tu estilo personal se podría describir como:",
        "opciones": [
            "Llamativo y original",
            "Clásico y elegante",
            "Tradicional y confortable",
            "Minimalista y funcional"
        ]
    },
    {
        "pregunta": "4. ¿Cómo manejas los desafíos?",
        "opciones": [
            "Con creatividad e ideas innovadoras",
            "Con paciencia y perseverancia",
            "Con calma y método probado",
            "Con decisión y acción inmediata"
        ]
    },
    {
        "pregunta": "5. Tu ambiente ideal sería:",
        "opciones": [
            "Un lugar lleno de estímulos y posibilidades",
            "Un espacio armonioso y acogedor",
            "Un entorno familiar y cómodo",
            "Algo práctico y sin complicaciones"
        ]
    },
    {
        "pregunta": "6. ¿Qué valoras más en las relaciones?",
        "opciones": [
            "La emoción y la espontaneidad",
            "La confianza y la lealtad",
            "La calidez y el cuidado",
            "La honestidad y la transparencia"
        ]
    },
    {
        "pregunta": "7. Tu filosofía de vida es:",
        "opciones": [
            "¡Vive el momento!",
            "Todo a su tiempo y con medida",
            "La tradición es sabia",
            "Menos es más"
        ]
    },
    {
        "pregunta": "8. En tu tiempo libre prefieres:",
        "opciones": [
            "Probar actividades nuevas y aventureras",
            "Disfrutar de momentos tranquilos con seres queridos",
            "Hacer actividades reconfortantes de siempre",
            "Enfocarte en tus hobbies específicos"
        ]
    },
    {
        "pregunta": "9. Tu approach culinario es:",
        "opciones": [
            "Experimental y atrevido",
            "Equilibrado y nutritivo",
            "Reconfortante y tradicional",
            "Funcional y sencillo"
        ]
    },
    {
        "pregunta": "10. ¿Cómo te ven los demás?",
        "opciones": [
            "Como alguien lleno de sorpresas",
            "Como una persona confiable y estable",
            "Como alguien cálido y acogedor",
            "Como una persona auténtica y directa"
        ]
    }
]

# Tipos de pan con descripciones personalizadas
tipos_pan = {
    "Brioche": {
        "descripcion": "{nombre}, eres **Brioche**: dulce, rico y un poco extravagante. Como el brioche, sabes disfrutar de los placeres de la vida. Tu personalidad cálida y alegre atrae a todos, con un toque indulgentemente dulce que hace que los demás se sientan cómodos. Eres el alma de la fiesta, pero también sabes ser refinado cuando la situación lo requiere."
    },
    "Pan Integral": {
        "descripcion": "{nombre}, eres **Pan Integral**: equilibrado, confiable y nutritivo. Eres la persona en quien todos confían, con los pies en la tierra y una sabiduría práctica que todos admiran. No necesitas ser el centro de atención, pero tu presencia constante y reconfortante es invaluable para tu círculo."
    },
    "Pan de Centeno": {
        "descripcion": "{nombre}, eres **Pan de Centeno**: intenso, con carácter y profundidad. Como el pan de centeno, tienes una personalidad compleja que se aprecia con el tiempo. Eres alguien con convicciones firmes y una sabiduría que viene de experiencias profundas, valorado por tu autenticidad."
    },
    "Baguette": {
        "descripcion": "{nombre}, eres **Baguette**: clásico, elegante y con estilo. Como la baguette, tienes una apariencia refinada y una esencia atemporal. Eres directo, honesto y aprecias la simplicidad y la calidad, con un toque de sofisticación que no pasa desapercibido."
    },
    "Pan de Maíz": {
        "descripcion": "{nombre}, eres **Pan de Maíz**: único, con personalidad y un toque especial. Como el pan de maíz, eres inesperadamente encantador y memorable. Tu calidez natural reconforta a los demás, y aunque puedas parecer simple, tienes una profundidad que te hace irresistible."
    },
    "Pan Árabe/Pita": {
        "descripcion": "{nombre}, eres **Pan Árabe/Pita**: versátil, adaptable y siempre útil. Como el pan pita, te amoldas a diferentes situaciones sin perder tu esencia. Eres práctico, ingenioso y siempre encuentras la manera de conectar con los demás, siendo indispensable en cualquier grupo."
    }
}

# Sistema de puntuación
puntuaciones = {
    0: ["Brioche", "Pan de Maíz", "Pan Integral", "Baguette"],
    1: ["Brioche", "Pan Integral", "Pan de Centeno", "Baguette"],
    2: ["Brioche", "Baguette", "Pan Integral", "Pan Árabe/Pita"],
    3: ["Brioche", "Pan Integral", "Pan de Centeno", "Baguette"],
    4: ["Brioche", "Pan Integral", "Pan de Maíz", "Pan Árabe/Pita"],
    5: ["Brioche", "Pan Integral", "Pan de Maíz", "Baguette"],
    6: ["Brioche", "Pan Integral", "Pan de Centeno", "Pan Árabe/Pita"],
    7: ["Brioche", "Pan Integral", "Pan de Maíz", "Pan Árabe/Pita"],
    8: ["Brioche", "Pan Integral", "Pan de Maíz", "Pan Árabe/Pita"],
    9: ["Brioche", "Pan Integral", "Pan de Maíz", "Baguette"]
}

# Función para calcular el resultado
def calcular_resultado(respuestas):
    contador = {pan: 0 for pan in tipos_pan.keys()}
    for i, respuesta in enumerate(respuestas):
        pan_asociado = puntuaciones[i][respuesta]
        contador[pan_asociado] += 1
    return max(contador, key=contador.get)

# Mostrar la pregunta actual
def mostrar_pregunta(num_pregunta):
    st.progress(num_pregunta / len(preguntas))
    st.caption(f"Pregunta {num_pregunta + 1} de {len(preguntas)}")
    st.subheader(preguntas[num_pregunta]["pregunta"])

    opcion_seleccionada = st.radio(
        "Selecciona una opción:",
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
            if st.button("Siguiente →" if num_pregunta < len(preguntas) - 1 else "🍞 Ver resultado"):
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
            st.button("Siguiente →" if num_pregunta < len(preguntas) - 1 else "🍞 Ver resultado", disabled=True)

# Mostrar resultados
def mostrar_resultado():
    resultado = calcular_resultado(st.session_state.respuestas)
    st.balloons()
    st.title(f"¡{st.session_state.nombre}, eres {resultado}!")
    st.markdown(tipos_pan[resultado]["descripcion"].format(nombre=st.session_state.nombre))

    st.subheader("Cómo se comparan tus resultados:")
    datos = {pan: 0 for pan in tipos_pan.keys()}
    for i, respuesta in enumerate(st.session_state.respuestas):
        pan_asociado = puntuaciones[i][respuesta]
        datos[pan_asociado] += 1
    df = pd.DataFrame.from_dict(datos, orient='index', columns=['Puntuación'])
    st.bar_chart(df, color="#d81b60")

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
st.caption("¡Horneado con ❤️ por tu panadería virtual!")