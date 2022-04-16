from datetime import datetime
from datetime import timedelta
import json
movimento=[]
agora=datetime.now()
depois=timedelta(minutes=10)
nova=agora+depois
formato="%d/%m/%Y %H:%M:%S"
movimento.append({"cliente":1, 
	"mercadoria":10, 
	"quantidade":5.5,
	"data":agora.strftime(formato)})
movimento.append({"cliente":2, 
	"mercadoria":15, 
	"quantidade":23.2,
	"data":nova.strftime(formato)})
with open('saida.json', 'w') as saida:
    json.dump(movimento,saida)