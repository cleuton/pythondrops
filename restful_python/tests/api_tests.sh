#!bash
# Selecionar pessoa
curl -X GET http://localhost:8000/pessoas/1

# Selecionar todas as pessoas
curl -X GET http://localhost:8000/pessoas

# Inserir pessoa
curl -X POST -H "Content-type: application/json" http://localhost:8000/pessoas -d '{"nome": "Fulano da Silva"}'

# Buscar pessoa inserida
curl -X GET http://localhost:8000/pessoas/3

# Atualizar pessoa
curl -X PUT -H "Content-type: application/json" http://localhost:8000/pessoas/3 -d '{"nome": "Fulano da Silva de Tal"}'

# Ver se atualizou
curl -X GET http://localhost:8000/pessoas/3

# Adicionar dependente
curl -X POST -H "Content-type: application/json" http://localhost:8000/pessoas/3/dependentes \
-d '{"nome": "Ciclano da Silva", "parentesco": "Filho", "nascimento": "2000-01-01"}'

# Verificar se adicionou
curl -X GET http://localhost:8000/pessoas/3/dependentes

# Remover pessoa
curl -X DELETE http://localhost:8000/pessoas/3

# Verificar se removeu  
curl -X GET http://localhost:8000/pessoas/3