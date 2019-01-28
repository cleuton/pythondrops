import psycopg2
import urllib.parse as up
import datetime
data = datetime.datetime.now()
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
cursor.execute("INSERT INTO account (user_id,username,password,email,created_on,last_login) VALUES (%s, %s, %s, %s, %s, %s)",
    (3, 'Beltrano', 'bbb', 'beltrano@test', data.strftime('%Y-%m-%d %H:%M:%S'), None))
db.commit()
db.close()