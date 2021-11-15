from flask import Flask
from flask import render_template,request,url_for,redirect
from google.cloud import bigquery
import plotly
import plotly.graph_objects as go
import json

app = Flask(__name__)

@app.route('/')
def home():
    message = "Welcome, you are at the home page"
    return render_template('homepage.html', welcome=message)