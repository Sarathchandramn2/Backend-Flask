from urllib import response
from models import Rating
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
from services.Logger import *
from services.Auth import *

#add rating for a particular track by particular user, datas are added to table rating
@app.route('/rating', methods = ['POST'])
@jwtauth
def addRating(rateid=None):
    try:
        json = request.json
        userid = json['userid']
        movieid = json['movieid']
        rating = json['rating']
        print(json)
        # //error = validateRating(rating)
        # if error :
        #     return error
        rates = Rating(rateid,userid, movieid, rating)
        if userid and movieid and rating and request.method == 'POST' :
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO rating(userid, movieid, rating) VALUES (%s, %s, %s)"
            bindData = (rates.userid, rates.movieid, rates.rating)
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify('Rating added successfully!')
            response.status_code = 200
            return response
    except KeyError:
        return jsonify('value missing')
    except pymysql.IntegrityError as e:
        return jsonify('You are entering wrong userid or movieid , which is not in table..!!!')
    except Exception as e :
        print(e)
        return jsonify("error")

# @app.route('/rating', methods = ['POST'])
# @jwtauth
# def add_rating(rateid=None):
#     try:
#         json_data = request.json
#         userid = json_data['userid']
#         movieid = json_data['movieid']
#         rating = json_data['rating']
#         print(json_data)

#         # //error = validateRating(rating)
#         # if error :
#         #     return error

#         rates = Rating(rateid, userid, movieid, rating)
#         if userid and movieid and rating and request.method == 'POST':
#             data_access_layer = DataAccessLayer()
#             data_access_layer.add_rating(rates)
#             response = jsonify('Rating added successfully!')
#             response.status_code = 200
#             return response
#     except KeyError:
#         return jsonify('value missing')
#     except pymysql.IntegrityError as e:
#         return jsonify('You are entering wrong userid or movieid , which is not in table..!!!')
#     except Exception as e:
#         print(e)
#         return jsonify("error")

# class DataAccessLayer:
#     def __init__(self):
#         self.conn = mydb.connect()
#         self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

#     def add_rating(self, rates):
#         sql_query = "INSERT INTO rating(userid, movieid, rating) VALUES (%s, %s, %s)"
#         bind_data = (rates.userid, rates.movieid, rates.rating)
#         self.cursor.execute(sql_query, bind_data)
#         self.conn.commit()