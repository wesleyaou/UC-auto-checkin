#!/usr/bin/env python3

#   A simple webscraping/request making script to automate Utica College's 
#   health screening.

#   This is NOT an attempt to undermine the procedures put in place to 
#   protect students, if you are sick disable the script and notify the
#   appropriate contacts. I just got pissed off everytime I was locked
#   out & late to class after forgetting.
#   ~ wesleyaou <3


import requests, logging, json, smtplib
from datetime import date
from bs4 import BeautifulSoup

today = date.today()
today_date = today.strftime("%m_%d_%Y")

# Config path HAS BEEN populated by the setup script
config_path = '/home/lame/projects/UC_Auto_Checkin/Final/UC-auto-checkin/config.json'

# Open the config json file and establish the values as a dictionary
with open(config_path) as json_config:
    config = json.load(json_config)

# Start logging based on the path specified in the config.json
log_path = config['prog_path'] + "Logging/" + today_date + ".log"
logging.basicConfig(filename=log_path, level=logging.DEBUG)

verify_url = config["login_url"] + "?"

# Function to confirm that everything went well and didn't return an error code.
def handleStatus(status, url, notify):
    if status == 200 or status == 201:
        message = 'Successful connection made to: "' + url + '" [' + str(status) + ']'
        outputMessages(message, "DEBUG")
        return True
    else:
        message = 'Invalid connection made to "' + url + '" [' + str(status) + ']'
        if notify:
            outputMessages(message, "ERROR")
        else:
            outputMessages(message, "DEBUG")
        return False

# TODO Loggining methods work but are clunky, need a more efficient update
# Sends a message to both the end user (via text message) and a message to the logging functions
def outputMessages(message, level):
    notif = config["notify"]
    print(level + ": " + message)
    if level == "INFO":
        logging.info(message)
        if notif:
            sendSms(message)
    elif level == "WARN":
        logging.warn(message)
    elif level == "ERROR":
        logging.error(message)
        if notif:
            sendSms(message)
    elif level == "CRITICAL":
        logging.critical(message)
        if notif:
            sendSms(message)
    elif level == "DEBUG":
        logging.debug(message)

# Uses SMTPLib to send a message via text confirming the checkin worked/failed
def sendSms(msg):
    eaddr = config["email_addr"]
    epass = config["email_pass"]
    num = config["conf_num"]

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(eaddr, epass)

    msg = "\n" + msg
    server.sendmail(eaddr, num, msg)
    outputMessages('SMS Sent! Contents: ' + msg, "DEBUG")

# Scrapes the page to confirm the "notcoming_div" is hidden, while "no_symptoms" is showing
def verifySuccess(bs):
    notcoming = str(bs.find(id="notcoming_div")).split("\n")
    coming = str(bs.find(id="nosymptoms_div")).split("\n")

    notcoming_status = len(notcoming[0].split(" ")) >= 3

    coming_status = len(coming[0].split(" ")) >= 3

    bp_msg = today_date.replace("_", "/") + ": " + "UC COVID Check-in Attempt: "

    if notcoming_status == coming_status:
        msg = "Failed, fields have same values!"
        outputMessages(bp_msg + msg, "ERROR")
    elif not notcoming_status:
        msg = "Failed, Symptoms Indicated!"
        outputMessages(bp_msg + msg, "ERROR")
    elif not coming_status:
        msg = "Success!"
        outputMessages(bp_msg + msg, "INFO")
    else:
        msg = "Failed, Invalid API?"
        outputMessages(bp_msg + msg, "ERROR")

# The brains of the operation, the function that makes all the authorized requests using the config.json username/password
def makeRequests():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest'
    }

    payload = {
        "loginusername" : config["UC_user"],
        "loginpassword" : config["UC_pass"]
    }

    with requests.session() as sesh:
        login_req = sesh.post(config["login_url"], headers=headers, data=payload)
        soup = BeautifulSoup(login_req.content, "html.parser")
        login_status = soup.find(class_="alert alert-danger")
        if login_status != None:
            if login_status.text.replace('\n', '').strip() == "Invalid Login!":
                print("Login invalid!")
                exit()
        else:
            checkin_req = sesh.post(config["checkin_url"], headers=headers)
            if handleStatus(checkin_req.status_code, config["checkin_url"], True):
                with open(config["prog_path"] + "Responses/success_resp" + today_date + ".txt", "w") as f:
                    f.write("".join(checkin_req.text.split()))
            else:
                exit()
            verify_req = sesh.get(verify_url, headers=headers)
            if handleStatus(checkin_req.status_code, config["checkin_url"], True):
                verifySuccess(BeautifulSoup(verify_req.content, "html.parser"))
            else:
                exit()

makeRequests()