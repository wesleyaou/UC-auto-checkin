# UC-auto-checkin
A script that automates the pesky Utica College daily health screening

## Description
This python script is incredibly simple as it just makes an authorized request to Utica College's COVID health screening webpage, and hits the endpoint of a student that is expected to come to campus but is not showing symptoms I was consistently getting angry at being late for class and locked out of a building because I had forgot to do my screening. The refresh rate for the card readers at the door seem to be 3-5 minutes, which seems like an eternity when you are already late. This eliminates that problem, byt utilizing cron jobs to make a request every morning at the same time (~6:25a). There is an option for a text verification that was added as an after thought as a verification that the request went through. This verification is done by doing a webscrape of the COVID health page and seeking out specific elements that indicate a green light.

## Requirements
- Python 3
- BeautifulSoup4 (soon the setup script will handle this)
- A linux machine (Tested on Ubuntu and PiOS)
- (Optional) A spare gmail account with less secure apps enabled

## Installation
The installation is mostly handled by the setup script, but for the time being 
1. Pull the repo and cd into it:

    `git clone https://github.com/wesleyaou/UC-auto-checkin.git`
    `cd UC-auto-checkin/'

3. BeautifulSoup4 needs to be installed via:

    `python3 -m pip install beautifulsoup4`

2. Run the setup script:

    `python3 setup.py`
    
3. Make the Auto_Checkin.py executable:
    `sudo chmod +x Auto_Checkin.py`

4. Move the executable to `/etc/cron.daily/` via:
    `sudo mv Auto_Checkin.py /etc/cron.daily/`
    
5. Profit!

## (Optional) Text Confirmation Notifications
This is pretty straight forward and a nice feature to have as well. Just make a new gmail account, and go to the following link (https://myaccount.google.com/lesssecureapps) to enable less secure apps, and enter the email login info upon the setup.py's prompt.
