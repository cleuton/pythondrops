# services/pessoa_service.py

from db.models import Pessoa, Dependente
from db import dao
from logger_config import logger
from mensagens import mensagens

def criar_pessoa(nome: str) -> Pessoa:
    nova_pessoa = Pessoa(nome=nome)
    return dao.inserir_pessoa(nova_pessoa)

def obter_pessoa(id_pessoa: int) -> Pessoa:
    return dao.buscar_pessoa_por_id(id_pessoa)

def obter_pessoas() -> list[Pessoa]:
    return dao.buscar_pessoas() 

def atualizar_nome_pessoa(id_pessoa: int, novo_nome: str) -> None:
    pessoa = obter_pessoa(id_pessoa)
    if not pessoa:
        logger.error(f"{mensagens.pessoa_nao_encontrada}: {id_pessoa}")
        raise ValueError(f"{mensagens.pessoa_nao_encontrada}: {id_pessoa}")
    pessoa.nome = novo_nome
    dao.atualizar_pessoa(pessoa)

def remover_pessoa(id_pessoa: int) -> None:
    dao.deletar_pessoa(id_pessoa)

def criar_dependente(id_pessoa: int, nome: str, nascimento, parentesco: str) -> Dependente:
    # Verifica se a pessoa existe
    pessoa = obter_pessoa(id_pessoa)
    if not pessoa:
        raise ValueError(f"{mensagens.pessoa_nao_encontrada}: {id_pessoa}")
    novo_dependente = Dependente(
        nome=nome,
        nascimento=nascimento,
        parentesco=parentesco,
        id_pessoa=pessoa.id
    )
    return dao.inserir_dependente(novo_dependente)

def listar_pessoa_e_dependentes(id_pessoa: int) -> Pessoa:
    """
    Retorna a pessoa e seus dependentes (objeto Pessoa com lista de Dependente).
    """
    pessoa = obter_pessoa(id_pessoa)
    dao.recuperar_dependentes(pessoa)
    return pessoa

# Você pode criar outros serviços para atualizar/remover dependentes etc.
