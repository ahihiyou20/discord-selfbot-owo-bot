import requests
from os import getcwd
import base64
import time

def file(file_name):
 directory = getcwd()
 filename = directory + "/" + file_name
 url = "https://api.github.com/repos/ahihiyou20/discord-selfbot-owo-bot/contents/source/{}".format(file_name)
 return filename, url

def main():
 filename, url = file('main.py')
 r = requests.get(url)
 if r.status_code == requests.codes.ok:
    req = r.json()
    content = base64.b64decode(req['content'])
    content = content.decode('utf-8')
    f = open(filename, "w", encoding="utf-8")
    f.write(content)
    f.close()
def newdata():
 filename, url = file('newdata.py')
 r = requests.get(url)
 if r.status_code == requests.codes.ok:
    req = r.json()
    content = base64.b64decode(req['content'])
    content = content.decode('utf-8')
    f = open(filename, "w", encoding="utf-8")
    f.write(content)
    f.close()
def settings():
 filename, url = file('settings.json')
 r = requests.get(url)
 if r.status_code == requests.codes.ok:
    req = r.json()
    content = base64.b64decode(req['content'])
    content = content.decode('utf-8')
    f = open(filename, "w", encoding="utf-8")
    f.write(content)
    f.close()
def version():
 filename, url = file('version.txt')
 r = requests.get(url)
 if r.status_code == requests.codes.ok:
    req = r.json()
    content = base64.b64decode(req['content'])
    content = content.decode('utf-8')
    f = open(filename, "w", encoding="utf-8")
    f.write(content)
    f.close()
def requirements():
 filename, url = file('requirements.txt')
 r = requests.get(url)
 if r.status_code == requests.codes.ok:
    req = r.json()
    content = base64.b64decode(req['content'])
    content = content.decode('utf-8')
    f = open(filename, "w", encoding="utf-8")
    f.write(content)
    f.close()
def setup():
 filename, url = file('setup.py')
 r = requests.get(url)
 if r.status_code == requests.codes.ok:
    req = r.json()
    content = base64.b64decode(req['content'])
    content = content.decode('utf-8')
    f = open(filename, "w", encoding="utf-8")
    f.write(content)
    f.close()

main()
newdata()
settings()
version()
requirements()
setup()
print("Successfuly Updated All Files!")
time.sleep(2)
