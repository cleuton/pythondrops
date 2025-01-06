class Queries:
    def __init__(self):
        self.select_pessoas = "SELECT id, nome FROM pessoa"
        self.insert_pessoa = "INSERT INTO pessoa (nome) VALUES (%s) RETURNING id"
        self.update_pessoa = "UPDATE pessoa SET nome = %s WHERE id = %s"
        self.delete_pessoa = "DELETE FROM pessoa WHERE id = %s"
        self.select_pessoa = "SELECT id, nome FROM pessoa WHERE id = %s"
        self.select_pessoa_dependentes = """
                        SELECT id, nome, nascimento, parentesco, id_pessoa 
                        FROM dependente 
                        WHERE id_pessoa = %s
                        """
        self.insert_dependente = """
                        INSERT INTO dependente (nome, nascimento, parentesco, id_pessoa) 
                        VALUES (%s, %s, %s, %s) RETURNING id
                        """
        self.update_dependente = """
                        UPDATE dependente
                        SET nome = %s, nascimento = %s, parentesco = %s
                        WHERE id = %s
                        """
        self.delete_dependente = "DELETE FROM dependente WHERE id = %s"
        self.select_dependente_por_id = """
                        SELECT id, nome, nascimento, parentesco, id_pessoa 
                        FROM dependente 
                        WHERE id = %s
                        """
queries = Queries()
