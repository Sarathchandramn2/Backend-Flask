from flask import Flask
import pymysql

app = Flask(__name__)



if __name__ == '__main__':
    from routes.movie_routes import *
    app.run(debug=True)
