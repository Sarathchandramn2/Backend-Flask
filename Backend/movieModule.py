import pymysql
import json
from app import app
from config import mydb
from flask import jsonify
from flask import flash, request

@app.route('/get', methods=['GET'])
def Get():
    return 'null'

@app.route('/insert', methods=['POST'])
def create_movie():
    try:
        json = request.json
        print(json)
       
        movie_name = json['movie_name']
        movie_genre = json['movie_genre']
        director = json['director']
        language    = json['language']
        if   movie_name and movie_genre and director and  language and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO movie(movie_name, movie_genre, director,  language) VALUES( %s, %s, %s,%s)"
            bindData = ( movie_name, movie_genre, director,language)
            cursor.execute(sqlQuery, bindData)
            # print(cursor.execute(sqlQuery, bindData))
            conn.commit()
            respone = jsonify('movie added successfully!')
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

@app.route('/view', methods =['GET'])
def movie():
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT movie_id,  movie_name, movie_genre, director,language FROM movie")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e: 
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/mov/<movie_id>', methods=['GET'])
def moviedetails(movie_id):
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT movie_id ,movie_name,movie_genre, director,language FROM movie WHERE movie_id =%s", (movie_id))
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/update/<movie_id>', methods=['PUT'])
def updatemovie(movie_id):
    try:
        _json = request.json
        print(_json)
        _movie_id = _json['movie_id']
        _movie_name = _json['movie_name']
        _movie_genre= _json['movie_genre']
        _director = _json['director']
        _language  = _json['language']
        if _movie_name and _movie_genre and  _director and _language  and request.method  == 'PUT':           
            sqlQuery = ("UPDATE movie SET movie_name= %s, movie_genre= %s, director= %s, language= %s WHERE movie_id=%s")
            bindData = ( _movie_name, _movie_genre, _director,   _language ,_movie_id)
            conn = mydb.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            respone = jsonify('moviee updated successfully!')
            respone.status_code = 200
            print(respone)
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close() 


@app.route('/delete/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    try:
        conn = mydb.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movie WHERE movie_id =%s",(movie_id))
        conn.commit()
        respone = jsonify('moviee deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
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
