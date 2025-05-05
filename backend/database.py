import psycopg2
from psycopg2 import pool

# Configurações do Banco de Dados
DB_CONFIG = {
    'dbname': 'industrias_wayne',  # Nome do banco criado
    'user': 'app_user',  # Nome do usuário
    'password': 'root',  # Substitua por sua senha
    'host': 'localhost',  # Host do banco
    'port': 5432  # Porta padrão do PostgreSQL
}

# Inicialização do pool de conexões
try:
    # Criando um pool de conexões para gerenciar as conexões com o banco
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1,  # Número mínimo de conexões abertas
        10,  # Número máximo de conexões abertas
        **DB_CONFIG  # Passando as configurações
    )

    if connection_pool:
        print("Conexão com o banco de dados estabelecida com sucesso!")
except Exception as error:
    print(f"Erro ao conectar ao banco de dados: {error}")


# Função para obter uma conexão
def get_connection():
    try:
        conn = connection_pool.getconn()
        if conn:
            print("Conexão obtida do pool.")
        return conn
    except Exception as e:
        print(f"Erro ao obter conexão: {e}")


# Função para liberar conexão de volta ao pool
def release_connection(conn):
    try:
        connection_pool.putconn(conn)
        print("Conexão devolvida ao pool.")
    except Exception as e:
        print(f"Erro ao liberar conexão: {e}")


# Função para fechar todas as conexões (utilizado ao encerrar o aplicativo)
def close_all_connections():
    try:
        connection_pool.closeall()
        print("Todas as conexões foram encerradas.")
    except Exception as e:
        print(f"Erro ao encerrar conexões: {e}")