import os
import plotly
import plotly.graph_objects as go
import pandas as pd
import json
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


from plot import plot_popularname, popular_names, plot_sentiment, wordcloud_generator
from dotenv import load_dotenv
# from flask import Flask
# from flask import render_template,request,url_for,redirect
from dash import Dash
import plotly.express as px


load_dotenv()

# read in data 
file = f"s3://we-rate-dogs-data/processed-data/master.csv"
twitter_archive = pd.read_csv(file)


app = Dash(__name__)


app.layout = html.Div([
    html.Center([
        dbc.Row([
        dbc.Col(html.H1('We Rate Dogs Dashboard')),
        dbc.Col(html.H3('Analysis'))])]),
    dcc.Tabs([
        dcc.Tab(label='Popular Graph', children=[
            dcc.Graph(
                figure=plot_popularname(twitter_archive)
            )
        ]),
        dcc.Tab(label='Sentiment Plot', children=[
            dcc.Graph(
                figure=plot_sentiment(twitter_archive)
            )
        ]),
        dcc.Tab(label='Popular Names', children=[
            dcc.Graph(
                figure=popular_names(twitter_archive)
            )
        ]),
        dcc.Tab(label='Word Clouds', children=[
            dcc.Graph(
                figure=wordcloud_generator(twitter_archive)
            )
        ])
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
    
