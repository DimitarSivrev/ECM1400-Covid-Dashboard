'''
This module performs:
    -the sheduliong of covid updates
    -calculating seconds left until time given
    -covid data API
'''
#Importing python modules that will be used in the program
import json
import sched
import time
import logging
import os
from datetime import datetime, timedelta
from uk_covid19 import Cov19API

#This is the format the logs will be displayed in the log-file
FORMAT = "%(levelname)s: %(asctime)s %(message)s"

#Configures the logging used through out the program
logging.basicConfig(filename="log-file.log",
    level=logging.DEBUG,
    format=FORMAT)

#Find the file path to this directory
file_dir = os.path.dirname(os.path.realpath(__file__))

#Opens the configuration file using file path
with open(file_dir + "\\config.json","r") as f:
    json_file = json.load(f)

#Assigns a variable to the apropriate config section for this program
covid_api = json_file["Covid-API"]

#Assings variables to information stored in the config file
config_location = covid_api["location"]
config_location_type = covid_api["location_type"]
config_country = covid_api["country"]
config_country_type = covid_api["country_type"]

#Calling sched and assigning it to a variable
s = sched.scheduler(time.time, time.sleep)

#List for the updates displaying on the dashboard
update = []

#List for the updates scheduled
events = []

def parse_csv_data(csv_filename = str):
    '''
    Extract csv file and transfrom it

    :param csv_filename: name of the csv file
    :return: list of strings
    '''
    logging.info("Running parse_scv_data")
    #Using try and except to seek out any errors when processing the file
    try:
        #Opens csv file ad creates a 2D array with the data
        file = open(csv_filename, "r")
        file_list = file.readlines()
        file_list2 = []
        for i in range (0,len(file_list)):
            file_list2.append(file_list[i].split(","))
        logging.info("Taking csv data and returning it")
    except TypeError:
        logging.error("No arguments were passed through")
    except FileNotFoundError:
        logging.error("File not found in directory")
    except OSError:
        logging.error("Wrong type of argument")
    except:
        logging.error("There is a problem with the file passed through ")
    else:
        return file_list2

def process_covid_csv_data(covid_csv_data):
    '''
    Processes the returned data from parse_csv_data

    :param covid_csv_data: The list with covid data
    :return: tuple with (the number of cases in the laste 7 days,
    the number of hospital cases,
    the cumulative number of deaths)
    '''
    seven_day_count = 0

    logging.info("Running process_covid_csv_data")
    #Avoids the first 2 element because the csv file isn't completed
    for i in range (3,10):
        try :
            #Tries to access the elements of the list passed as covid_csv_data
            seven_day_count = (seven_day_count
            + int(covid_csv_data[i][6]))
        except IndexError:
            logging.error(
            "The argumment doesn't match the index required")
        except:
            logging.error(
            "There was an error processing the data given as an argument")

    try:
        #Used to check if the return values exsist so there won't be problems returning them
        (seven_day_count,
        int(covid_csv_data[1][5]),
        int(covid_csv_data[14][4]))
    except:
        logging.error("Couldn't return data")
    else:
        logging.info("Processing the scv data")
        #If there aren't errors the values are returned
        return (
        seven_day_count,
        int(covid_csv_data[1][5]),
        int(covid_csv_data[14][4]))

def covid_API_request(
    location = config_location,
    location_type = config_location_type):
    '''
    Using API to get current covid statistics for a certain location

    :param location: The location name, stored in the config file
    :param location_type: Type of location, stored in the config file
    :return: Covid data for the location as a dictionary
    '''

    logging.info("Running covid_API_request")
    #This is the information that will be retrieved by the API
    structure = {
        "date": "date",
        "areaName": "areaName",
        "areaCode": "areaCode",
        "hospitalCases" : "hospitalCases",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate",
    }

    #Calculates the date 7 days ago
    date_7days_ago = str(datetime.now() - timedelta(days=7))
    date_7days_ago = date_7days_ago.split(" ", 1)
    date_7days_ago = date_7days_ago[0]

    #Using try and except to seek out any errors when processing the file
    try:
        #Joins the varaibles into a format the API uses
        api_filter = (str.join(";",
        [f"areaType={ location_type }",
        f"areaName={ location }",
        f"date={ date_7days_ago }"] ),)

        #The API returns a json document with the data
        api = Cov19API(
            filters=api_filter,
            structure=structure)
        data = api.get_json()

    except:
        logging.critical("Couldn't extract API information")
    else :
        logging.info("Returning the covid infection rates as a dictionary")
        return data

def schedule_covid_updates(
    update_interval,
    update_name,
    update_type = "non-repeating"):
    '''
    Schedules covid updates so the covid data in the dashboard updates

    :param update_interval: the time in which the update should happen
    :param update_name: the name of the update
    :param update_type: repeating or non-repeating update, deafult is non-repeating
    '''

    logging.info("Running schedule_covid_updates")
    #Using try and except to seek out any errors when processing the file
    try:
        #Calculates the time the update will happen so it can be displayed
        actual_time = str(datetime.now() + timedelta(seconds = update_interval))

        #Allows the update to be displayed in the index
        update.append({
            "title" : update_name,
            "content" : actual_time[11:19]
            })

        #Schedules an event
        event_name = s.enter(int(update_interval), 1, update_covid)

        #Adds event to list
        events.append(event_name)

        #Checks what type the update entered is
        if update_type == "non-repeating":

            #schedules the update to be removed from the list after it has ran
            s.enter(update_interval,2,
            delete_update,
            kwargs={"name": str(update_name)})

        if update_type == "repeating":
            #The repeating update means it runs every 24 hours
            #86400 sec = 24 hours
            #The function calls itself every 24 hours to shedule an update
            event_name= s.enter(86400, 1, schedule_covid_updates,
            kwargs={"update_interval" : 86400,"update_name": str(update_name),"type" : "repeating"})
            s.enter(86400,2,delete_update,kwargs={'name': str(update_name)})
            events.append(event_name)

    except TypeError:
        logging.critical("Can't schedule covid update")
    else:
        logging.info("The covid update has been scheduled")


def delete_update(name):
    '''
    Used to remove updates in the update tile displayed on the dashboard
    :param name: The name of the update that is being deleted
    '''
    logging.info("Running delete_update")
    #Increments checking if the title of any of the updates mathes the name
    try:
        for i in update:
            if name == i["title"]:
                update.remove(i)
    except:
        logging.error("Update couldn't be deleted")
    else:
        logging.info("Update was deleted")

def cancel_update(name):
    '''
    Used to cancell the update from happening by removing it from the sched queue
    Uses the principal that since an update will get added to
    the interface list (update) and the list of events at the same time
    the update would be in the same position in both lists
    :parameter name: Name of update being cancelled
    '''
    logging.info("Running cancel_update")
    try:
        for i in update:
            if name == i["title"]:
                position = update.index(i)
                update.remove(i)
                s.cancel(events[position])
                events.remove(events[position])
    except:
        logging.error("Update couldn't be cancelled")
    else:
        logging.info("Update was cancelled")

#Used to store the covid data displayed on the dashboard
local_cases_by_publish_date = []
national_cases_by_publish_date = []
hospital_cases = []
cumulative_cases = []

#Adds the relevant information using the covid API
local_cases_by_publish_date.append(
covid_API_request()["data"][0]["newCasesByPublishDate"])

national_cases_by_publish_date.append(
covid_API_request(config_country,config_country_type)
["data"][0]["newCasesByPublishDate"])

hospital_cases.append(covid_API_request(config_country,config_country_type)
["data"][0]["hospitalCases"])

cumulative_cases.append(covid_API_request(config_country,config_country_type)
["data"][0]["cumDeaths28DaysByDeathDate"])

def update_covid():
    '''When the data is updated the list get emptied then the new data is added'''
    logging.info("Running update_covid")
    try:
        local_cases_by_publish_date.pop(0)
        local_cases_by_publish_date.append(covid_API_request()["data"][0]["newCasesByPublishDate"])
        national_cases_by_publish_date.pop(0)
        national_cases_by_publish_date.append(covid_API_request(config_country,config_country_type)
            ["data"][0]["newCasesByPublishDate"])
        hospital_cases.pop(0)
        hospital_cases.append(covid_API_request(config_country,config_country_type)
            ["data"][0]["hospitalCases"])
        cumulative_cases.pop(0)
        cumulative_cases.append(covid_API_request(config_country,config_country_type)
            ["data"][0]["cumDeaths28DaysByDeathDate"])
    except:
        logging.error("Couldn't update the covid data")
    else:
        logging.info("Covid data has been updated")

def second_calculator(hour_minute):
    '''
    Function used to calculate the seconds until the time given
    in the format HH:MM(hours and minutes)
    :parameter hour_minute: The time that will be calculated
    :return: The seconds left until the time entered as an integer
    '''

    logging.info("Running second_calculator")

    #Using try and except to seek out any errors when processing the file
    try:
        #Tries to split the argument into two separate variables
        hour, minute = hour_minute.split(":")

        #Calculates the time left until the time given in the format days:hours:minutes
        now = datetime.now()
        time_str = (str(timedelta(hours=24)
        - (now - now.replace(hour=int(hour),
        minute=int(minute)))))

        #Used to remove the extra day that is calculated
        #when the time given is between the current time and 00:00
        time_str = time_str.replace("1 day, ","")

        #Splits the string into hours, minutes and seconds
        #so that they can be converted into seconds and returned
        h_h, m_m, s_s = time_str.split(":")
    except:
        logging.critical("Can't calculate the second until HH:MM")

    else:
        logging.info("The time in seconds until HH:MM has been calculated")
        #If there aren't any errors the seconds are returned
        seconds = int(h_h) * 3600 + int(m_m) * 60 + round(float(s_s))
        if seconds == 0:
            seconds = 86400
        return seconds
