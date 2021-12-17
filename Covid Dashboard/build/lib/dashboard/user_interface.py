'''
This module performs:
    -Mapps the index with functionality
    -Allows the user to schedule updates
    -Allows the user to cancel updates
    -Allows thhe user to remove news articles
'''

#Importing python modules that will be used in the program
import logging
from flask import Flask,request, render_template
from covid_data_handler import *
from covid_news_handling import *

app = Flask(__name__)

#This is the format the logs will be displayed in the log-file
FORMAT = '%(levelname)s: %(asctime)s %(message)s'

#Configures the logging used through out the programs
logging.basicConfig(filename='log-file.log' ,level=logging.DEBUG, format=FORMAT)

#Find the file path to this directory
file_dir = os.path.dirname(os.path.realpath(__file__))

#Opens the configuration file using file path
with open(file_dir + "\\config.json","r") as f:
    json_file = json.load(f)

#Assigns a variable to the apropriate config section for this program
interface = json_file["Interface"]

#Function used to map the index with functionallity
@app.route("/")
@app.route("/index")
def index():
    '''
    Checks to see if the user has performed any actions such as:
    submiting an update, removing an update, removing a news story

    :return: The rendered template with embedded data
    '''

    #Checks to see if the user has submited an update
    #text_field would be the name of that update
    text_field = request.args.get('two')

    #Checks to see if the user has removed a news article
    #remove_news would be the title of that article
    remove_news = request.args.get('notif')

    #Checks to see if the user has removed an update
    #remove_update would be the name of that update
    remove_update = request.args.get('update_item')

    #If the user submits an update    
    if text_field:
        logging.info("User has submited an update")

        #The time the user has set for the update
        update_time = request.args.get('update')

        #Whever the user has set the update to repeat
        repeat = request.args.get('repeat')

        #If the user wants to update the covid data
        covid_data = request.args.get('covid-data')

        #If the user wants to update the news articles
        news_update = request.args.get('news')

        #Calculates the seconds left until the time given
        future_time = second_calculator(str(update_time))

        #If the user wants to update the covid data
        if covid_data:
            #If the user wants that covid update to repeat or not
            if repeat:
                schedule_covid_updates(future_time,(text_field+" (repeating update) (covid)"),type = "repeating")
                logging.info("The user has scheduled a repeating covid update")
            else:
                schedule_covid_updates(future_time,(text_field+" (covid)"))
                logging.info("The user has scheduled a non-repeating covid update")

        #If the user want to update the news articles
        if news_update:
            #If the user wants that news update to repeat or not
            if repeat:
               schedule_news_updates(future_time,(text_field+" (repeating update) (news)"), type="repeating")
               logging.info("The user has scheduled a repeating news update")
            else:
                schedule_news_updates(future_time,(text_field+" (news)"))
                logging.info("The user has scheduled a non-repeating news update")
        
        #If the user doesn't want to update neither the covid data or the news articles
        #it is pointless to run the update
        else:
            print("nothing was selected to be updated")
            logging.error("The user has made an invalid update")

    #If the user removes a news article that article is removed from news
    #and added to the removed_news articles
    if remove_news:
        for article in news:
            if remove_news == article['title']:
                news.remove(article)
                removed_news_function(article)
                logging.info("An article was removed")

    #If an update is removed it is cancelled and removed from the dashboard                                        
    if remove_update:
        cancel_update(remove_update)
        logging.info("An update was cancelled")

    s.run(blocking=False)

    #The index gets filled and returned so that the user can access it
    return render_template(
    "index.html",
    #Covid data using the covid API
    location = config_location,
    local_7day_infections = LocalCasesByPublishDate[0],
    nation_location = config_country,
    national_7day_infections = NationalCasesByPublishDate[0],
    hospital_cases = ("Hospital Cases in " + config_country + " : " + str(HospitalCases[0])),
    deaths_total = ("Deaths in last 28 days in " + config_country + ": " + str(CumulativeCases[0])),

    #Title of the dashboard stored in config file
    title=interface['title'],

    #Image showing on the dashboard
    favicon = '.\static\favico.ico',
    image = 'covid-image.png',

    #List of updates
    updates = update,

    #Onlyt shows 4 news articles which makes the dashboard more convenient
    news_articles = news[0:4])

if __name__ == "__main__":
    news_API_request()
    app.run()

