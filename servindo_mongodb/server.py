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