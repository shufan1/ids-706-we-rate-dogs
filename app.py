import os
import plotly
import plotly.graph_objects as go
import pandas as pd
import json
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from plot import plot_popularname
from dotenv import load_dotenv
from flask import Flask
from flask import render_template,request,url_for,redirect
from dash import Dash
import plotly.express as px


load_dotenv()

# read in data 
bucket = os.getenv('AWS_S3_BUCKET')
file = f"s3://{bucket}/processed-data/master.csv"
twitter_archive = pd.read_csv(file)


app = Dash(__name__)

app.layout = html.Div(children=[
        html.H1(children='We Rate Dogs Analysis'),
        dcc.Graph(
            id='poplar-name',
            figure=plot_popularname(twitter_archive)
        )
    ])
    
if __name__ == '__main__':
    app.run_server(debug=True)
    