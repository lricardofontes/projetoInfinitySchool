from backend.database import get_connection, release_connection, close_all_connections

def test_database():
    # Obtém uma conexão
    conn = get_connection()
    if conn:
        print("Conexão bem-sucedida!")
        # Libera a conexão
        release_connection(conn)
    else:
        print("Falha ao conectar ao banco!")

if __name__ == "__main__":
    test_database()
    close_all_connections()