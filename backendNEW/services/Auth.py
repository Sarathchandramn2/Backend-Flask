from functools import wraps
from flask import request,jsonify
import jwt
from app import app


def jwtauth(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        acess_tocken = request.headers.get('Authorization')
        
        acess_tocken = acess_tocken.replace('Bearer ', '')
        # print(acess_tocken)
        if not acess_tocken:
            return jsonify({'message': 'Missing token!'}), 403
        try:
            jwt.decode(acess_tocken, app.config['JWT_SECRET_KEY'], algorithms='HS256')
            print(acess_tocken) 
        except:
            return jsonify({'message': 'Invalid token!'}), 403  
        return func(*args, **kwargs)
    return wrapped
