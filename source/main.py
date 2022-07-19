from colorama import init
import os
init()
from sys import *
import time
import requests
import atexit
from multiprocessing import Process, Pool
import random
import re
import base64
try:
 from inputimeout import inputimeout,TimeoutOccurred
except:
 from setup import install
 install()
 from inputimeout import inputimeout, TimeoutOccurred
import json
try:
  from discum import *
except:
  from setup import install
  install()
  from discum import *
try:
 from discord_webhook import DiscordWebhook
except:
 from setup import install
 install()
 from discum_webhook import DiscordWebhook
print("""\
░█████╗░░██╗░░░░░░░██╗░█████╗░  ░██████╗███████╗██╗░░░░░███████╗  ██████╗░░█████╗░████████╗
██╔══██╗░██║░░██╗░░██║██╔══██╗  ██╔════╝██╔════╝██║░░░░░██╔════╝  ██╔══██╗██╔══██╗╚══██╔══╝
██║░░██║░╚██╗████╗██╔╝██║░░██║  ╚█████╗░█████╗░░██║░░░░░█████╗░░  ██████╦╝██║░░██║░░░██║░░░
██║░░██║░░████╔═████║░██║░░██║  ░╚═══██╗██╔══╝░░██║░░░░░██╔══╝░░  ██╔══██╗██║░░██║░░░██║░░░
╚█████╔╝░░╚██╔╝░╚██╔╝░╚█████╔╝  ██████╔╝███████╗███████╗██║░░░░░  ██████╦╝╚█████╔╝░░░██║░░░
░╚════╝░░░░╚═╝░░░╚═╝░░░╚════╝░  ╚═════╝░╚══════╝╚══════╝╚═╝░░░░░  ╚═════╝░░╚════╝░░░░╚═╝░░░

**Version: 1.0.2**""")
print("Alright! If You See Someone Selling This Code Then He/She Is Scamming [READ INFO]")
wbm=[13,16]
class client:
  commands=[
    "owo hunt",
    "owo hunt",
    "owo battle"
    ]
  totalcmd = 0
  totaltext = 0
  stopped = False
  recentversion = "1.0.2"
  wait_time_daily = 60
  channel2 = []
  class color:
    purple = '\033[95m'
    okblue = '\033[94m'
    okcyan = '\033[96m'
    okgreen = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    reset = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
  with open('settings.json', "r") as file:
        data = json.load(file)
        token = data["token"]
        channel = data["channel"]
        gm = data["gm"]
        sm = data["sm"]
        pm = data["pm"]
        em = data["em"]
        prefix = data["prefix"]
        allowedid = data["allowedid"]
        webhook = data["webhook"]
        webhookping = data["webhookping"]
        daily = data["daily"]
        stop = data["stop"]
        change = data['change']
        sell = data['sell']
        solve = data['solve']
  if data["token"] and data["channel"] == 'nothing':
   print(f"{color.fail} !!! [ERROR] !!! {color.reset} Please Enter Information To Continue")
   time.sleep(2)
   from newdata import menu
   menu()
   os.execl(executable, executable, *argv)
  response = requests.get("https://api.github.com/repos/ahihiyou20/discord-selfbot-owo-bot/releases/latest")
  if recentversion in response.json()["name"]:
    print(f"{color.warning}Checking Update... {color.reset}")
    time.sleep(0.5)
    print(f"{color.okgreen}No Update Available {color.reset}")
  else:
   print(f"{color.warning}Checking Update... {color.reset}")
   time.sleep(0.5)
   print(f"{color.warning}Update Available {color.reset}")
   print(f"{color.purple}Update Info:{color.reset}")
   time.sleep(0.5)
   print(response.json()["name"])
   print(response.json()["body"])
   choice = input(f"{color.warning}Do You Want To Update (YES/NO): {color.reset}")
   if choice.lower() == "yes":
    import update
   else:
    pass
  print('=========================')
  print('|                       |')
  print(f'| [1] {color.purple}Load data         {color.reset}|')
  print(f'| [2] {color.purple}Create new data   {color.reset}|')
  print(f'| [3] {color.purple}Info              {color.reset}|')
  print('=========================')
try:
 print("Automatically Pick Option [1] In 10 Seconds.")
 choice = inputimeout(prompt='Enter Your Choice: ', timeout=10)
except TimeoutOccurred:
 choice = "1"
if choice == "1":
      pass
elif choice == "2":
 from newdata import menu
 menu()
elif choice == "3":
      print(f"{client.color.purple} =========Support========== {client.color.reset}")
      print(f"{client.color.purple}https://discord.gg/9uZ6eXFPHD{client.color.reset}")
      print(" ")
      print(f"{client.color.purple} =========Disclaimer========={client.color.reset}")
      print(f"{client.color.purple}This SelfBot Is Only For Education Purpose Only. Deny All Other Promises Or Responsibilities. Use The SelfBot At Your Own Risk.")
      print(" ")
      print(f'{client.color.purple} =========Credit=========={client.color.reset}')
      print(f'{client.color.purple} [Developer] {client.color.reset} Sudo-Nizel')
      print(f'{client.color.purple} [Developer] {client.color.reset} ahihiyou20')
      print(" ")
      print(f'{client.color.purple} =========Selfbot Commands=========={client.color.reset}')
      print("{Prefix}send {Message} [Send Your Provied Message}")
      print("{Prefix}restart [Restart The Selfbot]")
      print("{Prefix}exit [Stop The Selfbot]")
      print("{Prefix}sm {on/off} [Turn On Or Off Sleep Mode]")
      print("{Prefix}em {on/off} [Turn On Or Off Exp Mode]")
      print("{Prefix}pm {on/off} [Turn On Or Off Pray Mode]")
      print("{Prefix}gm {on/off} [Turn On Or Off Gems Mode]")
      print("{Prefix}gems [Use Gems]")
      print(" ")
      print("{Prefix} == Your Prefix")
      print(" ")
      print("Note: Alright If You See Someone Selling This Code Then You Got Scammed Because This Code Is Free!")
      time.sleep(1)
      print("Press Enter To Exit")
      input()
      raise SystemExit
else:
 print(f'{client.color.fail} !! [ERROR] !! {client.color.reset} Wrong input!')
 time.sleep(1)
 os.execl(executable, executable, *argv)
def at():
  return f'\033[0;43m{time.strftime("%d %b %Y %H:%M:%S", time.localtime())}\033[0;21m'
bot = discum.Client(token=client.token, build_num=5, log={'console': False, 'file': 'logs.txt', 'encoding': 'utf-8'}, user_agent=[
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36/PAsMWa7l-11',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.7.2) Gecko/20100101 / Firefox/60.7.2'])
if False in bot.checkToken(client.token):
  print(f"{client.color.fail}[ERROR]{client.color.reset} Invalid Token")
  time.sleep(2)
  raise SystemExit
@bot.gateway.command
def on_ready(resp):
    if resp.event.ready_supplemental: #ready_supplemental is sent after ready
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
@bot.gateway.command
def security(resp):
 if client.webhook != 'None':
  if issuechecker(resp) == "captcha":
    client.stopped = True
    user = bot.gateway.session.user
    if client.webhookping != 'None':
     sentwebhook = DiscordWebhook(url=client.webhook, content='<@{}> I Found A Captcha In Channel: <#{}>'.format(client.webhookping,client.channel))
     response = sentwebhook.execute()
     bot.gateway.close()
    else:
     sentwebhook = DiscordWebhook(url=client.webhook, content='<@{}> <@{}> I Found A Captcha In Channel: <#{}>'.format(user['id'],client.allowedid,client.channel))
     response = sentwebhook.execute()
     bot.gateway.close()
 if client.webhook == 'None':
  if issuechecker(resp) == "captcha":
   client.stopped = True
   bot.gateway.close()
@bot.gateway.command
def issuechecker(resp):
 try:
  if client.solve.lower() != "no":
   i = 0
   length = len(bot.gateway.session.DMIDs)
   while i < length:
    if '408785106942164992' in bot.gateway.session.DMs[bot.gateway.session.DMIDs[i]]['recipients']:
     dmsid = bot.gateway.session.DMIDs[i]
     i = length
    else:
     i += 1
 except KeyError:
  pass
 def solve(image_url):
  img_data = requests.get(image_url).content
  with open('captcha.png', 'wb') as handler:
   handler.write(img_data)
  with open('captcha.png', "rb") as image_file:
   encoded_string = base64.b64encode(image_file.read())
  data = { 'userid':'hoanghaianh', 'apikey':'5JzPnvYKF7iyHGIBYBXG', 'data': str(encoded_string)[2:-1], 'case': 'mixed'}
  r = requests.post(url = 'https://api.apitruecaptcha.org/one/gettext', json = data)
  j = json.loads(r.text)
  print(f"{client.color.okcyan}[INFO] {client.color.reset}Solved Captcha [Code: {j['result']}]")
  bot.sendMessage(dmsid, j['result'])
 if resp.event.message:
   m = resp.parsed.auto()
   if m['channel_id'] == client.channel or m['channel_id'] == dmsid if client.solve.lower() != "no" else False and client.stopped != True:
    if m['author']['id'] == '408785106942164992' or m['author']['username'] == 'OwO' or m['author']['discriminator'] == '8456' or m['author']['public_flags'] == '65536':
     if 'solving the captcha' in m['content'].lower():
       print(f'{at()}{client.color.warning} !! [CAPTCHA] !! {client.color.reset} CAPTCHA   ACTION REQUİRED')
       if client.solve.lower() != "no":
         solve(m['attachments'][0]['url'])
       return "captcha"
     if 'banned' in m['content'].lower():
       print(f'{at()}{client.color.fail} !!! [BANNED] !!! {client.color.reset} your account have been banned from owo bot please open a issue on the Support Discord server')
       return "captcha"
     if 'are you a real human'  in m['content'].lower():
       print(f'{at()}{client.color.warning} !! [CAPTCHA] !! {client.color.reset} CAPTCHA   ACTION REQUİRED')
       if client.solve.lower() != "no":
         solve(m['attachments'][0]['url'])
       return "captcha"
     def change_channel():
       if client.change.lower() == "yes":
         client.channel2 = []
         guild = bot.gateway.session.guild(m['guild_id']).channels
         channel = guild.keys()
         channel2 = random.choice(list(channel))
         try:
          if guild[channel2]['type'] == "guild_text":
            client.channel2.append(channel2)
            client.channel2.append(guild[channel2]['name'])
          else:
            change_channel()
         except RecursionError:
            client.channel2.append(channel2)
            client.channel2.append(guild[channel2]['name'])
     change_channel()
def runner():
        global wbm
        command=random.choice(client.commands)
        command2=random.choice(client.commands)
        bot.typingAction(str(client.channel))
        bot.sendMessage(str(client.channel), command)
        print(f"{at()}{client.color.okgreen} [SENT] {client.color.reset} {command}")
        client.totalcmd += 1
        if not command2==command and client.stopped != True:
          bot.typingAction(str(client.channel))
          time.sleep(13)
          bot.sendMessage(str(client.channel), command2)
          print(f"{at()}{client.color.okgreen} [SENT] {client.color.reset} {command2}")
          client.totalcmd += 1
        time.sleep(random.randint(wbm[0],wbm[1]))
def owoexp():
  if client.em.lower() == "yes":
        try:
         response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random")
         if response.status_code == 200:
           json_data = response.json()
           data = json_data['data']
           bot.sendMessage(str(client.channel), data[0]['quoteText'])
           client.totaltext += 1
           time.sleep(random.randint(1,6))
        except:
           pass
def owopray():
  if client.pm.lower() == "yes":
   if client.stopped != True:
    bot.sendMessage(str(client.channel), "owo pray")
    print(f"{at()}{client.color.okgreen} [SENT] {client.color.reset} owo pray")
    client.totalcmd += 1
    time.sleep(random.randint(13,18))
@bot.gateway.command
def gems2(resp):
   if client.gm.lower() == "yes":
    if resp.event.message:
      m = resp.parsed.auto()
      if m['channel_id'] == client.channel and client.stopped != True:
       if m['author']['id'] == '408785106942164992' or m['author']['username'] == 'OwO' or m['author']['discriminator'] == '8456' or m['author']['public_flags'] == '65536':
        if m['content'] != "" and m['embeds'] == [] and "hunt" in m['content']:
         if not "empowered" in m['content']:
           gems1()
         else:
            if '[0/' in m['content']:
             time.sleep(13)
             bot.sendMessage(str(client.channel), "owo hunt")
             gems1()
def gems1():
    bot.typingAction(str(client.channel))
    time.sleep(3)
    bot.sendMessage(str(client.channel), "owo inv")
    print(f"{at()}{client.color.okgreen} [SENT] {client.color.reset} owo inv")
    client.totalcmd += 1
    time.sleep(4)
    msgs=bot.getMessages(str(client.channel), num=5)
    msgs=json.loads(msgs.text)
    inv = 0
    length = len(msgs)
    i = 0
    while i < length:
     if msgs[i]['author']['id']=='408785106942164992' and 'Inventory' in msgs[i]['content']:
        inv=re.findall(r'`(.*?)`', msgs[i]['content'])
        i = length
     else:
        i += 1
    if not inv:
       time.sleep(5)
       client.totalcmd -= 1
       gems1()
    else:
      if '050' in inv:
        bot.sendMessage(str(client.channel), "owo lb all")
        print(f"{at()}{client.color.okgreen} [SENT] {client.color.reset} owo lb all")
        time.sleep(13)
        gems1()
      if '100' in inv:
        bot.sendMessage(str(client.channel), "owo crate all")
        print(f"{at()}{client.color.okgreen} [SENT] {client.color.reset} owo crate all")
        time.sleep(2)
      for item in inv:
        try:
          if int(item) >= 100 or int(item) <= 50:
            inv.pop(inv.index(item)) #weapons
        except: #backgounds etc
          inv.pop(inv.index(item))
      tier = [[],[],[]]
      print(f"{at()}{client.color.okblue} [INFO] {client.color.reset} Found {len(inv)} gems Inventory")
      for gem in inv:
        gem = re.sub(r"[^a-zA-Z0-9]", "", gem)
        gem = int(gem)
        if 50 < gem < 58:
          tier[0].append(gem)
        elif 64 < gem < 72:
          tier[1].append(gem)
        elif 71 < gem <  79:
          tier[2].append(gem)
      for level in range(3):
        if not len(tier[level]) == 0:
          time.sleep(5)
          bot.sendMessage(str(client.channel), "owo use "+str(max(tier[level])))
          print(f"{at()}{client.color.okgreen} [SENT] {client.color.reset} owo use {str(max(tier[level]))}")
def daily():
 if client.daily.lower() == "yes" and client.stopped != True:
    bot.typingAction(str(client.channel))
    time.sleep(3)
    bot.sendMessage(str(client.channel), "owo daily")
    print(f"{at()}{client.color.okgreen} [SENT] {client.color.reset} owo daily")
    client.totalcmd += 1
    time.sleep(3)
    msgs=bot.getMessages(str(client.channel), num=5)
    msgs=json.loads(msgs.text)
    daily = ""
    length = len(msgs)
    i = 0
    while i < length:
     if msgs[i]['author']['id']=='408785106942164992' and msgs[i]['content'] != "" and "Nu" or "daily" in msgs[i]['content']:
        daily = msgs[i]['content']
        i = length
     else:
        i += 1
    if not daily:
       time.sleep(5)
       client.totalcmd -= 1
       daily()
    else:
       if "Nu" in daily:
         daily = re.findall('[0-9]+', daily)
         client.wait_time_daily = str(int(daily[0]) * 3600 + int(daily[1]) * 60 + int(daily[2]))
         print(f"{at()}{client.color.okblue} [INFO] {client.color.reset} Next Daily: {client.wait_time_daily}s")
       if "Your next daily" in daily:
         print(f"{at()}{client.color.okblue} [INFO] {client.color.reset} Claimed Daily")
def sell():
 if client.sell != "None" and client.stopped != True:
    msgs=bot.getMessages(str(client.channel), num=10)
    msgs=json.loads(msgs.text)
    length = len(msgs)
    i = 0
    while i < length:
     if msgs[i]['author']['id']=='408785106942164992' and msgs[i]['content'] != "" and "You found" or "I AM BACK WITH" in msgs[i]['content']:
        i = length
     else:
       if not i == length:
        i += 1
       else:
        sell()
    if client.sell == "all":
          bot.typingAction(str(client.channel))
          time.sleep(3)
          bot.sendMessage(str(client.channel), "owo sell all")
          print(f"{at()}{client.color.okgreen} [SENT] {client.color.reset} owo sell all")
    else:
          bot.typingAction(str(client.channel))
          time.sleep(3)
          bot.sendMessage(str(client.channel), "owo sell {}".format(client.sell))
          print(f"{at()}{client.color.okgreen} [SENT] {client.color.reset} owo sell {client.sell}")
@bot.gateway.command
def othercommands(resp):
 prefix = client.prefix
 file = open("settings.json", "r")
 data = json.load(file)
 file.close()
 if resp.event.message:
   m = resp.parsed.auto()
   if m['author']['id'] == bot.gateway.session.user['id'] or m['channel_id'] == client.channel and m['author']['id'] == client.allowedid:
    if prefix == "None":
     bot.gateway.removeCommand(othercommands)
     return
    if "{}send".format(prefix) in m['content'].lower():
     message = m['content'].replace(f'{prefix}send ', '')
     bot.sendMessage(str(m['channel_id']), message)
     print(f"{at()}{client.color.okgreen} [SENT] {client.color.reset} {message}")
    if "{}restart".format(prefix) in m['content'].lower():
     bot.sendMessage(str(m['channel_id']), "Restarting...")
     print(f"{client.color.okcyan} [INFO] Restarting...  {client.color.reset}")
     time.sleep(1)
     os.execl(executable, executable, *argv)
    if "{}exit".format(prefix) in m['content'].lower():
     bot.sendMessage(str(m['channel_id']), "Exiting...")
     print(f"{client.color.okcyan} [INFO] Exiting...  {client.color.reset}")
     bot.gateway.close()
    if "{}gm".format(prefix) in m['content'].lower():
     if "on" in m['content'].lower():
      client.gm = "YES"
      bot.sendMessage(str(m['channel_id']), "Turned On Gems Mode")
      print(f"{client.color.okcyan}[INFO] Turned On Gems Mode{client.color.okcyan}")
      file = open("settings.json", "w")
      data['gm'] = "YES"
      json.dump(data, file)
      file.close()
     if "off" in m['content'].lower():
      client.gm = "NO"
      bot.sendMessage(str(m['channel_id']), "Turned Off Gems Mode")
      print(f"{client.color.okcyan}[INFO] Turned Off Gems Mode{client.color.okcyan}")
      file = open("settings.json", "w")
      data['gm'] = "NO"
      json.dump(data, file)
      file.close()
    if "{}pm".format(prefix) in m['content'].lower():
      if "on" in m['content'].lower():
       client.pm = "YES"
       bot.sendMessage(str(m['channel_id']), "Turned On Pray Mode")
       print(f"{client.color.okcyan}[INFO] Turned On Pray Mode{client.color.reset}")
       file = open("settings.json", "w")
       data['pm'] = "YES"
       json.dump(data, file)
       file.close()
      if "off" in m['content'].lower():
       client.pm = "NO"
       bot.sendMessage(str(m['channel_id']), "Turned Off Pray Mode")
       print(f"{client.color.okcyan}[INFO] Turned Off Pray Mode{client.color.reset}")
       file = open("settings.json", "w")
       data['pm'] = "NO"
       json.dump(data, file)
       file.close()
    if "{}sm".format(prefix) in m['content'].lower():
      if "on" in m['content'].lower():
       client.sm = "YES"
       bot.sendMessage(str(m['channel_id']), "Turned On Sleep Mode")
       print(f"{client.color.okcyan}[INFO] Turned On Sleep Mode{client.color.reset}")
       file = open("settings.json", "w")
       data['sm'] = "YES"
       json.dump(data, file)
       file.close()
      if "off" in m['content'].lower():
       client.sm = "NO"
       bot.sendMessage(str(m['channel_id']), "Turned Off Sleep Mode")
       print(f"{client.color.okcyan}[INFO] Turned Off Sleep Mode{client.color.reset}")
       file = open("settings.json", "w")
       data['sm'] = "NO"
       json.dump(data, file)
       file.close()
    if "{}em".format(prefix) in m['content'].lower():
      if "on" in m['content'].lower():
       client.em = "YES"
       bot.sendMessage(str(m['channel_id']), "Turned On Exp Mode")
       print(f"{client.color.okcyan}[INFO] Turned On Exp Mode{client.color.reset}")
       file = open("settings.json", "w")
       data['em'] = "YES"
       json.dump(data, file)
       file.close()
      if "off" in m['content'].lower():
       client.em = "NO"
       bot.sendMessage(str(m['channel_id']), "Turned Off Exp Mode")
       print(f"{client.color.okcyan}[INFO] Turned Off Exp Mode{client.color.reset}")
       file = open("settings.json", "w")
       data['em'] = "NO"
       json.dump(data, file)
       file.close()
    if "{}sell".format(prefix) in m['content'].lower():
       client.sell = m['content'].replace(f'{prefix}sell ', '').lower()
       print(f"{client.color.okcyan}[INFO] Turned On Sell Mode [{client.sell}]{client.color.reset}")
       bot.sendMessage(str(m['channel_id']), f"Turned On Gems Mode [{client.sell}]")
       file = open("settings.json", "w")
       data['sell'] = client.sell
       json.dump(data, file)
       file.close()
    if "{}gems".format(prefix) in m['content'].lower():
       gems1()
@bot.gateway.command
def loopie(resp):
 if resp.event.ready:
  x=True
  pray = 0
  owo=pray
  selltime=pray
  daily_time = pray
  main=time.time()
  stop=main
  change = main
  while x:
    if client.stopped == True:
       break
    if client.stopped != True:
      runner()
      if time.time() - pray > random.randint(300, 600) and client.stopped != True:
        owopray()
        pray=time.time()
      if time.time() - owo > random.randint(10, 20) and client.stopped != True:
        owoexp()
        owo=time.time()
      if client.sm.lower() == "yes":
       if time.time() - main > random.randint(600, 1000) and client.stopped != True:
        main=time.time()
        print(f"{at()}{client.color.okblue} [INFO]{client.color.reset} Sleeping")
        time.sleep(random.randint(400, 600))
      if time.time() - daily_time > int(client.wait_time_daily) and client.stopped != True:
        daily()
        daily_time = time.time()
      if client.stop.lower() == "yes" and client.stopped != True:
       if time.time() - stop > int(client.stop):
         bot.gateway.close()
      if client.change.lower() == "yes" and client.stopped != True:
        if time.time() - change > random.randint(600,1500):
         change=time.time()
         print(f"{at()}{client.color.okblue} [INFO] {client.color.reset} Changed Channel To: {client.channel2[1]}")
         client.channel = client.channel2[0]
      if client.sell != "None" and client.stopped != True:
        if time.time() - selltime > random.randint(600,1000):
         selltime=time.time()
         sell()
def defination1():
  global once
  if not once:
    once=True
    if __name__ == '__main__':
      lol2= Pool(os.cpu_count() - 1)
      lol2.map(loopie)
      lol=Process(target=loopie)
      lol.run()
bot.gateway.run(auto_reconnect=True)
@atexit.register
def atexit():
 print(f"{client.color.okgreen}Total Number Of Commands Executed: {client.totalcmd}{client.color.reset}")
 time.sleep(0.5)
 print(f"{client.color.okgreen}Total Number Of Random Text Sent: {client.totaltext}{client.color.reset}")
 time.sleep(0.5)
 print(f"{client.color.purple} [1] Restart {client.color.reset}")
 print(f"{client.color.purple} [2] Support {client.color.reset}")
 print(f"{client.color.purple} [3] Exit    {client.color.reset}")
 try:
  print("Automatically Pick Option [3] In 10 Seconds.")
  choice = inputimeout(prompt='Enter Your Choice: ', timeout=10)
 except TimeoutOccurred:
  choice = "3"
 if choice == "1":
  os.execl(executable, executable, *argv)
 elif choice == "2":
  print("Having Issue? Tell Us In Our Support Server")
  print(f"{client.color.purple} https://discord.gg/9uZ6eXFPHD {client.color.reset}")
 elif choice == "3":
  bot.gateway.close()
 else:
  bot.gateway.close()
