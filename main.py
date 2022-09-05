import requests,threading,sys
from random import choice
from colorama import Fore
from os import system
def clear():
    system('cls')

clear()


count = 0

print(f"{Fore.LIGHTYELLOW_EX}[?] Github View Counter Link: ") #Example View Counter Link: https://camo.githubusercontent.com/4d29071feb1358f324bd018ad789e974f4c5963e91aa6bbc57dec9bb118a67c9/68747470733a2f2f6b6f6d617265762e636f6d2f67687076632f3f757365726e616d653d736561646879
counter_url = input('> ')
print(f"{Fore.LIGHTYELLOW_EX}\n[?] Number of Threads: ")
threads_number = int(input('> '))
print(f"{Fore.LIGHTYELLOW_EX}\n[?] Use a Proxy: (y/n) ")
proxy_use = input('> ')
def run():
    while True:
        headers = {
            "authority": "camo.githubusercontent.com",
            "method": "GET",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "dnt": "1",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "cross-site",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }
        if proxy_use == 'y':
            proxies = open('proxies.txt','r',encoding='utf-8').read().splitlines()
            proxy = choice(proxies)

            proxy_dict = {
                "http": f"http://{proxy}",
                "https": f"https://{proxy}"
            }

            try:
                url = counter_url
                global r
                r = requests.get(url=url,headers=headers,proxies=proxy_dict)
            except requests.exceptions.ProxyError:
                print(f"{Fore.LIGHTRED_EX}[-] Bad Proxy: {proxy}")
            except requests.exceptions.MissingSchema:
                print(f"{Fore.LIGHTRED_EX}[-] Invalid link! Please make sure you enter the correct link.")
                input('')
                exit()
            if r.status_code == 200:
                global count
                count += 1

                print(f"{Fore.LIGHTGREEN_EX}[+] Successful Request! Total Successful Requests Sent: {count}")
            else:
                print(f"{Fore.LIGHTRED_EX}[-] Error Requests.")
        elif proxy_use == 'n':
            try:
                url = counter_url
                global req
                req = requests.get(url=url,headers=headers)
            except requests.exceptions.ProxyError:
                print(f"{Fore.LIGHTRED_EX}[-] Bad Proxy: {proxy}")
            except requests.exceptions.MissingSchema:
                print(f"{Fore.LIGHTRED_EX}[-] Invalid link! Please make sure you enter the correct link.")
                input('')
                exit()
            if req.status_code == 200:
                count += 1

                print(f"{Fore.LIGHTGREEN_EX}[+] Successful Request! Total Successful Requests Sent: {count}")
            else:
                print(f"{Fore.LIGHTRED_EX}[-] Error Requests.")


for i in range(1,threads_number+1):
    print(f"{i} | Thread started.")
    t = threading.Thread(target=run)
    t.start()