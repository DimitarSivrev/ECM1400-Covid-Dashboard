'''
This module performs:
    -extracting news articles from an API
    -updates the news displayed on the dashboard
    -scheduling updates for the news
'''
#Importing python modules that will be used in the program
import json
import logging
import os
import requests
from datetime import datetime, timedelta
from covid_data_handler import delete_update, update
from covid_data_handler import events
from covid_data_handler import delete_update
from covid_data_handler import s

#This is the format the logs will be displayed in the log-file
FORMAT = '%(levelname)s: %(asctime)s %(message)s'

#Configures the logging used through out the program
logging.basicConfig(filename='log-file.log' ,level=logging.DEBUG, format=FORMAT)

#Find the file path to this directory
file_dir = os.path.dirname(os.path.realpath(__file__))

#Opens the configuration file using file path
with open(file_dir + "\\config.json","r") as f:
    json_file = json.load(f)

#Assigns a variable to the apropriate config section for this program
news_api = json_file["News-API"]

#Creates a list called news that will be used to store and display the news storries
news = []

def news_API_request (covid_terms= news_api["covid_terms"] ):
    '''
    This function uses an API to retrieve news articles with the relevant terms
    currently these terms are accesssed from the config file
    :param covid_terms: string with key words
    :return: the news articles exracted from the API
    '''

    #Using try and except to seek out any errors when processing the file
    try:
        #Accesses the terms from the config file and creates a url that will
        #be used to retrieve the news articles
        api_key = news_api["api_key"]
        base_url = news_api["base_url"]
        complete_url = base_url + "apiKey=" + api_key + "&q=" + covid_terms

        #Uses request to get a dictionary with the news from the url
        news_dict = requests.get(complete_url).json()
        articles = news_dict["articles"]
    except:
        logging.critical("couldn't get news from link")
    else:

        #Adds the news articles to the news list
        global news
        for article in articles:
            news.append(
                {
                    'title': article['title'],
                    'content': article['content']
                }
            )
        logging.info("The news articles were extracted from the API")
        return(news)

#Updates the news by clreaing the news list and running the news API function
#CDoesn't display news articles that the user has manually removed
#by comparing the items to the removed items list
def update_news(removed_news_list):
    try:
        news.clear()
        news_API_request()
        for x in removed_news_list:
            for i in news:
                if i == x:
                    news.remove(i)
    except:
        logging.critical("failed to update the news")
    else:
        logging.info("The news has been updated")

def schedule_news_updates(update_interval,update_name, type = 'non-repeating'):
    '''
    Schedules news updates so the covid data in the dashboard updates

    :param update_interval: the time in which the update should happen
    :param update_name: the name of the update
    :param type: repeating or non-repeating update, deafult is non-repeating
    '''
    #Using try and except to seek out any errors when processing the file
    try:
        #Calculates the time the update will happen so it can be displayed
        actual_time = str(datetime.now() + timedelta(seconds = update_interval))

        #Allows the update to be displayed in the index
        update.append({
            'title' : update_name,
            'content' : actual_time[11:19]
            })

        #Schedules an event and passes through the news that have been removed
        global removed_news_list
        event_name = (s.enter(int(update_interval),
        1,
        update_news,
        kwargs=({'removed_news_list':removed_news_list})))

        #Adds the event to the event list
        events.append(event_name)

        #Checks what type the update entered is
        if type == 'non-repeating':
            #schedules the update to be removed from the list after it has ran
            s.enter(update_interval,2,delete_update,kwargs={'name': str(update_name)})

        if type == 'repeating':
            #The repeating update means it runs every 24 hours
            #86400 sec = 24 hours
            #The function calls itself every 24 hours to shedule an update
            event_name= s.enter(60, 
            1,
            schedule_news_updates,
            kwargs={'update_interval' : 60,
            'update_name': str(update_name),
            'type' : 'repeating'})
            events.append(event_name)
            s.enter(60,2,delete_update,kwargs={'name': str(update_name)})
    except TypeError:
        logging.critical("Can't schedule news update")
    else:
        logging.info("The news update has been scheduled")

#Used to track the news removed by the user
removed_news_list = []

#Adds the removed article to the list
def removed_news_function(article):
    global removed_news_list
    removed_news_list.append(article)
