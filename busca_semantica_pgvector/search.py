import os
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

# 1. Inicialização
print("1. Inicializando modelo de embeddings...")
try:

    # Carrega o modelo de embeddings
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    
except Exception as e:
    print(f"Erro na inicialização: {e}")
    exit(1)

# 2. Função de Pré-processamento (a mesma usada para carregar)
def preprocess_text(text):
    """
    Converte para minúsculas e remove espaços.
    """
    # Converte para minúsculas
    return text.lower().strip()

# 3. Conexão com o Banco de Dados
def get_db_connection():
    conn_string = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} port={DB_PORT}"
    conn = psycopg.connect(conn_string, row_factory=dict_row)
    # Registra o adaptador para o tipo VECTOR do pgvector
    register_vector(conn)
    return conn

# 4. Função de Busca
def search_similarity(query, k=3):
    print(f"\n2. Processando a consulta: '{query}'")
    
    # Pré-processa a consulta
    processed_query = preprocess_text(query)
    
    # Gera o embedding da consulta
    query_embedding = model.encode(processed_query).tolist()
    
    try:
        with get_db_connection() as conn:
            print("3. Conectado ao banco de dados. Realizando busca por similaridade...")
            
            # Realiza a busca por similaridade de cosseno (o operador '<=>' é para distância de cosseno no pgvector)
            # A distância de cosseno é 1 - similaridade de cosseno.
            # Para obter a maior similaridade, ordenamos pela menor distância.
            sql = """
            SELECT 
                filename, 
                content, 
                1 - (embedding <=> %s::vector) AS similarity_score
            FROM 
                articles
            ORDER BY 
                embedding <=> %s::vector
            LIMIT %s;
            """
            
            with conn.cursor() as cur:
                cur.execute(sql, (query_embedding, query_embedding, k))
                results = cur.fetchall()
                
            print(f"4. Busca concluída. Encontrados {len(results)} resultados.")
            return results

    except psycopg.OperationalError as e:
        print(f"\nERRO DE CONEXÃO COM O BANCO DE DADOS: {e}")
        print("Certifique-se de que o contêiner do PostgreSQL está rodando e acessível.")
        return []
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
        return []

# 5. Execução
if __name__ == "__main__":
    search_term = input("Digite o termo de busca: ")
    
    if not search_term:
        print("Termo de busca não pode ser vazio.")
    else:
        results = search_similarity(search_term, k=2)
        
        if results:
            print("\n--- Resultados da Busca por Similaridade ---")
            for i, result in enumerate(results):
                print(f"\n{i+1}. Arquivo: {result['filename']}")
                print(f"   Score de Similaridade: {result['similarity_score']:.4f}")
                print(f"   Conteúdo (Trecho): {result['content'][:200]}...")
            print("--------------------------------------------")
        else:
            print("Nenhum resultado encontrado ou erro na busca.")
