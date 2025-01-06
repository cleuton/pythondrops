# tests/test_services.py

import unittest
from unittest.mock import patch, MagicMock
from services import pessoa_service
from db.models import Pessoa

class TestPessoaService(unittest.TestCase):

    @patch('services.pessoa_service.dao')
    def test_criar_pessoa(self, mock_dao):
        # Configura o mock
        mock_dao.inserir_pessoa.return_value = Pessoa(id=1, nome='Fulano')

        pessoa = pessoa_service.criar_pessoa('Fulano')
        self.assertEqual(pessoa.id, 1)
        self.assertEqual(pessoa.nome, 'Fulano')

    @patch('services.pessoa_service.dao')
    def test_obter_pessoa_nao_encontrada(self, mock_dao):
        mock_dao.buscar_pessoa_por_id.return_value = None

        pessoa = pessoa_service.obter_pessoa(999)
        self.assertIsNone(pessoa)

if __name__ == '__main__':
    unittest.main()
