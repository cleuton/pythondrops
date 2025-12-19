

# Semantic Search com PostgreSQL e pgvector

Este projeto implementa um sistema de **Busca Semântica** utilizando embeddings vetoriais. Ele permite que você pesquise em uma base de documentos não apenas por palavras-chave exatas, mas pelo **significado contextual** dos termos.

## 1. O que são Vector Databases?

Diferente dos bancos de dados relacionais tradicionais que buscam correspondências exatas de texto, um **Vector Database** armazena dados como vetores matemáticos (listas de números).

Esses vetores representam a "posição" de um conceito em um espaço multidimensional. Conceitos similares ficam fisicamente próximos uns dos outros, permitindo que o sistema encontre resultados relevantes mesmo que as palavras usadas na busca sejam diferentes das palavras no documento (ex: buscar por "database" e encontrar "banco de dados").

---

## 2. Função do Projeto

O sistema automatiza o pipeline de:

1. **Ingestão:** Lê arquivos de texto locais (`.txt`).
2. **Embedding:** Converte o conteúdo textual em vetores numéricos de alta densidade.
3. **Armazenamento:** Salva o conteúdo original e seu vetor correspondente em um banco de dados PostgreSQL.
4. **Recuperação (Search):** Realiza buscas de proximidade vetorial para retornar os documentos mais relevantes para uma consulta.

---

## 3. Tecnologias e Bibliotecas

### Para Embedding (Geração de Vetores)

* **Sentence-Transformers (`all-MiniLM-L6-v2` / `paraphrase-multilingual`):** Biblioteca baseada em PyTorch que fornece modelos pré-treinados para transformar frases em vetores.
* **Numpy/Python:** Para manipulação das listas numéricas resultantes.

### Para a Busca e Armazenamento

* **PostgreSQL com pgvector:** O motor do banco de dados. A extensão `pgvector` permite armazenar o tipo de dado `VECTOR` e realizar cálculos de distância (Cosseno, Euclidiana) diretamente via SQL.
* **Psycopg (v3):** Adaptador de banco de dados para Python, utilizado para comunicação eficiente e segura com o Postgres.
* **pgvector-python:** Integração que permite ao Psycopg reconhecer e converter vetores nativamente entre Python e SQL.

---

## 4. Como Subir o PostgreSQL

O projeto utiliza **Docker Compose** para garantir que o ambiente do banco de dados esteja configurado corretamente com a extensão necessária.

1. Certifique-se de ter o Docker instalado.
2. No terminal, na raiz do projeto, execute:
```bash
docker-compose up -d

```


*Isso iniciará um contêiner com o PostgreSQL 16 e a extensão pgvector já habilitada.*

### Função de cada arquivo:

* **`docker-compose.yaml`**: Orquestra a criação do contêiner, define portas, volumes de dados e variáveis de ambiente do banco.
* **`init.sql`**: Script executado automaticamente no primeiro boot do banco para criar a extensão `vector` e a tabela `articles`.
* **`.env`**: Centraliza as credenciais de acesso e a configuração do modelo de linguagem.
* **`requirements.txt`**: Lista as dependências Python necessárias.

---

## 5. Como Executar

### Passo 1: Instalação

Instale as dependências:

```bash
pip install -r requirements.txt

```

### Passo 2: Carga de Dados

Coloque seus arquivos de texto na pasta `articles/` e execute o script de ingestão:

```bash
python loader.py

```

*(Substitua `loader.py` pelo nome do arquivo que contém a função `load_data`)*.

### Passo 3: Executar Buscas

Para realizar uma busca semântica, execute o script de busca:

```bash
python search.py

```

Ao ser solicitado, digite o seu termo de pesquisa. O sistema processará o embedding da sua pergunta e consultará o PostgreSQL usando a **Distância de Cosseno** para encontrar os 2 resultados mais próximos.

Exemplo de busca e resultados:

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

**Dica de Precisão:** Este projeto está configurado para usar o modelo `paraphrase-multilingual-MiniLM-L12-v2`, o que garante que buscas em Inglês encontrem resultados em Português e vice-versa.
