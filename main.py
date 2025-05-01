import json
import logging
import os
import time

import discord
from discord.ext import commands, tasks
import random
import datetime
from random import randint
import traceback
from rea import prefixresponse
from termcolor import cprint
import requests
from database import *
import tracemalloc
import platform
from inputimeout import inputimeout, TimeoutOccurred

tracemalloc.start()

os.environ["DISCORD_BOT_SECRET"] = "ODMwMTk5NTEyNTcyMTAwNjA5.GyR50E.sFezI207cDpL-hyhPGocIPxuiKbAD0unNV6IiE"
os.environ["DISCORD_BOT_SECRET_TEST"] = "MTI1MjYzMDY4NTI4MjQ3MjAyNg.GBTiJG.B__cmQkImH866KCuZmPeLiuMqLxcTOcoB71LiI"
os.environ["C.AI_TOKEN"] = "9d8224253e0afc39e09a9b8dfdef59f86c5b96a5"
os.environ["C.AI_FAX"] = "eAit4xbYC5wLNLaSxmtDMzwXW6X8XyxY01c35ZHZ77U"
os.environ["PATREON_KEY"] = get_db('misc')['patreon_key']
os.environ["PATREON_CLIENT_ID"] = "JILolnWOMpX8rpAViza_ww1zCwB1mesWe9XCUbN9tvQ0lEB0dwdqhOEHfWRrE0kq"
os.environ["PATREON_REFRESH_TOKEN"] = get_db('misc')['patreon_refresh_token']
os.environ["API_NINJAS_KEY"] = "8LxAVyDMAusp/1SV/svJjw==eIMYqUC8KOH6dHK5"
os.environ["OAUTH2_CLIENT_ID"] = "830199512572100609"
os.environ["OAUTH2_CLIENT_SECRET"] = "CZTQl12s2hPnC2hggCMIZusC3Ej7_kWZ"

patreon_id = 20100324

currency = "Kromer"

if platform.system() == "Windows":
    bot_prefix = "!"
else:
    bot_prefix = 'g!'

def check_name(name):
  if "#0" in str(name):
    name2 = str(name).replace("#0", "")
    return f"{name2}"
  else:
    return name

def get_prefix(bot, message):
    try:
        value = get_db('guilds')[f'{message.guild.id}']["prefix"]
    except:
        prefixes = [f"{bot_prefix}", f"{bot_prefix.upper()}"]
        return commands.when_mentioned_or(*prefixes)(bot, message)
    else:
        prefixes = [f"{value}"]
        return commands.when_mentioned_or(*prefixes)(bot, message)

def server_prefix(guild_id):
  try:
    value = get_db('guilds')[f'{guild_id}']["prefix"]
  except:
    return bot_prefix
  else:
    return value

def round_int(x):
    if x == float("inf") or x == float("-inf"):
        return float('nan')  # or x or return whatever makes sense
    return int(round(x))

client = commands.AutoShardedBot(command_prefix=get_prefix, description="The funny bot for the funny servers", case_insensitive=True, shard_count=2, shard_ids=[0, 1], intents=discord.Intents.all())
#lient = commands.Bot(command_prefix=get_prefix, description=f"The funny bot for the funny servers", case_insensitive=True, intents=discord.Intents.all())
Client = discord.Client(intents=discord.Intents.all())
client.remove_command('help')

#COLORS#
red = 0xc40000
green = 0x00d10a
logs = 639513264522526769
logs_global = "logs"
laure = 339823622774456322
faxname = f"Lauren's Fax Machine"
faxpfp = f"https://cdn.discordapp.com/attachments/863561097604497441/911788874349555732/fax.png"
cgs = []
words = []
ses = 645660675334471680
DIR = '/cogs'
site_link = "https://fax-machine.replit.app"
ch = 0
count = 0
msggg = 0
cl = ''


def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


def create_directories():
    directories = [
        "images/rps",
        "images/rr",
        "images/slots",
        "images/assets/backgrounds/custom"
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    else:
        return f"Checked and ensured directory exists"

caught_message = None
all_databases = ['Battleship', 'rr', 'TTT', 'Snipe', 'Hilo', 'Slots', 'RPS']
PING_DATA_FILE = 'templates/latencies.json'

@client.event
async def on_ready():
      cprint('----------------------------------', 'blue')
      cprint("The bot is now online.", "green")
      print(f"Logged in as: {client.user.name}")
      print(f"ID: {client.user.id}")
      print(f"Version: {discord.__version__}")
      print(f"Watching {len(client.guilds)} guilds.")
      print(f'Date and time: {round_time(datetime.datetime.now())}')
      await client.wait_until_ready()
      open('discord.log', 'w').close()
      if client.is_ready():
        cprint("Client ready.", "green")

        nm_lines = len(open(r"ai.txt", "r", encoding='utf-8', errors='replace').readlines())
        print(f"Number of lines in ai.txt: {nm_lines}")
        update_db("misc", 'none', {"ai_lines": nm_lines})

        if platform.system() == "Linux":
            global ch, msggg, cl, count
            ch = client.get_guild(508043534071365652).get_channel(788656008867086346)
            msggg = await ch.fetch_message(831865097726328833)
            cl = client.get_guild(msggg.guild.id)
            bot_data.start()
            del_db('misc', 'time_alive')

            change_status.start()

            all_guilds = []
            for x in client.guilds:
                all_guilds.append(x.id)
            else:
                update_db('misc', 'none', {"all_servers": all_guilds})

        for x in list(get_db('minigames')):
            if x != 'holder':
                del_db('minigames', f"{x}")
        else:
            cprint("Cleaned the 'minigames' database.", "blue")

        print(create_directories())

        ### START LATENCY GRAPH ###
        if os.path.exists(PING_DATA_FILE):
            open(PING_DATA_FILE, "w").close()
        monitor_shard_latency.start()

        ### delete all starboard_messages instances ###
        guilds = get_db('guilds')
        wiped_starboard = 0
        for x in guilds:
            try:
                starboard_messages = guilds[x]['starboard_messages']
                if starboard_messages:
                    del_db(f'guilds/{x}', 'starboard_messages')
                    wiped_starboard += 1
            except:
                continue
        else:
            print(f"Wiped {wiped_starboard} instance of starboard messages.")

        print(finished_cogs)
        cprint('----------------------------------', 'blue')

@client.event
async def on_shard_ready(shard_id):
    cprint('----------------------------------', 'blue')
    shard_ids = [0, 1]
    for x in shard_ids:
        shard = client.get_shard(x)
        print(f"Shard {x} is ready and running.")
        print(f"Ping: {round(shard.latency * 1000)}")
        print(f"Count: {shard.shard_count}")

#--------------------------------------------------------------------------------------------------------------------------------------------

loop = 30

def format_minutes(total_minutes):
    days = total_minutes // 1440
    hours = (total_minutes % 1440) // 60
    minutes = total_minutes % 60

    result = []

    if days > 0:
        result.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        result.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        result.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    return ', '.join(result)

@tasks.loop(seconds=30)
async def monitor_shard_latency():
    shard_ids = [0, 1]
    shard_data = []

    for shard_id in shard_ids:
        shard = client.get_shard(shard_id)
        if shard:
            try:
                ping = round(shard.latency * 1000)
            except:
                ping = 10000
            shard_info = {
                'shard_id': shard_id,
                'ping': ping,
                'time': time.time()
            }
            shard_data.append(shard_info)
    if os.path.exists(PING_DATA_FILE):
        with open(PING_DATA_FILE, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.extend(shard_data)
    if len(existing_data) > 100:
        existing_data = existing_data[-100:]

    with open(PING_DATA_FILE, 'w') as f:
        json.dump(existing_data, f)

@tasks.loop(minutes=loop)
async def bot_data():
    data = get_db('misc')
    total_time = format_minutes(loop)
    try:
        time = data['time_alive']
        time += loop
    except:
        update_db('misc', 'none', {'time_alive': 5})
    else:
        total_time = format_minutes(time)
        update_db('misc', 'none', {'time_alive': time})

    buttons = data['buttons']
    helpcount = data['helped']
    embed = discord.Embed(color=discord.Color.from_rgb(r=randint(0, 255), g=randint(0, 255), b=randint(0, 255)), timestamp=msggg.edited_at)
    embed.set_footer(text=f"This data is updated every {loop} minutes.\nLast restart: ")
    embed.set_thumbnail(url=cl.icon)
    embed.add_field(name=f"**`Data:`**", value=f"`Ping:` **{round_int(client.latency * 1000)}**\n`Version:` **{discord.__version__}**\n`Guilds:` **{len(client.guilds)}**\n`Helped:` **{helpcount}**\n`Cogs:` **{len(client.cogs)}**\n\n**`{msggg.guild}:`**\n`Members:` **{round_int(msggg.guild.member_count)}**\n`Boosts:` **{msggg.guild.premium_subscription_count}**\n`Roles:` **{round_int(len(msggg.guild.roles))}**", inline=True)
    embed.add_field(name=f"**`Other:`**", value=f"`Run-time:` {total_time}\n`Buttons:` **{buttons}**")
    await msggg.edit(embed=embed, content=None)

@tasks.loop(seconds=30)
async def change_status():
    chance2 = randint(1, 30)
    if chance2 == 30:
      line = random.choice(open("ai.txt", "r", encoding='cp932', errors='ignore').readlines())
      await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"ai.txt | {line}"))
      words.clear()
    else:
      await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} Guilds | {bot_prefix}help"))


def round_time(dt=None, round_to=60, tzinfo=None):
    if dt is None:
        dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)


lastuser = int


def fact_generator():
    limit = 1
    fact_api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit, encoding='cp932', errors='ignore')
    fact_token = os.environ.get("API_NINJAS_KEY")
    fact_response = requests.get(fact_api_url,
                                 headers={'X-Api-Key': f'{fact_token}'})
    response2 = fact_response.text.replace('"', "")
    response2 = response2.replace('}', "")
    response2 = response2.replace(']', "")
    response3 = response2.split(": ")[1]
    if fact_response.status_code == requests.codes.ok:
        return response3
    else:
        return


@client.event
async def on_message(message):
    ### prefix response ###
    global lastuser
    if lastuser != message.author.id:
        lastuser = message.author.id
        fact_chance = randint(1, 4)
        if message.content == bot_prefix:
            if fact_chance == 1:
                await message.channel.send(fact_generator())
            else:
                await message.channel.send(random.choice(prefixresponse))
        elif message.content == bot_prefix.upper():
            if fact_chance == 1:
                await message.channel.send(fact_generator())
            else:
                await message.channel.send(random.choice(prefixresponse))
        elif message.content == client.user.mention:
            if fact_chance == 1:
                await message.channel.send(fact_generator())
            else:
                try:
                    value = get_db("guilds")[f'{message.guild.id}']['prefix']
                except:
                    await message.channel.send(f"`My prefix in this server is <{bot_prefix}>.`")
                    pass
                else:
                    await message.channel.send(f"`My prefix in this server is <{value}>.`")
                    pass
        else:
            pass
    else:
        pass
    ### check prefix ###
    try:
      value = get_db("guilds")[f'{message.guild.id}']['prefix']
    except:
      if message.content.startswith(f"{bot_prefix}"):
        await client.process_commands(message)
      elif message.content.startswith(bot_prefix.upper()):
        await client.process_commands(message)
      elif message.content.startswith(client.user.mention):
        await client.process_commands(message)
    else:
      if message.content.startswith(f"{value}"):
        await client.process_commands(message)
      elif message.content.startswith(client.user.mention):
        await client.process_commands(message)


@client.event
async def on_error(event, *args, **kwargs):
    message = args[0]  #Gets the message object
    logging.warning(traceback.format_exc())  #logs the error
    server = client.get_guild(863561097604497438)
    channel = server.get_channel(943488712405291008)
    embed = discord.Embed(description=f"**`ERROR:`** ```python\n{message}\n```", color=0xc40000)
    await channel.send(embed=embed, content=None)

unloaded_cogs = []
all_files_num = 0
errors = ""
### LOAD COGS HERE TO MAKE TIMERS WORK ###
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            all_files_num += 1
            client.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            unloaded_cogs.append((f"{filename[:-3]}", f"{e}", f"{e.__traceback__.tb_lineno}"))
        else:
            if unloaded_cogs:
                for x in unloaded_cogs:
                    errors += f"- ERROR - COG: {x[0]}\n- ERROR - REASON: {x[1]}\n- ERROR - LINE: {x[2]}"

else:
    global finished_cogs
    finished_cogs = f"Finished cog loading. {len(client.cogs)}/{all_files_num}\n{errors}"

if platform.system() == "Windows":
    try:
        user_input = inputimeout(prompt='Test or Live? ', timeout=3)
        if user_input:
            token = os.environ.get("DISCORD_BOT_SECRET")
    except TimeoutOccurred:
        token = os.environ.get("DISCORD_BOT_SECRET_TEST")
else:
    token = os.environ.get("DISCORD_BOT_SECRET")

def exception_handler(loop, context):
  cprint("Caught the following exception", "red")
  cprint(context['message'], "red")


def run_bot():
    try:
        client.run(token)
    except discord.errors.HTTPException:
        print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
        os.system("python restarter.py")

# https://discordapp.com/oauth2/authorize?client_id=830199512572100609&scope=bot&permissions=8
# id=830199512572100609
