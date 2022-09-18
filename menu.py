import os, time, sys
from version import version
from color import color
class UI:

	@classmethod
	def slowPrinting(cls, text):
		for letter in text:
			time.sleep(.002)
			print(letter, end="", flush=True)
		print("")
	@classmethod
	def logo(cls):
		cls.slowPrinting("░█████╗░░██╗░░░░░░░██╗░█████╗░  ░██████╗███████╗██╗░░░░░███████╗  ██████╗░░█████╗░████████╗")
		cls.slowPrinting("██╔══██╗░██║░░██╗░░██║██╔══██╗  ██╔════╝██╔════╝██║░░░░░██╔════╝  ██╔══██╗██╔══██╗╚══██╔══╝")
		cls.slowPrinting("██║░░██║░╚██╗████╗██╔╝██║░░██║  ╚█████╗░█████╗░░██║░░░░░█████╗░░  ██████╦╝██║░░██║░░░██║░░░")
		cls.slowPrinting("██║░░██║░░████╔═████║░██║░░██║  ░╚═══██╗██╔══╝░░██║░░░░░██╔══╝░░  ██╔══██╗██║░░██║░░░██║░░░")
		cls.slowPrinting("╚█████╔╝░░╚██╔╝░╚██╔╝░╚█████╔╝  ██████╔╝███████╗███████╗██║░░░░░  ██████╦╝╚█████╔╝░░░██║░░░")
		cls.slowPrinting("░╚════╝░░░░╚═╝░░░╚═╝░░░╚════╝░  ╚═════╝░╚══════╝╚══════╝╚═╝░░░░░  ╚═════╝░░╚════╝░░░░╚═╝░░░")
		cls.slowPrinting(f"                                {color.purple}Version: {version}{color.reset}")
		time.sleep(0.5)
		print()

	@classmethod
	def start(cls):
		cls.slowPrinting("╔═══════════════════════════════╗")
		print()
		cls.slowPrinting(f"       {color.purple}[1]{color.reset} Load Data")
		cls.slowPrinting(f"       {color.purple}[2]{color.reset} Create New data")
		cls.slowPrinting(f"       {color.purple}[3]{color.reset} Additional Info")
		cls.slowPrinting(f"       {color.purple}[4]{color.reset} Quit")
		print()
		cls.slowPrinting("╚═══════════════════════════════╝")
	@classmethod
	def newData(cls):
		cls.slowPrinting("╔═══════════════════════════════════════════╗")
		print()
		cls.slowPrinting("         [0] Exit And Save")
		cls.slowPrinting("         [1] Change All Settings")
		cls.slowPrinting("         [2] Change Token")
		cls.slowPrinting("         [3] Change Channel")
		cls.slowPrinting("         [4] Change Pray Mode")
		cls.slowPrinting("         [5] Change Gems Mode")
		cls.slowPrinting("         [6] Change Exp Mode")
		cls.slowPrinting("         [7] Change Sleep Mode")
		cls.slowPrinting("         [8] Change Webhook Settings")
		cls.slowPrinting("         [9] Change Selfbot Commands")
		cls.slowPrinting("         [10] Change Daily Mode")
		cls.slowPrinting("         [11] Change Stop Time")
		cls.slowPrinting(f"         [12] Change Sell Mode")
		cls.slowPrinting("         [13] Change Switch Channel Mode")
		cls.slowPrinting("         [14] Change Solve Captcha")
		print()
		cls.slowPrinting("╚═══════════════════════════════════════════╝")
	@classmethod
	def info(cls):
		cls.slowPrinting(f"{color.purple}╔═════════════════Support════════════════╗{color.reset}")
		cls.slowPrinting(f"\t{color.purple}https://discord.gg/9uZ6eXFPHD{color.reset}")
		cls.slowPrinting(" ")
		cls.slowPrinting(f"{color.purple}╔═══════════════════════════════════════════════════════════════════════════Disclaimer═══════════════════════════════════════════════════════════╗{color.reset}")
		cls.slowPrinting(f"\t{color.purple}This SelfBot Is Only For Education Purpose Only. Deny All Other Promises Or Responsibilities. Use The SelfBot At Your Own Risk.")
		cls.slowPrinting(" ")
		cls.slowPrinting(f'{color.purple}╔═════════════════Credit═════════════════╗{color.reset}')
		cls.slowPrinting(f'\t{color.purple} [Developer] {color.reset} Sudo-Nizel')
		cls.slowPrinting(f'\t{color.purple} [Developer] {color.reset} ahihiyou20')
		cls.slowPrinting(" ")
		cls.slowPrinting(f'{color.purple}╔═════════════════════════Selfbot Commands════════════════════════╗{color.reset}')
		cls.slowPrinting("\t{Prefix}send {Message} [Send Your Provied Message}")
		cls.slowPrinting("\t{Prefix}restart [Restart The Selfbot]")
		cls.slowPrinting("\t{Prefix}exit [Stop The Selfbot]")
		cls.slowPrinting("\t{Prefix}sm {on/off} [Turn On Or Off Sleep Mode]")
		cls.slowPrinting("\t{Prefix}em {on/off} [Turn On Or Off Exp Mode]")
		cls.slowPrinting("\t{Prefix}pm {on/off} [Turn On Or Off Pray Mode]")
		cls.slowPrinting("\t{Prefix}gm {on/off} [Turn On Or Off Gems Mode]")
		cls.slowPrinting("\t{Prefix}gems [Use Gems]")
		cls.slowPrinting(" ")
		cls.slowPrinting("{Prefix} == Your Prefix")
		cls.slowPrinting(" ")
		cls.slowPrinting("Note: Alright If You See Someone Selling This Code Then You Got Scammed Because This Code Is Free!")
		time.sleep(0.5)
		cls.slowPrinting("Press Enter To Exit")
		input()
