from backend.services.user_service import UserService
from backend.models.user import User
import uuid

# Instâncias globais para os testes
service = UserService()




def test_create_user():
    # Gera um username único usando parte de um UUID
    username = f"usuario_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"
    password = "senha123"

    user_id = service.create_user(username, email, password)
    assert isinstance(user_id, int)
    assert user_id > 0


def test_get_user():
    """
    Testa a busca de um usuário recém-criado pelo ID.
    """
    print("\n=== Teste: get_user ===")
    user_id = 5  # Insira aqui um ID válido já existente no banco.

    user = service.get_user(user_id)

    if user:
        print(f"Usuário encontrado: {user.username} | Email: {user.email}")
    else:
        print(f"Usuário com ID {user_id} não encontrado ou deletado.")


def test_update_user():
    """
    Testa a atualização do nome ou email de um usuário ativo.
    """
    print("\n=== Teste: update_user ===")
    user_id = 5  # Insira aqui um ID válido já existente no banco.
    new_username = "usuario_atualizado"
    new_email = "email_atualizado@example.com"

    result = service.update_user(user_id, username=new_username, email=new_email)
    if result:
        print(f"Usuário {user_id} atualizado com sucesso!")
    else:
        print(f"Falha ao atualizar o usuário com ID {user_id}.")


def test_delete_user():
    """
    Testa a deleção lógica de um usuário pelo ID.
    """
    print("\n=== Teste: delete_user ===")
    user_id = 5  # Insira aqui um ID válido já existente no banco.

    result = service.delete_user(user_id)
    if result:
        print(f"Usuário {user_id} deletado com sucesso!")
    else:
        print(f"Falha ao deletar o usuário com ID {user_id}.")

def teardown_function(func):
    # apaga qualquer usuário com username 'usuario_teste' antes de cada teste
    u = service.repo.get_by_username("usuario_teste")
    if u:
        service.delete_user(u.id)


# --------- EXECUTAR TESTES --------- #
if __name__ == "__main__":
    print("\nIniciando os testes do UserService...\n")
    test_create_user()
    test_get_user()
    test_update_user()
    test_delete_user()
    print("\nTestes concluídos.")