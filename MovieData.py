#This script uses the RottenTomatoes API to fetch the title, description,, year of release and cast of the movies
#currently in theaters and saves it to the relational Database.

import sqlite3
import requests
import simplejson
import urllib
import urllib2
from bs4 import BeautifulSoup
import time

#connection to the database
conn = sqlite3.connect('moviedb')
cur = conn.cursor()

#this function is responsible for fetching the title, description,, year of release and cast of the movies
#currently in theaters and saving it to the relational Database. Invoking this function will print the
#attributes that are being fetched and execute the SQL queries to store that data in DB.
def inTheaterMovies():
    #this block of code gets the data from the provided url
    apikey = "qtqep7qydngcc7grk4r4hyd9"
    url = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/in_theaters.json?apikey=%s"
    rec = requests.get(url % apikey)
    
    data = rec.content
     
    jsn = simplejson.loads(data)            #decoding JSON
    arr = []                                #initializing a list to store the cast names

    #dropping the tables if already exists and then creating the tables. This way the DB is updated everytime
    #this function is called
    cur.execute('DROP TABLE IF EXISTS theaterMovie ')
    cur.execute('DROP TABLE IF EXISTS castinfo ')
    cur.execute('CREATE TABLE IF NOT EXISTS theaterMovie (name TEXT, description TEXT, year INTEGER, cast TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS castinfo (name TEXT, description TEXT)')

    #fetching the attributes we need
    movies = jsn["movies"]
    for movie in movies:
        print 'Title: ', movie["title"],'\n','Description:\n', movie['synopsis'],'\n','Year: ', movie['year'],'\n'
           
        print 'Cast:'
        for cast in movie['abridged_cast']:
            print cast['name']
            
            article  = cast['name']
            article = urllib.quote(article)
            arr.append(cast['name'])        #appending the case name to the list
            arrs = ', '.join(arr)
            try:
                #performing page scraping to get the first paragraph from wikipedia
                soup = BeautifulSoup(urllib2.urlopen('https://en.wikipedia.org/wiki/' + article).read(), "html.parser")
                para = soup.p               #filtering the first paragraph
                txt = para.get_text()       #extracting the text from html format
                #query to insert the data scraped
                cur.execute('INSERT INTO castinfo (name, description) VALUES ( ?, ?)',(cast['name'], txt))    
                                
            except Exception as x:
                #handling the error if information is not found
                cur.execute('INSERT INTO castinfo (name, description) VALUES ( ?, ?)',(cast['name'], str(x)))
        #query to insert attributes into the theaterMovie table
        cur.execute('INSERT INTO theaterMovie (name, description, year) VALUES ( ?, ?, ? )', ( movie["title"], movie['synopsis'], movie['year']) )
        #query to update cast names as list into the theaterMovie table
        cur.execute('UPDATE theaterMovie SET cast = ? WHERE name=?',(arrs, movie["title"],))
        
        print '\n###############################################################################\n'

    
    print 'Database last updated at ', time.strftime('%H:%M:%S'), 'on ', time.strftime('%m/%d/%y'),'\n'
    

#This function prints the contents saved in the DB
def printDB():
    rowCount = 0
    #comment one of the below queries to get the intended results
    cur.execute('SELECT * FROM theaterMovie')
    #cur.execute('SELECT * FROM castinfo')

    #This loop iterates over the DB rows and print out the values and count of rows
    for eachRow in cur:
        rowCount += 1
        print eachRow,'\n'
    print 'number of rows returned: ', rowCount
    cur.close()                             #closing the connection

inTheaterMovies()
printDB()
