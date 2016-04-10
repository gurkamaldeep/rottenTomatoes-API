# rottenTomatoes-API
getting attributes of the films currently in theaters and then storing into a relational database (sqlite3) using python.

##########################
######### README #########
##########################

Note: I have provided extensive commenting in the code file. It should not be difficult to read. In case you find it difficult, feel free to contact me at gurkamaldeep@live.com

###########################
####### DESCRIPTION #######
###########################
I wrote this python script to perform the task 3 using rottentomatoes API. I have used the API key provided in the assignment. I have created two functions namely inTheaterMovies() and printDB() respectively.

inTheaterMovies() is responsible for the main part. It uses the API and retrieves the json content and decoding it afterwards via the help of simplejson library.Then I have wrote two queries to drop the tables if they exist. This is done in order to update DB everytime the script is run. After this condition, new tables are created with the DDL provided. I have used sqlite3 as a relational DB to store the data. After that I traverse through the data getting the required attributes and storing them into the database and printing them side by side. Then I performed page scraping to extract the first paragraph of the actor's page on wikipedia. The logic I used behind this was to check for the '<p>' tag in the page and extracting that part only. I used BeautifulSoup library to achieve this and then storing into the DB. Entries not found on wikipedia are stored with the error 404 which means page not found. At the time I build this, it was returning 5 such errors and were handled by exception handling.

printDB() is used only when you want to see the results stored in the database to verify.

In conclusion, this app can be run on any machine and there are no dependencies required except for the python libraries used (you can install all the libraries with the help of pip). There is no need to specify any DB because wherever this app will be run, it will generate the DB file in that folder. 
