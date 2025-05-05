from backend.repository.user_repository import UserRepository
from backend.models.user import User
from datetime import datetime
import hashlib

class UserService:
    """
    Camada de serviço para operações de usuário. Aplica validações e lógicas de negócio antes de delegar ao repositório.
    """

    def __init__(self):
        self.repository = UserRepository()

    def _hash_password(self, password):
        """
        Gera um hash SHA-256 da senha fornecida.

        Parâmetros:
            password (str): Senha em texto puro.

        Retorna:
            str: Hash da senha.
        """
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def create_user(self, username, email, password):
        """
        Cria um novo usuário após validações e criptografia da senha.

        Parâmetros:
            username (str): Nome do usuário.
            email (str): E-mail do usuário.
            password (str): Senha em texto puro.

        Retorna:
            int: ID do usuário criado.
        """
        # TODO: Checar existência (não permitir nome/email duplicado, pode-se criar métodos no repositório para isso).
        password_hash = self._hash_password(password)
        return self.repository.create_user(username, email, password_hash)

    def get_user(self, user_id):
        """
        Busca um usuário ativo pelo ID.

        Parâmetros:
            user_id (int): ID do usuário.

        Retorna:
            User: Instância de User ou None.
        """
        return self.repository.get_user_by_id(user_id)

    def update_user(self, user_id, username=None, email=None, password=None):
        """
        Atualiza dados do usuário após as devidas validações.

        Parâmetros:
            user_id (int): ID do usuário.
            username (str, opcional)
            email (str, opcional)
            password (str, opcional, texto puro)

        Retorna:
            bool: True se a atualização for bem-sucedida.
        """
        password_hash = None
        if password:
            password_hash = self._hash_password(password)
        return self.repository.update_user(user_id, username, email, password_hash)

    def delete_user(self, user_id):
        """
        Realiza deleção lógica do usuário (soft delete).

        Parâmetros:
            user_id (int): ID do usuário.

        Retorna:
            bool: True se sucesso.
        """
        return self.repository.delete_user(user_id)