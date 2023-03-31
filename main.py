import os
import json
import threading
from os import system
from time import sleep
from random import choice

try:
    from colorama import Fore

except ModuleNotFoundError:
    print('[>] Modules not found! Installing, please wait...')
    os.system('pip install -r requirements.txt')
    os.system('cls')
    print('[>] Download successfuly complated! The booster will start in 3 seconds.')
    import httpx
    from colorama import Fore

    sleep(3)

config_file = json.load(open('config.json', 'r', encoding='utf-8'))
lock = threading.Lock()


# * Define Functions *#

def clear():
    system('cls')


def safe_print(*args):
    lock.acquire()
    for arg in args: print(arg, end=' ')
    print()
    lock.release()


def run():
    while True:
        if use_proxy == 'y' or use_proxy == 'yes':
            proxies = open('proxies.txt', 'r', encoding='utf-8').read().splitlines()
            proxy = choice(proxies)

            proxy_dict = {
                "http://": f"http://{proxy}",
                "https://": f"http://{proxy}"
            }

            try:
                url = counter_url
                global r
                r = httpx.get(url=url, proxies=proxy_dict, timeout=10)
            except httpx.ProxyError:
                safe_print(f"{Fore.LIGHTRED_EX}[-] Bad proxy: {proxy}")
                proxies.remove(proxy)
                continue
            except httpx.ConnectError:
                safe_print(f"{Fore.LIGHTRED_EX}[-] Connect Error proxy: {proxy}")
                continue
            except httpx.RemoteProtocolError:
                safe_print(f"{Fore.LIGHTRED_EX}[-] Remote Protocol Error, Retrying...")
                continue
            except httpx.ConnectTimeout:
                safe_print(f"{Fore.LIGHTRED_EX}[-] Connect Timeout proxy: {proxy}")
                continue
            except httpx.ReadTimeout:
                safe_print(f"{Fore.LIGHTRED_EX}[-] Read Timeout proxy: {proxy}")
                continue
            except ValueError:
                safe_print(
                    f"{Fore.LIGHTRED_EX}[-] Please change the 'counter_url' with a valid camo url in 'config.json'")
                break
            if r.status_code == 200:
                global count
                count += 1
                safe_print(f"{Fore.LIGHTGREEN_EX}[+] Successful request! Total successful requests sent: {count}")

            elif 'Bad Signature' in r.text:
                safe_print(
                    f"{Fore.LIGHTRED_EX}[-] Invalid Camo Link! Please change valid link. Example Camo Link: https://camo.githubusercontent.com/4d29071feb1358f324bd018ad789e974f4c5963e91aa6bbc57dec9bb118a67c9/68747470733a2f2f6b6f6d617265762e636f6d2f67687076632f3f757365726e616d653d736561646879")
                break
            else:
                safe_print(f"{Fore.LIGHTRED_EX}[-] Error request.")

        elif use_proxy == 'n' or use_proxy == 'no':
            try:
                url = counter_url
                global req
                req = httpx.get(url=url, timeout=10)

            except httpx.ConnectTimeout:
                safe_print(f"{Fore.LIGHTRED_EX}[-] Timeout error.")
                continue

            if req.status_code == 200:
                count += 1

                safe_print(f"{Fore.LIGHTGREEN_EX}[+] Successful request! Total successful requests sent: {count}")

            elif 'Bad Signature' in req.text:
                safe_print(
                    f"{Fore.LIGHTRED_EX}[-] Invalid Camo Link! Please change valid link. Example Camo Link: https://camo.githubusercontent.com/4d29071feb1358f324bd018ad789e974f4c5963e91aa6bbc57dec9bb118a67c9/68747470733a2f2f6b6f6d617265762e636f6d2f67687076632f3f757365726e616d653d736561646879")
                break
            else:
                # safe_print(req.text)
                safe_print(f"{Fore.LIGHTRED_EX}[-] Error request.")


# * Run Booster * #

clear()
count = 0

if __name__ == "__main__":
    counter_url = config_file['counter_url']
    threads = config_file['threads']
    use_proxy = config_file['use_proxy']

    for i in range(1, threads + 1):
        # print(f"{i} | Thread started.")
        t = threading.Thread(target=run).start()
