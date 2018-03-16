import requests
from bs4 import BeautifulSoup
import re
import json
import numpy as np
import pandas as pd
import collections
from sklearn.feature_extraction.text import CountVectorizer

def getjsons(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)

def getsentiment(df):
    sentiments = []
    for val in df['Rating']:
        if float(val) >= 3.0:
            sentiments.append("Positive")
        else:
            sentiments.append("Negative")
    return np.array(sentiments)

def createdf(dictionary):
    df = pd.DataFrame(dictionary.items(), columns = ['Review', 'Rating'], dtype=None)
    df['Sentiment'] = getsentiment(df)
    return df

def mostcommon(df, name):
    counts = []
    vector = CountVectorizer()
    words = df['Review']
    dtm = vector.fit(words.values.astype('U'))
    names = dtm.get_feature_names()
    dtm = vector.fit_transform(words.values.astype('U'))
    dtm_dense = dtm.todense()
    df = pd.DataFrame(dtm_dense, columns=names)
    for col in df:
        counts.append((df[col].sum(), col))
    print "\nTop 20 words to describe", name
    for i in sorted(counts)[-20:]:
        print i[1], ":", i[0]

starwars = getjsons("movies_data/starwars.json")
abouttime = getjsons("movies_data/abouttime.json")
taken = getjsons("movies_data/taken.json")
toystory = getjsons("movies_data/toystory.json")
cloudatlas = getjsons("movies_data/cloudatlas.json")
stepbrothers = getjsons("movies_data/stepbrothers.json")
saw = getjsons("movies_data/saw.json")
saw2 = getjsons("movies_data/saw2.json")
titanic = getjsons("movies_data/titanic.json")
piratesofthecaribbean = getjsons("movies_data/piratesofthecaribbean.json")

starwars = createdf(starwars)
abouttime = createdf(abouttime)
taken = createdf(taken)
toystory = createdf(toystory)
cloudatlas = createdf(cloudatlas)
stepbrothers = createdf(stepbrothers)
saw = createdf(saw)
saw2 = createdf(saw2)
titanic = createdf(titanic)
piratesofthecaribbean = createdf(piratesofthecaribbean)

mostcommon(starwars, "Star Wars")
mostcommon(abouttime, "About Time")
mostcommon(taken, "Taken")
mostcommon(toystory, "Toy Story")
mostcommon(cloudatlas, "Cloud Atlas")
mostcommon(stepbrothers, "Stepbrothers")
mostcommon(saw, "Saw")
mostcommon(saw2, "Saw 2")
mostcommon(titanic, "Titanic")
mostcommon(piratesofthecaribbean, "Pirates of the Caribbean")

dataframes = [starwars, abouttime, taken, toystory, cloudatlas, stepbrothers, saw, saw2, titanic, piratesofthecaribbean]
t2 = [starwars, abouttime, taken, toystory, cloudatlas, stepbrothers, titanic, piratesofthecaribbean]
t3 = [starwars, abouttime, taken, toystory, saw, saw2, titanic, piratesofthecaribbean]
t4 = [starwars, abouttime, cloudatlas, stepbrothers, saw, saw2, titanic, piratesofthecaribbean]


train1 = pd.concat(dataframes[0:8])
test1 = pd.concat(dataframes[8:10])
train2 = pd.concat(t2)
test2 = pd.concat(dataframes[6:8])
train3 = pd.concat(t3)
test3 = pd.concat(dataframes[4:6])
train4 = pd.concat(t4)
test4 = pd.concat(dataframes[2:4])
train5 = pd.concat(dataframes[2:10])
test5 = pd.concat(dataframes[0:2])

train1.to_csv("csv_files/train1.csv")
test1.to_csv("csv_files/test1.csv")
train2.to_csv("csv_files/train2.csv")
test2.to_csv("csv_files/test2.csv")
train3.to_csv("csv_files/train3.csv")
test3.to_csv("csv_files/test3.csv")
train4.to_csv("csv_files/train4.csv")
test4.to_csv("csv_files/test4.csv")
train5.to_csv("csv_files/train5.csv")
test5.to_csv("csv_files/test5.csv")
