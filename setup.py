# Setup script is ugly and not organized. It works.
# But maybe...
# TODO cleanup setup file into cute little neat functions

import os, json, subprocess
from getpass import getpass
from pip._internal import main as pipmain

if os.geteuid() != 0:
    print("\033[31;1;1mFailed!\033[0m Script needs to be run as root/sudo!")
    exit()

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

main_file_name = "Auto_Checkin"
path_to_crontab = "/etc/crontab"

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

print("\n\033[32;1;4mAttempting UC-auto-checkin setup...\033[0m\n")

print("Installing BeautifulSoup4...")

# TODO update method of pip use? warns it'll be depreciated soon, but works for now.
pipmain(['install', 'beautifulsoup4'])

while prog_path == "":
    prog_path_prompt = input("\nDesired path for script files to live in (default is current dir): ")
    if prog_path_prompt.replace(" ", "") == "":
        prog_path = os.getcwd() + "/"
    elif not os.path.isdir(prog_path_prompt):
        print("\033[31;1;1mFailed!\033[0m Path is not a directory.")
        continue
    else:
        prog_path = prog_path_prompt

if not os.path.exists(path_to_crontab):
    print("Crontab not found at " + path_to_crontab + "!")
    exit()
with open(path_to_crontab, "r") as cron:
    for line in cron:
        if "cron.daily" in line:
            mins, hours = line.split(" ")[0], line.split(" ")[1][:2].strip()
            print("\nLogin will be executed daily at \033[32;1;4m" + hours + ":" + mins + "\033[0m. To change this, edit /etc/crontab")

# pre_main = open(main_file_name, 'r')
# pre_config_lines = pre_main.readlines()
# pre_main.close()
# iter = 0
# for line in pre_config_lines:
#     if line.startswith("config_path = ''"):
#         del pre_config_lines[iter]
#         del pre_config_lines[iter - 1]
#         pre_config_lines.insert(iter - 1, "# Config path HAS BEEN populated by the setup script\n")
#         pre_config_lines.insert(iter, "config_path = '" + prog_path + "config.json'\n")
#     iter += 1
# with open(main_file_name, "w") as post_main:
#     post_main.writelines(pre_config_lines)

if not os.path.isdir(prog_path + "Responses/"):
    os.mkdir(prog_path + "Responses/")
if not os.path.isdir(prog_path + "Logging/"):
    os.mkdir(prog_path + "Logging/")

login_url_prompt = input("\nDefault login URL is: \033[32;1;4m" + login_url + "\033[0m\nPress enter to use default, or enter new URL: ")
if not login_url_prompt.replace(" ", "") == "":
    login_url_prompt = login_url

checkin_url_prompt = input("\nDefault checkin URL is: \033[32;1;4m" + checkin_url + "\033[0m\nPress enter to use default, or enter new URL: ")
if not checkin_url_prompt.replace(" ", "") == "":
    checkin_url_prompt = checkin_url

while UC_user == "":
    UC_user_prompt = input("\nEnter username to be used for UC login authentication: ")
    if UC_user_prompt.replace(" ", "") == "":
        print("\033[31;1;1mFailed!\033[0m Username Required.")
    else:
        UC_user = UC_user_prompt

while UC_pass == "":
    UC_pass_prompt = getpass("\nEnter password to be used for UC login authentication: ")
    if UC_pass_prompt.replace(" ", "") == "":
        print("\033[31;1;1mFailed!\033[0m Password Required.")
    
    UC_pass_conf = getpass("Confirm password: ")
    if UC_pass_prompt != UC_pass_conf:
        print("\033[31;1;1mFailed!\033[0m Password mismatch!")
        continue
    else:
        UC_pass = UC_pass_prompt

while notif == "":
    notif_prompt = input("\nWould you like SMS notifications for successful logins? [Y/n]: ")
    if notif_prompt.replace(" ", "") == "" or notif_prompt.lower() == 'y':
        notif = True
        while notif_email== "":
            notif_email_prompt = input("\nEnter the email created that can be accessed by smtplib (see README): ")
            if not "@" in notif_email_prompt:
                print("\033[31;1;1mFailed!\033[0m Invalid email address!")
                continue
            else:
                notif_email = notif_email_prompt
        while notif_pass== "":
            notif_passwd_prompt = getpass("\nEnter the password for the email created: ")
            notif_passwd_conf = getpass("Confirm password: ")
            if notif_passwd_prompt != notif_passwd_prompt:
                print("\033[31;1;1mFailed!\033[0m Password mismatch!")
                continue
            else:
                notif_pass = notif_passwd_prompt
        while notif_num == "":
            notif_num_prompt = input("\nEnter the phone number to recieve notifications on: ")
            if notif_num_prompt.startswith("1"):
                notif_num_prompt = notif_num_prompt[1:]
            if len(notif_num_prompt) > 10:
                print("\033[31;1;1mFailed!\033[0m Invalid Number Entry!")
            iter = 1
            for carrier_n in CELL_NAME:
                print("\t[ " + str(iter) + " ] " + carrier_n)
                iter += 1
            while carrier == "":
                carrier_prompt = input("Select your carrier! (0-" + str(iter - 1) + "): ")
                if int(carrier_prompt) < 1 or int(carrier_prompt) > iter - 1:
                    print("\033[31;1;1mFailed!\033[0m Invalid Selection!")
                    continue
                carrier = CELL_PROVIDERS[int(carrier_prompt)]
                notif_num = notif_num_prompt + "@" +  carrier
        break
    elif notif_prompt.lower() == 'n':
        notif = False
    else:
        print("\033[31;1;1mFailed!\033[0m Invalid Input!")
        
config_json = json.dumps({"prog_path" : prog_path,
                        "login_url" : login_url,
                        "checkin_url" : checkin_url,
                        "notify" : notif,
                        "UC_user" : UC_user,
                        "UC_pass" : UC_pass,
                        "email_addr" : notif_email,
                        "email_pass" : notif_pass,
                        "conf_num" : notif_num}, indent=1)


bash_caller_contents = ["#!/usr/bin/env bash\n",
                    "\n",
                    "python3 /home/lame/projects/UC_Auto_Checkin/Final/UC-auto-checkin/Auto_Checkin.py"]


os.rename(main_file_name + ".py", prog_path + main_file_name + ".py")

with open("/etc/cron.daily/" + main_file_name, "w") as bash_caller:
    bash_caller.writelines(bash_caller_contents)

make_executable_cmd = "chmod +x " + "/etc/cron.daily/" + main_file_name
subprocess.run(make_executable_cmd, shell=True, check=True)

config_file = open(prog_path + "config.json", "w")
config_file.write(config_json)
config_file.close()

print("\n\033[32;1;1mDone!\033[0m\n")

