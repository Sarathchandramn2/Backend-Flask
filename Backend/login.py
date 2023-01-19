import uuid
import pymysql
from cmath import log
from dataclasses import dataclass
from flask import Flask,session,render_template,request,redirect,g,url_for
from app import app
from config import mydb


import os

@app.route('/login',methods=['POST'])
def index():
    print(request.json['username'])
    print(request.json['password'])
    user=request.json['username']
    pas=request.json['password']
    loginDetails=request.json
    if loginDetails['username'] and loginDetails['password'] and  request.method == 'POST':
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
    
        sqlQuery = "SELECT yourname FROM user WHERE username= '%s'  and password='%s'" % (user, pas)
        data=cursor.execute(sqlQuery)
        
        print(data)
        if data==1:
            session['user']=loginDetails['username']
            sessionid = str(uuid.uuid4())
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery="INSERT INTO session VALUES (%s)"
            bindData = (sessionid)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            print(sessionid)
            return "user authenticated"
        else:
           return "access denied"
    
    

       






    # if(loginDetails['username']=="Ganga" and loginDetails['password']=="password"):
    #     session['user']=loginDetails['username']
    #     return "user authenticated"
    # return "access denied"


# @app.route('/home')
# def home():
#     if g.user:
#         return render_template('project.html',user=session['user'])
#     return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None


    if 'user' in session:
        g.user = session['user']

@app.route('/dropsession')
def dropsession():
    session.pop('user',None)
    return render_template('login.html')

if __name__ == "__main__":
    app.run()
