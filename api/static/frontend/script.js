let usuarioId = localStorage.getItem("usuario_id") || null;

// Mostrar estado del usuario
if (usuarioId) {
    document.getElementById("estado-usuario").innerText =
        "Usuario registrado con ID: " + usuarioId;
}

// ----- REGISTRO -----
document.getElementById("btn-registrar").addEventListener("click", async () => {
    const data = {
        nombre: document.getElementById("nombre").value,
        edad: document.getElementById("edad").value,
        profesion: document.getElementById("profesion").value,
        cosas_que_le_gustan: document.getElementById("cosas_que_le_gustan").value,
        cosas_que_le_afectan: document.getElementById("cosas_que_le_afectan").value,
        hobbies: document.getElementById("hobbies").value,
        deportes: document.getElementById("deportes").value,
        musica: document.getElementById("musica").value,
    };

    const res = await fetch("/api/registro-usuario/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    const json = await res.json();

    if (json.usuario_id) {
        usuarioId = json.usuario_id;
        localStorage.setItem("usuario_id", usuarioId);
        document.getElementById("estado-usuario").innerText =
            "Usuario registrado con ID: " + usuarioId;
        alert("Usuario registrado correctamente.");
    } else {
        alert("Error registrando usuario");
    }
});

// ----- CHAT -----
document.getElementById("send-btn").addEventListener("click", async () => {
    if (!usuarioId) {
        alert("Primero debes registrar un usuario.");
        return;
    }

    const userInput = document.getElementById("user-input");
    const texto = userInput.value;

    if (!texto.trim()) return;

    agregarMensaje("usuario", texto);
    userInput.value = "";

    const res = await fetch("/api/chatbot/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            texto: texto,
            usuario_id: usuarioId
        })
    });

    const json = await res.json();

    agregarMensaje("bot", json.response);
});

function agregarMensaje(tipo, texto) {
    const box = document.getElementById("chat-box");

    const div = document.createElement("div");
    div.classList.add("mensaje", tipo);

    div.innerHTML = `<strong>${tipo === "usuario" ? "Tú:" : "Bot:"}</strong> ${texto}`;

    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

async function enviarMensaje() {
    const input = document.getElementById("mensajeInput");
    const mensaje = input.value.trim();

    if (!mensaje) return;

    // Mostrar mensaje del usuario
    mostrarMensaje(mensaje, "usuario");
    input.value = "";

    try {
        const response = await fetch("/api/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": obtenerCSRFToken()
            },
            body: JSON.stringify({
                texto: mensaje,
                usuario_id: usuarioId || null
            })
        });

        if (!response.ok) {
            throw new Error(`Error HTTP ${response.status}`);
        }

        const datos = await response.json();

        console.log("✅ Respuesta del servidor:", datos);

        // Verificar que la respuesta tiene los campos esperados
        const respuesta = datos.respuesta || "Sin respuesta";
        const emocion = datos.emocion || "desconocida";
        const riesgo = datos.riesgo || false;

        // Mostrar respuesta del bot
        mostrarMensaje(`${respuesta} (Emoción: ${emocion})`, "bot");

        // Si hay riesgo, resaltar en rojo
        if (riesgo) {
            console.warn("⚠️ RIESGO DETECTADO");
        }

    } catch (error) {
        console.error("❌ Error:", error);
        mostrarMensaje("Error al conectar con el servidor", "bot");
    }
}

function mostrarMensaje(texto, remitente) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.className = `mensaje ${remitente}`;
    div.textContent = texto;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight; // Scroll automático
}

function obtenerCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || "";
}

// Para testing local (sin formulario CSRF)
let usuarioId = 1;
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("enviarBtn");
    const input = document.getElementById("mensajeInput");
    
    if (btn) btn.addEventListener("click", enviarMensaje);
    if (input) input.addEventListener("keypress", (e) => {
        if (e.key === "Enter") enviarMensaje();
    });
});
