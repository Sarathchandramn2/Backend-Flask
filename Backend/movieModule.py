
import pymysql
from config import mydb
from flask import jsonify
from flask import flash, request
from app import app
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, create_access_token
import pymysql
import json
from app import app
from config import mydb
from flask import jsonify
from flask import flash, request




#insert movie details into movie table
class Movie:
    def __init__(self, mydb):
        self.mydb = mydb

    def add_movie(self, movie_name, movie_genre, director, language):
        try:
            with self.mydb.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO movies(movieName, movieGenre, director, language) VALUES(%s, %s, %s, %s)", (movie_name, movie_genre, director, language))
                    conn.commit()
            return jsonify({'message': 'Movie details added successfully!'})
        except pymysql.err.IntegrityError as e:
            return jsonify({'error': 'Duplicate entry'}), 409
        except Exception as e:
            print(e)
            return jsonify({'error': 'Internal server error'}), 500

@app.route('/insert', methods=['POST'])
def add_movie():
    json_data = request.json
    movie_name = json_data.get('movieName')
    movie_genre = json_data.get('movieGenre') 
    director = json_data.get('director')
    language = json_data.get('language')

    if not all([movie_name, movie_genre, director, language]):
        return jsonify({'error': 'Missing required parameters in JSON object'}), 400

    movie = Movie(mydb)
    return movie.add_movie(movie_name, movie_genre, director, language)

# view all datas in table
class MovieView:
    def __init__(self, mydb):
        self.mydb = mydb
    
    def view_movie(self):
        try:
            with self.mydb.connect() as conn:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT * FROM movies")
                    emp_rows = cursor.fetchall()
                    respone = jsonify(emp_rows)
                    respone.status_code = 200
                    return respone
        except pymysql.MySQLError as e:
            print("Error connecting to database: ", e)
            return jsonify({"error": "Error connecting to database"}), 500

movie_view = MovieView(mydb)

@app.route('/view', methods =['GET'])
def view_movie():
    return movie_view.view_movie()



#view particular data from table

class MovieView:
    def __init__(self, mydb):
        self.mydb = mydb
    def view_movie_details(self,movieId):
        try:
            conn = self.mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT movieId , movieName, movieGenre, director, language FROM movies WHERE movieId =%s", (movieId))
            empRow = cursor.fetchone()
            if not empRow:
                return jsonify({"error":"Movie with the id {} not found".format(movieId)}),404
            respone = jsonify(empRow)
            respone.status_code = 200
            return respone
        except pymysql.MySQLError as e:
            print("Error connecting to database: ", e)
        return jsonify({"error": "Error connecting to database"}), 500

movie_details_view = MovieView(mydb)

@app.route('/view/<movieId>', methods=['GET'])
def MovieDetails(movieId):
    return movie_details_view.view_movie_details(movieId)

#update the movie details
class MovieUpdater:
    def __init__(self, mydb):
        self.mydb = mydb
        
    def update_movie(self, movieId, data):
        try:
            MovieId = data['movieId']
            MovieName = data['movieName']
            MovieGenre= data['movieGenre']
            Director = data['director']
            Language = data['language']

            if  MovieName and MovieGenre and Director and  Language and request.method  == 'PUT':   
                sqlQuery = ("UPDATE movies SET movieName= %s, movieGenre= %s, director= %s, language=%s  WHERE movieId=%s")
                bindData = ( MovieName, MovieGenre, Director,  Language,MovieId )
                conn = self.mydb.connect()
                cursor = conn.cursor()
                cursor.execute(sqlQuery,bindData)
                conn.commit()
                respone = jsonify('Movie updated successfully!')
                respone.status_code = 200
                return respone
            else:
                return jsonify({"error":"Invalid Request"}), 400
        except pymysql.MySQLError as e:
            print("Error connecting to database: ", e)
            return jsonify({"error": "Error connecting to database"}), 500
        except Exception as e: 
            print("Error: ", e)
            return jsonify({"error": "Internal server error"}), 500
        finally:
            cursor.close()
            conn.close()

movie_updater = MovieUpdater(mydb)

@app.route('/update/<movieId>', methods=['PUT'])
def updateMovie(movieId):
    data = request.json
    return movie_updater.update_movie(movieId, data)

# Deleting the Movie
class Movie:
    def __init__(self, db):
        self.conn = db.connect()
        self.cursor = self.conn.cursor()
        
    def delete(self, movieId):
        try:
            self.cursor.execute("SELECT movieId FROM movies WHERE movieId =%s",(movieId))
            if self.cursor.rowcount == 0:
                return jsonify(message="Movie not found"), 404
            self.cursor.execute("DELETE FROM movies WHERE movieId =%s",(movieId))
            self.conn.commit()
            respone = jsonify(message='Movie deleted successfully!')
            respone.status_code = 200
            return respone
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()
            self.conn.close()

movie = Movie(mydb)

@app.route('/delete/<movieId>', methods=['DELETE'])
def deleteMovie(movieId):
    return movie.delete(movieId)
