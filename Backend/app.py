import os
from flask import Flask, render_template

from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.secret_key = 'e5b8a5579ec140809c4df31f48c1d4f3'
CORS(app)
