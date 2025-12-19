-- Habilita a extensão pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Cria a tabela para armazenar os embeddings
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(384) -- O modelo 'all-MiniLM-L6-v2' gera embeddings de 384 dimensões
);
