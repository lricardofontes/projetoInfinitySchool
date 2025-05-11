const API_URL = "http://localhost:8000";

async function createUser() {
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("create-user-message");

    try {
        const response = await fetch(`${API_URL}/users`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            message.textContent = `Usuário criado com ID: ${data.id}`;
        } else {
            const error = await response.json();
            message.textContent = `Erro: ${error.error}`;
        }
    } catch (error) {
        message.textContent = `Erro ao criar usuário: ${error}`;
    }
}

async function loginUser() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    const message = document.getElementById("login-message");

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            message.textContent = "Login bem-sucedido!";
            // Aqui você pode guardar o token de autenticação (se usar)
        } else {
            const error = await response.json();
            message.textContent = `Erro no login: ${error.error}`;
        }
    } catch (error) {
        message.textContent = `Erro ao logar: ${error}`;
    }
}

async function createResource() {
  const name = document.getElementById("res-name").value;
  const type = document.getElementById("res-type").value;
  const description = document.getElementById("res-desc").value;
  const message = document.getElementById("create-res-message");

  const resp = await fetch(`${API_URL}/resources`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({name, type, description, details:{}})
  });
  if (resp.ok) {
    const data = await resp.json();
    message.textContent = `Criado Recurso ID ${data.id}`;
    listResources();
  } else {
    const err = await resp.json();
    message.textContent = `Erro: ${err.error}`;
  }
}

async function listResources() {
  const ul = document.getElementById("resources");
  ul.innerHTML = "";
  const resp = await fetch(`${API_URL}/resources`);
  const lst = await resp.json();
  lst.forEach(r => {
    const li = document.createElement("li");
    li.textContent = `${r.id} – ${r.name} (${r.type})`;
    ul.appendChild(li);
  });
}

// chame ao carregar a página
window.onload = () => {
  listResources();
};
