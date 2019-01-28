import psycopg2
import urllib.parse as up
up.uses_netloc.append("postgres")
# A url abaixo está propositadamente ofuscada:
url = up.urlparse("postgres://@@@@@@:*****@elmer.db.elephantsql.com:5432/##")
db = psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cursor = db.cursor()
cursor.execute('select * from account')
registros = cursor.fetchall()
for registro in registros:
   print (registro)
db.close()