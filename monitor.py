import requests
import random
import threading
import os
import json
import sys
import time
import task
from termcolor import colored
from playsound import playsound
import setProxy

link = ""
proxies = setProxy.setProxies()

def monitor(index, start, end, pf):
    site = link.split('/')
    site = site[2]

    while True:
        try:
            s = requests.Session()
            s.proxies = proxies[index]
            r = requests.get(link + ".js")
            r = r.json()
            break
        except:
            print(colored("Task [" + str(index) + "] \tPage Unavailable", "red"))
            return
            
    restock = []
    size = []
    
    for i in range(start,end):
          restock.append(r["variants"][i])

    for i in restock:
        tf = i['available']
        title = i['title']
        size.append(str(title))
        id = i['id']
        p = str(title) + " - " + str(tf) + " : " + str(id)
        if tf == True:
            print(colored("Task [" + str(index) + "] \tFound Product! Size " + str(title), 'blue'))
            playsound('sound/found.wav')
            task.startTask(index, site, str(id), proxies[index], pf)
    print(colored("Task [" + str(index) + "] \tWaiting For Restock " + size[0] + " - " + size[-1], 'white'))

def Start(start, end, pf):
    monitor(random.randrange(0,len(proxies)), start, end, pf)
    time.sleep(1)

def main(l, s, e, pf):
    os.system('cls||clear')
    global link
    link = str(l)
    start = int(s)
    end = int(e)

    while True:
        Start(start, end, pf)

if __name__ == "__main__":
	main()
