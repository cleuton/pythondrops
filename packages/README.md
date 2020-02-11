![](../python-drops.png)
# pythondrops
## Python drops &amp; technology

(c) 2018 [**Cleuton Sampaio**](https://github.com/cleuton).

[![](../banner_livros2.png)](https://www.lcm.com.br/site/#livros/busca?term=cleuton)

# Pythondrops 3: Packages

Temos que finalizar algumas coisas antes de entrarmos mais a fundo no python. Para começar, vamos ver como o python procura os módulos que você importa. Vamos supor que você importe o módulo "A":

1 - É um módulo padrão do python?
2 - Existe um arquivo "A.py" na pasta do módulo que o importou?
3 - Está em algum dos diretórios da variável *"sys.path"*, que é inicializada a partir da variável de ambiente *PYTHONPATH*?
4 - Está na pasta default de instalação? No Ubuntu é: /usr/local/lib/python...

Vamos ver como isso pode ser meio complicado...

Suponha a seguinte estrutura de pastas (como temos no nosso repositório): 

- ./
    - bdir
        - b.py
    - a.py
    - procura.py


Agora, vejamos o código de cada uma: 

**procura.py**
```
import a
print(a.calcular())
```
**a.py**
```
import b
def calcular():
    return b.xpto(4)
```
**bdir/b.py**
```
def xpto(n):
    return(n**2)
```

Se tentarmos executar *procura.py* (python procura.py): 
```
$ python procura.py
Traceback (most recent call last):
  File "procura.py", line 1, in <module>
    import a
  File "/home/cleuton/python/pythondrops/packages/a.py", line 1, in <module>
    import b
ModuleNotFoundError: No module named 'b'
```
Hmmmm. Como podemos resolver isso? Vamos tentar criar a variável de ambiente *PYTHONPATH*:
```
export PYTHONPATH=/home/python/pythondrops/packages/bdir
```
No Windows use: ```set PYTHONPATH=C:\diretorio```.

Bem, rodamos novamente e funcionou:
```
$ python procura.py
16
```
Mas tem outro jeito de fazer isto sem usar *PYTHONPATH*. Note que a pasta **bdir** está no mesmo nível do script **a.py**, isto faz dela um *pacote*! Se importarmos corretamente, o script deve funcionar. Para começar, remova a variável de ambiente PYTHONPATH e verifique se vai dar o mesmo erro de antes. Agora, mude o arquivo **a.py** para esta forma:
```
import bdir.b
def calcular():
    return bdir.b.xpto(4)
```
Funcionou, não? Ok. Mas esta forma fica meio ruim... Podemos melhorar esse *import*: 
```
from bdir import b
def calcular():
    return b.xpto(4)
```
Esta é a maneira de importar módulos de pacotes!

## Bytecode

Python é uma linguagem interpretada. O interpretador transforma código-fonte em algo intermediário, chamado de *"bytecode"*. São arquivos com extensão "pyc". 

Para otimizar o desempenho, o python gera, dentro da pasta do módulo, uma pasta "__pycache__" que contém os bytecodes dos módulos compilados.

O python sempre verifica o cache antes de compilar novamente um módulo. Ele só deixa de fazer isso quando o módulo é invocado, ou quando ele não encontra o código-fonte do módulo. 

É possível criar pacotes sem o código-fonte (somente com os pyc), mas isto é um assunto mais avançado, para outro **pythondrops**.

## dir()

O comando **dir()** verifica os nomes expostos por um módulo. Por exemplo, se abrirmos o python interativo (use o comando ```python```): 
```
>>> import a
>>> dir(a)
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'b', 'calcular']
```
Estes são os nomes que o módulo **a** exporta. Note que o nome do módulo **b** aparece nele.

## Criando um pacote

Vamos pegar os scripts do cálculo de **delta** e de **raízes** da equação do segundo grau, mostrados no [**exemplo anterior**](../modulos_imports) e criar um pacote chamado **bhaskara**: 
- bhaskara
    - ```__init__.py```
    - cdelta.py
    - raizes.py

O que é esse arquivo ```__init__.py```? É um arquivo que indica ao python para tratar esta pasta como um **pacote**. Isto serve para evitar que diretórios com nomes comuns, **ofusquem** pacotes. Você pode deixar o arquivo vazio ou pode usá-lo para inicialização.

O arquivo **cdelta.py** continua como estava: 
```
def calcDelta(a,b,c):
    delta = b**2 - 4*a*c
    if delta < 0:
        return float('nan')
    else:
        return delta
```

Já o arquivo **raizes.py** precisa ser modificado, pois agora ele faz parte de um pacote e precisa importar o arquivo **cdelta** de maneira diferente:
```
from . import cdelta
import math
def calcRaizes(a,b,c):
    delta = cdelta.calcDelta(a,b,c)
    if math.isnan(delta):
        print('Não possui raízes reais')
    elif delta == 0:
        raiz = -b / 2*a
        print('Possui apenas uma raiz: ',raiz)
    else:
        x1 = (-b + math.sqrt(delta)) / 2*a
        x2 = (-b - math.sqrt(delta)) / 2*a
        print('X1: ',x1,', X2: ',x2)
```

Estamos importando da pasta atual do pacote o arquivo **cdelta**. Se fosse de uma pasta superior, dentro do mesmo pacote, usaríamos ```from .. import```.

## Importando tudo

Vamos supor que você queira importar TUDO o que está definido em um pacote, portanto usaria o comando: ```from pacote import *```. Só que, para funcionar, é necessário definirmos uma lista dentro do ```__init__.py```: 
```
__all__=["cdelta","raizes"]
```
Dessa forma, você garantiria que todos os módulos do pacote seriam importados.

## So long

Por enquanto, é só. Espero que você agora tenha uma noção melhor de pacotes, módulos e imports em python. Há muito ainda a ver, especialmente se você quiser criar pacotes que possam ser baixados com **pip**, mas isto é assunto para outro **pythondrops**.



