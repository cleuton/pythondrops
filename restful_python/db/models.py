# db/models.py

class Pessoa:
    def __init__(self, id=None, nome=None):
        self.id = id
        self.nome = nome
        self.dependentes = []  # lista de Dependentes

class Dependente:
    def __init__(self, id=None, nome=None, nascimento=None, parentesco=None, id_pessoa=None):
        self.id = id
        self.nome = nome
        self.nascimento = nascimento
        self.parentesco = parentesco
        self.id_pessoa = id_pessoa
