from menu import UI
from json import load, dump
from time import sleep
from color import color
ui = UI()

#[0] Exit And Save
#[1] Change All Settings
#[2] Change Token
#[3] Change Channel
#[4] Change Pray Mode
#[5] Change Gems Mode
#[6] Change Exp Mode
#[7] Change Sleep Mode
#[8] Change Webhook Settings
#[9] Change Selfbot Commands
#[10] Change Daily Mode
#[11] Change Stop Time
#[12] Change Sell Mode
#[13] Change Switch Channel
#[14] Change Solve Captcha

def main():
	with open("settings.json", "r") as f:
		data = load(f)
	ui.newData()
	choice = input(f"{color.okgreen}Enter Your Choice: {color.reset}")
	if choice == "0":
		pass
	elif choice == "1":
		t(data, True)
		c(data, True)
		pm(data, True)
		gm(data, True)
		em(data, True)
		sm(data, True)
		webhook(data, True)
		oc(data, True)
		daily(data, True)
		stop(data, True)
		sell(data, True)
		change(data, True)
		solve(data, True)
	elif choice == "2":
		t(data, False)
	elif choice == "3":
		c(data, False)
	elif choice == "4":
		pm(data, False)
	elif choice == "5":
		gm(data, False)
	elif choice == "6":
		em(data, False)
	elif choice == "7":
		sm(data, False)
	elif choice == "8":
		webhook(data, False)
	elif choice == "9":
		oc(data, False)
	elif choice == "10":
		daily(data, False)
	elif choice == "11":
		stop(data, False)
	elif choice == "12":
		sell(data, False)
	elif choice == "13":
		change(data, False)
	elif choice == "14":
		solve(data, False)
	else:
		ui.slowPrinting(f"{color.fail}[INFO] {color.reset}Invalid Choice")
def t(data, all):
 data['token'] = input("Please Enter Your Account Token: ")
 file = open("settings.json", "w")
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def c(data, all):
 data['channel'] = input("Please Enter Your Channel ID: ")
 file = open("settings.json", "w")
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def pm(data, all):
 data['pm'] = input("Toggle Automatically Sending Pray (YES/NO): ")
 data['pm'] = data['pm'].lower() == "yes"
 file = open("settings.json", "w")
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def gm(data, all):
 data['gm'] = input("Toggle Automatically Using Gems (YES/NO): ")
 file = open("settings.json", "w")
 data['gm'] = data['gm'].lower() == "yes"
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def em(data, all):
 data['em']['text'] = input("Toggle Automatically Sending Random Text To Level Up (YES/NO): ")
 if data['em']['text'].lower() == "yes":
    data['em']['owo'] = input("\t +)Do You Want To Enable Automatically Sending \"OwO\" Also? (YES/NO): ")
    data['em']['owo'] = data['em']['owo'].lower() == "yes"
 data['em']['text'] = data['em']['text'].lower() == "yes"
 file = open("settings.json", "w")
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def sm(data, all):
 data['sm'] = input("Toggle Sleep Mode (YES/NO): ")
 file = open("settings.json", "w")
 data['sm'] = data['sm'].lower() == "yes"
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def webhook(data, all):
 data['webhook']['link'] = input("Toggle Discord Webhook (Enter Webhook Link, It'll Ping You If OwO Ask For Captcha. Otherwise Enter \"None\"): ")
 if data['webhook']['link'].lower() != "none":
  data['webhook']['ping'] = input("\t +)Do You Want To Ping A Specified User When OwO Asked Captcha? If Yes Enter User ID. Otherwise Enter \"None\": ")
 file = open("settings.json", "w")
 if data['webhook']['link'].lower() == "none":
  data['webhook']['link'] = None
 if data['webhook']['ping'] and data['webhook']['ping'].lower() == "none":
  data['webhook']['ping'] = None
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def oc(data, all):
 data['sbcommands']['enable'] = input("Toggle Selfbot Commands, You Can Control Your Selfbot Using Commands (YES/NO): ")
 if data['sbcommands']['enable'].lower() == "yes":
  data['sbcommands']['prefix'] = input("\t +)Enter Your Selfbot Prefix: ")
  data['sbcommands']['allowedid'] = input("\t +)Do You Want Allow An User To Use Your Selfbot Commands? If Yes Enter The Account ID, Otherwise Enter \"None\": ")
  ui.slowPrinting("Great! You Can View Selfbot Commands At Option [3] Info At The Main Menu!")
  sleep(1)
 data['sbcommands']['enable'] = data['sbcommands']['enable'].lower() == "yes"
 if data['sbcommands']['allowedid'] and data['sbcommands']['allowedid'].lower() == "none":
  data['sbcommands']['allowedid'] = None
 file = open("settings.json", "w")
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def daily(data, all):
 data['daily'] = input("Toggle Automatically Claiming Daily (YES/NO): ")
 data['daily'] = data['daily'].lower() == "yes"
 file = open("settings.json", "w")
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def stop(data, all):
 data['stop'] = input("Toggle Stop After A Specifice Time (YES/NO): ")
 if data['stop'].lower() == "yes":
  data['stop'] = input("Enter Stop Time (Seconds): ")
 else:
  data['stop'] = False
 file = open("settings.json", "w")
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def sell(data, all):
 data['sell']['enable'] = input("Toggle Automatically Selling Animals (YES/NO): ")
 if data['sell']['enable'].lower() != "no":
  ui.slowPrinting("Animal Type: C, U, R, M... (Type \"all\" To Sell All Animals)")
  ui.slowPrinting("C = Common, U = Uncommon, ect...")
  data['sell']['types'] = input("Enter Animal Type: ")
  file = open("settings.json", "w")
  dump(data, file, indent = 4)
  file.close()
 data['sell']['enable'] = data['sell']['enable'].lower() == "yes"
 file = open("settings.json", "w")
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def solve(data, all):
 data['solve']['enable'] = input("Toggle Automatically Captcha Solving By Human (YES/NO): ")
 if data['solve']['enable'].lower() == "yes":
 	ui.slowPrinting("Available Captcha Solving Server:\n1: https://autofarmsupport.tk\n2: https://afbot.dev")
 	data['solve']['server'] = input("Which Server Do You Want To Use (1/2): ")
 	if data['solve']['server'].isdigit():
 		data['solve']['server'] = int(data['solve']['server'])
 	else:
 		ui.slowPrinting("Invalid Input")
 		solve(data, all)
 data['solve']['enable'] = data['solve']['enable'].lower() == "yes"
 file = open("settings.json", "w")
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
def change(data, all):
 data['change'] = input("Toggle Automatically Change Channel (YES/NO): ")
 file = open("settings.json", "w")
 data['change'] = data['change'].lower() == "yes"
 dump(data, file, indent = 4)
 file.close()
 ui.slowPrinting(f"{color.okcyan}[INFO] {color.reset}Successfully Saved!")
 if not all:
  main()
if __name__ == "__main__":
	main()
