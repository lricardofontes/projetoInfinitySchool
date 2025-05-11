from backend.database import get_db_connection, get_dict_cursor
from backend.models.user import User
from psycopg2 import sql
from datetime import datetime

class UserRepository:
    def __init__(self):
        self.conn = None

    def _connect(self):
        if not self.conn or self.conn.closed:
            self.conn = get_db_connection()

    def create(self, user: User) -> int:
        """
        Insere um novo usuário e retorna seu ID.
        """
        self._connect()
        cur = get_dict_cursor(self.conn)
        query = """
            INSERT INTO wayne_db.users (username, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        cur.execute(query, (user.username, user.email, user.password_hash))
        new_id = cur.fetchone()['id']
        self.conn.commit()
        cur.close()
        return new_id

    def get_by_id(self, user_id: int) -> User | None:
        self._connect()
        cur = get_dict_cursor(self.conn)
        query = """
            SELECT * FROM wayne_db.users
            WHERE id = %s AND deleted_at IS NULL;
        """
        cur.execute(query, (user_id,))
        row = cur.fetchone()
        cur.close()
        if not row:
            return None
        return User(**row)

    def get_by_username(self, username: str) -> User | None:
        self._connect()
        cur = get_dict_cursor(self.conn)
        cur.execute("""
            SELECT * FROM wayne_db.users
            WHERE username = %s AND deleted_at IS NULL
        """, (username,))
        row = cur.fetchone()
        cur.close()
        return User(**row) if row else None

    def update(self, user: User) -> bool:
        self._connect()
        cur = get_dict_cursor(self.conn)
        query = """
            UPDATE wayne_db.users
            SET username=%s, email=%s, password_hash=%s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id=%s AND deleted_at IS NULL
        """
        cur.execute(query, (user.username, user.email,
                            user.password_hash, user.id))
        updated = cur.rowcount > 0
        self.conn.commit()
        cur.close()
        return updated

    def soft_delete(self, user_id: int) -> bool:
        self._connect()
        cur = get_dict_cursor(self.conn)
        cur.execute("""
            UPDATE wayne_db.users
            SET deleted_at = CURRENT_TIMESTAMP
            WHERE id = %s AND deleted_at IS NULL
        """, (user_id,))
        deleted = cur.rowcount > 0
        self.conn.commit()
        cur.close()
        return deleted
