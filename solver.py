#################################
############# Made By TheAxes #######
### Leave credits if u use any snippet ###



























import requests
import httpx
import tls_client
import time
from io import BytesIO
import base64
import json
from twocaptcha import TwoCaptcha
client = httpx.Client()
session = tls_client.Session(client_identifier="firefox_111", random_tls_extension_order=True)    

# By Youtube.com/@theaxes

with open('config.json') as f:
    config = json.load(f)
which_solver = config["captcha_service"]

api_key = config['cap_key']
def solvehcap():
    payload = {
        "clientKey": api_key,
        "task": {
            "type": 'HCaptchaTaskProxyLess',
            "websiteKey": "a6a1d5ce-612d-472d-8e37-7601408fbc09",
            "websiteURL": "https://owobot.com"
        }
    }
    res = requests.post("https://api.capsolver.com/createTask", json=payload)
    resp = res.json()
    task_id = resp.get("taskId")
    if not task_id:
        print("Failed to create task:", res.text)
        return
    print(f"Got taskId: {task_id} / Getting result...")

    while True:
        time.sleep(1)  # delay
        payload = {"clientKey": api_key, "taskId": task_id}
        res = requests.post("https://api.capsolver.com/getTaskResult", json=payload)
        resp = res.json()
        status = resp.get("status")
        if status == "ready":
            print("got result of captcha")
            return resp.get("solution", {}).get('gRecaptchaResponse')
            
        if status == "failed" or resp.get("errorId"):
            print("Solve failed! response", res.text)
            #retry = solvehcap()
            #return retry
        
def auth(token):
    uri = "https://owobot.com/api/auth/discord"
    r = client.get(uri)
    oauth_reqstr = r.headers.get("location")
    refer_oauth = client.get(oauth_reqstr).text.split("<a href=\"")[1].split("\">")[0]

    payload = {
            "permissions": "0",
            "authorize": True
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
            res2 = client.get(locauri, headers=headers)
            print(res2.headers['Set-Cookie'])
            cook = res2.headers['Set-Cookie'].split(";")[0]
            if res2.status_code in (302, 307):
                cookie = f"_ga=GA1.2.509834688.1718790840; _gid=GA1.2.1642127289.1718790840;{cook};"
                print("retrived cookie for solver")
                return cookie
            else:
                print(f"(-) Failed to add token to oauth | {res2.text}, {res2.status_code}")
        elif "You need to verify your account" in response.text:
            print(f"(!) Invalid Token [{token[:25]}...]")
        else:
            print(f"(!) Submit Error | {response.text}")

def to_base64(image_location, is_url=True):
    try:
        if is_url:
            response = requests.get(image_location)
            if response.status_code == 200:
                image_bytes = BytesIO(response.content)
            else:
                return "Unable to fetch image. Status code: " + str(response.status_code)
        else:
            with open(image_location, 'rb') as image_file:
                image_bytes = BytesIO(image_file.read())

        base64_string = base64.b64encode(image_bytes.read()).decode('utf-8')
        return base64_string
    except Exception as e:
        return str(e)
    
def solve_imagecaptcha(imageurl):
	if which_solver == "twocaptcha":
		twosolver = TwoCaptcha(api_key)
		result = twosolver.normal(imageurl)
	else:
		base64Image = to_base64(image_location=imageurl, is_url=True)
		createtask = requests.post("https://api.capsolver.com/createTask",
		json={
		"clientKey": api_key,
		"task": {
		"type": "ImageToTextTask",
		"body":base64Image
		}
		})
		result = createtask.json().get("solution", {}).get('text')   
    return result

def solve_owo(cookie):
	if which_solver == "twocaptcha":
		twosolver = TwoCaptcha(api_key)
		solution = twosolver.hcaptcha(sitekey='a6a1d5ce-612d-472d-8e37-7601408fbc09', url='https://owobot.com')
	else:
		solution =  solvehcap()
	solve = requests.post("https://owobot.com/api/captcha/verify", json={"token": solution}, headers={"Cookie": cookie})
	if solve.status_code == 200:
		print("(+) Solved Captcha")
		return "solved"
	else:
		print(f'cannot submit response reason: {solve.text}')
		return "cant" 
