import pymysql
import json
from app import app
from config import mydb
from flask import jsonify
from flask import flash, request
from flask_jwt_extended import JWTManager, create_access_token


# @app.route('/get', methods=['GET'])
# def Get():
#     return 'null'

# inserting the datas

@app.route('/insert', methods=['POST'])
def createMovie():
    try:
        json = request.json
        print(json)
       
        movieName = json['movieName']
        movieGenre = json['movieGenre']
        director = json['director']
        language    = json['language']
        if   movieName and movieGenre and director and  language and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO movie(movieName, movieGenre, director,  language) VALUES( %s, %s, %s,%s)"
            bindData = ( movieName, movieGenre, director,language)
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
        

#View all the datas 

@app.route('/view', methods =['GET'])
def movieView():
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT movieId,  movieName, movieGenre, director,language FROM movie")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e: 
        print(e)
    finally:
        cursor.close() 
        conn.close() 
        
#View particular movie with respect to movie_id 
@app.route('/mov/<movieId>', methods=['GET'])
def movieDetails(movieId):
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT movieId ,movieName,movieGenre, director,language FROM movie WHERE movie_id =%s", (movieId))
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        
#updating the  data
@app.route('/update/<movieId>', methods=['PUT'])
def updatemovie(movieId):
    try:
        data= request.json
        print(data)
        movieId = data['movieId']
        movieName = data['movieName']
        movieGenre= data['movieGenre']
        director = data['director']
        language  = data['language']
        if movieName and movieGenre and  director and language  and request.method  == 'PUT':           
            sqlQuery = ("UPDATE movie SET movieName= %s, movie_genre= %s, director= %s, language= %s WHERE movieId=%s")
            bindData = ( movieName, movieGenre, director,   language ,movieId)
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

#deleting the  datas
@app.route('/delete/<movieId>', methods=['DELETE'])
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



#Registration of user
@app.route('/register', methods=['POST'])
def register():
    try:
        json = request.json
        print(json)
        email= json['email']
        username = json['username']
        password = json['password']
        usertype = "user"
        # hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # print(hashed)
      
        if email and username and password and usertype and request.method == 'POST':
            
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            query= "SELECT * FROM user WHERE username= '%s'" % (username)
            data=cursor.execute(query)
            print(data)
            if data>0:
                conn.commit()
                response = jsonify('User already Exsist!!')
                response.status_code = 200
                return response
            else:
                sqlQuery = "INSERT INTO user(email,username,password, usertype) VALUES(%s, %s, %s , %s)"
                bindData = (email,username,password, usertype)
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

#Login user
@app.route('/login', methods=['POST'])
def login():
    try:
        json = request.json
        print(json)
        username = json['username']
        password = json['password']
        # login_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(username)
        if username and password and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            sqlQuery="SELECT * FROM user WHERE username= '%s'  and password='%s'" % (username, password)
            # sqlQuery="SELECT * FROM user WHERE username= '%s' " % (username)
            # print(sqlQuery)
            data=cursor.execute(sqlQuery)
            row = cursor.fetchone()
            usertype=row.get('usertype')         
            if data==1:
                access_token = create_access_token(identity=username)
                conn.commit()
                return jsonify(message='Login Successful', access_token=access_token ,usertype=usertype),200
                
            else:
                conn.commit()
                return jsonify('Bad email or Password... Access Denied!'), 401
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
