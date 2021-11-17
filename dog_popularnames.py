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
# read in data 
twitter_archive = pd.read_csv('twitter-archive-enhanced.csv')

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
twitter_archive.head()

# check the bucket sizes
twitter_archive.rating_bucket.value_counts()

# twitter_archive.loc[twitter_archive['rating_bucket'] =='cutene', 'text']
bucket_data = dict.fromkeys(['not_so_cute', 'okay', 'cute', 'cuteness_overflow'], list())
bucket_data

np.sum(twitter_archive["name"]=="None")

def top_value_count(x, n=5):
    return x.value_counts().head(n)

twitter_archive_copy = twitter_archive[(twitter_archive['name']!="None")&(twitter_archive['name']!="a")
                                      &(twitter_archive['name']!="an")&(twitter_archive['name']!="the")]
group_by_rating =twitter_archive_copy.groupby("rating_bucket").name
top_names_by_rating =group_by_rating.apply(top_value_count).reset_index()
top_names_by_rating=top_names_by_rating.rename(columns=dict(level_1='name', name='count'))
top_names_by_rating

rating_levels = ['cuteness_overflow', 'okay', 'cute', 'not_so_cute']

fig = make_subplots(rows=1, cols=4,subplot_titles=rating_levels)

for i in range(len(rating_level)):
    df = top_names_by_rating[top_names_by_rating['rating_bucket']==rating_level[i]]
    fig.add_trace(go.Histogram(x=np.repeat(df['name'],df['count'])),row=1, col=i+1)


fig.update_layout(title_text="Most frequent names by rating")
fig.show()

