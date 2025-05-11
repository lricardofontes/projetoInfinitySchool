from backend.models.user import User
from backend.repository.user_repository import UserRepository
from backend.utils.security import hash_password, verify_password

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, username: str, email: str, password: str) -> int:
        # checa duplicidade
        if self.repo.get_by_username(username):
            raise ValueError("Username já existe")
        salt, pwd_hash = hash_password(password)
        # armazena salt+hash juntos (ex: salt+hash em hex) ou em colunas separadas
        stored = salt.hex() + pwd_hash.hex()
        u = User(username=username, email=email, password_hash=stored)
        return self.repo.create(u)

    def get_user(self, user_id: int) -> User | None:
        return self.repo.get_by_id(user_id)

    def authenticate(self, username: str, password: str) -> bool:
        u = self.repo.get_by_username(username)
        if not u:
            return False
        # separa salt e hash
        salt = bytes.fromhex(u.password_hash[:32])
        stored_hash = bytes.fromhex(u.password_hash[32:])
        return verify_password(password, salt, stored_hash)

    def update_user(self, user_id: int, **fields) -> bool:
        u = self.repo.get_by_id(user_id)
        if not u:
            return False
        for k, v in fields.items():
            if hasattr(u, k) and v is not None:
                setattr(u, k, v)
        return self.repo.update(u)

    def delete_user(self, user_id: int) -> bool:
        return self.repo.soft_delete(user_id)
