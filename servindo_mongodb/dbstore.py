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
    