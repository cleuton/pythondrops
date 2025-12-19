# Semantic Search with PostgreSQL and pgvector

This project implements a **Semantic Search** system using vector embeddings. It allows you to search through a document database not just by exact keywords, but by the **contextual meaning** of the terms.

## 1. What are Vector Databases?

Unlike traditional relational databases that look for exact text matches, a **Vector Database** stores data as mathematical vectors (lists of numbers).

These vectors represent the "position" of a concept in a multi-dimensional space. Similar concepts are placed physically close to each other, allowing the system to find relevant results even if the words used in the search differ from those in the document (e.g., searching for "database" and finding "banco de dados").

---

## 2. Project Purpose

The system automates the following pipeline:

1. **Ingestion:** Reads local text files (`.txt`).
2. **Embedding:** Converts textual content into high-density numerical vectors.
3. **Storage:** Saves the original content and its corresponding vector in a PostgreSQL database.
4. **Retrieval (Search):** Performs vector proximity searches to return the most relevant documents for a query.

---

## 3. Technologies and Libraries

### For Embedding (Vector Generation)

* **Sentence-Transformers (`all-MiniLM-L6-v2` / `paraphrase-multilingual`):** A PyTorch-based library providing pre-trained models to transform sentences into vectors.
* **Numpy/Python:** For handling the resulting numerical lists.

### For Search and Storage

* **PostgreSQL with pgvector:** The database engine. The `pgvector` extension allows storing the `VECTOR` data type and performing distance calculations (Cosine, Euclidean) directly via SQL.
* **Psycopg (v3):** A Python database adapter used for efficient and secure communication with Postgres.
* **pgvector-python:** Integration that enables Psycopg to natively recognize and convert vectors between Python and SQL.

---

## 4. How to Set Up PostgreSQL

The project uses **Docker Compose** to ensure the database environment is correctly configured with the required extension.

1. Ensure you have Docker installed.
2. In the terminal, at the project root, run:

```bash
docker-compose up -d

```

*This will start a container with PostgreSQL 16 and the pgvector extension already enabled.*

### Function of each file:

* **`docker-compose.yaml`**: Orchestrates container creation, defines ports, data volumes, and database environment variables.
* **`init.sql`**: A script executed automatically during the database's first boot to create the `vector` extension and the `articles` table.
* **`.env`**: Centralizes access credentials and language model configurations.
* **`requirements.txt`**: Lists the necessary Python dependencies.

---

## 5. How to Run

### Step 1: Installation

Install the dependencies:

```bash
pip install -r requirements.txt

```

### Step 2: Data Loading

Place your text files in the `articles/` folder and run the ingestion script:

```bash
python loader.py

```

*(Replace `loader.py` with the name of the file containing the `load_data` function).*

### Step 3: Run Searches

To perform a semantic search, run the search script:

```bash
python search.py

```

When prompted, type your search term. The system will process the embedding of your query and consult PostgreSQL using **Cosine Distance** to find the 2 closest results.

Search example and results:

```bash
$ python search.py
1. Inicializando modelo de embeddings...
Digite o termo de busca: database

2. Processando a consulta: 'database'
3. Conectado ao banco de dados. Realizando busca por similaridade...
4. Busca concluída. Encontrados 2 resultados.

--- Resultados da Busca por Similaridade ---

1. Arquivo: article_2.txt
   Score de Similaridade: 0.5103
   Conteúdo (Trecho): O PostgreSQL é um sistema de gerenciamento de banco de dados objeto-relacional robusto e de código aberto. Com a extensão pgvector, ele se torna uma ferramenta poderosa para a busca por similaridade v...

2. Arquivo: article_1.txt
   Score de Similaridade: 0.2397
   Conteúdo (Trecho): A inteligência artificial (IA) está revolucionando a maneira como interagimos com a tecnologia. O aprendizado de máquina, um subcampo da IA, permite que sistemas melhorem seu desempenho em tarefas esp...
```

**Precision Tip:** This project is configured to use the `paraphrase-multilingual-MiniLM-L12-v2` model on the env file, which ensures that searches in English can find results in Portuguese and vice-versa.