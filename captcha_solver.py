import os, json, requests, time, colorama
from colorama import Fore
from io import BytesIO
import base64
from twocaptcha import TwoCaptcha

with open('config.json') as f:
    config = json.load(f)

service = config['captcha_service'].lower()
api_key = config['cap_key']
website = "https://owobot.com"
sitekey = "a6a1d5ce-612d-472d-8e37-7601408fbc09"
if service not in config['avail_services']:
    print(f"{Fore.RED}[Error]Invalid Captcha Solver Provider Provided Please Correct It.{Fore.RESET}")
else:
    print(f"Captcha Solver: {service}")

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
    else:
        print(f"{Fore.RED}[Error] invalid Captcha Provider{Fore.RESET}")
            
def ImageToTextSolver(image, length):
    if service == "capsolver":
        base64Image = to_base64(image_location=image, is_url=True)
        res = requests.post("https://api.capsolver.com/createTask",
                            json={
                                "clientKey": api_key,
                                "appId": "5122588A-8581-4440-8044-15D010D2B23C",
                                "task": {
                                    "type": "ImageToTextTask",
                                    "body":base64Image
                                    }
                                    })
        return res.json().get("solution", {}).get('text')
    elif service == "twocaptcha":
        solver = TwoCaptcha(apiKey=api_key, softId=4663)
        result = solver.normal(image, numeric = 2, minLen = length, maxLen = length, phrase = 0, caseSensitive = 0, calc = 0, lang = "en")
        return result['code']
    elif service == "capmonster":
        base64Image = to_base64(image_location=image, is_url=True)
        payload = {
            "clientKey": api_key,
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
        print(f"{Fore.LIGHTBLUE_EX}[{service}] Got taskId: {task_id} / Getting result...{Fore.RESET}")
        while True:
            time.sleep(1)
            payload = {"clientKey": api_key, "taskId": task_id}
            res = requests.post("https://api.capmonster.cloud/getTaskResult", json=payload)
            resp = res.json()
            status = resp.get("status")
            if status == "ready":
                print(f"{Fore.LIGHTBLUE_EX}[{service}] Solved ImageToText, Submitting results to owobot...{Fore.RESET}")
                return resp.get("solution", {}).get('text')
            if status == "failed" or resp.get("errorId"):
                print("Solve failed! response:", res.text)
                return
    elif service == "captchaai":
        base64Image = to_base64(image_location=image, is_url=True)
        res = requests.post(f"https://ocr.captchaai.com/solve.php?key={api_key}&method=base64&body={base64Image}")
        return res.text 
	


