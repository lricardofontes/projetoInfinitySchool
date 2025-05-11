import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """
    Retorna uma conexão psycopg2 usando variáveis de ambiente:
    PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
    """
    conn = psycopg2.connect(
        host     = os.getenv('PGHOST',    'localhost'),
        port     = os.getenv('PGPORT',    5432),
        user     = os.getenv('PGUSER',    'app_user'),
        password = os.getenv('PGPASSWORD','root'),
        database = os.getenv('PGDATABASE','industrias_wayne')
    )
    return conn

def get_dict_cursor(conn):
    """
    Cursor que retorna dicionários em vez de tuplas.
    """
    return conn.cursor(cursor_factory=RealDictCursor)
