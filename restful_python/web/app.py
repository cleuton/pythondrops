# web/app.py

from flask import Flask, request, jsonify
from services import pessoa_service
from db.connection_pool import DatabasePool
from mensagens import mensagens

def create_app():
    app = Flask(__name__)

    # Inicializa o pool de conexões ao iniciar a aplicação
    DatabasePool.initialize(minconn=1, maxconn=5)

    @app.route('/pessoas', methods=['GET'])
    def obter_todas_pessoas():
        try:
            pessoas = pessoa_service.obter_pessoas()
            return jsonify([{'id': p.id, 'nome': p.nome} for p in pessoas]), 200
        except:
            return jsonify({'error': mensagens.erro_buscar_pessoas}), 500

    @app.route('/pessoas', methods=['POST'])
    def criar_pessoa():
        data = request.get_json()
        nome = data.get('nome')
        if not nome:
            return jsonify({'error': mensagens.nome_obrigatorio}), 400
        try:
            nova_pessoa = pessoa_service.criar_pessoa(nome)
            return jsonify({'id': nova_pessoa.id, 'nome': nova_pessoa.nome}), 201
        except:
            return jsonify({'error': mensagens.erro_criar_pessoa}), 500

    # Retorna apenas a pessoa, sem os dependentes
    @app.route('/pessoas/<int:id_pessoa>', methods=['GET'])
    def obter_pessoa(id_pessoa):
        try:
            pessoa = pessoa_service.obter_pessoa(id_pessoa)
            if not pessoa:
                return jsonify({'error': mensagens.pessoa_nao_encontrada}), 404
            return jsonify({
                'id': pessoa.id,
                'nome': pessoa.nome,
                'dependentes': [],
            }), 200
        except:
            return jsonify({'error': mensagens.erro_obter_pessoa}), 500
    
    @app.route('/pessoas/<int:id_pessoa>/dependentes', methods=['GET'])
    def obter_dependentes(id_pessoa):
        try:
            pessoa = pessoa_service.listar_pessoa_e_dependentes(id_pessoa)
            if not pessoa:
                return jsonify({'error': mensagens.pessoa_nao_encontrada}), 404
            return jsonify({
                'id': pessoa.id,
                'nome': pessoa.nome,
                'dependentes': [
                    {
                        'id': dep.id,
                        'nome': dep.nome,
                        'nascimento': str(dep.nascimento),
                        'parentesco': dep.parentesco,
                        'id_pessoa': dep.id_pessoa
                    }
                    for dep in pessoa.dependentes
                ]}), 200
        except:
            return jsonify({'error': mensagens.erro_obter_dependentes}), 500    

    @app.route('/pessoas/<int:id_pessoa>', methods=['PUT'])
    def atualizar_pessoa(id_pessoa):
        data = request.get_json()
        novo_nome = data.get('nome')
        try:
            pessoa_service.atualizar_nome_pessoa(id_pessoa, novo_nome)
            return jsonify({'message': mensagens.pessoa_atualizada_com_sucesso}), 200
        except ValueError as e:
            return jsonify({'erro': str(e)}), 404
        except:
            return jsonify({'error': mensagens.erro_atualizar_pessoa_log}), 500

    @app.route('/pessoas/<int:id_pessoa>', methods=['DELETE'])
    def deletar_pessoa(id_pessoa):
        try: 
            pessoa_service.remover_pessoa(id_pessoa)
            return jsonify({'message': mensagens.pessoa_removida_com_sucesso}), 200
        except:
            return jsonify({'error': mensagens.erro_remover_pessoa}), 500

    @app.route('/pessoas/<int:id_pessoa>/dependentes', methods=['POST'])
    def criar_dependente(id_pessoa):
        data = request.get_json()
        nome = data.get('nome')
        nascimento = data.get('nascimento')
        parentesco = data.get('parentesco')
        if not all([nome, nascimento, parentesco]):
            return jsonify({'error': mensagens.erro_faltam_campos}), 400
        try:
            novo_dep = pessoa_service.criar_dependente(
                id_pessoa=id_pessoa,
                nome=nome,
                nascimento=nascimento,  # Converter para date se necessário
                parentesco=parentesco
            )
            return jsonify({
                'id': novo_dep.id,
                'nome': novo_dep.nome,
                'nascimento': str(novo_dep.nascimento),
                'parentesco': novo_dep.parentesco,
                'id_pessoa': novo_dep.id_pessoa
            }), 201
        except:
            return jsonify({'error': mensagens.erro_criar_dependente}), 500

    return app
