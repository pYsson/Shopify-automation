import monitor
import os
import webhook
import requests
import threading
import json
import sys
import time
import task
from termcolor import colored
from pyfiglet import Figlet


def extract(link):
    print("")
    r = requests.get(link + ".js")
    r = r.json()

    index = 0
    for i in r['variants']:
        tf = i['available']
        size = i['title']
        variant = i['id']
        p = str(size) + " - " + str(tf) + " : " + str(variant)
        if tf == True:
            print("\t[" + str(index) + "]", end=' ')
            print(colored(p, 'green'))
        else:
            print("\t[" + str(index) + "]", end=' ')
            print(colored(p, 'red'))
        index += 1
    print("")


def main():
    while True:
        os.system('cls||clear')
        f = Figlet(font='slant')
        print(f.renderText('    pYsson'))
        print(colored("\t1. Launch Task", 'yellow'))
        print(colored("\t2. Setting Webhook", 'yellow'))
        print(colored("\t3. Test Webhook", 'yellow'))
        print(colored("\t4. Quit Bot\n", 'yellow'))
        launch = int(input(colored("\tinput: ", 'yellow')))

        if launch == 1:
            os.system('cls||clear')
            print(f.renderText('    pYsson'))
            print(colored("\t1. Shopify", 'yellow'))
            select = int(input("\n\tinput: "))
            if select == 1:
              os.system('cls||clear')
              print(f.renderText('    pYsson'))
              link = input("\tlink: ")
              extract(link)
              size_s = input("\tsize_start: ")
              size_e = input("\tsize_end: ")
              os.system('cls||clear')
              profile_dir = "./profile"
              file_list = os.listdir(profile_dir)
              length = len(file_list)
              for i in range(0,length):
                l = "\t" + str(i+1) + ". "
                l = l + str(file_list[i].replace('.json', ''))
                print(l)
              print("")
              selected_profile = input("\tinput: ")
              monitor.main(link, size_s, int(size_e) + 1, file_list[i])
        elif launch == 2:
            os.system('cls||clear')
            webhook_link = input("webhook link: ")
            with open('setting.json', 'w', encoding='utf-8') as f:
                setting = {'webhook': webhook_link}
                json.dump(setting, f)
        elif launch == 3:
            os.system('cls||clear')
            print("Sending Test Webhook")
            time.sleep(2)
            webhook.test()
        elif launch == 4:
            os.system('cls||clear')
            return


if __name__ == "__main__":
    main()
