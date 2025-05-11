from datetime import datetime
from typing import Optional

class Resource:
    """
    Modelo que representa equipamentos.
    """
    def __init__(
            self,
            id: Optional[int] = None,
            name: Optional[str] = None,
            description: Optional[str] = None,
            type: Optional[str] = None,
            details: Optional[str] = None,
            created_at: Optional[datetime] = None,
            updated_at: Optional[datetime] = None,
            deleted_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.details = details
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"