from version import Version
from requests import get
from color import color
from menu import UI
from time import sleep
from re import findall
from inputimeout import TimeoutOccurred, inputimeout
from webbrowser import open as open_browser
from os import getcwd
import json
ui = UI()
class data:
	def __init__(self):
		self.commands=[
			"hunt",
			"hunt",
			"battle"
			]
		self.wbm = [13,18]
		self.OwOID = '408785106942164992'
		self.totalcmd = 0
		self.totaltext = 0
		self.stopped = False
		self.version = int(''.join(map(str, Version)))
		self.wait_time_daily = 60
		with open(f'{getcwd()}/settings.json', "r") as file:
			data = json.load(file)
			self.token = data["token"]
			self.channel = data["channel"]
			self.gm = data["gm"]
			self.sm = data["sm"]
			self.pm = data["pm"]
			self.em = data["em"]
			self.sbcommands = data['sbcommands']
			self.webhook = data["webhook"]
			self.daily = data["daily"]
			self.stop = data["stop"]
			self.sell = data['sell']
			self.solve = data['solve']
			self.change = data['change']
			self.dmsID = None
	def Version(self):
		response = get("https://raw.githubusercontent.com/ahihiyou20/discord-selfbot-owo-bot/main/version.py")
		version = response.text
		version = findall(r'\b\d+\b', version)
		return int(''.join(version))
	def check(self):
		version = self.Version()
		if self.token and self.channel == 'nothing':
			ui.slowPrinting(f"{color.fail} !!! [ERROR] !!! {color.reset} Please Enter Information To Continue")
			sleep(2)
			from newdata import main
			main()
		else:
			response = get('https://discord.com/api/v9/users/@me',headers={"Authorization": self.token})
			if not response.ok:
				ui.slowPrinting(f"{color.fail} !!! [ERROR] !!! {color.reset} Invalid Token")
				sleep(2)
		ui.slowPrinting(f"{color.warning}Checking Update... {color.reset}")
		sleep(0.5)
		if self.version >= version:
			ui.slowPrinting(f"{color.okgreen}You're Using The Latest Version {color.reset}")
			sleep(2)
		elif self.version < version:
			sleep(0.5)
			ui.slowPrinting(f"{color.warning}You're Using An Out-dated Version. Please Install Latest Version On Github{color.reset}")
			ui.slowPrinting("Automatically Pick Option [NO] In 10 Seconds.")
			try:
				choice = inputimeout(prompt=f"{color.warning}Do You Want To Update (YES/NO): {color.reset}", timeout=10)
			except TimeoutOccurred:
				choice = "NO"
			if choice.lower() == "yes":
				if open_browser("https://github.com/ahihiyou20/discord-selfbot-owo-bot/archive/refs/heads/main.zip"):
					ui.slowPrinting(f"{color.okgreen}Installed Latest Version In Browser{color.reset}")
				else:
					ui.slowPrinting(f"{color.fail}Failed To Download Latest Version In Browser {color.reset}")
				sleep(2)
				raise SystemExit
