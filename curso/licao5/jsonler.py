from datetime import datetime
import json
from json.decoder import JSONDecodeError
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
lista=[]
produtos={10:"Leite",15:"Iogurte",20:"Manteiga"}
formato="%d/%m/%Y %H:%M:%S"
try:
    with open('saida.json','r') as arq:
        lista=json.load(arq)
    for venda in lista:
        nome_produto=produtos[venda['mercadoria']]
        data=datetime.strptime(venda['data'],formato)
        sdata=data.strftime(locale.nl_langinfo(locale.D_T_FMT))
        quantidade=locale.format_string('%.2f',venda['quantidade'])
        print('Cliente: {}, Produto: {}, Data: {}, Quantidade: {}'.format(
            venda['cliente'],nome_produto,sdata,quantidade
        )
        )
except JSONDecodeError:
    print('O arquivo de movimento está inválido!')