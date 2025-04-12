#################################
############# Made By TheAxes #######
### Leave credits if u use any snippet ###



























import requests
import httpx
import tls_client
import time
from captcha_solver import Hcaptcha_Solver, ImageToTextSolver
import json
from colorama import Fore

    

# By Youtube.com/@theaxes
with open('config.json') as f:
    config = json.load(f)
token = config['token']
hservice = config['captcha']['hcaptcha_service'].lower()
api_key = api_key = config['captcha']['hcaptcha_key']


def auth(token):
    client = httpx.Client()
    session = tls_client.Session(client_identifier="firefox_120")
    uri = "https://owobot.com/api/auth/discord"
    r = client.get(uri)
    oauth_reqstr = r.headers.get("location")
   # print(oauth_reqstr)
    refer_oauth = session.get(oauth_reqstr).text.split("<a href=\"")[1].split("\">")[0]
   # print(refer_oauth)
    payload = {"permissions":"0","authorize":True,"integration_type":0,"location_context":{"guild_id":"10000","channel_id":"10000","channel_type":10000}}
    params = {
  "client_id": "408785106942164992",
  "response_type": "code",
  "redirect_uri": "https://owobot.com/api/auth/discord/redirect",
  "scope": "identify guilds email guilds.members.read"
}

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Authorization': token,
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwOS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzExMS4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTExLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTg3NTk5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
            'X-Discord-Locale': 'en-US',
            'X-Debug-Options': 'bugReporterEnabled',
            'Origin': 'https://discord.com',
            'Connection': 'keep-alive',
            'Referer': refer_oauth,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers',
        }
    response = session.post(oauth_reqstr, headers=headers, json=payload)
   
    if response.status_code == 200:
        if "location" in response.text:
            locauri = response.json().get("location")
            hosturi = locauri.replace("https://", "").replace("http://", "").split("/")[0]
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8","accept-encoding": "gzip, deflate, br","accept-language": "en-US,en;q=0.5","connection": "keep-alive",
                "host": hosturi,
                "referer": "https://discord.com/","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "cross-site","sec-fetch-user": "?1", "upgrade-insecure-requests": "1","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
            }
            res2 = session.get(locauri, headers=headers)
            if res2.status_code in (302, 307):
                try:
                    cook = res2.headers['Set-Cookie'].split(";")[0]
                except:
                    cook = None
                cookie = f"_ga=GA1.2.509834688.1718790840; _gid=GA1.2.1642127289.1718790840;{cook};"
                print("retrived cookie for solver")
                return cookie
            else:
                print(f"(-) Failed to add token to oauth | {res2.text}, {res2.status_code}")
        elif "You need to verify your account" in response.text:
            print(f"(!) Invalid Token [{token[:25]}...]")
        else:
            print(f"(!) Submit Error | {response.text}")


def solve_owo_by_scrappey_api_method(cookie):
     url = f'https://publisher.scrappey.com/api/v1?key={api_key}'
     headers = {'Content-Type': 'application/json'}
     data = {
    'cmd': 'request.get',
    'url': 'https://owo-captcha-solver.vercel.app/solve_hcaptcha',
    'video': True,
     "browserActions": [
         {
            "type": "wait",
            "wait": 1
        },
         {
                "type": "solve_captcha",
                "captcha": "hcaptcha",
                "captchaData": {
                    "sitekey": "a6a1d5ce-612d-472d-8e37-7601408fbc09"
                }
            },
{
                "type": "execute_js",
                "code": "document.getElementsByName('h-captcha-response')[0].value = '{javascriptReturn[0]}'"
            },
             {
            "type": "wait",
            "wait": 10
        },
            
            ]
}
     response = requests.post(url, headers=headers, json=data)
     if response.json()["solution"]["javascriptReturn"][0]:
         print(f"{Fore.LIGHTBLUE_EX}[{hservice}] Solved Hcaptcha, Submitting results to owobot...{Fore.RESET}")
         print(response.json()["solution"]["javascriptReturn"][0])
         res = requests.post("https://owobot.com/api/captcha/verify", json={"token": response.json()['solution']['innerText']}, headers={"Cookie": cookie})
         if res.status_code == 200:
             print(f"{Fore.GREEN}[Solver] HCaptcha Responsed Succuessfully{Fore.RESET}")
             return "solved"
         else:
             print(f'{Fore.RED}[Solver] cannot submit response reason: {res.text}{Fore.RESET}')
             return "cant" 
     else:
         print(f"Hcaptcha Solve failed: {response.json()}")
         return "cant"






def solve_owo_by_scrappey(cookie):
    url = f'https://publisher.scrappey.com/api/v1?key={api_key}'
    headers = {'Content-Type': 'application/json'}
    data = {
    'cmd': 'request.get',
    'url': 'https://owobot.com/captcha',
    'video': True,
    "automaticallySolveCaptchas": True,
     "alwaysLoad": [
        ""
    ],
     "browserActions": [
        {
            "type": "discord_login",
            "token": f"{token}",
            "when": "beforeload"
        },
            {
                "type": "click",
                "cssSelector": "button[class='mb-3 v-btn v-btn--has-bg theme--dark v-size--default primary']",
            }, 
         {
                "type": "click",
                "cssSelector": "div.appMount_ea7e65:nth-child(1) div.appAsidePanelWrapper_bd26cc:nth-child(4) div.notAppAsidePanel_bd26cc div.app_bd26cc:nth-child(1) div.theme-dark.images-dark.wave_c2b22e.wrapper_bb3b80.scrollbarGhost_c858ce.scrollbar_c858ce div.leftSplit_bb3b80 div.oauth2Wrapper_c2b22e div.authorize_c5a065 div.fullWidth_c5a065 div.footer_c5a065 div.action_c5a065 button.button_dd4f85.lookFilled_dd4f85.colorBrand_dd4f85.sizeMedium_dd4f85.grow_dd4f85 > div.contents_dd4f85",
            }, 
             {
            "type": "wait",
            "wait": 18
        },
            
            ]
}
    response = requests.post(url, headers=headers, json=data)
    try:
        if response.json()["solution"]["javascriptReturn"][0]:
            if "I have verified that you're a human!" in response.json()["solution"]["innerText"]:
                print(f"{Fore.LIGHTBLUE_EX}[{hservice}] Solved Hcaptcha,  results submitted to owobot...{Fore.RESET}")
                return "solved"
        else:
            print(f'{Fore.RED}[Solver] cannot submit response reason: {response.text}{Fore.RESET}, Trying WIth Api Function')
            time.sleep(3)
            return solve_owo_by_scrappey_api_method(cookie)
    except:
        print(f'{Fore.RED}[Solver] cannot retrieve response reason: {response.text}{Fore.RESET}, Trying WIth Api Function')
        return solve_owo_by_scrappey_api_method(cookie)
    
def solve_owo(cookie):
     if hservice == "scrappey":
         sol = solve_owo_by_scrappey_api_method(cookie)
         print(sol)
         return sol
     
     else:
         solution = Hcaptcha_Solver()
         response = requests.post("https://owobot.com/api/captcha/verify", json={"token": solution}, headers={"Cookie": cookie})
         if response.status_code == 200:
             print(f"{Fore.GREEN}[Solver] HCaptcha Responsed Succuessfully{Fore.RESET}")
             #print(response.text)
             return "solved"
         else:
             print(f'{Fore.RED}[Solver] cannot submit response reason: {response.text}{Fore.RESET}')
             print(solution)
             
             return "cant" 

