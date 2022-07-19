import time
import json
import os
from sys import exit
def menu():
 file = open("settings.json", "r")
 data = json.load(file)
 file.close()
 print('================================')
 print(f'| [0] Exit And Save           |')
 print(f'| [1] Change All Settings     |')
 print(f'| [2] Change Token            |')
 print(f'| [3] Change Channel          |')
 print(f'| [4] Change Pray Mode        |')
 print(f'| [5] Change Gems Mode        |')
 print(f'| [6] Change Exp Mode         |')
 print(f'| [7] Change Sleep Mode       |')
 print(f'| [8] Change Webhook Settings |')
 print(f'| [9] Change Selfbot Commands |')
 print(f'| [10] Change Daily Mode      |')
 print(f'| [11] Change Stop Time       |')
 print(f'| [12] Change Switch Channel  |')
 print(f'| [13] Change Sell Mode       |')
 print(f'| [14] Change Solve Captcha   |')
 print('================================')
 choice = input("Enter Your Choice: ")
 if choice == "0":
  raise SystemExit
 if choice == "1":
  t(data,"True")
  c(data,"True")
  pm(data,"True")
  gm(data,"True")
  em(data,"True")
  sm(data,"True")
  webhook(data,"True")
  oc(data,"True")
  daily(data,"True")
  stop(data,"True")
  change(data,"True")
  sell(data,"True")
  solve(data,"True")
 if choice == "2":
  t(data,"False")
 if choice == "3":
  c(data,"False")
 if choice == "4":
  pm(data,"False")
 if choice == "5":
  gm(data,"False")
 if choice == "6":
  em(data,"False")
 if choice == "7":
  sm(data,"False")
 if choice == "8":
  webhook(data,"False")
 if choice == "9":
  oc(data,"False")
 if choice == "10":
  daily(data,"False")
 if choice == "11":
  stop(data,"False")
 if choice == "12":
  change(data,"False")
 if choice == "13":
  sell(data, "False")
 if choice == "14":
  solve(data, "False")
def t(data,all):
 data['token'] = input("Please Enter Your Account Token: ")
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def c(data,all):
 data['channel'] = input("Please Enter Your Channel ID: ")
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def pm(data,all):
 data['pm'] = input("Toggle Automatically Send Pray (YES/NO): ")
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def gm(data,all):
 data['gm'] = input("Toggle Automatically Use Gems Mode (YES/NO): ")
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def em(data,all):
 data['em'] = input("Toggle Automatically Send Random Text To Level Up (YES/NO): ")
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def sm(data,all):
 data['sm'] = input("Toggle Sleep Mode (YES/NO): ")
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def webhook(data,all):
 data['webhook'] = input("Toggle Discord Webhook, Enter Webhook Link If You Want It To Ping You If OwO Asked Captcha. Otherwise Enter \"None\": ")
 if data['webhook'] != "None":
  data['webhookping'] = input("Do You Want To Ping A Specified User When OwO Asked Captcha? If Yes Enter User ID. Otherwise Enter \"None\": ")
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def oc(data,all):
 data['prefix'] = input("Toggle Selfbot Commands, You Can Control Your Selfbot Using Commands (YES/NO): ")
 if data['prefix'].lower() == "yes":
  data['prefix'] = input("Enter Your Selfbot Prefix: ")
  data['allowedid'] = input("Do You Want Allow An User To Use Your Selfbot Commands? If Yes Enter The Account ID, Otherwise Enter \"None\": ")
  print("Great! You Can View Selfbot Commands At Option [3] Info At The Main Menu!")
  time.sleep(1)
 else:
  data['prefix'] = "NO"
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def daily(data,all):
 data['daily'] = input("Toggle Automatically Claim Daily (YES/NO): ")
 if data['daily'].lower() == "no":
  data['daily'] = "None"
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def stop(data,all):
 data['stop'] = input("Toggle Stop After A Specifice Time (YES/NO): ")
 if data['stop'].lower() == "yes":
  data['stop'] = input("Enter Stop Time (Seconds): ")
 else:
  data['stop'] = "NO"
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def change(data,all):
 data['change'] = input("Toggle Automatically Switch Channel To Avoid Channel EXP Limit (YES/NO): ")
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def sell(data, all):
 data['sell'] = input("Toggle Automatically Sell Animal (YES/NO): ")
 if data['sell'].lower() != "no":
  print("Animal Type: C, U, R, M... (Type \"all\" To Sell All Animals)")
  print("C = Common, U = Uncommon, ect...")
  data['sell'] = input("Enter Animal Type: ")
  file = open("settings.json", "w")
  json.dump(data, file)
  file.close()
 else:
  data['sell'] = "None"
  file = open("settings.json", "w")
  json.dump(data, file)
  file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
def solve(data, all):
 data['solve'] = input("Toggle Automatically Solve Captcha With AI (YES/NO): ")
 file = open("settings.json", "w")
 json.dump(data, file)
 file.close()
 print('Successfully saved!')
 if not all == "True":
  menu()
menu()
