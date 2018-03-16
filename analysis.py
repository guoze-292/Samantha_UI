import json
import numpy as np
import pandas as pd
import collections
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

##return file as json variable for training purpose
def getjsons(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)
##convert the rating into sentiment
def getsentiment(df):
    sentiments = []
    for val in df['Rating']:
        if float(val) >= 3.0:
            sentiments.append("Positive")
        else:
            sentiments.append("Negative")
    return np.array(sentiments)

##create dataframe to training purpose
def createdf(dictionary):
    df = pd.DataFrame(dictionary.items(), columns = ['Review', 'Rating'], dtype=None)
    df['Sentiment'] = getsentiment(df)
    return df

##naive_bayes algorithm implementation, this funciton has been revised for web application
def naive_bayes(train, test):
    # Map positive as 1, negative as 0 for training and testing data
    train['Label_num'] = train.Sentiment.map({'Positive':1, 'Negative':0})

    # X (train and test) will be the review, y will be positive or negative
    X_train = train.Review
    y_train = train.Label_num
    X_test = test.Review

    # Initialize a CountVectorizer
    vector = CountVectorizer()
    # Create document-term matrices (note: astype('U') deals with strange unicode characters)
    X_train_dtm = vector.fit_transform(X_train.values.astype('U'))
    X_test_dtm = vector.transform(X_test.values.astype('U'))

    # Initialize a MultinomialNB object
    nb = MultinomialNB()
    # Fit the data
    nb.fit(X_train_dtm, y_train)
    # Predict values with X testing data
    y_pred_class = nb.predict(X_test_dtm)

    # Grab accuracy score and return
    return (np.sum(y_pred_class)/float(len(y_pred_class)))

##logistic regression algorithm implementation, this funciton has been revised for web application
def log_reg_app(train, test):
    # Map positive to 1, negative to 0 for training and testing data
    train['Label_num'] = train.Sentiment.map({'Positive':1, 'Negative':0})
    test['Label_num'] = test.Sentiment.map({'Positive':1, 'Negative':0})

    # X (train and test) is the review, y is the positive or negative sentiment
    X_train = train.Review
    y_train = train.Label_num
    X_test = test.Review
    y_test = test.Label_num

    # Initailize CountVectorizer object and create document-term matrices (note: astype('U') handles strange unicode characters)
    vector = CountVectorizer()
    X_train_dtm = vector.fit_transform(X_train.values.astype('U'))
    X_test_dtm = vector.transform(X_test.values.astype('U'))

    # Initialize LogisticRegression object and fit the data
    logistic = LogisticRegression()
    logistic.fit(X_train_dtm, y_train)

    # Obtain predicted result and return the accuracy score
    y_predicted_class = logistic.predict(X_test_dtm)
    return (np.sum(y_predicted_class)/float(len(y_predicted_class)))

##use existed file to train our model
def train_data():
    starwars = getjsons("movies_data/star_wars_episode_vii_the_force_awakens.json")
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
    dataframes = [starwars, abouttime, taken, toystory, cloudatlas, stepbrothers, saw, saw2, titanic, piratesofthecaribbean]
    train1 = pd.concat(dataframes[0:8])
    return train1;

##predict movie score using Naive Bayes functino and Logistic Regression function 
def analyze_movie(train1,movie):
    return (naive_bayes(train1,movie),log_reg_app(train1,movie))
