# db/connection_pool.py

import psycopg2
from psycopg2 import pool
import os

# Exemplo de variáveis de ambiente
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')

class DatabasePool:
    __pool = None

    @staticmethod
    def initialize(minconn=1, maxconn=5):
        if DatabasePool.__pool is None:
            DatabasePool.__pool = psycopg2.pool.SimpleConnectionPool(
                minconn,
                maxconn,
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )

    @staticmethod
    def get_connection():
        if DatabasePool.__pool is None:
            raise Exception("Pool de conexões não foi inicializado.")
        return DatabasePool.__pool.getconn()

    @staticmethod
    def release_connection(conn):
        if DatabasePool.__pool is None:
            raise Exception("Pool de conexões não foi inicializado.")
        DatabasePool.__pool.putconn(conn)

    @staticmethod
    def close_all():
        if DatabasePool.__pool:
            DatabasePool.__pool.closeall()
            DatabasePool.__pool = None
