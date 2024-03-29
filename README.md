# Covid 19 Dashboard

# Summary of the program

The covid dashboard is designed to show news articles as well as current covid data in the location
entered in the cofiguration file. 

The program allows the news articles and covid data to be updated by scheduling updates.

# Prerequisites

A version of Python 3.9 or above is required

Lates versions of these python packages needs to be installed:

-uk-covid19
-flask
-pytest

# Getting Started

Firstly run user_interface.py

Then go to http://127.0.0.1:5000/ on your browser (this is a server hosted by you computer)

After that you should be greated with a dashboard displaying news articles and covid data
The covid data is current and accessed from the uk-covid19 API fromo the government
The news articles are the top news articles for the search terms in the config file

How to schedule an update:

-By pressing on the clock icon you can select the time you want your update to happen
-You can press on the 'Update label' text box and type the name of your update (this field is required)
-The 'Repeat update' checkbox is optional and allows your update to keep on repeating if ticked
-The 'Update covid data' checkbox is optional and will make the covid data update if ticked
-The 'Update news articles' checkbox is optional and will make the news articles update to new once if ticked
-By pressing submit your update will schedule and execute at the time specified

You can have as many updates as you want scheduled

# Configuration

You can change the information on your covid dashboard by going inside of the config.json file
and changing the settings. Keep in mind some of the nations might not work with as the API
might not have information on them. You will need to go into the file and enter your own API key.

# Testing

Running pytest on the program with the provided tests is the easiest way to ensure that the program is functioning.
Pytest is run by typing 'python -m pytest' into the command line. For the tests to work you need to be in the directory
'dashboard'.

# Details

Developed by Dimitar Sivrev

MIT License (LICENSE FILE)