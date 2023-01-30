import pymysql
from config import mydb
from flask import jsonify
from flask import flash, request
import traceback


class Movies:
    def __init__(self, name, genre, director, language):
        if not name.isalpha():
            raise ValueError("Invalid movie name. Only alphabets are allowed.")
        
        self.name = name
        self.genre = genre
        self.director = director
        self.language = language

    def addTodb(self):
        try:
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO movies(moviename ,moviegenre, director, language) VALUES(%s, %s, %s, %s)"
            bindData = (self.name, self.genre, self.director, self.language)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            return {"message": "Movie details added successfully!"}
        except pymysql.err.IntegrityError as e:
            if "name" in str(e):
                return {"error": "Movie name already exists. Try with a different movie name."}, 409
            if "director" in str(e):
                return {"error": "Director already exists. Try with a different director name."}, 409
            return {"error": "Duplicate entry : Try again"}, 409
        except pymysql.err.ProgrammingError as e:
            if "unknown column" in str(e):
                return {"error": "Invalid column name. Please check the column names."}, 400
            if "table" in str(e):
                return {"error": "Invalid table name. Please check the table name."}, 400
        except pymysql.err.OperationalError as e:
            if "Access denied" in str(e):
                return {"error": "Access denied to the database. Check your database credentials."}, 401
            if "Unknown database" in str(e):
                return {"error": "Unknown database. Check your database name."}, 400
        
        except Exception as e:
            print(traceback.format_exc())
            return {"error": "Internal server error"}, 500


class MovieView:
    def __init__(self, mydb):
        self.mydb = mydb

    def viewMovie(self):
        try:
            with self.mydb.connect() as conn:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT * FROM movies")
                    emp_rows = cursor.fetchall()
                    return emp_rows
        except pymysql.MySQLError as e:
            print("Error connecting to database: ", e)
            return {"error": "Error connecting to database"}, 500

    def viewMoviedetails(self, movieid):
        try:
            conn = self.mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT movieid, moviename, moviegenre, director, language FROM movies WHERE movieid =%s", (movieid))
            empRow = cursor.fetchone()
            if not empRow:
                return {"error": "Movie with the id {} not found".format(movieid)}, 404
            return empRow
        except pymysql.MySQLError as e:
            print("Error connecting to database: ", e)
            return {"error": "Error connecting to database"}, 500

class MovieUpdater:
    def __init__(self, mydb):
         self.mydb = mydb
        
    def updateMovie(self, movieid, data):
        try:
            Id = data['movieid']
            Name = data['moviename']
            Genre= data['moviegenre']
            Director = data['director']
            Language = data['language']

            if  Name and Genre and Director and  Language and request.method  == 'PUT':   
                sqlQuery = ("UPDATE movies SET movieName= %s, movieGenre= %s, director= %s, language=%s  WHERE movieId=%s")
                bindData = ( Name, Genre, Director,  Language,Id )
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
