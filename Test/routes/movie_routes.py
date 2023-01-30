from flask import request, jsonify
from models.movies import Movies
from models.movies import MovieView,MovieUpdater,Movie
from app import app
from config import mydb
from flask import Blueprint


#Inserting the data
@app.route('/movies', methods=['POST'])
def addMovie():
    try:
        json = request.json
        Name= json['moviename']
        Genre = json['moviegenre'] 
        director = json['director']
        language = json['language']

        if Name and Genre and director and language  and request.method =='POST':
            movie = Movies(Name, Genre, director, language)
            return movie.addTodb()
        else:
            return Exception
    except Exception as e:
        print(e)
        return 'Exception'


#For viewing the data
movie_view = MovieView(mydb)

@app.route('/movies', methods =['GET'])
def viewMovie():
    return movie_view.viewMovie()

#For Viewing particular data from table
movie_details_view = MovieView(mydb)

@app.route('/movies/<movieId>', methods=['GET'])
def viewMoviedetails(movieId):
    return movie_details_view.viewMoviedetails(movieId)

#updating the datas in table 
movie_updater = MovieUpdater(mydb)

@app.route('/movies/<movieId>', methods=['PUT'])
def updateMovie(movieId):
    data = request.json
    return movie_updater.updateMovie(movieId, data)

#Deleting the datas form table
movie = Movie(mydb)

@app.route('/movies/<movieId>', methods=['DELETE'])
def delete(movieId):
    return movie.delete(movieId)
    

