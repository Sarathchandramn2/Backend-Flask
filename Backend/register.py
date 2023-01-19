import pymysql
import json
from app import app
from config import mydb
from flask import jsonify
from flask import flash, request




@app.route('/get', methods=['GET'])
def Get():
    return 'null'

@app.route('/register', methods=['POST'])
def register():
    try:
        json = request.json
        print(json)
        yourname= json['yourname']
        username = json['username']
        password = json['password']
        if yourname and username and password  and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO user(yourname,username, password) VALUES(%s, %s, %s)"
            bindData = (yourname , username, password)
            cursor.execute(sqlQuery, bindData)
            conn.commit()  
            respone = jsonify('User added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'Exception'
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone



    
if __name__ == "__main__":
    app.run()
    