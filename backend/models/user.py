from datetime import datetime
from typing import Optional

class User:
    """
    Modelo que representa um usuário da aplicação.
    """
    def __init__(
            self,
            id: Optional[int] = None,
            username: Optional[str] = None,
            email: Optional[str] = None,
            password_hash: Optional[str] = None,
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None,
            deleted_at: Optional[datetime] = None
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"