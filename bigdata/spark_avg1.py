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