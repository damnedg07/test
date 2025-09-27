import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="¿Qué Tipo de Taco Eres?",
    page_icon="🌮",
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
    .taco-image {
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Título e introducción
st.title("🌮 Test de Personalidad: ¿Qué Tipo de Taco Eres?")
st.markdown("""
Descubre qué tipo de taco refleja mejor tu personalidad con este test basado en dimensiones psicológicas del 16PF de Cattell.  
Responde las 16 preguntas y conoce tu esencia taquera, ¡personalizada solo para ti!
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

# Preguntas basadas en las 16 dimensiones del 16PF de Cattell
preguntas = [
    {
        "pregunta": "1. ¿Cómo te describes en situaciones sociales?",
        "dimension": "Afectividad (Reservado vs. Abierto)",
        "opciones": [
            "Prefiero observar desde la distancia",
            "Disfruto interactuar pero con personas conocidas",
            "Soy el centro de atención en cualquier reunión",
            "Me adapto según el grupo, puedo ser ambas cosas"
        ]
    },
    {
        "pregunta": "2. Cuando enfrentas problemas complejos, ¿cómo reaccionas?",
        "dimension": "Razonamiento (Concreto vs. Abstracto)",
        "opciones": [
            "Busco soluciones prácticas e inmediatas",
            "Analizo todas las posibilidades antes de decidir",
            "Confío en mi intuición más que en el análisis",
            "Pido consejo a personas con experiencia"
        ]
    },
    {
        "pregunta": "3. ¿Cómo manejas tus emociones en situaciones estresantes?",
        "dimension": "Estabilidad (Reactivo vs. Estable)",
        "opciones": [
            "Me altero fácilmente y lo demuestro",
            "Mantengo la calma exterior aunque internamente esté estresado",
            "Raramente me altero, mantengo el control",
            "Depende del nivel de estrés, varía mi reacción"
        ]
    },
    {
        "pregunta": "4. En tu estilo de vida, ¿qué valoras más?",
        "dimension": "Dominancia (Sumiso vs. Dominante)",
        "opciones": [
            "Seguir mis propias reglas y dirigir mi camino",
            "Adaptarme a las circunstancias sin confrontar",
            "Encontrar equilibrio entre dirigir y seguir",
            "Colaborar en igualdad con los demás"
        ]
    },
    {
        "pregunta": "5. ¿Cómo describes tu nivel de energía habitual?",
        "dimension": "Impulsividad (Sereno vs. Entusiasta)",
        "opciones": [
            "Soy tranquilo y pausado en mis acciones",
            "Tengo explosiones de energía intermitentes",
            "Mantengo un nivel constante de energía",
            "Siempre estoy lleno de vitalidad y entusiasmo"
        ]
    },
    {
        "pregunta": "6. Al tomar decisiones, ¿qué tiendes a priorizar?",
        "dimension": "Conformidad (Normativo vs. Flexible)",
        "opciones": [
            "Sigo las reglas y procedimientos establecidos",
            "Adapto las reglas a la situación particular",
            "Creo mis propias reglas según mi criterio",
            "Busco consenso con el grupo antes de decidir"
        ]
    },
    {
        "pregunta": "7. En situaciones de riesgo, ¿cómo sueles comportarte?",
        "dimension": "Atrevimiento (Tímido vs. Aventurero)",
        "opciones": [
            "Evito los riesgos y prefiero la seguridad",
            "Calculo cuidadosamente antes de tomar riesgos",
            "Disfruto la adrenalina de tomar riesgos",
            "Depende del área, soy diferente en lo profesional vs. personal"
        ]
    },
    {
        "pregunta": "8. ¿Cómo es tu sensibilidad hacia los demás?",
        "dimension": "Sensibilidad (Duro vs. Sensible)",
        "opciones": [
            "Soy práctico y me centro en los hechos",
            "Soy empático y me afectan las emociones ajenas",
            "Intento equilibrar razón y emoción",
            "Depende de mi relación con la persona"
        ]
    },
    {
        "pregunta": "9. ¿Cómo manejas la desconfianza en las relaciones?",
        "dimension": "Vigilancia (Confiado vs. Suspicaz)",
        "opciones": [
            "Confío hasta que me demuestren lo contrario",
            "Soy cauteloso al principio hasta ganar confianza",
            "Desconfío instintivamente de personas nuevas",
            "Analizo cada caso particular sin generalizar"
        ]
    },
    {
        "pregunta": "10. ¿Dónde sueles poner el foco de tu atención?",
        "dimension": "Abrasión (Práctico vs. Imaginativo)",
        "opciones": [
            "En lo concreto y tangible",
            "En posibilidades futuras e ideas innovadoras",
            "En el presente, disfrutando el momento",
            "En el análisis de patrones y conexiones"
        ]
    },
    {
        "pregunta": "11. ¿Cómo manejas la información privada?",
        "dimension": "Privacidad (Franco vs. Discreto)",
        "opciones": [
            "Soy abierto y comparto fácilmente",
            "Soy selectivo sobre qué comparto y con quién",
            "Soy reservado y mantengo mi privacidad",
            "Depende del tema, hay áreas más privadas que otras"
        ]
    },
    {
        "pregunta": "12. ¿Cómo te sientes acerca del cambio?",
        "dimension": "Apertura (Tradicional vs. Abierto)",
        "opciones": [
            "Prefiero la estabilidad y lo conocido",
            "Disfruto explorar nuevas experiencias",
            "Acepto cambios necesarios pero no los busco",
            "Me entusiasma crear e impulsar cambios"
        ]
    },
    {
        "pregunta": "13. ¿Cómo es tu autopercepción?",
        "dimension": "Autosuficiencia (Grupal vs. Autónomo)",
        "opciones": [
            "Confío en mi propio criterio por encima de todo",
            "Valoro las opiniones del grupo para decidir",
            "Busco equilibrio entre autonomía y consejo",
            "Depende del área, soy más autónomo en unos temas que en otros"
        ]
    },
    {
        "pregunta": "14. ¿Cómo manejas tus metas personales?",
        "dimension": "Perfeccionismo (Tolerante vs. Perfeccionista)",
        "opciones": [
            "Soy flexible y me adapto a los resultados",
            "Me esfuerzo por alcanzar estándares altos",
            "Soy exigente conmigo mismo y con los demás",
            "Equilibro ambición con bienestar emocional"
        ]
    },
    {
        "pregunta": "15. ¿Cómo manejas la tensión en tu vida?",
        "dimension": "Tensión (Relajado vs. Tensión)",
        "opciones": [
            "Manejo el estrés con facilidad",
            "Experimento altibajos de tensión",
            "Me siento frecuentemente tensionado",
            "Tengo áreas de tensión específicas pero no generalizadas"
        ]
    },
    {
        "pregunta": "16. Finalmente, ¿cómo describes tu actitud general hacia la vida?",
        "dimension": "Optimismo (Serio vs. Despreocupado)",
        "opciones": [
            "Soy realista, veo tanto lo positivo como lo negativo",
            "Tengo una actitud positiva y optimista",
            "Soy cauteloso y anticipo posibles problemas",
            "Varío según las circunstancias, no tengo una actitud fija"
        ]
    }
]

# Tipos de tacos con descripciones basadas en perfiles psicológicos
tipos_taco = {
    "Al Pastor": {
        "descripcion": "{nombre}, eres un Taco **Al Pastor**: Extrovertido, vibrante y siempre listo para la fiesta. Como el pastor, tienes una personalidad carismática que atrae a los demás. Eres sociable (A+), entusiasta (F+) y abierto al cambio (Q1+). Sabes adaptarte a diferentes situaciones pero siempre mantienes tu esencia única. Tu energía es contagiosa y brings sazón a cualquier reunión.",
        "factores": ["A+", "F+", "Q1+", "H+"]
    },
    "Suadero": {
        "descripcion": "{nombre}, eres un Taco de **Suadero**: Relajado, adaptable y siempre presente. Eres estable emocionalmente (C+), sereno (F-) y práctico (I-). No necesitas ser el centro de atención pero tu presencia constante es reconfortante. Eres la persona en quien todos confían para mantener la calma y encontrar soluciones pragmáticas. Tu flexibilidad (Q3-) te permite amoldarte a diferentes situaciones sin perder tu esencia.",
        "factores": ["C+", "F-", "I-", "Q3-"]
    },
    "Barbacoa": {
        "descripcion": "{nombre}, eres un Taco de **Barbacoa**: Serio, profundo y de domingo. Eres reservado (A-), analítico (B+) y tradicional (Q1-). Como la barbacoa, tienes capas de complejidad que se aprecian con tiempo. Valoras la calidad sobre la cantidad en tus relaciones y actividades. Eres perfeccionista (Q3+) y autónomo (Q2+), prefiriendo profundizar en pocos temas antes que superficialmente en muchos.",
        "factores": ["A-", "B+", "Q1-", "Q3+"]
    },
    "Carnitas": {
        "descripcion": "{nombre}, eres un Taco de **Carnitas**: Auténtico, intenso y con carácter. Eres dominante (E+), atrevido (H+) y vigilante (L+). Como las carnitas, no pasas desapercibido y tienes una presencia que se hace notar. Eres directo en tu comunicación y valoras la honestidad por encima de la diplomacia. Tomas riesgos calculados (H+) y confías en tu propio criterio (Q2+).",
        "factores": ["E+", "H+", "L+", "Q2+"]
    },
    "Lengua": {
        "descripcion": "{nombre}, eres un Taco de **Lengua**: Sofisticado, de gustos refinados y no para todos los paladares. Eres imaginativo (M+), sensible (I+) y discreto (N+). Como la lengua, eres un gusto adquirido que no todos aprecian inmediatamente. Tienes profundidad intelectual y emocional, prefiriendo conversaciones sustanciales sobre trivialidades. Valoras la privacidad (N+) y tienes un círculo cercano pequeño pero significativo.",
        "factores": ["M+", "I+", "N+", "Q2+"]
    },
    "Birria": {
        "descripcion": "{nombre}, eres un Taco de **Birria**: Reconfortante, tradicional y con profundidad de sabor. Eres estable (C+), normativo (G+) y grupal (Q2-). Como la birria, represents comfort y tradición. Eres la persona a quien acuden los demás para sentirse reconfortados y aconsejados. Valoras las tradiciones (Q1-) y mantienes conexiones profundas con tus raíces y comunidad. Eres confiable (L-) y afectuoso (A+).",
        "factores": ["C+", "G+", "Q1-", "Q2-"]
    },
    "Vegano": {
        "descripcion": "{nombre}, eres un Taco **Vegano**: Innovador, consciente y con principios firmes. Eres abierto al cambio (Q1+), flexible (Q3-) y idealista (M+). Como el taco vegano, challenges convenciones y buscas alternativas diferentes. Eres suspicaz (L+) hacia normas establecidas y cuestionas el status quo. Tienes fuertes convicciones éticas y buscas coherencia entre tus valores y acciones. A veces juzgas en silencio (L+) pero desde un lugar de integridad personal.",
        "factores": ["Q1+", "Q3-", "M+", "L+"]
    },
    "Canasta": {
        "descripcion": "{nombre}, eres un Taco de **Canasta**: Práctico, eficiente y siempre disponible. Eres concreto (B-), relajado (Q4-) y funcional (I-). Como el taco de canasta, eres accesible y resolutivo. No te complicas con teorías abstractas cuando hay problemas prácticos que resolver. Eres la persona que mantiene los pies en la tierra y encuentra soluciones simples a desafíos complejos. Valoras la utilidad por encima de la apariencia.",
        "factores": ["B-", "Q4-", "I-", "F-"]
    },
    "Pescado": {
        "descripcion": "{nombre}, eres un Taco de **Pescado**: Fresco, ligero y con un toque diferente. Eres abierto (A+), flexible (Q3-) y despreocupado (F+). Como el taco de pescado, traes una perspectiva refrescante a cualquier situación. Eres adaptable y te mueves fácilmente entre diferentes ambientes sociales. Prefieres evitar conflictos (E-) y buscas armonía en tus relaciones. Tu actitud positiva (O-) hace que los demás disfruten de tu compañía.",
        "factores": ["A+", "Q3-", "F+", "E-"]
    },
    "Cochinita": {
        "descripcion": "{nombre}, eres un Taco de **Cochinita**: Sabroso, tradicional pero con un toque especial. Eres estable (C+), normativo (G+) pero con apertura a nuevas experiencias (Q1+). Como la cochinita, combines lo mejor de la tradición con innovación subtle. Eres confiable y consistente, pero sabes cuándo incorporar nuevas ideas. Mantienes equilibrio entre estabilidad emocional y apertura al cambio, siendo tanto ancla como vela en tus relaciones.",
        "factores": ["C+", "G+", "Q1+", "Q3+"]
    }
}

# Sistema de puntuación basado en 16PF
# Cada opción corresponde a una tendencia en los factores del 16PF
puntuaciones = {
    # Pregunta 1: Afectividad (A) | -: Reservado, +: Abierto
    0: ["Barbacoa", "Birria", "Al Pastor", "Pescado"],

    # Pregunta 2: Razonamiento (B) | -: Concreto, +: Abstracto
    1: ["Canasta", "Lengua", "Vegano", "Barbacoa"],

    # Pregunta 3: Estabilidad (C) | -: Reactivo, +: Estable
    2: ["Vegano", "Pescado", "Birria", "Suadero"],

    # Pregunta 4: Dominancia (E) | -: Sumiso, +: Dominante
    3: ["Carnitas", "Canasta", "Cochinita", "Pescado"],

    # Pregunta 5: Impulsividad (F) | -: Sereno, +: Entusiasta
    4: ["Suadero", "Barbacoa", "Birria", "Al Pastor"],

    # Pregunta 6: Conformidad (G) | -: Flexible, +: Normativo
    5: ["Vegano", "Pescado", "Carnitas", "Birria"],

    # Pregunta 7: Atrevimiento (H) | -: Tímido, +: Aventurero
    6: ["Canasta", "Birria", "Carnitas", "Lengua"],

    # Pregunta 8: Sensibilidad (I) | -: Duro, +: Sensible
    7: ["Canasta", "Lengua", "Vegano", "Pescado"],

    # Pregunta 9: Vigilancia (L) | -: Confiado, +: Suspicaz
    8: ["Birria", "Pescado", "Vegano", "Carnitas"],

    # Pregunta 10: Abrasión (M) | -: Práctico, +: Imaginativo
    9: ["Canasta", "Vegano", "Al Pastor", "Lengua"],

    # Pregunta 11: Privacidad (N) | -: Franco, +: Discreto
    10: ["Al Pastor", "Pescado", "Lengua", "Barbacoa"],

    # Pregunta 12: Apertura (Q1) | -: Tradicional, +: Abierto
    11: ["Barbacoa", "Al Pastor", "Birria", "Vegano"],

    # Pregunta 13: Autosuficiencia (Q2) | -: Grupal, +: Autónomo
    12: ["Carnitas", "Birria", "Lengua", "Pescado"],

    # Pregunta 14: Perfeccionismo (Q3) | -: Tolerante, +: Perfeccionista
    13: ["Pescado", "Barbacoa", "Carnitas", "Cochinita"],

    # Pregunta 15: Tensión (Q4) | -: Relajado, +: Tensión
    14: ["Canasta", "Birria", "Vegano", "Barbacoa"],

    # Pregunta 16: Optimismo (O) | -: Optimista, +: Aprensivo
    15: ["Cochinita", "Al Pastor", "Barbacoa", "Pescado"]
}


# Función para calcular el resultado
def calcular_resultado(respuestas):
    contador = {taco: 0 for taco in tipos_taco.keys()}
    for i, respuesta in enumerate(respuestas):
        taco_asociado = puntuaciones[i][respuesta]
        contador[taco_asociado] += 1
    return max(contador, key=contador.get)


# Mostrar la pregunta actual
def mostrar_pregunta(num_pregunta):
    st.progress(num_pregunta / len(preguntas))
    st.caption(f"Pregunta {num_pregunta + 1} de {len(preguntas)}")
    st.subheader(preguntas[num_pregunta]["pregunta"])
    st.caption(f"Dimensión psicológica: {preguntas[num_pregunta]['dimension']}")

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
            if st.button("Siguiente →" if num_pregunta < len(preguntas) - 1 else "🌮 Ver resultado"):
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
            st.button("Siguiente →" if num_pregunta < len(preguntas) - 1 else "🌮 Ver resultado", disabled=True)


# Mostrar resultados
def mostrar_resultado():
    resultado = calcular_resultado(st.session_state.respuestas)
    st.balloons()
    st.title(f"¡{st.session_state.nombre}, eres {resultado}!")
    st.markdown(tipos_taco[resultado]["descripcion"].format(nombre=st.session_state.nombre))

    # Mostrar emoji del taco
    emojis_tacos = {
        "Al Pastor": "🌮",
        "Suadero": "🌮",
        "Barbacoa": "🌮",
        "Carnitas": "🌮",
        "Lengua": "🌮",
        "Birria": "🌮",
        "Vegano": "🌮",
        "Canasta": "🌮",
        "Pescado": "🌮",
        "Cochinita": "🌮"
    }

    st.markdown(f"<div class='taco-image' style='font-size: 5em;'>{emojis_tacos[resultado]}</div>",
                unsafe_allow_html=True)

    st.subheader("Cómo se comparan tus resultados:")
    datos = {taco: 0 for taco in tipos_taco.keys()}
    for i, respuesta in enumerate(st.session_state.respuestas):
        taco_asociado = puntuaciones[i][respuesta]
        datos[taco_asociado] += 1

    # Crear gráfica de resultados
    df = pd.DataFrame.from_dict(datos, orient='index', columns=['Puntuación'])
    df = df.sort_values('Puntuación', ascending=False)
    st.bar_chart(df, color="#e65100")

    # Explicación de factores
    with st.expander("📊 Ver explicación de mi perfil psicológico"):
        st.markdown(f"**Factores primarios del 16PF en tu personalidad:**")
        factores = tipos_taco[resultado]["factores"]
        for factor in factores:
            nombre_factor = ""
            if factor[0] == "A":
                nombre_factor = "Afectividad"
            elif factor[0] == "B":
                nombre_factor = "Razonamiento"
            elif factor[0] == "C":
                nombre_factor = "Estabilidad"
            elif factor[0] == "E":
                nombre_factor = "Dominancia"
            elif factor[0] == "F":
                nombre_factor = "Impulsividad"
            elif factor[0] == "G":
                nombre_factor = "Conformidad"
            elif factor[0] == "H":
                nombre_factor = "Atrevimiento"
            elif factor[0] == "I":
                nombre_factor = "Sensibilidad"
            elif factor[0] == "L":
                nombre_factor = "Vigilancia"
            elif factor[0] == "M":
                nombre_factor = "Abrasión"
            elif factor[0] == "N":
                nombre_factor = "Privacidad"
            elif factor[0] == "O":
                nombre_factor = "Optimismo"
            elif factor[0] == "Q1":
                nombre_factor = "Apertura"
            elif factor[0] == "Q2":
                nombre_factor = "Autosuficiencia"
            elif factor[0] == "Q3":
                nombre_factor = "Perfeccionismo"
            elif factor[0] == "Q4":
                nombre_factor = "Tensión"

            polaridad = "Alto" if factor[1] == "+" else "Bajo"
            st.markdown(f"- **{factor}**: {nombre_factor} ({polaridad})")

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
st.caption("¡Preparado con ❤️ por tu taquería psicológica! Basado en el 16PF de Cattell")