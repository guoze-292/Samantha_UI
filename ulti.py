import json
import numpy as np
import pandas as pd
import collections
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

def getjsons(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)

def createdf(dictionary):
    df = pd.DataFrame(dictionary.items(), columns = ['Review', 'Rating'], dtype=None)
    df['Sentiment'] = getsentiment(df)
    return df

def getsentiment(df):
    sentiments = []
    for val in df['Rating']:
        if float(val) >= 3.0:
            sentiments.append("Positive")
        else:
            sentiments.append("Negative")
    return np.array(sentiments)

def mostcommon(df):
    # Initialize empty counts array (will contain dictionary of counts to their words)
    counts = []
    result = {}
    # Initialize a CountVectorizer
    vector = CountVectorizer()
    # Create a DataFrame containing words and their counts
    words = df['Review']
    dtm = vector.fit(words.values.astype('U'))
    names = dtm.get_feature_names()
    dtm = vector.fit_transform(words.values.astype('U'))
    dtm_dense = dtm.todense()
    df = pd.DataFrame(dtm_dense, columns=names)
    for col in df:
        counts.append((df[col].sum(), col))
    # Sort the dictionary by count and print out word correlated to count in top 20 counts
    for i in sorted(counts)[-20:]:
        result[i[1]]=i[0]
    return result
