console.log("auth.js cargado");

// Si ya hay usuario guardado, redirigir directamente al chat
const usuarioId = localStorage.getItem("usuario_id");
if (usuarioId) {
    console.log("Usuario ya logueado, redirigiendo a /chat/");
    window.location.href = "/chat/";
}

// ===== ELEMENTOS LOGIN =====
const loginEmail = document.getElementById("login-email");
const loginPass = document.getElementById("login-password");
const btnLogin = document.getElementById("btn-login");

// ===== ELEMENTOS REGISTER =====
const regNombre = document.getElementById("reg-nombre");
const regEmail = document.getElementById("reg-email");
const regEmailConfirm = document.getElementById("reg-email-confirm");
const regPass = document.getElementById("reg-password");
const regPassConfirm = document.getElementById("reg-password-confirm");
const regEdad = document.getElementById("reg-edad");
const regProfesion = document.getElementById("reg-profesion");
const regGustan = document.getElementById("reg-gustan");
const regAfectan = document.getElementById("reg-afectan");
const regHobbies = document.getElementById("reg-hobbies");
const regDeportes = document.getElementById("reg-deportes");
const regMusica = document.getElementById("reg-musica");
const regTerms = document.getElementById("reg-terms");
const btnRegister = document.getElementById("btn-register");
const ageError = document.getElementById("age-error");

// ===== VALIDAR EDAD EN TIEMPO REAL =====
regEdad.addEventListener("change", () => {
    const edad = parseInt(regEdad.value);
    if (edad < 18) {
        ageError.textContent = "❌ Debes ser mayor de 18 años para usar esta aplicación";
        ageError.style.color = "#ff4757";
        regEdad.style.borderBottomColor = "#ff4757";
        btnRegister.disabled = true;
    } else {
        ageError.textContent = "✅ Edad válida";
        ageError.style.color = "#2ed573";
        regEdad.style.borderBottomColor = "#2ed573";
        btnRegister.disabled = false;
    }
});

// ===== LOGIN =====
btnLogin.addEventListener("click", async () => {
    const email = loginEmail.value.trim();
    const password = loginPass.value.trim();

    if (!email || !password) {
        alert("Por favor completa todos los campos");
        return;
    }

    try {
        const res = await fetch("/api/login/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        const data = await res.json();

        if (!res.ok) {
            alert("❌ " + (data.error || "Error en login"));
            return;
        }

        console.log("✅ Login exitoso:", data);
        localStorage.setItem("usuario_id", data.usuario_id);
        window.location.href = "/chat/";
    } catch (err) {
        console.error("Error:", err);
        alert("Error de conexión");
    }
});

// ===== REGISTER =====
btnRegister.addEventListener("click", async () => {
    const nombre = regNombre.value.trim();
    const email = regEmail.value.trim();
    const emailConfirm = regEmailConfirm.value.trim();
    const password = regPass.value.trim();
    const passwordConfirm = regPassConfirm.value.trim();
    const edad = parseInt(regEdad.value);
    const profesion = regProfesion.value.trim();
    const gustan = regGustan.value.trim();
    const afectan = regAfectan.value.trim();
    const hobbies = regHobbies.value.trim();
    const deportes = regDeportes.value.trim();
    const musica = regMusica.value.trim();

    // Validaciones
    if (!nombre || !email || !password || !edad) {
        alert("Por favor completa los campos requeridos");
        return;
    }

    if (!regTerms.checked) {
        alert("Debes confirmar que eres mayor de 18 años y aceptas los términos de uso");
        return;
    }

    if (edad < 18) {
        alert("❌ Lo sentimos, esta aplicación está reservada para mayores de 18 años. Si eres menor, consulta con un adulto responsable o profesional de la salud mental.");
        return;
    }

    if (email !== emailConfirm) {
        alert("Los correos no coinciden");
        return;
    }

    if (password !== passwordConfirm) {
        alert("Las contraseñas no coinciden");
        return;
    }

    if (password.length < 6) {
        alert("La contraseña debe tener al menos 6 caracteres");
        return;
    }

    try {
        const res = await fetch("/api/registrar/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                nombre,
                email,
                password,
                edad,
                profesion,
                cosas_que_le_gustan: gustan,
                cosas_que_le_afectan: afectan,
                hobbies,
                deportes,
                musica,
            }),
        });

        const data = await res.json();

        if (!res.ok) {
            alert("❌ " + (data.error || "Error en registro"));
            return;
        }

        console.log("✅ Registro exitoso:", data);
        localStorage.setItem("usuario_id", data.usuario_id);
        alert("¡Bienvenido " + data.nombre + "! Entrando al chat...");
        window.location.href = "/chat/";
    } catch (err) {
        console.error("Error:", err);
        alert("Error de conexión");
    }
});