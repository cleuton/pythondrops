# db/dao.py

from .connection_pool import DatabasePool
from .models import Pessoa, Dependente
from logger_config import logger
from mensagens import mensagens
from .queries_script import queries
import toml
import os

def buscar_pessoas() -> list[Pessoa]:
    conn = DatabasePool.get_connection()
    pessoas = []
    try:
        with conn.cursor() as cur:
            cur.execute(queries.select_pessoas)
            rows = cur.fetchall()
            for r in rows:
                pessoa = Pessoa(id=r[0], nome=r[1])
                pessoas.append(pessoa)
        return pessoas
    except Exception as e:
        logger.error(f"{mensagens.erro_buscar_pessoas}{e}")
        raise
    finally:
        DatabasePool.release_connection(conn)

def inserir_pessoa(pessoa: Pessoa) -> Pessoa:
    conn = DatabasePool.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                queries.insert_pessoa,
                (pessoa.nome,)
            )
            generated_id = cur.fetchone()[0]
            pessoa.id = generated_id
            conn.commit()
            logger.info(f"Pessoa inserida com ID: {pessoa.id}")
        return pessoa
    except Exception as e:
        logger.error(f"{mensagens.erro_inserir_pessoa}{e}")
        raise
    finally:
        DatabasePool.release_connection(conn)

def atualizar_pessoa(pessoa: Pessoa) -> None:
    if not pessoa:
        logger.error(mensagens.pessoa_sem_id)    
        raise ValueError(mensagens.pessoa_sem_id)
    conn = DatabasePool.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                queries.update_pessoa,
                (pessoa.nome, pessoa.id)
            )
            conn.commit()
    except Exception as e:
        logger.error(f"{mensagens.erro_atualizar_pessoa}{e}")
        raise
    finally:
        DatabasePool.release_connection(conn)

def deletar_pessoa(id_pessoa: int) -> None:
    conn = DatabasePool.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(queries.delete_pessoa, (id_pessoa,))
            conn.commit()
    except Exception as e:
        logger.error(f"{mensagens.erro_deletar_pessoa}{e}")
        raise
    finally:
        DatabasePool.release_connection(conn)

def buscar_pessoa_por_id(id_pessoa: int) -> Pessoa:
    conn = DatabasePool.get_connection()
    pessoa = None
    try:
        with conn.cursor() as cur:
            cur.execute(queries.select_pessoa, (id_pessoa,))
            row = cur.fetchone()
            if row:
                pessoa = Pessoa(id=row[0], nome=row[1])
            
        return pessoa
    except Exception as e:
        logger.error(f"{mensagens.erro_buscar_pessoa}{e}")
        raise   
    finally:
        DatabasePool.release_connection(conn)

# Atenção: Método que altera o parâmetro passado!
def recuperar_dependentes(pessoa: Pessoa) -> None:
    if not pessoa: 
        logger.error(mensagens.pessoa_nao_informada)
        raise ValueError(mensagens.pessoa_nao_informada)
    conn = DatabasePool.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(queries.select_pessoa_dependentes, (pessoa.id,))
            rows_dep = cur.fetchall()
            for d in rows_dep:
                dep = Dependente(
                    id=d[0],
                    nome=d[1],
                    nascimento=d[2],
                    parentesco=d[3],
                    id_pessoa=d[4]
                )
                pessoa.dependentes.append(dep)
    except Exception as e:
        logger.error(f"{mensagens.erro_recuperar_dependentes}{e}")
        raise   
    finally:
        DatabasePool.release_connection(conn)

# Métodos para Dependente

def inserir_dependente(dependente: Dependente) -> Dependente:
    conn = DatabasePool.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                queries.insert_dependente,
                (dependente.nome, dependente.nascimento, dependente.parentesco, dependente.id_pessoa)
            )
            generated_id = cur.fetchone()[0]
            dependente.id = generated_id
            conn.commit()
        return dependente
    except Exception as e:
        logger.error(f"{mensagens.erro_inserir_dependente}{e}")
        raise   
    finally:
        DatabasePool.release_connection(conn)

def atualizar_dependente(dependente: Dependente) -> None:
    if not dependente.id:
        logger.error(mensagens.dependente_sem_id)
        raise ValueError(mensagens.dependente_sem_id)
    conn = DatabasePool.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                queries.update_dependente,
                (dependente.nome, dependente.nascimento, dependente.parentesco, dependente.id)
            )
            conn.commit()
    except Exception as e:
        logger.error(f"{mensagens.erro_atualizar_dependente}{e}")
        raise   
    finally:
        DatabasePool.release_connection(conn)

def deletar_dependente(id_dependente: int) -> None:
    conn = DatabasePool.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(queries.delete_dependente, (id_dependente,))
            conn.commit()
    except Exception as e:
        logger.error(f"{mensagens.erro_deletar_dependente}{e}")
        raise
    finally:
        DatabasePool.release_connection(conn)

def buscar_dependente_por_id(id_dependente: int) -> Dependente:
    conn = DatabasePool.get_connection()
    dep = None
    try:
        with conn.cursor() as cur:
            cur.execute(
                queries.select_dependente_por_id, 
                (id_dependente,)
            )
            row = cur.fetchone()
            if row:
                dep = Dependente(
                    id=row[0],
                    nome=row[1],
                    nascimento=row[2],
                    parentesco=row[3],
                    id_pessoa=row[4]
                )
        return dep
    except Exception as e:  
        logger.error(f"{mensagens.erro_buscar_dependente}{e}")
        raise   
    finally:
        DatabasePool.release_connection(conn)
