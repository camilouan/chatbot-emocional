import re

# -------------------------------
# Utilidades de texto
# -------------------------------

def _normalizar(texto: str) -> str:
    """Pasa a minúsculas, quita signos raros, deja solo letras/números/espacios."""
    t = texto.lower()
    t = re.sub(r"[^\w\sáéíóúñ]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


# -------------------------------
# Saludos
# -------------------------------

SALUDOS = [
    "hola",
    "buenas",
    "buenos dias",
    "buenas tardes",
    "buenas noches",
    "hey",
    "ey",
    "que mas",
    "qué más",
    "que tal",
    "qué tal",
]


def es_saludo(texto: str) -> bool:
    t = _normalizar(texto)
    if len(t.split()) <= 3:
        return any(frase in t for frase in SALUDOS)
    return False


# -------------------------------
# Mensajes de riesgo (suicidio / autolesión)
# -------------------------------

EXPRESIONES_RIESGO = [
    "quiero morirme",
    "quiero morir",
    "me quiero morir",
    "no quiero vivir",
    "no quiero seguir viviendo",
    "no vale la pena vivir",
    "la vida no tiene sentido",
    "me quiero matar",
    "pienso matarme",
    "pienso suicidarme",
    "quiero suicidarme",
    "me voy a matar",
    "no aguanto mas",
    "no aguanto más",
]


def es_mensaje_de_riesgo(texto: str) -> bool:
    t = _normalizar(texto)
    return any(frase in t for frase in EXPRESIONES_RIESGO)


# -------------------------------
# Detección muy simple de emoción
# (puedes mejorarla luego)
# -------------------------------

PALABRAS_POSITIVAS = [
    "bien",
    "feliz",
    "tranquilo",
    "contento",
    "contenta",
    "motivado",
    "motivada",
    "animado",
    "animada",
    "genial",
    "super",
]

PALABRAS_TRISTEZA = [
    "triste",
    "deprimido",
    "deprimida",
    "solo",
    "sola",
    "vacío",
    "vacio",
    "sin ganas",
    "llorando",
]

PALABRAS_ENOJO = [
    "bravo",
    "brava",
    "enojado",
    "enojada",
    "furioso",
    "furiosa",
    "rabia",
    "rabioso",
    "molesto",
    "molesta",
]

PALABRAS_ANSIEDAD = [
    "ansioso",
    "ansiosa",
    "estresado",
    "estresada",
    "estres",
    "estrés",
    "preocupado",
    "preocupada",
    "angustiado",
    "angustiada",
]


def detectar_emocion(texto: str) -> str:
    """
    Devuelve una etiqueta muy simple:
      - "positiva"
      - "tristeza"
      - "enojo"
      - "ansiedad"
      - "neutra"
    """
    t = _normalizar(texto)

    # primero chequeos por palabras clave
    if any(pal in t for pal in PALABRAS_TRISTEZA):
        return "tristeza"
    if any(pal in t for pal in PALABRAS_ENOJO):
        return "enojo"
    if any(pal in t for pal in PALABRAS_ANSIEDAD):
        return "ansiedad"
    if any(pal in t for pal in PALABRAS_POSITIVAS):
        return "positiva"

    return "neutra"


# -------------------------------
# Generación de respuesta
# -------------------------------

def _perfil_a_diccionario(perfil):
    """
    Acepta un modelo Django UsuarioPerfil o un dict ya preparado
    y devuelve un dict seguro.
    """
    if perfil is None:
        return {
            "gustos": "",
            "afectan": "",
            "hobbies": "",
            "deportes": "",
            "musica": "",
        }

    # Si ya es dict, lo rellenamos con claves por si faltan
    if isinstance(perfil, dict):
        return {
            "gustos": perfil.get("cosas_que_le_gustan", "") or perfil.get("gustos", ""),
            "afectan": perfil.get("cosas_que_le_afectan", "") or perfil.get("afectan", ""),
            "hobbies": perfil.get("hobbies", ""),
            "deportes": perfil.get("deportes", ""),
            "musica": perfil.get("musica", ""),
        }

    # Asumimos que es un modelo Django
    return {
        "gustos": getattr(perfil, "cosas_que_le_gustan", "") or "",
        "afectan": getattr(perfil, "cosas_que_le_afectan", "") or "",
        "hobbies": getattr(perfil, "hobbies", "") or "",
        "deportes": getattr(perfil, "deportes", "") or "",
        "musica": getattr(perfil, "musica", "") or "",
    }


def generar_respuesta_personalizada(texto_usuario: str, emocion: str, perfil=None) -> str:
    """
    Genera la respuesta final del bot:
    - Prioriza mensajes de riesgo (suicidio / autolesión)
    - Luego saludos
    - Luego emociones
    """
    # 0) Chequeo de riesgo alto
    if es_mensaje_de_riesgo(texto_usuario):
        return (
            "Lamento muchísimo que te sientas así 💔. Que tengas pensamientos de hacerte daño "
            "es una señal de que estás pasando por algo muy pesado, y nadie debería cargar con eso en soledad.\n\n"
            "👉 Lo más importante ahora es que NO estés solo con esto. Hablar con una persona real puede marcar la diferencia.\n\n"
            "Si estás en Bogotá, podrías comunicarte con:\n"
            "• Línea 106 (Línea de Orientación en Salud Mental – disponible 24/7)\n"
            "• Línea 123 opción 5 (atención en crisis emocional)\n\n"
            "También puedes acudir a un servicio de urgencias cercano y decir claramente que estás teniendo "
            "pensamientos de hacerte daño.\n\n"
            "Tu vida vale mucho más de lo que sientes ahora mismo 💛. No eres una carga, ni estás solo: "
            "pedir ayuda es un acto de valentía."
        )

    # 1) Saludo
    if es_saludo(texto_usuario):
        return (
            "👋 Hola, gracias por escribir. ¿Cómo te has sentido últimamente? "
            "Puedes contarme si te has sentido bien, triste, estresado, enojado… "
            "Estoy aquí para escucharte."
        )

    # 2) Procesar perfil
    p = _perfil_a_diccionario(perfil)
    gustos = p["gustos"]
    afectan = p["afectan"]
    hobbies = p["hobbies"]
    deportes = p["deportes"]
    musica = p["musica"]

    # 3) Respuestas según emoción
    if emocion == "positiva":
        return (
            "Me alegra mucho que te sientas bien 😊. Cuando uno está en un buen momento, "
            "es importante seguir cuidando esos hábitos que te hacen bien. "
            f"Por ejemplo, podrías seguir con tus hobbies ({hobbies or gustos or 'lo que disfrutas hacer'}), "
            f"mantenerte activo con deportes como {deportes or 'algún deporte que te guste'} "
            f"o disfrutar tu música favorita, como {musica or 'la música que más te gusta'}. "
            "Sigue cuidando de ti, eso hace mucha diferencia a largo plazo."
        )

    if emocion == "tristeza":
        return (
            "Siento que estés pasando por un momento de tristeza 🫂. Es válido sentirse así. "
            f"A veces ayuda retomar algo que te gusta, como {hobbies or gustos or 'alguna actividad que disfrutes'}, "
            f"escuchar {musica or 'música que te calme'} o hacer un poco de "
            f"{deportes or 'actividad física suave'}. "
            "Si quieres, cuéntame un poco más de qué te tiene así, y lo vamos conversando paso a paso."
        )

    if emocion == "enojo":
        return (
            "Parece que estás molesto 😠, y es totalmente válido sentir rabia a veces. "
            f"Cuando algo nos afecta (por ejemplo: {afectan or 'esas situaciones que te cargan'}), "
            "puede ayudar hacer una pausa, respirar profundo y soltar un poco la tensión. "
            f"También sirve desconectarse un rato con {hobbies or gustos or 'alguna actividad que disfrutes'} "
            "o mover el cuerpo (un paseo, algún deporte ligero). "
            "Si quieres, dime qué pasó y lo vamos desarmando juntos."
        )

    if emocion == "ansiedad":
        return (
            "Suena a que estás algo ansioso o estresado 😥. "
            "Intenta probar algo que te ayude a bajar revoluciones: respirar profundo, "
            f"salir a dar una vuelta, escuchar {musica or 'música tranquila'} "
            f"o dedicar unos minutos a {hobbies or gustos or 'alguna actividad que te guste y no sea muy exigente'}. "
            "Si quieres, cuéntame qué es lo que más te preocupa ahora mismo y lo miramos paso a paso."
        )

    # 4) Emoción neutra / no clara
    return (
        "No me queda del todo claro cómo te sientes todavía 🤔. "
        "Puedes decirme algo como: “me siento triste”, “estoy estresado”, “me siento bien” "
        "o “estoy muy enojado”, para poder darte recomendaciones más ajustadas a ti."
    )
