console.log("chat.js cargado");

const usuarioId = localStorage.getItem("usuario_id");
const estado = document.getElementById("estado-usuario");
const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const btnSend = document.getElementById("send-btn");
const btnLogout = document.getElementById("btn-logout");

// Si no hay usuario, manda al login
if (!usuarioId) {
    console.log("No hay usuario en localStorage, redirigiendo a /");
    window.location.href = "/";
} else {
    console.log("Usuario actual:", usuarioId);
}

estado.textContent = "Usando usuario ID: " + usuarioId;

// ===== CERRAR SESIÓN =====
btnLogout.addEventListener("click", () => {
    console.log("Click en Cerrar sesión");
    localStorage.clear();
    console.log("localStorage después de clear():", localStorage);
    window.location.href = "/";
});

// ===== CHAT =====
btnSend.addEventListener("click", enviarMensaje);

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        enviarMensaje();
    }
});

async function enviarMensaje() {
    const texto = input.value.trim();
    if (!texto) return;

    agregarMensaje("usuario", texto);
    input.value = "";

    try {
        const res = await fetch("/api/chatbot/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto, usuario_id: usuarioId }),
        });

        if (!res.ok) {
            agregarMensaje("bot", "❌ Error: " + res.status);
            return;
        }

        const json = await res.json();
        const respuesta = json.respuesta || "Sin respuesta";
        const emocion = json.emocion || "";
        agregarMensaje("bot", respuesta, emocion);
    } catch (err) {
        agregarMensaje("bot", "Hubo un problema al conectar con el servidor.");
    }
}

function agregarMensaje(tipo, texto, meta = "") {
    // tipo: "usuario" | "bot"
    const cont = document.createElement("div");
    cont.className = `mensaje ${tipo}`;

    const burbuja = document.createElement("div");
    burbuja.className = "bubble";
    burbuja.textContent = texto;

    cont.appendChild(burbuja);

    if (meta) {
        const m = document.createElement("div");
        m.className = "meta";
        m.textContent = meta;
        cont.appendChild(m);
    }

    chatBox.appendChild(cont);
    chatBox.scrollTop = chatBox.scrollHeight;
}
