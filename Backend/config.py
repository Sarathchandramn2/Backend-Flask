from app import app

from flaskext.mysql import MySQL

mydb = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'

app.config['MYSQL_DATABASE_PASSWORD'] = ''

app.config['MYSQL_DATABASE_DB'] = 'indproject'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mydb.init_app(app)
