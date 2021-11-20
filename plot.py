import os
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
#from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import re
import nltk
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sia = SentimentIntensityAnalyzer()

def clean_data(twitter_archive):
    # create conditions to seperate them into buckets 
    conditions = [
        (twitter_archive ['rating_numerator'] <= 4),
        (twitter_archive ['rating_numerator'] > 4) & (twitter_archive ['rating_numerator'] <= 6 ),
        (twitter_archive ['rating_numerator'] > 6) & (twitter_archive ['rating_numerator'] <= 10),
        (twitter_archive ['rating_numerator'] > 10)
        ]
    
    # create a list of the values we want to assign for each condition
    values = ['not_so_cute', 'okay', 'cute', 'cuteness_overflow']
    # create a new column with the condition 
    twitter_archive['rating_bucket'] = np.select(conditions, values)
    # twitter_archive.loc[twitter_archive['rating_bucket'] =='cutene', 'text']
    # bucket_data = dict.fromkeys(['not_so_cute', 'okay', 'cute', 'cuteness_overflow'], list())
    return twitter_archive


def top_value_count(x, n=5):
    return x.value_counts().head(n)

def plot_popularname(twitter_archive):
    twitter_archive = clean_data(twitter_archive)
    twitter_archive_copy = twitter_archive[(twitter_archive['name']!="None")&(twitter_archive['name']!="a")
                                          &(twitter_archive['name']!="an")&(twitter_archive['name']!="the")]
    group_by_rating =twitter_archive_copy.groupby("rating_bucket").name
    top_names_by_rating =group_by_rating.apply(top_value_count).reset_index()
    top_names_by_rating=top_names_by_rating.rename(columns=dict(level_1='name', name='count'))
    
    
    rating_levels = ['cuteness_overflow', 'okay', 'cute', 'not_so_cute']
    
    fig = make_subplots(rows=1, cols=4,subplot_titles=rating_levels)
    
    for i in range(len(rating_levels)):
        df = top_names_by_rating[top_names_by_rating['rating_bucket']==rating_levels[i]]
        fig.add_trace(go.Histogram(x=np.repeat(df['name'],df['count']),name=rating_levels[i]),row=1, col=i+1)
    fig.update_layout(title_text="Most frequent names by rating")
    
    return fig
    


    
    
def word_processing(tag) : 
    b = twitter_archive.loc[twitter_archive['rating_bucket'] ==tag, 'text'].tolist()
    b1 = ' '.join(b)
    b1 = re.sub(r"https://\S+","",b1)
    b1 = re.sub(r"\d+/\d+","",b1)
    b1 = re.sub(r"RT",'',b1)
    b1 = re.sub(r"^[@#]\S+",'', b1) # removing hashtag and at 
    wordcloud2 = WordCloud().generate(b1)
    return wordcloud2 

def word_cloud(rate):
    plt.imshow(word_processing(rate), interpolation='bilinear')
    plt.axis("off")
    plt.show()

    
    
if __name__=="__main__":
        # read in data 
    
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
    file = "s3://we-rate-dogs-data/processed-data/master.csv"
    twitter_archive = pd.read_csv(file)

    fig = plot_popularname(twitter_archive)
    fig.show()
    