class User:
    """
    Modelo que representa um usuário da aplicação.
    """
    def __init__(self, user_id, username, email, password, created_at=None, updated_at=None, deleted_at=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"