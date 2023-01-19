from urllib import response
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
def create_project():
    try:
        json = request.json
        
        project_id= json['project_id']
        emp_id = json['emp_id']
        project_name = json['project_name']
      
        
        if project_id and emp_id and project_name and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO projects(project_id,emp_id, project_name) VALUES(%s, %s, %s)"
            bindData = (project_id,emp_id  , project_name)
            cursor.execute(sqlQuery, bindData)
           
            conn.commit()
            respone = jsonify('project added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:

        print(e)

        # print(type(e))

        return e.__str__()


    finally:
        cursor.close()
        conn.close()

@app.route('/getprojects', methods =['GET'])
def getpro():
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor) 
        cursor.execute("SELECT * FROM projects;")
        proRows = cursor.fetchall()
        respone = jsonify(proRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/getproject/<project_id>', methods=['GET'])
def project_details(project_id):
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT project_id , emp_id, project_name FROM projects WHERE project_id =%s", (project_id))
        proRow = cursor.fetchone()
        respone = jsonify(proRow)
        return respone
        # respone.status_code = 200
        
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/update/<project_id>', methods=['PUT'])
def update_pro(project_id):
    try:
        print("_json")
        _json = request.json
        
        _project_id = _json['project_id']
        _emp_id = _json['emp_id']
        _project_name= _json['project_name']
      
        if _emp_id and _project_name and _project_id and request.method == 'PUT':
                        
            sqlQuery = ("UPDATE projects SET emp_id= %s, project_name=%s WHERE project_id=%s")
            bindData = (_emp_id,_project_name,_project_id)
            conn = mydb.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery,bindData)
            
            conn.commit()
            respone = jsonify('Project updated successfully!')
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


@app.route('/delete/<project_id>', methods=['DELETE'])
def delete_pro(project_id):
    try:
        conn = mydb.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE project_id =%s", (project_id))
        conn.commit()
        respone = jsonify('Project deleted successfully!')
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
