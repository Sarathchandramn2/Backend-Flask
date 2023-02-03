from models import Movie
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
from services.services import execute,commitConnection
import logging
from services.Logger import *
from services.Auth import *
from flask import make_response

# insert Movie details into movie table

@app.route('/movie', methods=['POST'])
@jwtauth
def createMovie(movieid=None):
    try:
        json = request.json
        moviename = json['moviename']
        check_For_String(moviename)
        check_For_Empty_String(moviename)
        moviegenre = json['moviegenre']
        check_For_String(moviegenre)
        check_For_Empty_String(moviegenre)
        language = json['language']
        check_For_String(language)
        check_For_Empty_String(language)
        director = json['director']
        check_For_Empty_String(director)
        
        #Calling the function demo 
        demo(None, moviename, moviegenre, language, director, request)
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify('Some Columns are missing or Mispelled the Column name')
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        return jsonify(str(e))
    except Exception as e :
        logger.error(f"Exception: {e}")
        return jsonify('something went wrong..!!')
    return jsonify({'message': 'movie added successfully!'})

# delete movie from table movie
@app.route('/movie/<movieid>', methods=['DELETE'])
@jwtauth
def deletemovie(movieid, moviename=None, moviegenre=None,  director=None, language=None):
    try:
        movie = Movie(movieid, moviename, moviegenre, director, language)
        sqlQuery = "SELECT moviename FROM movies WHERE movieid =%s"
        bindData = movie.movieid
        data = execute(sqlQuery, bindData)
        if data == 0:
            commitConnection()
            response = jsonify('movie does not exist')
            return response
        elif data == 1:
            sqlQuery = "DELETE FROM movies WHERE movieid =%s"
            bindData = movie.movieid
            data = execute(sqlQuery, bindData)
            commitConnection()
            respone = jsonify('movie deleted successfully!')
            respone.status_code = 200
            return respone
    except Exception as e:
        logger.error(f"Error Occurred: {e}")
        return "Error Occurred: {}".format(e), 500

    
            
# update movie from table
@app.route('/movie/<movieid>', methods=['PUT'])
@jwtauth
def updateMovie(movieid):
    
    try:
        data = request.json
        newId = movieid
        newName = data['moviename']
        newGenre = data['moviegenre']
        newDirector = data['director']
        newLanguage = data['language']
        
        movie = Movie(newId, newName, newGenre, newDirector, newLanguage)
        if newId and newName and newGenre and newDirector and newLanguage and request.method == 'PUT':
            query = "SELECT moviename FROM movies WHERE movieid=%s"
            bindData = movie.movieid
            data = execute(query, bindData)
            if data == 0:
                commitConnection()
                response = jsonify('Movie does not exist')
                return response
            elif data == 1:
                sqlQuery = "UPDATE movies SET moviename= %s, moviegenre= %s, director= %s, language= %s WHERE movieid=%s"
                bindData = (movie.moviename, movie.moviegenre, movie.director, movie.language, movie.movieid)
                execute(sqlQuery, bindData)
                commitConnection()
                response = jsonify('movie updated successfully!')
                response.status_code = 200
                return response
        else:
            return jsonify('something went wrong')
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify('Some Columns are missing or Mispelled the Column name')
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        return jsonify(str(e))
    except Exception as e :
        logger.error(f"Exception: {e}")
        return jsonify('something went wrong..!!')

# view all Movies from movie table
@app.route('/movie', methods=['GET'])
@jwtauth
def viewMovies():
    try:
        
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT movies.movieid,movies.moviename, genre.genre, movies.director, movies.language FROM movies JOIN genre ON movies.moviegenre = genre.genreid;")
        empRows = cursor.fetchall()
        conn.commit()
        # commitConnection()
        response = jsonify(empRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error while retrieving movies from database'})

        
# view particular movies from movie table

@app.route('/movie/<movieid>', methods=['GET'])
@jwtauth
def movieDetail(movieid, moviename=None, moviegenre=None, director=None, language=None):
    try:
        movie = Movie(movieid,moviename, moviegenre, director, language)
        
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = ("SELECT movies.movieid, genre.genre, movies.director, movies.language FROM movies JOIN genre ON movies.moviegenre = genre.genreid WHERE movieid= %s")
        bindData = movie.movieid
        cursor.execute(sqlQuery, bindData)
        empRow = cursor.fetchone()
        reponse = jsonify(empRow)
        reponse.status_code = 200
        return reponse
    except Exception as e:
        return jsonify({'error': 'Error while retrieving movies from database'})
        

# error handling
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

#function to check the values are in string
def check_For_String(value):
    if not isinstance(value, str):
        raise ValueError(f"{value} should be a string")
    
#function to check the values are empty or not
def check_For_Empty_String(value):
    if not value or not value.strip():
        raise ValueError(f"{value} cannot be empty or only whitespace")


def demo(movieid, moviename, moviegenre, language, director, request):
    if not moviename or not moviegenre or not language or not director:
        response = make_response(jsonify({'message': 'All fields are required'}))
        response.status_code = 400
        return response

    movie = Movie(movieid, moviename, moviegenre, language, director)
    if request.method == 'POST':
        sqlQuery = "INSERT INTO movies(moviename, moviegenre, language, director) VALUES( %s, %s, %s,%s)"
        bindData = (movie.moviename, movie.moviegenre, movie.director, movie.language)
        try:
            execute(sqlQuery, bindData)
            commitConnection()
        except pymysql.err.IntegrityError as e:
            logger.error(f"IntegrityError: {e}")
            # return jsonify({'message': 'Movie already exists with the same name'})
        
        response = jsonify({'message': 'movie added successfully!'})
        response.status_code = 200
        return response