import bcrypt
from models import User
import jwt
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
from services.services import execute,closeConnection,commitConnection
from validation import validateRegisterData,validateLoginData
# registration of user, here datas are entered to user table
@app.route('/register', methods=['POST'])
def register(userid=None):
    try:
        json = request.json
        name = json['fullname']
        user = json['username']
        password = json['password']
        usertype = "3"
        validation_error =validateRegisterData(name,user,password)
        if validation_error:
            return validation_error
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User (userid, name, user, password, usertype)
        if name and user and password and usertype and request.method == 'POST' :
            query = "SELECT fullname FROM user WHERE username= %s"
            bindData = user.username
            data = execute(query, bindData)
            #data will return 1 when it excute sucessfully and return 0 when no data found
            if(data == 1):
                # conn.commit()
                commitConnection()
                return jsonify('User already exist !!')
            elif (data == 0):
                sqlQuery = "INSERT INTO user(fullname, username, password, usertype) VALUES( %s, %s, %s, %s)"
                bindData = (user.fullname, user.username, user.password, user.usertype)
                execute(sqlQuery, bindData)
                # conn.commit()
                commitConnection()
                respone = jsonify('User added successfully!')
                respone.status_code = 200
                return respone
        else:
            return jsonify("something went wrong")
    except KeyError:
        return jsonify(' Some Columns are missing or Mispelled the Column name')
    except Exception as e :
        print(e)
        return ("error")

# login function of user
@app.route('/login', methods = ['POST'])
def login(userid=None, fullname=None, usertype=None):
    try: 
        json = request.json
        name = json['username']
        password = json['password']
        validation_error = validateLoginData( name, password)
        if validation_error:
            return validation_error
        user = User (userid, fullname, name, password, usertype)
        if name and password and request.method == 'POST' :
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT * FROM user WHERE username= %s"
            bindData = user.username
            data = cursor.execute(query, bindData)
            if(data == 1):
                row = cursor.fetchone()
                password = row.get('password')
                usertype = row.get('usertype')
                if ( bcrypt.checkpw(user.password.encode('utf-8'),password.encode('utf-8'))):
                    access_token = jwt.encode({'username': name}, app.config['JWT_SECRET_KEY'])
                    conn.commit()
                    return jsonify(message='Login Successful', access_token=access_token ,usertype=usertype),200
                else:
                    conn.commit()
                    return jsonify('Password is incorrect, Try with the correct one..!!')
            else:
                conn.commit()
                return jsonify('Bad email or Password... Access Denied!'), 401
    except KeyError:
        return jsonify(' Some Columns are missing or Mispelled the Column name')
    except Exception as e :
        print(e)
        return jsonify("error")



    