![](../python-drops.png)
# pythondrops
## Python drops & technology

(c) 2018 [**Cleuton Sampaio**](https://github.com/cleuton).

# PythonDrops 6: Bigdata com Python & Spark

Muito bem, agora chegou o momento de usarmos uma ferramenta de Big data e realizar uma análise. E vamos usar o Spark com a linguagem Python!
Vamos ver com usar o Spark para criar jobs de análise de big data de maneira simples e prática. Você terá que instalar o Spark, mas isto não é trabalho algum. Para evitar custos, vamos executar localmente, em sua máquina, com um conjunto reduzido de dados. Mas o processo para executar em nuvem é bem simples.

**Dados climáticos**

Eu participo de um projeto de sustentabilidade chamado "Kuaray" (http://kuaray.org), que significa "Sol", em Tupi-guarani. O objetivo deste projeto é medir o impacto dos gases de efeito estufa, de maneira independente, nos fornecendo um dataset atualizado para estudos sobre o aquecimento global. 

O projeto Kuaray criou um modelo de sensor, movido à energia solar, capaz de coletar dados climáticos 24 x 7 e transmitir para um "broker" MTQQ. É um projeto de IoT associado a Big data. 

**Instalação do Spark**

A instalação do Spark é um pouco mais complexa, logo, vamos devagar. 

    1. Primeiramente, certifique-se que você tenha instalado a linguagem Java, na versão JDK (Java Development Kit): 
        1. Abra um Terminal Linux ou Prompt de comandos;
        2. Digite "javac -version";
        3. Se houver algum erro, tipo "comando não encontrado", então você precisa instalar o Java JDK;
        4. Caso contrário, pule a etapa 2;
    2. Baixe o Java JDK 8.x (eu não testei com a versão 9). Se tiver problemas na instalação do Java, siga estes passos: https://www.devmedia.com.br/instalacao-e-configuracao-do-pacote-java-jdk/23749;
    3. Agora, baixe um arquivo binário do Apache Spark: https://spark.apache.org/downloads.html; Escolha um executável já com o Hadoop junto.

O arquivo do Spark que você baixou já é pré-compilado e pronto para usar. Podemos utilizá-lo imediatamente. Basta descompactar o arquivo "tgz" que você baixou, abrir uma janela Terminal (ou prompt de comandos) e ativar seu ambiente virtual. Então, navegue para a pasta "bin" da instalação do Spark e execute o comando: "./pyspark".

Se tudo deu certo, a saída no Terminal será mais ou menos assim:
``` 
$ cd ~/spark-2.2.0-bin-hadoop2.7/
$ cd bin
$ source activate datascience
(datascience) $ ls
beeline             load-spark-env.sh  run-example       spark-class.cmd  spark-shell       spark-submit
beeline.cmd         pyspark            run-example.cmd   sparkR           spark-shell2.cmd  spark-submit2.cmd
find-spark-home     pyspark2.cmd       spark-class       sparkR2.cmd      spark-shell.cmd   spark-submit.cmd
load-spark-env.cmd  pyspark.cmd        spark-class2.cmd  sparkR.cmd       spark-sql
(datascience) $ ./pyspark

Python 3.6.2 |Continuum Analytics, Inc.| (default, Jul 20 2017, 13:51:32) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
17/11/28 07:37:38 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
17/11/28 07:37:38 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
17/11/28 07:37:57 WARN ObjectStore: Version information not found in metastore. hive.metastore.schema.verification is not enabled so recording the schema version 1.2.0
17/11/28 07:37:58 WARN ObjectStore: Failed to get database default, returning NoSuchObjectException
17/11/28 07:38:00 WARN ObjectStore: Failed to get database global_temp, returning NoSuchObjectException
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.2.0
      /_/

Using Python version 3.6.2 (default, Jul 20 2017 13:51:32)
SparkSession available as 'spark'.
>>> 
```
**O dataset**

O dataset que vamos usar é uma amostra de apenas dois sensores, com poucos dados, já que vamos executar o Spark em apenas uma máquina. O Layout das informações é assim:

- id: Texto;
- date: Data/Hora formato ISO;
- humidity: Real, umidade do ar;
- latitude: Real;
- longitude: Real;
- nodeName: Texto;
- quality: Real, indicador de GHG na atmosfera;
- temperature: Real.

O que desejamos é agregar os dados por localização. Para isto, vamos usar a latitude e longitude. Vamos agregar os valores de qualidade do ar (quality) por localização. Para isto, vamos criar uma chave composta com latitude e longitude, contar os registros e somar os valores de qualidade do ar, e depois dividir a soma pela contagem.

**Primeiro programa**

Dentro do nosso repositório (veja o capítulo de introdução) há um código Python para executarmos com o Spark: "book/capt14/spark_avg1.py", além do dataset de medições (“medicoes.csv”). 

Note que não é um Notebook Jupyter, mas um script Python autônomo. Vamos executá-lo usando um comando do Spark. Antes de mais nada, vejamos o código-fonte: 
```
from pyspark import SparkConf, SparkContext

import sys

APP_NAME = " Agrega indicador de GHG "

def parseLine(line):
    fields = line.split(',')
    regiao = repr(fields[3]) + repr(fields[4])
    valor = float(fields[6])
    return (regiao, valor)

def main(sc,arquivo):
   lines = sc.textFile(arquivo)   
   filterDD = lines.filter(lambda l: not l.startswith('id'))   
   campos = filterDD.map(parseLine)
   medias = campos \
        .mapValues(lambda valor: (valor, 1)) \
        .reduceByKey(lambda x,y: (x[0]+y[0], x[1]+y[1])) \
        .mapValues(lambda v: v[0]/v[1]) \
        .collect()   
   for result in medias:
       print(result)

if __name__ == "__main__":
   conf = SparkConf().setAppName(APP_NAME)
   conf = conf.setMaster("local[*]")
   sc   = SparkContext(conf=conf)
   filename = sys.argv[1]
   main(sc, filename)

```
O programa tem alguns grandes blocos. Para começar, gostaria de chamar sua atenção para a linha que inicia por "if __name__ == "__main__"". Esta linha separa o código imediato do código das funções. 

Se um script Python for executado, ele começará a executar as linhas imediatas. Porém, pode ser que queiramos usar o script como uma biblioteca, compartilhando código, logo, não queremos que as linhas imediatas sejam executadas. Este comando "if" só executa as linhas de comandos imediatos se o programa estiver sendo invocado diretamente como programa principal, e não sendo importado por outros programas. 

O pacote “pyspark” contém as classes necessárias para trabalharmos com Spark na linguagem Python: SparkConf e SparkContext. Vamos analisar a estrutura geral do código: 

**1 – Inicialização do código: **

No bloco final do programa, dentro do “if __name__ == "__main__" temos o código que inicializa o Spark, criando uma instância de SparkConf. Esta instância serve para configurarmos o uso do Spark, passando, entre outras coisas, o nome da aplicação e quem será o nó “master” do Spark. Se estivermos executando em Cluster, informamos a URL do nó Master no método “setMaster”. Se estivermos executando local (é o nosso caso), especificamos apenas “local”. Entre colchetes, especificamos o número de threads a serem utilizados. Um asterisco significa: Tudo, inclusive GPU.

Finalmente, criamos uma instância de “SparkContext”. Todos os métodos da API devem ser invocados a partir dela.

E pegamos o nome do arquivo do primeiro argumento passado ao programa, e invocamos a função “main”.

**2 – Execução da tarefa: **

A função “main” recebe o nome do arquivo e executa a tarefa. Basicamente, ela: 

a) Lê o arquivo;
b) Despreza a linha de cabeçalho;
c) Mapeia os campos do CSV em variáveis, através da função “parseline”, que retorna a “chave” (região) e o valor;
d) Conta os registros, soma as medições;
e) Calcula as médias por região e exibe.


Vamos executar esse programa!

Abra um Terminal ou prompt de comandos. Vá para a pasta “bin” dentro da pasta do Spark. Digite o comando “spark-submit”: 

spark-submit /[path]/spark_avg1.py /[path]/medicoes.csv

Note que “/[path]” é o caminho onde você baixou o código-fonte e o arquivo de medições.

O Spark é muito verboso, e vai “vomitar” muita coisa na tela. Você pode controlar o nível de “log” no arquivo “log4j.properties” (renomeie “log4j.properties.template” e altere o nível de log).

No meio da verborragia do Spark, você verá o resultado do nosso “print”: 
```
("'-22.9222276''-43.2428463'", 102.07051282051283)
("'-22.9148359''-43.2291778'", 120.62433022720697)
```

Aí está a média de medições de qualidade do ar por região!

**Código-fonte**

O código-fonte deste programa está no arquivo [**spark_avg1.py**](./spark_avg1.py) e o arquivo de dados em [**medicoes.csv**](./medicoes.csv).
