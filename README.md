
# UC-auto-checkin

A script that automates the pesky Utica College daily health screening

## Description

This python script is incredibly simple as it just makes an authorized request to Utica College's COVID health screening webpage, and hits the endpoint of a student that is expected to come to campus but is not showing symptoms. I was consistently getting pissed being late for class and locked out of a building because I forgot the screening. The refresh rate for the card readers at the door are 3-5 minutes, which seems like an eternity when you're already late. This eliminates that problem, by utilizing cron jobs to make a request every morning at the same time (~6:25a). There's an option for a text verification that was added as an after thought as a confirmation that the request went through. This verification is done by doing a webscrape of the COVID health page and seeking out specific elements that indicate a green light. *This is NOT an attempt to undermine the procedures put in place to protect students, if you are sick disable the script and notify the appropriate contacts.*

**This script was designed for Utica College but could easily be expanded and used as a framework for any other similar COVID screening.**

## Requirements

- Python 3
- BeautifulSoup4 (soon the setup script ~~will~~ *does* handle this)
- A linux machine (Tested on Ubuntu and PiOS)
- (Optional) A spare gmail account with less secure apps enabled

## Installation

The installation is mostly handled by the setup script, but for the time being 
1. Pull the repo and cd into it:

    `git clone https://github.com/wesleyaou/UC-auto-checkin.git`

    `cd UC-auto-checkin/`

2. Run the setup script **as root!**:

    `sudo python3 setup.py`
    
3. (Optional) Test the script with output:

    `sudo run-parts --report /etc/cron.daily/`

4. Profit!

## (Optional) Text Confirmation Notifications

This is pretty straight forward and a nice feature to have. Just make a new gmail account, and go to the following link (<https://myaccount.google.com/lesssecureapps>) to enable less secure apps, and enter the email login info upon the setup.py's prompt. You'll be prompted for your phone number along with your carrier. This will allow the script the send you SMS messages through your carrier's email format. 

## (Optional) IFTTT Integration

To integrate this script into IFTTT and allow it to trigger other automation services, you will need to setup the Webhooks service and get your key.
Go to (<https://ifttt.com>) and sign in.
Create an applet, using Webhooks as the trigger (Select the "Receive a web request" option)
After you create your applet, click your profile icon in the top-right corner, go to "My Services" and select "Webhooks". 
Click "Documentation". Your key will be at the top of the page.
