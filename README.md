# 🤖 Chatbot Emocional – Acompañamiento con Inteligencia Artificial

Este proyecto es una aplicación web desarrollada con **Django** y **IA emocional**, diseñada para ofrecer acompañamiento digital mediante un **chat empático** que analiza los sentimientos de los usuarios y responde de forma comprensiva.  

> 💬 “No es solo código, es empatía digital.”

---

## 🧠 Descripción General

El **Chatbot Emocional** permite que los usuarios se registren, inicien sesión y conversen con una inteligencia artificial capaz de **detectar emociones en el texto** (como alegría, tristeza, enojo, calma o ansiedad).  
El sistema fue creado con un enfoque ético y educativo, promoviendo el uso responsable de la tecnología para el bienestar emocional.

⚠️ **Aviso importante:**  
Este sistema **no reemplaza la atención psicológica profesional**. Está orientado a brindar acompañamiento básico y educativo.

---

## 🚀 Características principales

- Análisis de emociones a partir de texto.
- Generación de respuestas empáticas basadas en el contexto.
- Sistema de registro e inicio de sesión con restricción de edad (18+).
- Almacenamiento de usuarios y conversaciones.
- Diseño moderno y minimalista con colores cálidos.
- Despliegue en la nube con **Render**.

---

## 🧩 Arquitectura del Proyecto

Frontend (HTML, CSS, JavaScript)
↓
Backend (Django + Django REST Framework)
↓
IA emocional (emotion_ai.py)
↓
Base de datos (SQLite / MySQL)
El flujo general es:  
Usuario → Interfaz Web → API REST → Análisis de emociones → Respuesta empática.

---

## ⚙️ Tecnologías Utilizadas

- 🐍 **Python 3.13**
- 🌐 **Django 5.2.8**
- ⚙️ **Django REST Framework**
- 💾 **SQLite / MySQL**
- ☁️ **Render** (para despliegue en la nube)
- 🧠 **Hugging Face** (detección emocional)
- 🧰 Librerías:  
  - `python-dotenv`  
  - `django-cors-headers`  
  - `whitenoise`  
  - `gunicorn`  
  - `mysqlclient` / `pymysql`  
  - `requests`, `httpx`, `tqdm`, `typer-slim`

---

## 🛠️ Instalación Local

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tuusuario/chatbot_emociones.git
   cd chatbot_emociones
Crea un entorno virtual

python -m venv venv
source venv/Scripts/activate   # En Windows


Instala las dependencias

pip install -r requirements.txt


Crea el archivo .env

SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_HOSTS=*


Aplica las migraciones

python manage.py migrate


Ejecuta el servidor

python manage.py runserver


Abre la app

http://127.0.0.1:8000

☁️ Despliegue en Render

El proyecto está configurado con:

requirements.txt → dependencias.

runtime.txt → versión de Python.

Procfile → ejecución con gunicorn.

Render instalará automáticamente las dependencias y ejecutará el proyecto con:

gunicorn detector.wsgi

🧠 Inteligencia Artificial

El archivo emotion_ai.py contiene la lógica de análisis de emociones.
Detecta emociones como:

😊 Alegría

😢 Tristeza

😠 Enojo

😰 Ansiedad

😌 Calma

Ejemplo:

analyze_emotion("Hoy me siento muy triste")
# → 'tristeza'


El sistema devuelve una respuesta empática según la emoción detectada.

🧱 Estructura del Proyecto
chatbot_emociones/
│
├── detector/                 # App principal Django
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── emotion_ai.py
│   ├── urls.py
│   ├── tests.py
│
├── templates/
│   ├── auth.html
│   ├── chat.html
│   ├── index.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── auth.css
│   │   ├── chat.css
│   ├── js/
│       ├── script.js
│       ├── auth.js
│       ├── chat.js
│       ├── registro.js
│
├── db.sqlite3
├── manage.py
├── requirements.txt
├── runtime.txt
├── Procfile
└── README.md

⚖️ Aspectos Éticos

El sistema incluye:

Aviso de responsabilidad legal y línea de ayuda (106 y 123 en Colombia).

Restricción de edad (solo mayores de 18 años).

Claridad sobre que no sustituye atención psicológica profesional.

📚 Créditos

Autor: Camilo Andrés Parra Cuenca y Nicolas Camilo Moreno
Universidad: Universidad Antonio Nariño (UAN)
Programa: Tecnólogo en Construcción de Software

Desarrollado como proyecto académico con fines de aprendizaje y responsabilidad social.

📜 Licencia

Este proyecto se distribuye bajo la licencia MIT.
Puedes modificarlo y usarlo libremente, siempre que mantengas los créditos originales.

💚 Gracias por visitar este proyecto.

La empatía también puede programarse.
