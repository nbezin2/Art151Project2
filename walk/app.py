from flask import Flask, render_template

app = Flask(__name__)

# Dependencies
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import random

# random number based on the current system clock
random.seed(datetime.now()) 

page1 = requests.get("https://en.wikipedia.org/wiki/Portal:Video_games")
page2 = requests.get("https://en.wikipedia.org/wiki/Portal:Film")
page3 = requests.get("https://en.wikipedia.org/wiki/Portal:Music")

def scrape(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    
    pageLinks = soup.find(id="bodyContent").find_all("a")
    random.shuffle(pageLinks)
    scrapedLink = 0
    
    for i in pageLinks:
        if i['href'].find("/wiki/") != -1:
            scrapedLink = i
            break
    
    newPage = requests.get("https://en.wikipedia.org" + scrapedLink['href'])
    scrapedSoup = BeautifulSoup(newPage.content, 'html.parser')
    title = scrapedSoup.find(id="firstHeading")
    paras = scrapedSoup.find(id="bodyContent").find_all("p")
    random.shuffle(paras)
    para = 0
    
    for i in paras:
        if len(i.text) > 100:
            para = i
            break
            
    return newPage, title.text, para.text

@app.route('/')

def index():
    
    return render_template("index.html")




#set route for user navigation
@app.route('/videogames')

#define app function
def videogames():
    
    nPage, title, text = scrape(page1)
    return render_template("videogames.html", text=text, title=title)




#set route for user navigation
@app.route('/films')

#define app function
def films():

    nPage, title, text = scrape(page2)
    return render_template("films.html", text=text, title=title)


#set route for user navigation
@app.route('/music')

#define app function
def music():

    nPage, title, text = scrape(page3)
    return render_template("music.html", text=text, title=title)
