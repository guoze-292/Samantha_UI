from flask import Flask, request, redirect, url_for, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import re
import json
import os
import datacollection as dc
import numpy as np
import pandas as pd
import collections
import ulti as ut
import analysis as ay

app = Flask(__name__)

@app.before_first_request
def activate_model():
    #train the model when server starts
    train_model = ay.train_data()

@app.route("/",methods=['GET','POST'])
def index():
    #return static home pages
    if request.method == 'GET':
        return render_template('index.html')
    #return 'POST' request
    if request.method == 'POST':
        movie_url = request.form['url']
        movie_data = dc.collectPic(movie_url)
        movie_result = {'title':movie_data[0],'imgurl':movie_data[1],'words':[],'scores':()}
        movie_name = movie_url.replace("https://www.rottentomatoes.com/m/","")

        print "successfully collect title and pic"
        print "parsing reviews online, this may take a bit time.... "
        if(dc.collectData(movie_name)):
            # "file collected"
            json_file = ut.getjsons("movies_data/"+movie_name+".json")
            # "creating dataframe"
            df_file = ut.createdf(json_file)
            # "finding most common words"
            words = ut.mostcommon(df_file)
            for x,y in words.iteritems():
                movie_result['words'].append({"text":x,"weight":y})
            movie_score = ay.analyze_movie(train_model,df_file)
            movie_result['scores'] = movie_score
            print "result ready"
        return jsonify(movie_result)
