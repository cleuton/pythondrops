![](../python-drops.png)
# pythondrops
## Python drops & technology

(c) 2018 [**Cleuton Sampaio**](https://github.com/cleuton).

# PythonDrops 5: Servindo MongoDB

Uma das necessidades que sempre aparecem é a de servir recursos oriundos de Bancos de dados. Em REST, o cliente não deve se preocupar de onde vieram e como são armazenados os recursos, e o Servidor deve ser transparente quanto a isso. 

Já vimos como criar [**Clientes e Servidores HTTP**](../clientes_servidores) em python, agora, vamos criar uma app servidora simples, porém completa. 

## O caso de estudo 

Imagine uma rede de sensores que enviam medidas de temperatura através de um “broker. Um componente precisa registrar as temperaturas, que serão recebidas neste formato: 
```
{
	"latitude" : -22.921665, 
	"longitude": -43.240887,
	"data" : 2018-01-10 10:08:10,
	"temperatura": 31.05
}
```
A localização identifica o sensor. 

Precisamos de um componente servidor que armazene e recupere as temperaturas, utilizando HTTP Rest. Inicialmente, teremos apenas duas transações: 
- Armazenar temperatura (POST);
- Obter temperatura (GET);

A transação de obter temperatura, inicialmente, retornará a lista das temperaturas (e seus sensores) coletadas na própria data da consulta (a qualquer hora). 

## A transação de envio de temperatura

Se quiser registrar uma temperatura, um Sensor deverá **criar um recurso** no Servidor, e, para criar recursos, utilizamos o método HTTP **POST**. Podemos simular isso utilizando o programa **curl**: 

Exemplo de POST de temperatura: 
```
curl -i -H "Content-Type: application/json" -X POST -d '{"latit65,"longitude": -43.240887,"data" : "2018-04-26 10:12:03","temperatura": 30.10}' http://.../sensor
```
A resposta seria algo assim: 
```
http status 200 ok
...
{'status':'ok'}
```

## Leitura das temperaturas

As apps *frontend* (mobile e web) recuperarão sempre a lista das temperaturas medidas no dia. Futuramente, podemos ter outras formas de recuperação, mas vamos começar com o princípio **KISS** (Keep It Simple, Stupid). A transação de recuperar as temperaturas do dia seria assim: 
```
curl -i http://.../sensor
```
E a resposta seria um vetor JSON como este: 
```
[{"latitude":-22.921665,"longitude":-43.240887,"data":"2018-04-27 10:12:03","temperatura":30.1}]
```

## Arquitetura

Precisamos criar um Servidor HTTP / REST, e podemos fazer isso com o **Flask**, como vimos no [artigo passado](./clientes_servidores). 

Para armazenar a temperatura, podemos optar por um SGBD. Eu gosto muito do [**MongoDB**](https://www.mongodb.com/), que armazena objetos [**BSON**](http://bsonspec.org/). 

Ele possui uma API e uma biblioteca cliente para python: [**pymongo**](https://api.mongodb.com/python/current/) muito fácil de usar.

## Preparando

Precisamos instalar o MongoDB. É só seguir as [**instruções de instalação**](https://docs.mongodb.com/manual/installation/).

Depois precisamos instalar o **pymongo**: 
```
$ python -m pip install pymongo
``` 

E precisamos instalar algumas coisinhas mais: 
- **Flask**: ```pip install Flask```

## Database storage

Eu vou criar um [**módulo**](../modulos_imports) com as funções de persistência da aplicação. Com isso, eu diminuo o acoplamento entre o Servidor e o SGBD utilizado. Este módulo exportará duas funções:  

- storeTemp(latitude, longitude, dataMedicao, temperatura)
- getTemps(dataHoje)

Eis o código do módulo [**dbstore.py**](./dbstore.py): 
```
from pymongo import MongoClient
import datetime

client = MongoClient(port=27017)
db=client.temperaturas

def storeTemp(latitude, longitude, dataMedicao, temperatura):
    reg = {"latitude" : latitude,
           "longitude": longitude,
           "data" : dataMedicao,
           "temperatura": temperatura}
    db.temp.insert_one(reg)

def getTemps(dataHoje):
    dataOntem = dataHoje - datetime.timedelta(days=1)
    dataAmanha = dataHoje + datetime.timedelta(days=1)
    recs = db.temp.find({'data': {'$lt': dataAmanha, '$gt': dataOntem}})
    return recs
```
Para funcionar, eu preciso criar o banco de dados no MongoDB utilizando o [**Mongo Shell**](https://docs.mongodb.com/manual/mongo/): 
```
use temperaturas
```
E preciso criar uma coleção (que chamei de "temp") para armazenar meus documentos: 
```
db.createCollection("temp")
```
Para começar, meu módulo **dbstore** inicia uma conexão com o MongoDB e cria uma instância do banco de dados: 
```
client = MongoClient(port=27017)
db=client.temperaturas
```
Este código é imediato e executado sempre que você usar o módulo. 

Para inserir uma medição basta utilizar a função db.```<collection>```.insertOne(), que me permite inserir um documento na coleção.

Se você não conhece bem a API do MongoDB, há uma [**excelente documentação**](http://api.mongodb.com/python/3.6.1/) no seu site. 

Para ler as medições, eu utilizo a função "find()" passando uma expressão que filtrará os resultados. Eu quero as medições de um determinado dia, logo, eu utilizo a data, informando o dia de ontem e o de amanhã como parâmetros. Como eu posso passar qualquer data como parâmetro, preciso saber qual é o dia de amanhã, e pegar apenas as medições de hoje.

O objeto retornado é um [**Cursor**](http://api.mongodb.com/python/3.6.1/api/pymongo/cursor.html) MongoDB. 

## Servidor HTTP / REST

O módulo servidor é o [**server.py**](./server.py): 
```
import os, sys
from flask import Flask, request, json
import dbstore
from datetime import datetime
from bson.json_util import dumps

app = Flask(__name__)

@app.route('/sensor', methods=['GET'])
def getTemps():        
        status=200
        temps = dbstore.getTemps(datetime.now())
        lista = []
        for temp in temps:
            registro = {}
            registro['latitude'] = temp['latitude']
            registro['longitude'] = temp['longitude']
            registro['data'] = temp['data'].strftime("%Y-%m-%d %H:%M:%S")
            registro['temperatura'] = temp['temperatura']
        lista.append(registro)
        response = app.response_class(
            response=dumps(lista),
            status=status,
            mimetype='application/json')
        return response

@app.route('/sensor', methods=['POST'])
def storeTemps():
    content = request.json
    data = datetime.strptime(content['data'], '%Y-%m-%d %H:%M:%S')
    dbstore.storeTemp(content['latitude'],content['longitude'],
    data,content['temperatura'])
    return app.response_class(
            response="{'status':'ok'}",
            status=200,
            mimetype='application/json'
    ) 

app.run(host='0.0.0.0', port=8088)
```

Ele tem duas funções, cada uma associada a um método HTTP: 
```
@app.route('/sensor', methods=['GET'])
def getTemps(): 
...

@app.route('/sensor', methods=['POST'])
def storeTemps():
```
A função **storeTemps()** armazena uma medição. Eu uso a coleção **request.json** para obter as propriedades do objeto JSON informado no request POST. 

Um cuidado especial precisa ser tomado para fazer o "unmarshalling" da data, que vem em um formato string. Eu uso o método [**strptime**](https://docs.python.org/3/library/datetime.html), da classe **datetime** para isto. 

A função **getTemps()** retorna as temperaturas. Ela passa a data desejada para o módulo **dbstore**, que retorna um **cursor** com as medições encontradas. Eu poderia retornar diretamente esse cursor, modificando o código assim: 
```
        response = app.response_class(
            response=dumps(temps),
            status=status,
            mimetype='application/json')
```
O problema é que viriam todos os dados do **documento BSON** incluindo o campo **id**, gerado pelo MongoDB, e isto não me interessa enviar ao cliente. Outro problema seria a formatação da data. Por isto eu formato cada elemento que vou retornar na lista. Eu uso um objeto [**dictionary** ](http://www.pythonforbeginners.com/dictionary/how-to-use-dictionaries-in-python) para isto. A função **dumps** do pacote **bson.json_util** transforma minha **list** de **dictionary** em um string JSON.

