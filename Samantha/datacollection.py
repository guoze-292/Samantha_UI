# TOTAL RUN TIME ON STANDARD LAPTOP: APPROX. 30 MINS

# Import necessary modules
import requests
from bs4 import BeautifulSoup
import re
import json
import os

# Grab stopwords from a stopword file
stopwords = set([stopword.strip('\n') for stopword in open('stopwords.csv')])

# Input: text of a review
# Output: alphabetic text without stopwords
def clean(review):
    words = (re.sub('[^a-zA-Z]', " ", review)).split()
    return " ".join([word for word in words if not word in stopwords])

def find_exist(filename):
    files = [f for f in os.listdir('movies_data') if os.path.isfile(os.path.join('movies_data', f))]
    for f in files:
        if(f==filename):
            return True
    return False


def collectPic(url):
    home_page = requests.get(url)
    soup = BeautifulSoup(home_page.content,'lxml')
    img_info = soup.find_all('img',{'class':'posterImage'})
    return (img_info[0]['alt'],img_info[0]['src'])

# Input: url of movie reviews on Rotten Tomatoes, filename to write out to
def collectData(moviename):
    if find_exist(moviename+".json"):
        print ("file existed")
    else:
        #format the names of the movies for url usage
        moviename = moviename.replace(" ","_")
        url = "https://www.rottentomatoes.com/m/"+moviename+"/reviews/?type=user"
        # get requests from the webpage
        page = requests.get(url)
        # soup contains html data from the page
        soup = BeautifulSoup(page.content, "lxml")
        # find the main_container div
        maindiv = soup.find(id="main_container")
        outD = {}
        # Loop through 50 pages since there are about 20 reviews per page
        for i in range(50):
            # url of pages after page 1 need to be updated with page=i
            if i != 0:
                updatedurl = url.split('?')[0] + "?page=" + str(i + 1) + "&" + url.split('?')[1] + "&sort="
                page = requests.get(updatedurl)
                soup = BeautifulSoup(page.content, "lxml")
                maindiv = soup.find(id="main_container")
            # Grab all reviews, strip out strange unicode characters
            reviews = maindiv.find_all('div', class_="user_review")
            textReviews = [clean(r.get_text().encode('ascii', 'ignore').decode('utf-8')) for r in reviews]

            # Grab all ratings
            ratings = maindiv.find_all('span', class_='fl')

            starReviews = []
            star = 0.0

            # Look through glyphicon stars and count the number of them
            # If there is text with 1/2, add 0.5 to the count of stars
            for rating in ratings:
                star = 0.0
                if not rating.get_text().isspace():
                    star += 0.5
                stars = rating.find_all('span', class_="glyphicon glyphicon-star")
                star += len(stars)
                starReviews.append(star)

            # Add the new review: rating into the outD dictionary
            outD.update(dict(zip(textReviews, starReviews)))

        # Once the loop is finished, write the dictionary out to a json file
        with open(os.path.join("movies_data", moviename+".json"), 'w') as fp:
            json.dump(outD, fp, indent=2)


collectPic("https://www.rottentomatoes.com/m/call_me_by_your_name")
# Call collectData function on all 10 movies and write results out to json files
# collectData("star_wars_episode_vii_the_force_awakens")
# collectData("about_time")
# collectData("toy_story")
# collectData("taken")
# collectData("cloud atlas 2012")
# collectData("1193743-step_brothers")# collectData('https://www.rottentomatoes.com/m/1193743-step_brothers/reviews/?type=user', 'stepbrothers.json')
# collectData('saw')
# collectData('saw_ii')
# collectData('titanic')
# collectData('pirates_of_the_caribbean_the_curse_of_the_black_pearl')
