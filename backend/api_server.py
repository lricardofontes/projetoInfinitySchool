import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from backend.services.user_service import UserService
# Você pode adicionar ProdutoService, PedidoService, etc.

user_service = UserService()

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Para permitir CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Trata requisições GET"""
        parts = self.path.split("/")
        if self.path.startswith("/users"):
            if len(parts) == 3 and parts[2].isdigit():
                # GET /users/<id>
                user_id = int(parts[2])
                user = user_service.get_user(user_id)
                if user:
                    response = {
                        "user_id": user.user_id,
                        "username": user.username,
                        "email": user.email,
                        "created_at": str(user.created_at),
                        "updated_at": str(user.updated_at)
                    }
                    self._send_response(response, 200)
                else:
                    self._send_response({"message": "Usuário não encontrado"}, 404)
            else:
                # GET /users (rota futura para listar todos os usuários)
                self._send_response({"message": "Listar todos os usuários ainda não implementado"}, 501)
        else:
            self._send_response({"message": "Endpoint não encontrado"}, 404)

    def do_POST(self):
        """Trata requisições POST"""
        if self.path == "/users":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data = json.loads(body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            user_id = user_service.create_user(username, email, password)
            if user_id:
                self._send_response({"user_id": user_id}, 201)
            else:
                self._send_response({"message": "Erro ao criar usuário"}, 400)
        else:
            self._send_response({"message": "Endpoint não encontrado"}, 404)

    def do_PUT(self):
        """Trata requisições PUT"""
        parts = self.path.split("/")
        if len(parts) == 3 and parts[1] == "users" and parts[2].isdigit():
            user_id = int(parts[2])
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode()
            data = json.loads(body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            if user_service.update_user(user_id, username, email, password):
                self._send_response({"message": "Usuário atualizado com sucesso"}, 200)
            else:
                self._send_response({"message": "Erro ao atualizar usuário"}, 400)
        else:
            self._send_response({"message": "Endpoint não encontrado"}, 404)

    def do_DELETE(self):
        """Trata requisições DELETE"""
        parts = self.path.split("/")
        if len(parts) == 3 and parts[1] == "users" and parts[2].isdigit():
            user_id = int(parts[2])
            if user_service.delete_user(user_id):
                self._send_response({"message": "Usuário deletado com sucesso"}, 200)
            else:
                self._send_response({"message": "Erro ao deletar usuário"}, 400)
        else:
            self._send_response({"message": "Endpoint não encontrado"}, 404)

    def _send_response(self, data, status=200):
        """Função para enviar respostas JSON"""
        response = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Permite CORS
        self.end_headers()
        self.wfile.write(response)

# Inicializa o servidor
def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Servidor rodando em http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()