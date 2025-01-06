# tests/test_integration.py

import unittest
from db.connection_pool import DatabasePool
from services import pessoa_service

class TestPessoaServiceIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Inicializa o pool de conexões
        DatabasePool.initialize(minconn=1, maxconn=5)

    def test_criar_e_obter_pessoa(self):
        nova_pessoa = pessoa_service.criar_pessoa('Teste Integracao')
        self.assertIsNotNone(nova_pessoa.id)

        pessoa_db = pessoa_service.obter_pessoa(nova_pessoa.id)
        self.assertIsNotNone(pessoa_db)
        self.assertEqual(pessoa_db.nome, 'Teste Integracao')

    @classmethod
    def tearDownClass(cls):
        # Fechar pool de conexões ao final (se desejado)
        DatabasePool.close_all()

if __name__ == '__main__':
    unittest.main()
