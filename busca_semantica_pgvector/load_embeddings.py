import os
import glob
import re
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import psycopg
from psycopg.rows import dict_row
from pgvector.psycopg import register_vector

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do Banco de Dados
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Diretório dos artigos
ARTICLES_DIR = "articles"

# 1. Inicialização
print("1. Inicializando modelo de embeddings...")
try:
    
    # Carrega o modelo de embeddings
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
       
except Exception as e:
    print(f"Erro na inicialização: {e}")
    exit(1)

# 2. Função de Pré-processamento
def preprocess_text(text):
    """
    converte para minúsculas e remove espaços extras
    """
    # Converte para minúsculas
    return text.lower().strip()

# 3. Conexão com o Banco de Dados
def get_db_connection():
    conn_string = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} port={DB_PORT}"
    print(f"Conectando ao banco de dados em {DB_HOST}:{DB_PORT}...")
    conn = psycopg.connect(conn_string, row_factory=dict_row)
    # Registra o adaptador para o tipo VECTOR do pgvector
    register_vector(conn)
    return conn

# 4. Processamento e Carregamento
def load_data():
    try:
        with get_db_connection() as conn:
            # Limpa a tabela antes de carregar novos dados
            with conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE articles RESTART IDENTITY;")
                print("Tabela 'articles' limpa.")

            article_files = glob.glob(os.path.join(ARTICLES_DIR, "*.txt"))
            if not article_files:
                print(f"Nenhum arquivo .txt encontrado no diretório '{ARTICLES_DIR}'.")
                return

            print(f"Encontrados {len(article_files)} arquivos para processar.")

            for filepath in article_files:
                filename = os.path.basename(filepath)
                print(f"Processando arquivo: {filename}")

                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Pré-processamento para gerar o embedding
                processed_content = preprocess_text(content)
                
                # Geração do embedding
                embedding = model.encode(processed_content).tolist()

                # Inserção no banco de dados
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO articles (filename, content, embedding) VALUES (%s, %s, %s)",
                        (filename, content, embedding)
                    )
                print(f"Embedding de '{filename}' carregado com sucesso.")

            conn.commit()
            print("Todos os embeddings foram carregados e a transação foi confirmada.")

    except psycopg.OperationalError as e:
        print(f"\nERRO DE CONEXÃO COM O BANCO DE DADOS: {e}")
        print("Certifique-se de que o contêiner do PostgreSQL está rodando e acessível.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")

if __name__ == "__main__":
    load_data()