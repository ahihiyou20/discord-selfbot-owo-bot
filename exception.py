import sys
from menu import UI
from colorama import init
from color import color
init(convert=True)
ui = UI()
def exception(type, value, tback):
	# manage unhandled exception here
	if type is KeyboardInterrupt:
		return
	ui.slowPrinting(f"{color.fail}[INFO] {color.reset}Unexpected Error Occured")
	with open('exception.txt', 'w'):
		pass
	with open('exception.txt', 'a') as f:
		print(str(type) + "\n", str(value) + "\n", str(tback) + "\n", file=f)
sys.excepthook = exception
