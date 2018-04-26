![](../python-drops.png)
# pythondrops
## Python drops & technology

(c) 2018 [**Cleuton Sampaio**](https://github.com/cleuton).

# Pythondrops 4: Clientes e servidores HTTP

Nesse mundo de [**microsserviços**](http://www.obomprogramador.com/2015/03/micro-servicos-o-que-sao-e-para-que.html) é cada vez mais importante aprender a construir os dois lados da história: O frontend (cliente) e o backend (servidor).

Python tem bibliotecas fantásticas para isto, como o cliente HTTP [**requests**](http://docs.python-requests.org/en/master/) e o servidor HTTP [**Flask**](http://flask.pocoo.org/). 

![](./requests_flask.png)

## Aplicacação exemplo

Para demonstrar a criação de clientes e servidores com python, eu escolhi a minha aplicação [**FaceGuard**](https://github.com/cleuton/FaceGuard), que está publicada no meu blog [**OlharComputacional**](http://olharcomputacional.com).

![](https://github.com/cleuton/FaceGuard/blob/master/img/ml_iot_1_completo.jpg)

É uma aplicação de reconhecimento facial, que envolve um cliente **Raspberry PI** e um servidor. Após tirar uma foto, o Raspi a envia ao servidor (utilizando POST), que o recebe, processa e devolve uma resposta HTTP.

Mas eu nem vou entrar em detalhes sobre o processo de reconhecimento facial, pois não é objetivo deste blog. Só vou falar do **requests** e do **Flask**.

O código-fonte do cliente python, que roda no Raspi, está [**AQUI**](https://github.com/cleuton/FaceGuard/blob/master/FaceNet/photoclient.py), e o código-fonte do servidor, que roda em um computador remoto, está [**AQUI**](https://github.com/cleuton/FaceGuard/blob/master/facenetmaster/src/photoserver.py).

## Cliente python

O cliente roda em um **Raspberry PI 3** com o sistema operacional **Raspbian** (uma compilação do Debian para ARM). Eis o código-fonte: 
```
import requests
import RPi.GPIO as GPIO
import time
import picamera

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23,GPIO.OUT) # Yellow
GPIO.setup(24,GPIO.OUT) # Green
GPIO.setup(25,GPIO.OUT) # Red
camera = picamera.PiCamera()

def uploadFoto(foto):
    url = 'http://localhost:8088'
    files = {'file': open(foto, 'rb')}
    r = requests.post(url, files=files)
    return r.status_code == requests.codes.ok


def waitFoto():
    input_state = GPIO.input(18)
    if input_state == 0:
        GPIO.output(23,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)
        GPIO.output(24,GPIO.LOW)
        print('Tirou foto!')
        GPIO.output(23,GPIO.HIGH)
        camera.capture('foto.jpg')
        time.sleep(0.2)
        retorno = uploadFoto('foto.jpg')
        print('*** Retorno do processamento da foto: ', retorno)
        GPIO.output(23,GPIO.LOW)
        if retorno = True:
            GPIO.output(24,GPIO.HIGH)
        else:
            GPIO.output(25,GPIO.HIGH)
        time.sleep(0.2)    
    

while (True):
    waitFoto()
```
Este código utiliza a biblioteca RPi.GPIO para acessar as portas [**GPIO**](https://www.raspberrypi.org/documentation/usage/gpio/) do Raspberry. Mas isto também não faz parte deste tutorial (se quiser saber mais: [**leia no Bom Programador**](http://www.obomprogramador.com/2018/02/tutorial-de-machine-learning-iot.html)). 

Ele simplesmente entra em um *loop infinito* aguardando que um botão, na *protoboard* ligada ao Raspberry, seja acionado. Se isto acontecer, ele apaga todos os **LEDs** (há um verde, um amarelo e um vermelho), tira uma foto e envia para o servidor utilizando **HTTP POST**, de maneira síncrona. Ao receber a resposta, acende o LED Verde, se for **HTTP STATUS 200**, ou o LED Vermelho, se for **HTTP STATUS 404**. 

O método utilizado para enviar a foto está na função "uploadFoto()" e é simplesmente um POST: 
```
r = requests.post(url, files=files)
```
E estou comparando a resposta (r.status_codes) com a lista de **HTTP Status OK** e retornando isso: 
```
return r.status_code == requests.codes.ok
```

Se o status for 200, então eu acenderei o LED verde, senão, o vermelho.

## O Servidor python

Para o Servidor, utilizei a biblioteca [**Flask**](http://flask.pocoo.org/) que permite criar servidores sem complicação. 

Eis o código-fonte do servidor: 
```
import os, sys
from flask import Flask, request, redirect, url_for, abort,  json
from werkzeug.utils import secure_filename
import Foto
from glob import glob

UPLOAD_FOLDER = 'serverutil/uploads/unknown'
ALLOWED_EXTENSIONS = set(['jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print('No file part!', file=sys.stderr)
        return 'No File Part', 422
    file = request.files['file']
    if file.filename == '':
        print('No selected file!', file=sys.stderr)
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        for ftxt in glob("/Users/cleuton/Documents/projetos/DL_iot/facenetmaster/src/serverutil/processadas/*.*"):
            os.remove(ftxt)        
        retorno = Foto.process()
        print('Retorno do processamento: ', retorno)
        status=200
        if not retorno:
            status=404
        response = app.response_class(
            response=json.dumps({'status':'OK'}),
            status=status,
            mimetype='application/json'
        )        
        return response
app.run(host='0.0.0.0', port=8088, debug=True)
```

O **Flask** utiliza [**decorators**](https://pythonhelp.wordpress.com/2013/06/09/entendendo-os-decorators/) para demarcar as funções que tratarão os requests, de acordo com a **URL** e o **Método HTTP** utilizado. Por exemplo, no código-fonte temos: 
```
@app.route('/', methods=['POST'])
```
Isto indica que função "decorada", **upload_file()**, atenderá a requests para a raiz do servidor, feitos com método POST.

Ao receber um request, eu faço algumas verificações:
1 - Veio um arquivo dentro do request? (```if 'file' not in request.files:```);
2 - O nome do arquivo está vazio? (```if file.filename == '':```);
3 - É uma das extensões permitidas? (```if file and allowed_file(file.filename):```).

Eu aceito apenas arquivos 'jpg', como você pode ver na função **allowed_file()**. O objeto **request**, que eu importei do Flask, contém tudo o que preciso saber sobre o request HTTP.

A lista **request.files** retorna os arquivos que vieram com o request. E o objeto retornado possui um método **save()**, que nos permite salvar no HD.

Eu criei uma instância de **app** para indicar a minha aplicação Flask. Ela possui uma classe chamada "response_class" que me permite criar uma resposta a ser enviada ao Cliente. Utilizando o objeto **json**, também importado do Flask, eu posso construir uma resposta: 
```
response = app.response_class(
            response=json.dumps({'status':'OK'}),
            status=status,
            mimetype='application/json'
```
Finalmente, tenho o comando imediato que inicia minha aplicação Flask: 
```
app.run(host='0.0.0.0', port=8088, debug=True)
```

## Experimente

Você pode criar servidores e clientes, inclusive analisando objetos enviados, querystring etc. Só para ter uma ideia, aqui está um exemplo do meu outro blog [**ReactDontPanic**](http://reactdontpanic.com/redux_form/), que processa POST de formulários:
```
from flask import Flask
from flask_cors import CORS
from flask import request
app = Flask(__name__)
CORS(app)
@app.route('/', methods=['POST'])
def logon():
    return '{"user": "' + request.form['usuario'] + '","status":"autenticado"}';
```
Eu acessei os campos enviados através da lista **request.form**. 

**E, se quiser enviar JSON?** 

Sem problemas! Aqui está um exemplo, do [**StackOverflow**](https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask) que faz exatamente isto: 
```
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    print content['mytext']
    return jsonify({"uuid":uuid})

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)
```
Ele recebe um objeto JSON e um Querystring. O seguinte código cliente funciona com ele: 
```
import requests
res = requests.post('http://localhost:5000/api/add_message/1234', json={"mytext":"lalala"})
```
O servidor pega o dado através da propriedade "uuid", recebida na URL definida no **decorator**, e recebe um objeto **JSON** dentro do corpo do post.

## Deploy

Você já notou que o Flask tem um servidor embutido, não? O comando abaixo o inicia: 
```
app.run(host='0.0.0.0', port=8088, debug=True)
```
Só que este servidor não é próprio para ambientes de Produção! Se você quiser instalar sua aplicação Flask e servir seus usuários, é melhor escolher um "host" que suporte o padrão [**wsgi**](https://pt.wikipedia.org/wiki/Web_Server_Gateway_Interface). Existem várias opções, entre elas: 
- [**Apache**](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/#installing-mod-wsgi) com *mod_wsgi*;
- [**NGix**](http://flask.pocoo.org/docs/0.12/deploying/uwsgi/#configuring-nginx);

Se você iniciar seu servidor diretamente, sem usar o Flask, ele também funcionará: 
```
...
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088)
```
Mas, se iniciar através do Flask, lembre-se que a linha acima não será executada, pois o programa não será mais o "```__main__```".

Mas veremos isso em um outro Post. Para desenvolvimento, o servidor do Flask é mais do que suficiente.