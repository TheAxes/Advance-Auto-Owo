# Skids Go Away Else I'll kidnap your basements kids


















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
from solver import auth, solve_owo
from captcha_solver import ImageToTextSolver, solve_image_by_scrappey, fetch_hcaptcha_balance, fetch_texttoimage_balance, scrappey_balance
from colorama import Fore
sentences = RandomSentence()


version = "1.2" # Logic * 69999999999999999

def clear():
    os.system("title Advanced Auto OwO && cls" if os.name == "nt" else "clear")


with open("config.json") as f:
    config = json.load(f)
try:
    prefix = config.get("prefix")
    token = config.get("token")
    captcha_hook_url = config["notifications"]["captcha_alerts"]
    daily_hook_url = config["notifications"]["daily_claim_alerts"]
    huntbot_hook_url = config["notifications"]["huntbot_alert"]
    funds_hook_url = config["notifications"]["funds_alerts"]
    
except:
    print("no token found")
owochannels = config["settings"]["channel_ids"]
change_channel_after = config["settings"]["channel_change_interval"]
owochannel = 0


    
banner = """

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

"""
user_data = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}).json()
globalname = user_data["global_name"]
if not globalname:
    print(f"{Fore.RED}[Error] Incorrect Token Provided{Fore.RESET}")
    os.system('exit')

all_tasks = []
all_tasks_stop = []


def create_tasks():
    global all_tasks
    global all_tasks_stop
    plugins = config["plugins"]
    try:
        if plugins["autosell"] == "true":
            all_tasks.append(autosell)
            all_tasks_stop.append(autosell)
        if plugins["autolevelup"] == "true":
            all_tasks.append(autolevelup)
            all_tasks_stop.append(autolevelup)
        if plugins["autoslot"] == "true":
            all_tasks.append(autoslot)
            all_tasks_stop.append(autoslot)
        if plugins["autocoinflip"] == "true":
            all_tasks.append(autocf)
            all_tasks_stop.append(autocf)
        if plugins["autopray"] == "true":
            all_tasks.append(autopray)
            all_tasks_stop.append(autopray)
        if plugins["use_random_commands"] == "true":
            all_tasks.append(autorandomcommand)
            all_tasks_stop.append(autorandomcommand)
        if plugins["autohuntbot"] == "true":
            all_tasks.append(autohuntbot)
            all_tasks_stop.append(autohuntbot)
        
    except Exception as e:
        print(e)
    print("")
    try:
        all_tasks.append(autohunter)
        all_tasks.append(owobalace)
        all_tasks.append(autodaily)
        all_tasks.append(autosleep)
        all_tasks.append(auto_channelchange)
        all_tasks.append(balanace_alerts)
        all_tasks_stop.append(autohunter)
        all_tasks_stop.append(autodaily)
        all_tasks_stop.append(owobalace)
        all_tasks_stop.append(autosleep)
        all_tasks_stop.append(auto_channelchange)
        all_tasks_stop.append(balanace_alerts)

    except Exception as e:
        print(e)


client = commands.Bot(
    description="Advanced Auto OwO",
    command_prefix=prefix,
    case_insensitive=True,
    self_bot=True,
    help_command=None,
)


def check_version():
    r = requests.get(
        "https://raw.githubusercontent.com/TheAxes/Advance-Auto-Owo/main/Current-version.txt"
    )
    if r.text.rstrip() == version:
        return ""
    else:
        print(r.text)
        return f"{Fore.LIGHTMAGENTA_EX}A Newer Version Is Available: {r.text}\nConsider updating it: https://github.com/TheAxes/Advance-Auto-Owo{Fore.RESET}"


def get_entry():
    file_path = "entry.json"
    with open(file_path, "r") as file:
        data = json.load(file)
        cowoncy, nextdaily, cookie, nexthuntbot = (
            data.get("cowoncy", ""),
            data.get("nextdaily", ""),
            data.get("cookie", ""),
            data.get("nexthuntbot")
        )
        return cowoncy, nextdaily, cookie, nexthuntbot, 


def update_entry(new_cowoncy=None, new_nextdaily=None, new_cookie=None, new_nexthuntbot=None):
    file_path = "entry.json"
    with open(file_path, "r+") as file:
        data = json.load(file)
        if new_cowoncy is not None:
            data["cowoncy"] = new_cowoncy
        if new_nextdaily is not None:
            data["nextdaily"] = new_nextdaily
        if new_cookie is not None:
            data["cookie"] = new_cookie
        if new_nexthuntbot is not None:
            data["nexthuntbot"] = new_nexthuntbot
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def solvecap(problem, lambaa=None):
    if problem == "https://owobot.com/captcha":
        cooked = get_entry()[2]
        sol = solve_owo(cooked)
        return f"{sol}|hcap"
    else:
        sol = ImageToTextSolver(image=problem, length=lambaa, mode='captcha')
        return f"{sol}|image"


def sendhook(hook_url, content, description, image_url):
    payload = {
        "username": "OwO Logger",  # Set the username here
        "content": content,
        "embeds": [
            {
                "title": "Auto OwO",
                "description": description,
                "image": {
                    "url": image_url
                },
                "footer": {
                    "text": "Made By @Theaxes",
                    "icon_url": "https://images-ext-1.discordapp.net/external/LEdJvbRy1zsqteshdxeKJ9sk5GCksjlNwiEO5_bCYhk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/824522317899235360/2cbb4933cb3c03a205f4ed85167a8530.png?format=webp&quality=lossless&width=291&height=291",  # Replace with your footer icon URL
                },
            }
        ],
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(hook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print(f"{Fore.LIGHTGREEN_EX}[Notification] Sent A Webhook{Fore.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[Notification] Unable to Sent A Webhook: {e}{Fore.RESET}")


@client.event
async def on_connect():
    print("please wait, bot loading")
    create_tasks()
    cook = auth(token)
    update_entry(new_cookie=cook)
    clear()
    print(f"{Fore.LIGHTCYAN_EX}{banner}{Fore.RESET}")
    print(f"Account : {globalname}")
    print(f"prefix : {prefix}")
    print(check_version())
    await client.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="Auto OwO",
            details="Made By @TheAxes",
            timestamps={"start": time.time()},
            state="youtube.com/@theaxes",
        ),
    )


@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.bot:
        if message.author.id == 408785106942164992:
            # Check for cowoncy update message
            if "cowoncy" in message.content and not "sent" in message.content:
                pattern = r"\| {}\*\*, you currently have \*\*__([\d,]+)__ cowoncy!".format(
                    re.escape(globalname)
                )
                match = re.search(pattern, message.content)
                if match:
                    cowoncy_amount = match.group(1).replace(",", "")
                    print(
                        f"{Fore.LIGHTYELLOW_EX}[Logger] You Have {cowoncy_amount} Cowoncy{Fore.RESET}"
                    )
                    update_entry(new_cowoncy=cowoncy_amount)
                return
            else:
                # Check for captcha detection message
                if ("⚠️" in message.content) and (
                    ("letter word" in message.content)
                    or ("https://owobot.com/captcha" in message.content)
                ):
                    # Stop various tasks
                    for task in all_tasks_stop:
                        task.cancel()
                    # Retrieve captcha details
                    captchamsg = message.jump_url
                    try:
                        captcha = message.attachments[0].url
                    except:
                        captcha = "https://owobot.com/captcha"
                    # Send notification using webhook
                    sendhook(hook_url=captcha_hook_url,
                        content=f"@everyone Captcha Alert!",
                        description=f"A Captcha Has Been Detected!\n*Captcha Message*: [Jump to Message]({captchamsg})", image_url="https://images-ext-1.discordapp.net/external/mflqo1HcoLk6g1HEXdHLOBbKSVZ8Lq690mXrNA3yeX4/https/repository-images.githubusercontent.com/520888256/df57c468-cb50-4f1e-bb10-be6d7341b262?format=webp&width=797&height=448")
                    # Solve captcha
                    if "letter word" in message.content:
                        solution = solvecap(
                            captcha, lambaa=message.content[message.content.find("letter word") - 2]
                        )
                    else:
                        solution = solvecap(captcha, lambaa=None)
                    user = client.get_user(408785106942164992)
                    # Send the solution to the channel
                    if solution.split("|")[1] == "image":
                        await user.send(solution.split("|")[0])
                    elif solution.split("|")[1] == "hcap":
                        await user.send("ok")
                    try:
                        # Wait for user confirmation message with a timeout of 120 seconds
                        verification_message = await asyncio.wait_for(
                            client.wait_for(
                                "message",
                                check=lambda m: m.author == message.author
                                and "I have verified that you are human! Thank you! :3"
                                in m.content,
                            ),
                            timeout=220,
                        )

                        # Check if the user's message indicates correct verification
                        if "I have verified" in verification_message.content:
                            # Start tasks again
                            channel = client.get_channel(owochannel)
                            sendhook(hook_url=captcha_hook_url,
                                content=f"@everyone Captcha Alert!",
                                description=f"Captcha Has Been Solved!", image_url="https://images-ext-1.discordapp.net/external/mflqo1HcoLk6g1HEXdHLOBbKSVZ8Lq690mXrNA3yeX4/https/repository-images.githubusercontent.com/520888256/df57c468-cb50-4f1e-bb10-be6d7341b262?format=webp&width=797&height=448")
                            await channel.send(f"{prefix}autoowo")
                        else:
                            sendhook(hook_url=captcha_hook_url, image_url="https://images-ext-1.discordapp.net/external/mflqo1HcoLk6g1HEXdHLOBbKSVZ8Lq690mXrNA3yeX4/https/repository-images.githubusercontent.com/520888256/df57c468-cb50-4f1e-bb10-be6d7341b262?format=webp&width=797&height=448"
                                ,content=f"@everyone Captcha Alert!",
                                description=f"A Captcha Cant Be Solved, Bot Has Been Stopped!",
                            )
                            await client.close()
                    except asyncio.TimeoutError:
                        print(f"{Fore.RED}[Timeout] captcha timed out.{Fore.RESET}")
                        sendhook(hook_url=captcha_hook_url, image_url="https://images-ext-1.discordapp.net/external/mflqo1HcoLk6g1HEXdHLOBbKSVZ8Lq690mXrNA3yeX4/https/repository-images.githubusercontent.com/520888256/df57c468-cb50-4f1e-bb10-be6d7341b262?format=webp&width=797&height=448",
                            content=f"@everyone Captcha Alert!",
                            description=f"A Captcha Cant Be Solved, Bot Has Been Stopped!, Reason: Captcha Took Too Long Too Solve",
                        )
                        await client.close()
                    # Close the bot client after verification
                if "nu" or "your next" or "your daily" in message.content.lower():
                    if message.author.id == 408785106942164992:
                        if globalname in message.content:
                            target_message = message
                            if "nu" in target_message.content.lower():
                                pattern = r"(\d+)H (\d+)M (\d+)S"
                                match = re.search(pattern, target_message.content)
                                hours = int(match.group(1))
                                minutes = int(match.group(2))
                                seconds = int(match.group(3))
                                total_seconds = hours * 3600 + minutes * 60 + seconds
                                next_daily = time.time() + total_seconds
                                update_entry(new_nextdaily=next_daily)
                                print(
                                    f"{Fore.LIGHTYELLOW_EX}[Logger] Your Next Daily: {str(timedelta(seconds=total_seconds))}s{Fore.RESET}"
                                )
                            else:
                                if ":cowoncy:" in target_message.content:
                                    print(
                                        f"{Fore.LIGHTYELLOW_EX}[Logger] Daily Has Been Claimed{Fore.RESET}"
                                    )
def change_channel():
    global owochannel
    new_owochannel = random.choice(owochannels)
    after = client.get_channel(new_owochannel)
    owochannel = new_owochannel
    print(f"{Fore.YELLOW}[Logger] Set OwO Channel To #{after.name}")

@tasks.loop(seconds=random.randrange(18, 30))
async def autohunter():
    channel = client.get_channel(owochannel)
    await channel.trigger_typing()
    await asyncio.sleep(3)
    await channel.send("owo hunt")
    await asyncio.sleep(9)
    await channel.send("owo battle")


@tasks.loop(minutes=random.randrange(5, 7))
async def autopray():
    channel = client.get_channel(owochannel)
    await asyncio.sleep(8)
    await channel.trigger_typing()
    await channel.send("owo pray")


@tasks.loop(seconds=random.randrange(15, 60))
async def autolevelup():
    channel = client.get_channel(owochannel)
    await channel.trigger_typing()
    await asyncio.sleep(11)
    xp = random.choice(("owo", "UwUUwU", "uwu"))
    message = random.choice((xp, f"{sentences.sentence()}owo"))
    await channel.send(message)
    await asyncio.sleep(3)


@tasks.loop(minutes=3)
async def autodaily():
    channel = client.get_channel(owochannel)
    if not get_entry()[1] - time.time() <= 0:
        return
    await channel.trigger_typing()
    await asyncio.sleep(3)
    await channel.send("owo daily")
    daily_message = await asyncio.wait_for(
                            client.wait_for(
                                "message",
                                check=lambda m: "Here is your daily"
                                in m.content,
                            ),
                            timeout=60,
                        )
    if daily_message:
        sendhook(content="Daily Alert!!", description="A Daily Has been Claimed", hook_url=daily_hook_url, image_url="https://cdn.discordapp.com/emojis/427352600476647425.webp?size=56&quality=lossless")
    await channel.send("owo cookie <@408785106942164992>")


@tasks.loop(minutes=2)
async def autosell():
    channel = client.get_channel(owochannel)
    await asyncio.sleep(13)
    await channel.send(f"owo sell {config['settings']['animal_types']}")


@tasks.loop(minutes=4)
async def autoslot():
    await asyncio.sleep(30)
    channel = client.get_channel(owochannel)
    amount = random.choice(config["settings"]["slotamount"])
    await channel.send(f"owo s {amount}")

@tasks.loop(minutes=5)
async def autocf():
    channel = client.get_channel(owochannel)
    amount = random.choice(config["settings"]["autocoinflip_amount"])
    await channel.send(f"owo cf {amount}")


@tasks.loop(minutes=5)
async def owobalace():
    channel = client.get_channel(owochannel)
    await asyncio.sleep(5)
    await channel.send(f"owo cash")


@tasks.loop(minutes=random.randrange(15, 20))
async def autosleep():
    await asyncio.sleep(random.randrange(180, 360))
    print(f"{Fore.LIGHTGREEN_EX}[Sleeper] Bot Sleeping{Fore.RESET}")
    all_tasks_stop.remove(autosleep)
    try:
        for task in all_tasks_stop:
            task.cancel()
    except RuntimeError:
        return
    await asyncio.sleep(random.randrange(180, 360))
    all_tasks_stop.append(autosleep)
    print(f"{Fore.LIGHTGREEN_EX}[Sleeper] Bot Again Resumed{Fore.RESET}")
    try:
        for task in all_tasks:
            task.start()
            await asyncio.sleep(3)
    except RuntimeError:
        return
    
def extract_amount(text):
    pattern = r'owo\s+autohunt\s+(\d+)'
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    else:
        return None
    
@tasks.loop(minutes=5)
async def autohuntbot():
    channel = client.get_channel(owochannel)
    if not get_entry()[3] - time.time() <= 0:
        return
    else:
        await asyncio.sleep(15)
        await channel.send("owo autohunt")
        await asyncio.sleep(30)
        await channel.send("owo autohunt 1d")
        amount_message = await asyncio.wait_for(
                            client.wait_for(
                                "message",
                                check=lambda m: "password"
                                in m.content,
                            ),
                            timeout=60,
                        )
        if amount_message.attachments[0].url:
            password = solve_image_by_scrappey(amount_message.attachments[0].url, mode="huntbot")
            amount = extract_amount(amount_message.content)
            await channel.send(f"owo autohunt {amount} {password} ")
            huntbot_msg = await asyncio.wait_for(
                            client.wait_for(
                                "message",
                                check=lambda m: "I WILL BE BACK IN"
                                in m.content,
                            ),
                            timeout=60,
                        )
            time_str = re.search(r'(\d+)M', huntbot_msg.content)
            minutes = int(time_str.group(1)) + 2
            seconds = minutes * 60
            sendhook(hook_url=huntbot_hook_url, content="HuntBot Alert!!", description=f"Huntbot Started!!\n[Jump to Message]({huntbot_msg.jump_url})", image_url="https://images-ext-1.discordapp.net/external/r-T0CN-zkuhykmnsWyy6gRSkZyAb-mm7EDeH-lUi_w8/https/cdn.discordapp.com/emojis/459996048379609098.png?format=webp&quality=lossless&width=160&height=160")
            update_entry(new_nexthuntbot=time.time() + seconds)
            await asyncio.sleep(seconds) 

@tasks.loop(seconds=random.randrange(60, 120))
async def autorandomcommand():
    channel = client.get_channel(owochannel)
    await channel.trigger_typing()
    msg = random.choice(config['settings']['random_commands'])
    await channel.send(f"owo {msg}")
    await asyncio.sleep(3)

@tasks.loop(minutes=2)
async def balanace_alerts():
    hbal = fetch_hcaptcha_balance()
    txtbal = fetch_texttoimage_balance()
    scrappeybal = scrappey_balance()
    if hbal or txtbal < 0:
        sendhook(description="Keys Ran Out Of Funds Please Refill ANd then Restart Bo", hook_url=funds_hook_url, content="@everyone Bot Stopped!!", image_url="https://media.discordapp.net/attachments/1251479335647576169/1271412600915230720/Money-Bag-Transparent-PNG.png?ex=66b73ec1&is=66b5ed41&hm=33fadea61e4229b908c3e5c0a3423bf48318f1a5e111f93245618141ae5ce607&=&format=webp&quality=lossless&width=437&height=437")
        os.system("exit")
    elif scrappeybal < 0:
        sendhook(description="Scrappey Funds Ran Out, Pls Refill And restart to enable huntbot", hook_url=funds_hook_url, content="@everyone huntbot Stopped!!", image_url="https://media.discordapp.net/attachments/1251479335647576169/1271412600915230720/Money-Bag-Transparent-PNG.png?ex=66b73ec1&is=66b5ed41&hm=33fadea61e4229b908c3e5c0a3423bf48318f1a5e111f93245618141ae5ce607&=&format=webp&quality=lossless&width=437&height=437")
        all_tasks.remove(autohuntbot)
        all_tasks_stop.remove(autohuntbot)
        autohuntbot.cancel()
    else:
        return


@tasks.loop(minutes=random.choice(change_channel_after))
async def auto_channelchange():
    change_channel()

@client.command()
async def help(ctx):
    await ctx.send(f"> {prefix}autoowo\n> {prefix}stopautoowo")


@client.command()
async def autoowo(ctx):
    await ctx.send("> Started Auto OwO")
    change_channel()
    try:
        for task in all_tasks:
            task.start()
            await asyncio.sleep(3)
    except RuntimeError:
        return


@client.command()
async def stopautoowo(ctx):
    await ctx.send("> Stopped Auto OwO")
    try:
        for task in all_tasks_stop:
            task.cancel()
    except RuntimeError:
        return


client.run(token)
