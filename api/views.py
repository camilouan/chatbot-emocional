# api/views.py

import os
import random
import time
import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import UsuarioPerfil
from .serializers import UsuarioPerfilSerializer

# HuggingFace
from huggingface_hub import InferenceClient


# ============================================================
# CONFIGURACIÓN DE HUGGING FACE
# ============================================================

HF_TOKEN = os.getenv("HF_TOKEN", "")
hf_client = None
if HF_TOKEN:
    try:
        hf_client = InferenceClient(api_key=HF_TOKEN)
        print("🔵 HuggingFace listo")
    except Exception as e:
        print("❌ ERROR inicializando HuggingFace:", e)
else:
    print("⚠️ HF_TOKEN no configurado. Usando respuestas por reglas.")

def generar_respuesta_IA(texto, usuario=None):
    """
    Paso 1: pedir al modelo que ANALICE el mensaje y devuelva JSON con:
      { "intent": "...", "confidence": 0.9, "need_clarification": true/false, "clarifying_question": "..." , "summary": "..." }
    Paso 2: si necesita aclaración -> devolver la pregunta de aclaración.
    Paso 3: si no -> generar respuesta terapéutica en español, usando contexto del usuario.
    Se añade una pequeña pausa (time.sleep) para simular "pensamiento".
    """
    if hf_client is None:
        return None

    # pausa corta para simular análisis (ajusta si quieres)
    time.sleep(0.8)

    contexto_usuario = ""
    if usuario:
        contexto_usuario = (
            f"Nombre: {usuario.nombre}\n"
            f"Edad: {usuario.edad}\n"
            f"Profesión: {usuario.profesion}\n"
            f"Gustan: {usuario.cosas_que_le_gustan}\n"
            f"Afectan: {usuario.cosas_que_le_afectan}\n"
            f"Hobbies: {usuario.hobbies}\n"
            f"Deportes: {usuario.deportes}\n"
            f"Música: {usuario.musica}\n"
        )

    # 1) pedir ANALISIS estructurado
    analyze_prompt = (
        "Eres un analizador de mensajes. Devuelve SOLO JSON válido con claves:\n"
        "intent (string), confidence (0.0-1.0), need_clarification (true/false), clarifying_question (string), summary (string).\n"
        "Analiza el siguiente mensaje (idioma original). No añadas texto fuera del JSON.\n\n"
        f"Mensaje: \"{texto}\"\n"
    )

    try:
        resp_an = hf_client.chat_completion(
            model="google/gemma-2-2b-it",
            messages=[{"role":"user","content":analyze_prompt}],
            max_tokens=200,
            temperature=0.0
        )
        an_text = resp_an.choices[0].message.content.strip()
        print("DEBUG - análisis crudo:", repr(an_text))

        # Intentar extraer JSON entre la primera '{' y la última '}' si existe
        analysis = {"intent":"unknown", "confidence":0.0, "need_clarification":False, "clarifying_question":"", "summary":""}
        start = an_text.find("{")
        end = an_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_str = an_text[start:end+1]
            try:
                analysis = json.loads(json_str)
            except Exception as parse_err:
                print("DEBUG - no se pudo parsear JSON extraído:", parse_err)
        else:
            # intentar parsear todo el texto como JSON (último recurso)
            try:
                analysis = json.loads(an_text)
            except Exception as parse_err2:
                print("DEBUG - no hay JSON en la respuesta de análisis:", parse_err2)

    except Exception as e:
        print("❌ Error al analizar mensaje (petición):", e)
        analysis = {"intent":"unknown", "confidence":0.0, "need_clarification":False, "clarifying_question":"", "summary":""}

    # Si requiere aclaración, devolver la pregunta al usuario
    if analysis.get("need_clarification"):
        question = analysis.get("clarifying_question") or "¿Podrías darme más detalles sobre eso?"
        return question

    # 2) generar respuesta terapéutica en ESPAÑOL usando el resumen y contexto
    prompt_resp = (
        "Eres un terapeuta empático y profesional. RESPONDE SIEMPRE EN ESPAÑOL.\n"
        "Usa el resumen del análisis y el contexto del usuario para personalizar tu respuesta.\n"
        "Sé empático, breve (máx 120 palabras), práctico y ofrece un consejo o pregunta que promueva la reflexión.\n\n"
        f"Contexto del usuario:\n{contexto_usuario}\n\n"
        f"Resumen del análisis: {analysis.get('summary','')}\n\n"
        f"Mensaje original: \"{texto}\"\n\n"
        "Respuesta:"
    )

    try:
        resp_final = hf_client.chat_completion(
            model="google/gemma-2-2b-it",
            messages=[{"role":"user","content":prompt_resp}],
            max_tokens=220,
            temperature=0.7
        )
        salida = resp_final.choices[0].message.content.strip()
        return salida
    except Exception as e:
        print("❌ Error generando respuesta IA:", e)
        return None

# ============================================================
# FRONTEND
# ============================================================

def auth_page(request):
    return render(request, "frontend/auth.html")


def chat_page(request):
    return render(request, "frontend/chat.html")


def index(request):
    return render(request, "frontend/auth.html")


# ============================================================
# DETECCIÓN DE EMOCIONES
# ============================================================

EMOCIONES_NEGATIVAS = ["tristeza", "enojo", "ansiedad", "miedo", "estres", "soledad"]


def detectar_emocion(texto):
    """Detecta emoción por palabras clave."""
    texto = texto.lower()

    reglas = {
        "tristeza": ["triste", "deprimido", "solo", "sin ganas", "vacío"],
        "enojo": ["molesto", "rabia", "enojado", "furioso"],
        "ansiedad": ["ansioso", "nervioso", "estresado", "preocupado"],
        "miedo": ["miedo", "temor", "asustado"],
        "alegria": ["feliz", "contento", "bien", "motivado"],
    }

    for emocion, palabras in reglas.items():
        if any(p in texto for p in palabras):
            return emocion

    return "neutra"


def detectar_riesgo_suicida(texto):
    """Detecta riesgo de suicidio."""
    texto = texto.lower()
    palabras = [
        "matarme", "suicidio", "terminar con todo",
        "quitarme la vida", "auto lesion",
        "cortarme", "lastimarme", "no quiero seguir",
        "desaparecer", "no valgo nada"
    ]
    return any(p in texto for p in palabras)


# ============================================================
# RESPUESTAS
# ============================================================

def generar_respuesta_reglas(texto, emocion, usuario):
    """Genera respuesta por reglas (fallback)."""
    if emocion in EMOCIONES_NEGATIVAS:
        sugerencias = [
            "meditar 10 minutos",
            "salir a caminar",
            "hablar con alguien de confianza",
            "hacer ejercicio",
            "escribir tus sentimientos"
        ]
        nombre = usuario.nombre if usuario else "Hey"
        return (
            f"Hola {nombre}, siento que estés pasando por esto 😔. "
            f"Quizá podría ayudarte {random.choice(sugerencias)}. "
            f"Estoy aquí para escucharte."
        )

    return (
        "Me alegra que compartas cómo te sientes 😊. "
        "Recuerda cuidar tu bienestar. Estoy aquí para ti."
    )


def generar_respuesta_crisis(usuario):
    """Genera respuesta en crisis."""
    nombre = usuario.nombre if usuario else "Hey"
    return (
        f"{nombre}, tu vida vale muchísimo 💛. No estás solo.\n\n"
        "📞 Línea 106 Bogotá – Crisis emocional (24h)\n"
        "🏥 Urgencias psicológicas en hospital cercano\n\n"
        "Hablar de esto muestra valentía. Estoy contigo."
    )


# ============================================================
# CHATBOT
# ============================================================

@api_view(["POST"])
def registrar_usuario(request):
    """Registra un nuevo usuario y devuelve su ID."""
    nombre = request.data.get("nombre", "").strip()
    email = request.data.get("email", "").strip()
    password = request.data.get("password", "").strip()

    if not nombre or not email or not password:
        return Response({"error": "Faltan datos requeridos"}, status=400)

    # Verificar si el email ya existe
    if UsuarioPerfil.objects.filter(email=email).exists():
        return Response({"error": "El correo ya está registrado"}, status=400)

    try:
        usuario = UsuarioPerfil.objects.create(
            nombre=nombre,
            email=email,
            password=password,  # En producción, hashear con make_password()
            edad=request.data.get("edad"),
            profesion=request.data.get("profesion", ""),
            cosas_que_le_gustan=request.data.get("cosas_que_le_gustan", ""),
            cosas_que_le_afectan=request.data.get("cosas_que_le_afectan", ""),
            hobbies=request.data.get("hobbies", ""),
            deportes=request.data.get("deportes", ""),
            musica=request.data.get("musica", ""),
        )
        return Response({
            "usuario_id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email
        }, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(["POST"])
def login_usuario(request):
    """Login de usuario — verifica email y contraseña."""
    email = request.data.get("email", "").strip()
    password = request.data.get("password", "").strip()

    if not email or not password:
        return Response({"error": "Faltan email o contraseña"}, status=400)

    try:
        usuario = UsuarioPerfil.objects.get(email=email)
        
        # Verificar contraseña (simple — en producción usar check_password())
        if usuario.password != password:
            return Response({"error": "Contraseña incorrecta"}, status=401)

        return Response({
            "usuario_id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email
        }, status=200)
    except UsuarioPerfil.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=404)


@api_view(["GET"])
def obtener_usuario(request, usuario_id):
    """Obtiene datos de un usuario por ID."""
    try:
        usuario = UsuarioPerfil.objects.get(id=usuario_id)
        serializer = UsuarioPerfilSerializer(usuario)
        return Response(serializer.data)
    except UsuarioPerfil.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=404)


@api_view(["POST"])
def chatbot(request):
    """Endpoint principal del chatbot."""
    texto = request.data.get("texto", "").strip()
    usuario_id = request.data.get("usuario_id")

    if not texto:
        return Response({"error": "Texto vacío"}, status=400)

    print(f"\n🟢 MENSAJE: {texto}")

    # Obtener usuario
    usuario = None
    if usuario_id:
        try:
            usuario = UsuarioPerfil.objects.get(id=usuario_id)
            print(f"👤 Usuario: {usuario.nombre}")
        except UsuarioPerfil.DoesNotExist:
            pass

    # Detectar riesgo
    if detectar_riesgo_suicida(texto):
        respuesta = generar_respuesta_crisis(usuario)
        return Response({
            "respuesta": respuesta,
            "emocion": "crisis",
            "riesgo": True
        })

    # Detectar emoción
    emocion = detectar_emocion(texto)

    # Intentar IA primero (con contexto del usuario), si no funciona usar reglas
    respuesta = generar_respuesta_IA(texto, usuario) if hf_client else None

    if not respuesta:
        respuesta = generar_respuesta_reglas(texto, emocion, usuario)
        print("⚠️ Usando respuesta por reglas")

    return Response({
        "respuesta": respuesta,
        "emocion": emocion,
        "riesgo": False
    })