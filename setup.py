# Setup script is ugly and not organized. It works.
# But maybe...
# TODO cleanup setup file into cute little neat functions

import os, json
from getpass import getpass


CELL_PROVIDERS = {1 : "vtext.com",              # Verizon
                2 : "txt.att.net",              # AT&T
                3 : "sms.cricketwireless.net",  # Cricket Wireless
                4 : "mymetropcs.com",           # MetroPCS
                5 : "tmomail.net",              # T-Mobile
                6 : "mailmymobile.net"}         # Consumer Cellular

CELL_NAME = ["Verizon", 
            "AT&T", 
            "Cricket Wireless", 
            "MetroPCS", 
            "T-Mobile", 
            "Consumer Cellular"]


login_url = "https://www.utica.edu/forms/covid-19-screening/index.cfm"
checkin_url = "https://www.utica.edu/apps/covid-19-screening/covid19screening.cfc?method=insert&pidm=452205&status=S&campus=Y&symptoms=N&_=1631702345870"

# Vars to be modified later
prog_path = ""
UC_user = ""
UC_pass = ""
notif = ""
notif_email = ""
notif_pass = ""
notif_addr = ""
notif_num = ""
carrier = ""

while prog_path == "":
    prog_path_prompt = input("Desired path for script files to live in (default is current dir): ")
    if prog_path_prompt.replace(" ", "") == "":
        prog_path = os.getcwd() + "/"
    elif not os.path.isdir(prog_path_prompt):
        print("Failed! Path is not a directory.")
        continue
    else:
        prog_path = prog_path_prompt

pre_main = open("Auto_Checkin.py", 'r')
pre_config_lines = pre_main.readlines()
pre_main.close()
iter = 0
for line in pre_config_lines:
    if line.startswith("config_path = ''"):
        del pre_config_lines[iter]
        del pre_config_lines[iter - 1]
        pre_config_lines.insert(iter - 1, "# Config path HAS BEEN populated by the setup script\n")
        pre_config_lines.insert(iter, "config_path = '" + prog_path + "config.json'\n")
    iter += 1
with open("Auto_Checkin.py", "w") as post_main:
    post_main.writelines(pre_config_lines)

if not os.path.isdir(prog_path + "Responses/"):
    os.mkdir(prog_path + "Responses/")
if not os.path.isdir(prog_path + "Logging/"):
    os.mkdir(prog_path + "Logging/")

login_url_prompt = input("Default login URL is: " + login_url + "\nPress enter to use default, or enter new URL: ")
if not login_url_prompt.replace(" ", "") == "":
    login_url_prompt = login_url

checkin_url_prompt = input("Default checkin URL is: " + login_url + "\nPress enter to use default, or enter new URL: ")
if not checkin_url_prompt.replace(" ", "") == "":
    checkin_url_prompt = checkin_url

while UC_user == "":
    UC_user_prompt = input("Enter username to be used for login authentication: ")
    if UC_user_prompt.replace(" ", "") == "":
        print("Failed! Username Required.")
    else:
        UC_user = UC_user_prompt

while UC_pass == "":
    UC_pass_prompt = getpass("Enter password to be used for login authentication: ")
    if UC_pass_prompt.replace(" ", "") == "":
        print("Failed! Password Required.")
    else:
        UC_pass = UC_pass_prompt

while notif == "":
    notif_prompt = input("Would you like SMS notifications [Y/n]: ")
    if notif_prompt.replace(" ", "") == "" or notif_prompt.lower() == 'y':
        notif = True
        while notif_email== "":
            notif_email_prompt = input("Enter the email created that can be accessed by smtplib (see README): ")
            if not "@" in notif_email_prompt:
                print("Invalid email address!")
                continue
            else:
                notif_email = notif_email_prompt
        while notif_pass== "":
            notif_passwd_prompt = getpass("Enter the password for the email created: ")
            notif_passwd_conf = getpass("Confirm password: ")
            if notif_passwd_prompt != notif_passwd_prompt:
                print("Password mismatch!")
                continue
            else:
                notif_pass = notif_passwd_prompt
        while notif_num == "":
            notif_num_prompt = input("Enter the phone number to recieve notifications on: ")
            if notif_num_prompt.startswith("1"):
                notif_num_prompt = notif_num_prompt[1:]
            if len(notif_num_prompt) > 10:
                print("Invalid Number Entry!")
            iter = 1
            for carrier_n in CELL_NAME:
                print("\t[ " + str(iter) + " ] " + carrier_n)
                iter += 1
            while carrier == "":
                carrier_prompt = input("Select your carrier! (0-" + str(iter) + "): ")
                if int(carrier_prompt) < 0 or int(carrier_prompt) > iter + 1:
                    print("Invalid Selection!")
                    continue
                carrier = CELL_PROVIDERS[int(carrier_prompt)]
                notif_num = notif_num_prompt + "@" +  carrier
        break
    elif notif_prompt.lower == 'n':
        notif = False
    else:
        print("Failed! Invalid Input!")
        
config_json = json.dumps({"prog_path" : prog_path,
                        "login_url" : login_url,
                        "checkin_url" : checkin_url,
                        "notify" : str(notif),
                        "UC_user" : UC_user,
                        "UC_pass" : UC_pass,
                        "email_addr" : notif_email,
                        "email_pass" : notif_pass,
                        "conf_num" : notif_num})

config_file = open(prog_path + "config.json", "w")
config_file.write(config_json)
config_file.close()


