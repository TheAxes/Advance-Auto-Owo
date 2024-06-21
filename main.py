import os
import discord, time, requests, asyncio, random, json, colorama
import re
from discord.ext import commands
from discord.ext import tasks
import wonderwords
from wonderwords import RandomSentence
from datetime import timedelta
from io import BytesIO
import base64
import capsolver
from solver import auth, solve_imagecaptcha, solve_owo
from colorama import Fore
sentences = RandomSentence()
def clear():
    os.system('title Advanced Auto OwO && cls' if os.name=='nt' else 'clear')

with open('config.json') as f:
    config = json.load(f)


try:
    prefix = config.get('prefix')
    token = config.get('token')
    hook_url = config.get('webhook')
except:
	print("no token found")
owochannel = []
banner = '''

              _                               _                 _           ____                
     /\      | |                             | |     /\        | |         / __ \               
    /  \   __| |_   ____ _ _ __   ___ ___  __| |    /  \  _   _| |_ ___   | |  | |_      _____  
   / /\ \ / _` \ \ / / _` | '_ \ / __/ _ \/ _` |   / /\ \| | | | __/ _ \  | |  | \ \ /\ / / _ \ 
  / ____ \ (_| |\ V / (_| | | | | (_|  __/ (_| |  / ____ \ |_| | || (_) | | |__| |\ V  V / (_) |
 /_/    \_\__,_| \_/ \__,_|_| |_|\___\___|\__,_| /_/    \_\__,_|\__\___/   \____/  \_/\_/ \___/ 
                   ____                _______ _                                                
                  |  _ \           ___|__   __| |            /\                                 
                  | |_) |_   _    / __ \ | |  | |__   ___   /  \   __  _____  ___               
                  |  _ <| | | |  / / _` || |  | '_ \ / _ \ / /\ \  \ \/ / _ \/ __|              
                  | |_) | |_| | | | (_| || |  | | | |  __// ____ \  >  <  __/\__ \              
                  |____/ \__, |  \ \__,_||_|  |_| |_|\___/_/    \_\/_/\_\___||___/              
                          __/ |   \____/                                                        
                         |___/                                                                  

'''
headers = {"Authorization": token}
r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
user_data = r.json()
globalname =  user_data["global_name"]	
	

client = commands.Bot(description='Advanced Auto OwO', command_prefix=prefix, case_insensitive=True, self_bot=True, help_command=None)
def get_entry():
    file_path = "entry.json"
    with open(file_path, "r") as file:
        data = json.load(file)
        cowoncy, nextdaily, cookie = data.get("cowoncy", ""), data.get("nextdaily", ""), data.get("cookie", "")
        return cowoncy, nextdaily, cookie

def update_entry(new_cowoncy=None, new_nextdaily=None, new_cookie=None):
    file_path = "entry.json"
    with open(file_path, "r+") as file:
        data = json.load(file)
        if new_cowoncy is not None:
            data["cowoncy"] = new_cowoncy
        if new_nextdaily is not None:
            data["nextdaily"] = new_nextdaily
        if new_cookie is not None:
             data["cookie"] = new_cookie
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
		
    



def solvecap(problem):
     if problem == "https://owobot.com/captcha":
          cooked = get_entry()[2]
          sol = solve_owo(cooked) 
          return f"{sol}|hcap"     
     else:
          sol = solve_imagecaptcha(imageurl=problem)
          return f"{sol}|image"
   
def sendhook(content, description):
    webhook_url = hook_url
    
    # Create JSON payload
    payload = {
        'username': 'OwO Logger',  # Set the username here
        'content': content,
        'embeds': [{
            'title': 'Auto OwO',
            'description': description,
           'image': {
                'url': 'https://images-ext-1.discordapp.net/external/mflqo1HcoLk6g1HEXdHLOBbKSVZ8Lq690mXrNA3yeX4/https/repository-images.githubusercontent.com/520888256/df57c468-cb50-4f1e-bb10-be6d7341b262?format=webp&width=797&height=448'
            },
            'footer': {
                'text': 'Made By @Theaxes',
                'icon_url': 'https://images-ext-1.discordapp.net/external/LEdJvbRy1zsqteshdxeKJ9sk5GCksjlNwiEO5_bCYhk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/824522317899235360/2cbb4933cb3c03a205f4ed85167a8530.png?format=webp&quality=lossless&width=291&height=291'  # Replace with your footer icon URL
            }
        }]
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Send POST request to the webhook URL
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print('Webhook sent successfully!')
    except requests.exceptions.RequestException as e:
        print(f'Failed to send WEbhook: {e}')

@client.event
async def on_connect():
          print("please wait, bot loading")
          cook = auth(token)
          update_entry(new_cookie=cook)
          clear()
          print(f"{Fore.LIGHTCYAN_EX}{banner}{Fore.RESET}")
          print(f"Account : {client.user}")
          print(f"prefix : {prefix}")
          await client.change_presence(status=discord.Status.dnd, 
                             activity=discord.Activity(type=discord.ActivityType.playing, 
                                                         name="Auto OwO",
                                                           details="Made By @TheAxes", 
                                                           timestamps={"start": time.time()}, 
                                                           state="youtube.com/@theaxes"))
        

		
		

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.bot:
        if message.author.id == 408785106942164992:
            # Check for cowoncy update message
            if "cowoncy" in message.content and not "sent" in message.content:
                pattern = r"\| {}\*\*, you currently have \*\*__([\d,]+)__ cowoncy!".format(re.escape(globalname))
                match = re.search(pattern, message.content)
                if match:
                    cowoncy_amount = match.group(1).replace(",", "")
                    print(f"You Have {cowoncy_amount} Cowoncy")
                    update_entry(new_cowoncy=cowoncy_amount)
                return
            else:
                # Check for captcha detection message
                if "⚠️" in message.content:
                    # Stop various tasks
                    tasks = [
                        autohunter.cancel(),
        autopray.cancel(),
        autolevelup.cancel(),
        autodaily.cancel(),
        autosell.cancel(),
        owobalace.cancel(),
        autosleep.cancel()
                    ]
                    for task in tasks:
                         task
                    
                    # Retrieve captcha details
                    captchamsg = message.jump_url
                    try:
                         captcha = message.attachments[0].url
                    except:
                         captcha = "https://owobot.com/captcha"
                    
                    # Send notification using webhook
                    sendhook(content=f"@everyone Captcha Alert!", description=f"A Captcha Has Been Detected!\n*Captcha Message*: [Jump to Message]({captchamsg})")
                    
                    # Solve captcha
                    solution = solvecap(captcha) 
                    user = client.get_user(408785106942164992)
                    # Send the solution to the channel
                    if solution.split("|")[1] == "image":
                         await user.send(solution.split("|")[0])
                    elif solution.split("|")[1] == "image":
                         await user.send("dn")
                    
                    try:
                        # Wait for user confirmation message with a timeout of 120 seconds
                        verification_message = await asyncio.wait_for(client.wait_for('message', check=lambda m: m.author == message.author and "I have verified that you are human! Thank you! :3" in m.content), timeout=120)
                        
                        # Check if the user's message indicates correct verification
                        if "I have verified" in verification_message.content:
                            # Start tasks again
                            channel = client.get_channel(owochannel)
                            sendhook(content=f"@everyone Captcha Alert!", description=f"Captcha Has Been Solved!")
                            await channel.send(f"{prefix}autoowo")
                        else:
                            sendhook(content=f"@everyone Captcha Alert!", description=f"A Captcha Cant Be Solved, Bot Has Been Stopped!")
                            await client.close()
                    
                    except asyncio.TimeoutError:
                        print(f"{Fore.RED}captcha timed out.{Fore.RESET}")
                        sendhook(content=f"@everyone Captcha Alert!", description=f"A Captcha Cant Be Solved, Bot Has Been Stopped!, Reason: Captcha Took Too Long Too Solve")
                        await client.close()
                    
                    
                      # Close the bot client after verification
                if "nu" or "your next" in message.content.lower():
                     if message.author.id == 408785106942164992:
                          if globalname in message.content:
                               target_message = message
                               if "nu" in target_message.content.lower():
                                    pattern = r'(\d+)H (\d+)M (\d+)S'
                                    match = re.search(pattern, target_message.content)
                                    hours = int(match.group(1))
                                    minutes = int(match.group(2))
                                    seconds = int(match.group(3))
                                    total_seconds = hours * 3600 + minutes * 60 + seconds
                                    next_daily = time.time() + total_seconds
                                    update_entry(new_nextdaily=next_daily)
                                    print(f"Next Daily: {str(timedelta(seconds=total_seconds))}s")
                               else:
                                    if "Here is your daily" in target_message.content:
                                         print("Claimed Daily")
                            

			
@tasks.loop(seconds=random.randrange(18, 30))
async def autohunter(ctx):
     await ctx.channel.trigger_typing()
     await asyncio.sleep(3)
     await ctx.channel.send("owo hunt")
     await asyncio.sleep(9)
     await ctx.channel.send("owo battle")

@tasks.loop(minutes=random.randrange(5, 7))
async def autopray(ctx):
    await asyncio.sleep(8)
    await ctx.channel.trigger_typing()
    await ctx.channel.send("owo pray")
	


@tasks.loop(seconds=random.randrange(15, 60))
async def autolevelup(ctx):
     await ctx.channel.trigger_typing()
     await asyncio.sleep(11)
     xp = random.choice(("owo", "owo xp", "uwu"))
     message = random.choice((xp, f"{sentences.sentence()}{xp}"))
     await ctx.channel.send(message)
     await asyncio.sleep(3)

@tasks.loop(minutes=3)
async def autodaily(ctx):
            if not get_entry()[1] - time.time() <= 0:
                  return
            await ctx.channel.trigger_typing()
            await asyncio.sleep(3)
            await ctx.channel.send("owo daily")
            

@tasks.loop(minutes=2)
async def autosell(ctx):
     await asyncio.sleep(13)
     if config["autosell"] == "true":
        await ctx.channel.send(f"owo sell {config['animal_types']}")
     else:
          return

@tasks.loop(minutes=5)
async def owobalace(ctx):
     await asyncio.sleep(5)
     await ctx.channel.send(f"owo cash")

@tasks.loop(minutes=random.randrange(15, 20))
async def autosleep(ctx):
     await asyncio.sleep(random.randrange(180, 360))
     print("bot sleeping")
     await ctx.channel.send(f"{prefix}stopautoowo")
     await asyncio.sleep(random.randrange(180, 360))
     await ctx.channel.send(f"{prefix}autoowo")

	
@client.command()
async def autoowo(ctx):
    global owochannel
    owochannel = ctx.channel.id
    tasks = [
        autohunter.start(ctx),
        autopray.start(ctx),
        autolevelup.start(ctx),
        autosell.start(ctx),
        owobalace.start(ctx),
        autodaily.start(ctx),
        autosleep.start(ctx)
    ]
    await ctx.send("> Started Auto OwO")
    try:
        for task in tasks:
             task
             await asyncio.sleep(3)
        
    except RuntimeError:

        return

@client.command()
async def stopautoowo(ctx):
    tasks = [
        autohunter.cancel(),
        autopray.cancel(),
        autolevelup.cancel(),
        autodaily.cancel(),
        autosell.cancel(),
        owobalace.cancel(),
        autosleep.cancel()
    ]
    await ctx.send("> Stopped Auto OwO")
    try:
        for task in tasks:
             task
    except RuntimeError:
        return

client.run(token)

