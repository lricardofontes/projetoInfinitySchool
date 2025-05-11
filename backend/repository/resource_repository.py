from backend.database import get_db_connection, get_dict_cursor
from backend.models.resource import Resource
from psycopg2.extras import Json

class ResourceRepository:
    def __init__(self):
        self.conn = None

    def _connect(self):
        if not self.conn or self.conn.closed:
            self.conn = get_db_connection()

    def create(self, res: Resource) -> int:
        self._connect()
        cur = get_dict_cursor(self.conn)
        sql = """
            INSERT INTO wayne_db.resources
                (name, description, type, details)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """
        cur.execute(sql, (
            res.name,
            res.description,
            res.type,
            Json(res.details)    # <<< wrap dict em Json()
        ))
        new_id = cur.fetchone()['id']
        self.conn.commit()
        cur.close()
        return new_id

    def update(self, res: Resource) -> bool:
        self._connect()
        cur = get_dict_cursor(self.conn)
        sql = """
            UPDATE wayne_db.resources
            SET name=%s, description=%s, type=%s, details=%s,
                updated_at=CURRENT_TIMESTAMP
            WHERE id=%s
        """
        cur.execute(sql, (
            res.name,
            res.description,
            res.type,
            Json(res.details),   # <<< também aqui
            res.id
        ))
        ok = cur.rowcount > 0
        self.conn.commit()
        cur.close()
        return ok

    def list_all(self) -> list[Resource]:
        self._connect()
        cur = get_dict_cursor(self.conn)
        cur.execute("SELECT * FROM wayne_db.resources")
        rows = cur.fetchall()
        cur.close()
        return [Resource(**r) for r in rows]

    def get_by_id(self, res_id: int) -> Resource | None:
        self._connect()
        cur = get_dict_cursor(self.conn)
        cur.execute("SELECT * FROM wayne_db.resources WHERE id = %s", (res_id,))
        row = cur.fetchone()
        cur.close()
        return Resource(**row) if row else None

    def delete(self, res_id: int) -> bool:
        self._connect()
        cur = get_dict_cursor(self.conn)
        cur.execute("DELETE FROM wayne_db.resources WHERE id = %s", (res_id,))
        ok = cur.rowcount > 0
        self.conn.commit()
        cur.close()
        return ok
