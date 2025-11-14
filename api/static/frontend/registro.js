let usuarioId = localStorage.getItem("usuario_id") || null;

if (usuarioId) {
    document.getElementById("estado-usuario").innerText =
        "Ya tienes registrado el usuario ID: " + usuarioId;
}

document.getElementById("btn-registrar").addEventListener("click", async () => {
    const data = {
        nombre: document.getElementById("nombre").value,
        edad: document.getElementById("edad").value || null,
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

    if (!res.ok || !json.usuario_id) {
        console.error(json);
        alert("Error al registrar usuario.");
        return;
    }

    usuarioId = json.usuario_id;
    localStorage.setItem("usuario_id", usuarioId);

    document.getElementById("estado-usuario").innerText =
        "Usuario registrado con ID: " + usuarioId;

    alert("Usuario registrado correctamente. Ahora puedes ir al chat.");
});
