from datetime import datetime

from backend.database import get_connection, release_connection
from backend.models.user import User


class UserRepository:
    """
    Classe responsável por gerenciar operações de persistência relacionadas ao usuário no banco de dados.
    """

    # ... outros métodos

    def create_user(self, username, email, password):
        """
        Insere um novo usuário no banco de dados.

        Parâmetros:
            username (str): Nome do usuário.
            email (str): Email do usuário.
            password (str): Hash da senha do usuário.

        Retorna:
            int: O ID do usuário criado.
        """
        conn = get_connection()  # Obtem conexão do banco
        try:
            cursor = conn.cursor()
            # Insere dados no banco
            cursor.execute(
                "INSERT INTO wayne_db.users (username, email, password) VALUES (%s, %s, %s) RETURNING user_id",
                (username, email, password)
            )
            user_id = cursor.fetchone()[0]  # Recupera ID gerado
            conn.commit()
            return user_id
        except Exception as e:
            conn.rollback()
            print("Erro ao criar usuário:", e)
        finally:
            release_connection(conn)  # Libera conexão

    def update_user(self, user_id, username=None, email=None, password=None):
        """
        Atualiza informações do usuário no banco de dados e atualiza o campo updated_at.

        Parâmetros:
            user_id (int): ID do usuário a ser atualizado.
            username (str, opcional): Novo nome de usuário.
            email (str, opcional): Novo e-mail.
            password (str, opcional): Nova senha já criptografada.

        Retorna:
            bool: True se atualizado com sucesso, False caso contrário.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            updates = []
            params = []

            if username:
                updates.append("username = %s")
                params.append(username)
            if email:
                updates.append("email = %s")
                params.append(email)
            if password:
                updates.append("password = %s")
                params.append(password)
            # Sempre atualizar o updated_at
            updates.append("updated_at = %s")
            params.append(datetime.now())

            if not updates:
                return True  # Sem alterações a fazer

            params.append(user_id)
            query = "UPDATE wayne_db.users SET " + ", ".join(updates) + " WHERE user_id = %s AND deleted_at IS NULL"
            cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print("Erro ao atualizar usuário:", e)
            return False
        finally:
            if conn:
                release_connection(conn)

    def delete_user(self, user_id):
        """
        Inativa (deleta logicamente) um usuário preenchendo o campo deleted_at.

        Parâmetros:
            user_id (int): ID do usuário a ser removido.

        Retorna:
            bool: True se inativado com sucesso, False caso contrário.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            delete_time = datetime.now()
            cursor.execute(
                "UPDATE wayne_db.users SET deleted_at = %s, updated_at = %s WHERE user_id = %s AND deleted_at IS NULL",
                (delete_time, delete_time, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print("Erro ao inativar usuário:", e)
            return False
        finally:
            if conn:
                release_connection(conn)

    def get_user_by_id(self, user_id):
        """
        Busca um usuário ativo (não deletado logicamente) pelo seu ID.

        Parâmetros:
            user_id (int): O ID do usuário a ser buscado.

        Retorna:
            User: Um objeto User se encontrado, ou None caso contrário.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, username, email, password, created_at, updated_at, deleted_at "
                "FROM wayne_db.users WHERE user_id = %s AND deleted_at IS NULL",
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                user = User(
                    user_id=row[0],
                    username=row[1],
                    email=row[2],
                    password=row[3],
                    created_at=row[4],
                    updated_at=row[5],
                    deleted_at=row[6],
                )
                return user
            return None
        except Exception as e:
            print("Erro ao buscar usuário:", e)
        finally:
            if conn:
                release_connection(conn)