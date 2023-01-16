import requests
import random
import os
import time
from colorama import Fore
from logs import Logger
import ctypes
import fade
os.system('cls')
from datetime import datetime, timedelta

log = Logger()

checked = 0
valid = 0
invalid = 0
nitro_tokens = 0


def Title():
    ctypes.windll.kernel32.SetConsoleTitleW(f"Nitro Checker | Checked: {checked} | Valid: {valid} | Invalid: {invalid} | Nitro: {nitro_tokens}")

Title()


def CenterText(var:str, space:int=None):
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())


def get_proxies():
    apis = ['https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt','https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt']
    api = random.choice(apis)
    try:
        r = requests.get(api)
        with open('proxies.txt','wb')as nig:
            nig.close()
        os.remove('proxies.txt')
        with open('proxies.txt','wb')as f:
            f.write(r.content)
            i =  r.content.splitlines()
            log.Success(f"Fetched {len(i)} Proxies")
    except:
        log.Error("Failed to Fetch Proxies")

log.Info("Auto Fetching Proxies")
get_proxies()
time.sleep(1)
os.system('cls')
# def check_type(token : None):
#     url = "https://discord.com/api/v9/users/@me"
#     headers = {"Authorization": token}
#     r = requests.get(url, headers=headers)
#     s = r.json()
#     premium_type = s['premium_type']
#     if premium_type == 0:
#         return 0
#     elif premium_type == 1:
#         return 1
#     elif premium_type == 2:
#         return 2


# def sub_id(token : None):
#     headers = {"Authorization": token}
#     r = requests.get('https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots',headers=headers)
#     re = r.json()
#     for i in re:
#         s = i['subscription_id']
#         return s

promxies = open('proxies.txt','r',encoding='utf-8').read().splitlines()

def get_proxy(): #formats the proxy and returns json string
    proxy = random.choice(promxies)
    proxies = {
        "http://": f"http://{proxy}",
        "https://": f"http://{proxy}"
        }
    return proxies

def remove_token(arg : None):
        with open('tokens.txt', "r") as f:
            lines = f.readlines()
        with open('tokens.txt', "w") as f:
            for line in lines:
                if line.strip("\n") != arg:
                    f.write(line)


def check_token(tk : None):
    global valid
    global invalid
    global checked
    global nitro_tokens
    idk = tk.strip()
    proxies = get_proxy()
    r = requests.get(f"https://discord.com/api/v9/users/@me", headers={"authorization": idk} , proxies=proxies)
    if r.status_code == 200:
        nig = r.json()
        if nig['premium_type'] != 2:
            log.Warning(f"No Nitro | Token {tk[:20]} is Valid But Has No Nitro Booster, Removing...")
            remove_token(idk)
            invalid+=1
            checked+=1
            Title()
        else:
            log.Success("Nitro Token" + " | "f"{tk[:20]}*********** is Valid")
            valid+=1
            nitro_tokens+=1
            checked+=1
            Title()
    elif r.status_code == 429:
        time.sleep(1)
        check_token(tk=idk)
    else:
        log.Error(f"Invalid Token | Token {tk[:20]} is Invalid, Removing ...")
        invalid +=1
        checked+=1
        Title()
        remove_token(idk)



def time_check(token):
    headers = {'Authorization': token}
    url2 = 'https://discord.com/api/v9/users/@me/billing/subscriptions'
    r2 = requests.get(url2,headers=headers).json()
    for i in r2:
        st = i['created_at'][:10]
        se = st.split('-')
        month_st = int(se[1])
        end = i['current_period_end'][:10]
        ee = end.split('-')
        end_st = int(ee[1])
        am = end_st - month_st
        end_trial = datetime.strptime(i['current_period_end'], "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%d/%m/%Y")
        log.Info(f"Nitro {am}m |  Token : {token[:20]} | Trial Ends on : {end_trial}")
        open(f"{am}-month.txt", "a").write(token + "\n")


tokens = open("tokens.txt",'r').read().splitlines()
amount = len(tokens)
print(Fore.MAGENTA + "Nitro Token Checker" + Fore.RESET)
log.Info(f"Checking tokens")
log.Info(f"Total : " + str(amount))

for i in tokens:
    token = i.strip()
    check_token(tk = token)
    
log.Info(f'Sorting Tokens')
for i in tokens:
    token = i.strip()
    time_check(token)


print()
print()
print("Nitro tokens : " + str(nitro_tokens))
print("Total Checked  : " + str(checked))
print("Valid  : " + str(valid))
print("Invalid : " + str(invalid))
