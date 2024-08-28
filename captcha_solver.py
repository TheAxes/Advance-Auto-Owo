import os, json, requests, time, colorama
from colorama import Fore
from io import BytesIO
import base64
from twocaptcha import TwoCaptcha
import urllib.parse
with open('config.json') as f:
    config = json.load(f)

service = config['captcha']['hcaptcha_service'].lower()
api_key = config['captcha']['hcaptcha_key']
tservice = config['captcha']['TextToImage_service'].lower()
tapi_key = config['captcha']['TextToImage_key']
huntbot_key = config['captcha']['huntbot_key']
website = "https://owobot.com"
sitekey = "a6a1d5ce-612d-472d-8e37-7601408fbc09"
if service not in config['captcha']['avail_services']:
    print(f"{Fore.RED}[Error]Invalid Captcha Solver Provider Provided Please Correct It.{Fore.RESET}")
else:
    print(f"HCaptcha Solver: {service}")
    print(f"TextToImage Solver: {tservice}")

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
    



def Hcaptcha_Solver():
    if service == "capsolver":
        payload = {
            "clientKey": api_key,
            "appId": "5122588A-8581-4440-8044-15D010D2B23C",
            "task": {
            "type": 'HCaptchaTaskProxyLess',
            "websiteKey": sitekey,
            "websiteURL": website
            }
            }
        res = requests.post("https://api.capsolver.com/createTask", json=payload)
        resp = res.json()
        task_id = resp.get("taskId")
        if not task_id:
            print("Failed to create task:", res.text)
            return
        print(f"{Fore.LIGHTBLUE_EX}[{service}] Got taskId: {task_id} / Getting result...{Fore.RESET}")
        while True:
            time.sleep(1)
            payload = {"clientKey": api_key, "taskId": task_id}
            res = requests.post("https://api.capsolver.com/getTaskResult", json=payload)
            resp = res.json()
            status = resp.get("status")
            if status == "ready":
                print(f"{Fore.LIGHTBLUE_EX}[{service}] Solved Hcaptcha, Submitting results to owobot...{Fore.RESET}")
                return resp.get("solution", {}).get('gRecaptchaResponse')
            if status == "failed" or resp.get("errorId"):
                print("Solve failed! response:", res.text)
                return
    elif service == "twocaptcha":
        solver = TwoCaptcha(apiKey=api_key, softId=4663)
        result = solver.hcaptcha(sitekey = sitekey, url = website)
        if result:
            print(f"{Fore.LIGHTBLUE_EX}[{service}] Solved Hcaptcha, Submitting results to owobot...{Fore.RESET}")
            return result['code']
        else:
            print("Hcaptcha Solve failed!")
            return
    elif service == "capmonster":
        payload = {
            "clientKey": api_key,
            "task": {
            "type": 'HCaptchaTaskProxyLess',
            "websiteKey": sitekey,
            "websiteURL": website
            }
            }
        res = requests.post("https://api.capmonster.cloud/createTask", json=payload)
        resp = res.json()
        task_id = resp.get("taskId")
        if not task_id:
            print("Failed to create task:", res.text)
            return
        print(f"{Fore.LIGHTBLUE_EX}[{service}] Got taskId: {task_id} / Getting result...{Fore.RESET}")
        while True:
            time.sleep(1)
            payload = {"clientKey": api_key, "taskId": task_id}
            res = requests.post("https://api.capmonster.cloud/getTaskResult", json=payload)
            resp = res.json()
            status = resp.get("status")
            if status == "ready":
                print(f"{Fore.LIGHTBLUE_EX}[{service}] Solved Hcaptcha, Submitting results to owobot...{Fore.RESET}")
                return resp.get("solution", {}).get('gRecaptchaResponse')
            if status == "failed" or resp.get("errorId"):
                print("Solve failed! response:", res.text)
                return
    elif service == "captchaai":
        res = requests.post(f"https://ocr.captchaai.com/in.php?key={api_key}&method=hcaptcha&sitekey={sitekey}&pageurl={website}")
        resp = res.json()
        task_id = resp.get("request")
        if not task_id:
            print("Failed to create task:", res.text)
            return
        print(f"{Fore.LIGHTBLUE_EX}[{service}] Got taskId: {task_id} / Getting result...{Fore.RESET}")
        while True:
            time.sleep(5)
            res = requests.get(f"https://ocr.captchaai.com/res.php?key={api_key}8&action=get&id={task_id}")
            resp = res.text
            if resp.startswith("P"):
                print(f"{Fore.LIGHTBLUE_EX}[{service}] Solved Hcaptcha, Submitting results to owobot...{Fore.RESET}")
                return resp
            if resp == "ERROR_CAPTCHA_UNSOLVABLE":
                print("Solve failed! response:", res.text)
                return
    elif service == "nopecha":
        res = requests.post(f'https://api.nopecha.com/token',
                            json = {
                                'type': 'hcaptcha',
                                'sitekey': sitekey,
                                'url': website,
                                'key': api_key,
                                })
        task_id = res.json()['data']
        if not task_id:
            print("Failed to create task:", res.text)
            return
        print(f"{Fore.LIGHTBLUE_EX}[{service}] Got taskId: {task_id} / Getting result...{Fore.RESET}")
        url = f"https://api.nopecha.com/token?key={api_key}&id={task_id}"
        resp = requests.get(url)
        if resp.json()['data']:
            print(f"{Fore.LIGHTBLUE_EX}[{service}] Solved Hcaptcha, Submitting results to owobot...{Fore.RESET}")
            return resp.json()['data'][0]
        else:
              print("Solve failed! response:", resp.text)

    else:
        print(f"{Fore.RED}[Error] invalid Captcha Provider{Fore.RESET}")
            

def solve_image_by_scrappey(image, mode):
    if mode == "huntbot":
        keytouse = tapi_key
    else:
        keytouse = tapi_key
    encoded_url =  urllib.parse.quote(image)
    url = f'https://publisher.scrappey.com/api/v1?key={keytouse}'
    headers = {'Content-Type': 'application/json'}
    data = {
    "cmd": "request.get",
    "url": f"https://owo-captcha-solver.vercel.app/captcha_solution?url={encoded_url}",
    "alwaysLoad": [
        ""
    ],
    "browserActions": [
        {
            "type": "wait",
            "wait": 3
        },
        {
            "type": "solve_captcha",
            "captcha": "custom",
            "cssSelector": "img[class='captcha-image']",
            "inputSelector": "input[id='solution']",
            "clickSelector": "button[class='button']"
        },
        {
            "type": "wait",
            "wait": 10
        }

    ]
}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        try:
            print(f"{Fore.LIGHTBLUE_EX}[{service}] Solved ImageToText, Submitting results to owobot...{Fore.RESET}")
            return response.json()["solution"]["innerText"]
        except:
            print("Solve failed! response:", response.text)
            return
    else:
        print("Solve failed! response:", response.text)
        return
        

def ImageToTextSolver(image, length, mode):
    if service == "capsolver":
        base64Image = to_base64(image_location=image, is_url=True)
        res = requests.post("https://api.capsolver.com/createTask",
                            json={
                                "clientKey": tapi_key,
                                "appId": "5122588A-8581-4440-8044-15D010D2B23C",
                                "task": {
                                    "type": "ImageToTextTask",
                                    "body":base64Image
                                    }
                                    })
        return res.json().get("solution", {}).get('text')
    elif service == "twocaptcha":
        solver = TwoCaptcha(apiKey=tapi_key, softId=4663)
        result = solver.normal(image, numeric = 2, minLen = length, maxLen = length, phrase = 0, caseSensitive = 0, calc = 0, lang = "en")
        return result['code']
    elif service == "capmonster":
        base64Image = to_base64(image_location=image, is_url=True)
        payload = {
            "clientKey": tapi_key,
            "task": {
            "type": 'ImageToTextTask',
            "body": base64Image,
            }
            }
        res = requests.post("https://api.capmonster.cloud/createTask", json=payload)
        resp = res.json()
        task_id = resp.get("taskId")
        if not task_id:
            print("Failed to create task:", res.text)
            return
        print(f"{Fore.LIGHTBLUE_EX}[{tservice}] Got taskId: {task_id} / Getting result...{Fore.RESET}")
        while True:
            time.sleep(1)
            payload = {"clientKey": tapi_key, "taskId": task_id}
            res = requests.post("https://api.capmonster.cloud/getTaskResult", json=payload)
            resp = res.json()
            status = resp.get("status")
            if status == "ready":
                print(f"{Fore.LIGHTBLUE_EX}[{tservice}] Solved ImageToText, Submitting results to owobot...{Fore.RESET}")
                return resp.get("solution", {}).get('text')
            if status == "failed" or resp.get("errorId"):
                print("Solve failed! response:", res.text)
                return
    elif service == "captchaai":
        base64Image = to_base64(image_location=image, is_url=True)
        res = requests.post(f"https://ocr.captchaai.com/solve.php?key={tapi_key}&method=base64&body={base64Image}")
        return res.text 
    
    elif service == "scrappey":
        sol = solve_image_by_scrappey(image, mode=mode)
        return sol
    elif service == "nopecha":
        base64Image = to_base64(image_location=image, is_url=True)
        res = requests.post("https://api.nopecha.com/",
                            json={
                                "key": tapi_key,
                                "type": "textcaptcha",
                                "image_data": base64Image
                                    })
        task_id = res.json()['data']
        sol = requests.get(f"https://api.nopecha.com/?key={tapi_key}&id={task_id}")
        return sol.json()['data'][0]

def fetch_hcaptcha_balance():
    '''
    HCAPTCHA BALANCE
    '''
    if service == 'capsolver':
        r =  requests.post(f"https://api.capsolver.com/getBalance", json={
            "clientKey": api_key
            })
        return r.json()['balance']
    elif service == "twocaptcha":
        r =  requests.post(f"https://api.2captcha.com/getBalance", json={
            "clientKey": api_key
            })
        return r.json()['balance']
    elif service == "capmonster":
         r =  requests.post(f"https://api.capmonster.cloud/getBalance", json={
            "clientKey": api_key
            })
         return r.json()['balance']
    elif service == "captchaai":
         r =  requests.post(f"https://ocr.captchaai.com/res.php?key={api_key}&action=getbalance")
         return r.text
    elif service == 'scrappey':
        r =  requests.get(f"https://publisher.scrappey.com/api/v1/balance?key={api_key}")
        return r.json()['balance']
    elif service == 'nopecha':
        r = requests.get(f" https://api.nopecha.com/status?key={api_key}")
        return r.json()['credit']
    
    

def fetch_texttoimage_balance():
    '''
    TExtToImage'''

    if tservice == 'capsolver':
        r =  requests.post(f"https://api.capsolver.com/getBalance", json={
            "clientKey": tapi_key
            })
        return r.json()['balance']
    elif tservice == "twocaptcha":
        r =  requests.post(f"https://api.2captcha.com/getBalance", json={
            "clientKey": tapi_key
            })
        return r.json()['balance']
    elif tservice == "capmonster":
         r =  requests.post(f"https://api.capmonster.cloud/getBalance", json={
            "clientKey": tapi_key
            })
         return r.json()['balance']
    elif tservice == "captchaai":
         r =  requests.post(f"https://ocr.captchaai.com/res.php?key={tapi_key}&action=getbalance")
         return r.text
    elif tservice == 'scrappey':
        r =  requests.get(f"https://publisher.scrappey.com/api/v1/balance?key={tapi_key}")
        return r.json()['balance']
    elif tservice == 'nopecha':
        r = requests.get(f" https://api.nopecha.com/status?key={tapi_key}")
        return r.json()['credit']




