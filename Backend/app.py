import os
from flask import Flask, render_template

from flask_cors import CORS, cross_origin

app = Flask(__name__)


app.secret_key=os.urandom(24)

CORS(app)
