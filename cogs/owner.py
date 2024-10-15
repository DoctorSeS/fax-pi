import discord
from discord.ext import commands, tasks
from main import client, round_time, patreon_id, check_name, currency, red, green
import os
import asyncio
import json
import requests
from random import randint
import random
import DiscordUtils
from termcolor import cprint
import patreon
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import datetime
from cogs.score import check_currency, check_folder, check_role
from database import *

token = os.environ.get("DISCORD_BOT_SECRET")
cai_token = os.environ.get("C.AI_TOKEN")
cai_fax = os.environ.get("C.AI_FAX")
nm = 0
logs_global = "logs"
gil = []
gil2 = 0
listofcogs = client.cogs
empty = '\uFEFF'


def role_pos(role):
  x = 625
  y = 195
  if "Common" in role:
    return (x-15,  y+5)
  elif "Uncommon" in role:
    return (x+60, y+5)
  elif "Rare" in role:
    return (x-155, y+5)
  elif "Legendary" in role:
    return (x+35, y+5)
  elif "Exotic" in role:
    return (x-100, y+5)
  elif "Daredevil" in role:
    return (x-5, y)
  elif "Prophet" in role:
    return (x-40, y)

def get_dominant_color(pil_img):
  img = pil_img.copy()
  img = img.convert("RGBA")
  img = img.resize((1, 1), resample=0)
  dominant_color = img.getpixel((0, 0))
  return dominant_color

def smooth_corners(im, rad):
  circle = Image.new('L', (rad * 2, rad * 2), 0)
  draw = ImageDraw.Draw(circle)
  draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
  alpha = Image.new('L', im.size, 255)
  w, h = im.size
  alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
  alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
  alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
  alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
  im.putalpha(alpha)
  return im

def next_milestone(current):
  milestone = current + 10000
  milestone = int(str(milestone)[:-4]) * 10000
  return milestone

def next_reward(current, to, guild_id):
  if current < 10000:
    return "Common Role (1.1x multiplier)"
  elif current < 20000:
    return "Uncommon Role (1.2x multiplier)"
  elif current < 30000:
    return "Rare Role (1.3x multiplier)"
  elif current < 40000:
    return "Legendary Role (1.4x multiplier)"
  elif current < 50000:
    return "Exotic Role (1.5x multiplier)"
  else:
    return f"{int(to / 40)} {check_currency(guild_id)}"

def check_level(name, userid):
  milestones = get_db('users')[f'{userid}']['milestones']
  if "gamble" in name.lower():
    num = milestones['Compulsive Gambler']['amount']
    if num >= 10000:
      return 6
    elif num >= 5000:
      return 5
    elif num >= 2500:
      return 4
    elif num >= 1000:
      return 3
    elif num >= 500:
      return 2
    elif num >= 100:
      return 1
    else:
      return 1
  if "game" in name.lower():
    num = milestones['Mini-Games Won']['amount']
    if num >= 1000:
      return 6
    elif num >= 750:
      return 5
    elif num >= 500:
      return 4
    elif num >= 250:
      return 3
    elif num >= 100:
      return 2
    elif num >= 50:
      return 1
    else:
      return 1
      
  elif "role" in name:
    num = milestones['Beta Role']['level']
    return num
  
  else:
    return 1

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

def fixtime(dt):
  dt2 = str(dt)
  timelen = len(dt2)

  dt = dt2[:timelen - 13]
  return dt

class Test(discord.ui.View):
  def __init__(self, ctx):
    super().__init__(timeout=30)
    self.ctx = ctx

  @discord.ui.button(label="Edit Profile", style=discord.ButtonStyle.secondary, custom_id="Edit")
  async def edit(self, button, interaction):
    await self.ctx.invoke(client.get_command("inventory"))
    await interaction.message.delete()

  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    return

class Confirm(discord.ui.View):
  def __init__(self, id):
    super().__init__(timeout=30)
    self.id = id

  @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="Yes")
  async def yes(self, button, interaction):
    if interaction.user.id == self.id:
      embed = discord.Embed(description="Killed all processes.")
      await interaction.message.edit(embed=embed, content=None, view=None)
      os.system("kill 1")
  
  @discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="No")
  async def no(self, button, interaction):
    if interaction.user.id == self.id:
      embed = discord.Embed(description="Cancelled request.")
      await interaction.message.edit(embed=embed, content=None, view=None)
      return

class Owner(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  @commands.is_owner()
  async def embedtest(self, ctx, url_select):
    embed = discord.Embed(title="Test", description="Test", color=discord.Color.blue())
    embed.set_image(url=url_select)
    
    await ctx.send(embed=embed)
  
  @commands.command()
  @commands.is_owner()
  async def perms(self, ctx, *, server: int):
    server = client.get_guild(int(server))
    member = server.get_member(client.user.id)
    roles = [role for role in member.roles]
    rols = str([role.mention for role in roles])
    rols2 = rols.replace("'", '')
    rols3 = rols2.replace("[", '')
    rols4 = rols3.replace("]", '')
    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"Information about {member.name}'s roles")
    embed.set_thumbnail(url=member.avatar)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar)
    embed.add_field(name='Permissions:',
                      value=f"`Administrator:` {member.guild_permissions.administrator}\n`Ban members:` {member.guild_permissions.ban_members}\n`Kick members:` {member.guild_permissions.kick_members}\n`Can view the logs:` {member.guild_permissions.view_audit_log}\n"
                            f"`Manage channels:` {member.guild_permissions.manage_channels}\n`Manage messages:` {member.guild_permissions.manage_messages}\n`Manage server:` {member.guild_permissions.manage_guild}\n`View insights:` {member.guild_permissions.view_guild_insights}\n"
                            f"`Manage emojis:` {member.guild_permissions.manage_emojis}\n`Manage roles:` {member.guild_permissions.manage_roles}\n`Manage Permissions:` {member.guild_permissions.manage_permissions}\n`View`<#{ctx.channel.id}>`:` {member.guild_permissions.view_channel}")
    embed.add_field(name=f'Information about `{member.top_role}`:',
                      value=f"`ID:` {member.top_role.id}\n`Color:` {member.top_role.color}\n`Position:` {member.top_role.position}\n`Default?` {member.top_role.is_default()}\n"
                            f"`Created at:` {fixtime(member.top_role.created_at)}\n`Mentionable?` {member.top_role.mentionable}")
    embed.add_field(name=f'Roles ({len(roles)})', value=f"{rols4}", inline=False)
    embed.add_field(name='Top role:', value=f"{member.top_role.name} - {member.top_role.id}", inline=True)
    if member.id == member.guild.owner.id:
      embed.add_field(name='Important:', value=f"**`Server Owner`**", inline=True)
      
    async with ctx.typing():
      await asyncio.sleep(0.5)
      await ctx.send(embed=embed, content=None)
  
  """@commands.command()
  @commands.is_owner()
  async def ask_test(self, ctx, *, ask: str): 
    ch_client = PyAsyncCAI(cai_token)
    await ch_client.start()
    mes = ctx.message.content

    data = await ch_client.chat.send_message(cai_fax, mes)

    ch_message = data['replies'][0]['text']
    name = data['src_char']['participant']['name']

    await ctx.send(ch_message)"""
  
  @commands.command()
  @commands.is_owner()
  async def read(self, ctx, *, pref: str):  
    key = open(f"{pref}", "r")
    keys = key.readlines()
    keyslist = list(keys)
    keystr = str(keyslist)
    keysplit = []
    num = 0
    n  = 1800
    for index in range(0, len(keystr), n):
        keysplit.append(keystr[index : index + n])
    else:
      keylen = len(keysplit)
    while num < keylen:
      await ctx.send(f"""```python\n{keysplit[num]}```""")
      num += 1
    else:
      await ctx.send(f"Done. {keylen}")

  @commands.command()
  @commands.is_owner()
  async def view_test(self, ctx):
    embed = discord.Embed(description="hih")
    embed.add_field(name="sex1", value="nuh uh")
    embed.add_field(name="sex2", value="huh")
    await ctx.send(embed=embed, content=None)

    embeds = ctx.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()

    h = embeddict['fields'][0]
    await ctx.send(h)

  @commands.command()
  @commands.is_owner()
  async def rate(self, ctx):
    req = requests.get("https://discord.com/api/path/to/the/endpoint")

    await ctx.send(f'{req.headers} requests left.')
    
  @commands.command()
  @commands.is_owner()
  async def nick_change(self, ctx, *, nickname: str):
    await ctx.author.edit(nick=f"{nickname}", reason="hi")
    await ctx.message.delete()
    
  @commands.command()
  @commands.is_owner()
  async def wipe(self, ctx, file: str):
    try:
      openfile = open(f"{file}.txt", "r+")
    except discord.HTTPException as error:
      await ctx.send(error)
    if openfile != None:
      embed = discord.Embed(description=f'Are you sure you want to wipe **`{file}.txt`**?\nTo confirm, please respond with `yes`')
      embed.set_footer(text='This request will expire in 15 seconds.')
      embed3 = discord.Embed(description=f'**`{file}.txt`** has been wiped.')
      shut = await ctx.send(embed=embed, content=None, delete_after=15)

      def check(m):
        return m.content.startswith('yes') and m.author == ctx.author

      msg = await client.wait_for("message", check=check, timeout=20)
      await shut.edit(embed=embed3, content=None)
      await msg.delete()
      openfile.truncate(0)
      openfile.close()
      
  @commands.command()
  @commands.is_owner()
  async def cmd(self, ctx, *, com: str):
    success = False
    comclean = com.replace("```", "")
    comclean2 = comclean.replace("python", "", 1)
    comclean3 = comclean2.replace("\n", "", 1)
    try:
      exec(comclean3)
    except discord.HTTPException as er:
      embed = discord.Embed(description=f"```python\nAn error has occured.\n\n{comclean3}\n\nThe code cannot be run.\n\nError: {er}```")
      await ctx.send(embed=embed, content=None)
      success = False
    else:
      success = True
    if success == True:
      embed = discord.Embed(description=f"```python\n{comclean3}\n\nThe code has been executed sucessfully.```")
      await ctx.send(embed=embed, content=None)
    else:
      return

  @commands.command()
  @commands.is_owner()
  async def emp(self, ctx):
    col = discord.Color.dark_theme()
    embed = discord.Embed(title="Supporting this project", description="[Patreon:](https://patreon.com/doctorses) https://patreon.com/doctorses\n[Paypal:](https://paypal.me/faxmachinebot) https://paypal.me/faxmachinebot\n```fix\nIf you wish to support me on a monthly basis, even for just one month, you can do so on my patreon.\n\nIf subscriptions aren't your style, you can also send a tip on my paypal.```", color=col)
    await ctx.message.delete()
    await ctx.send(embed=embed, content=None)

  @commands.command(aliases=["kill"])
  @commands.is_owner()
  async def killswitch(self, ctx):
    embed = discord.Embed(description="Are you sure you want to kill all processes?")
    id = ctx.author.id
    view = Confirm(id)
    await ctx.send(embed=embed, content=None, view=view)
  
  @commands.command()
  @commands.is_owner()
  async def globalsay(self, ctx, guild: int, channel: int, *, say: str):
    server = client.get_guild(guild)
    channel = server.get_channel(channel)
    embed = discord.Embed(description=f"Message sent in **`{server.name}`**, Channel: **`{channel.name}`**\n\nMessage: {say}")
    await ctx.message.delete()
    async with channel.typing():
      await asyncio.sleep(2)
      await channel.send(say)
      await ctx.send(embed=embed, content=None)

  @commands.command(aliases=["search"])
  @commands.is_owner()
  async def print(self, ctx, *, input: str):
    nmb = randint(0, 19)
    url = "https://google-search83.p.rapidapi.com/google/search_image"

    querystring = {"query":f"{input}","gl":"us","lr":"en","num":"1","start":"0"}
    
    headers = {
    	"X-RapidAPI-Key": "656579fde0msh1a659fc425536d6p163315jsn94162aa70de6",
    	"X-RapidAPI-Host": "google-search83.p.rapidapi.com"
    }
    
    googleresponse = requests.request("GET", url, headers=headers, params=querystring)
    res2 = googleresponse.json()[nmb]['url']
    await ctx.send(res2)

  @commands.command(aliases=["sban"])
  @commands.is_owner()
  async def suggestionban(self, ctx, user: int):
    user2 = await client.fetch_user(user)
    user3 = str(user)
    with open("suggestionbans.txt", "r") as bans:
      bans2 = bans.read()
      if user3 in bans2:
        embed = discord.Embed(description=f"**`ERROR:`** ```\n{user2} is already banned from using the suggestion command.\n```", color=red)
        await ctx.send(embed=embed, content=None, delete_after=5)
        await ctx.message.delete(delay=5)
        bans.close()
      else:
        bans.close()
        f = open("suggestionbans.txt", "a")
        embed = discord.Embed(description=f"**`SUCCESS:`** ```\n{user2} has been banned from using the suggestion command.\n```", color=0x008a12)
        embed2 = discord.Embed(title="You have been banned from using the suggestion command.", description=f"Moderator: {ctx.author} - {fixtime(ctx.message.created_at)}", color=red)
        await ctx.send(embed=embed, content=None, delete_after=5)
        await user2.send(embed=embed2, content=None)
        f.write(user3 + "\n")
        f.close()
        await ctx.message.delete(delay=5)
  
  @commands.command(aliases=["sunban"])
  @commands.is_owner()
  async def suggestionunban(self, ctx, user: int):
    user2 = await client.fetch_user(user)
    user3 = str(user)
    with open("suggestionbans.txt", "r") as bans:
      bans2 = bans.read()
      if user3 in bans2:
        embed = discord.Embed(description=f"**`SUCCESS:`** ```\n{user2} has been unbanned from using the suggestion command.\n```", color=0x008a12)
        embed2 = discord.Embed(title="You have been unbanned from using the suggestion command.", description=f"Moderator: {ctx.author} - {fixtime(ctx.message.created_at)}", color=0x008a12)
        await ctx.send(embed=embed, content=None, delete_after=5)
        await user2.send(embed=embed2, content=None)
        await ctx.message.delete(delay=5)
        with open("suggestionbans.txt", "r") as f:
          lines = f.readlines()
        with open("suggestionbans.txt", "w") as f:
          for line in lines:
            if line.strip("\n") != user3:
              f.write(user3)
              bans.close()
      else:
        embed = discord.Embed(description=f"**`ERROR:`** ```\n{user2} is not banned from using the suggestion command.\n```", color=red)
        await ctx.send(embed=embed, content=None, delete_after=5)
        await ctx.message.delete(delay=5)
        bans.close()
  
  @commands.command()
  @commands.is_owner()
  async def msgdata(self, ctx, msg_id: int):
    server = client.get_guild(ctx.guild.id)
    channel = server.get_channel(ctx.channel.id)
    message = await channel.fetch_message(msg_id)
    embed = discord.Embed(description=f"{message}")
    embed2 = discord.Embed(description=f"{message.type}")
    if message.components:
      embed3 = discord.Embed(description=f"{message.components}")
      await ctx.send(embed=embed3, content=None)  
    
    try:
      embed6 = discord.Embed(description=f"{message.stickers[0].url}")
      await ctx.send(embed=embed6, content=None)
    except:
      pass
    try:
      if message.reference.message_id:
        msg = await ctx.channel.fetch_message(message.reference.message_id)
        embed4 = discord.Embed(description=f"{message.reference.message_id}\n```\n{msg.content}```")
        await ctx.send(embed=embed4, content=None)
        try:
          embeds = msg.embeds
          for embed in embeds:
            embeddict = embed.to_dict()
          embed7 = discord.Embed(description=f"{embeddict}")
          await ctx.send(embed=embed7, content=None)
        except:
          pass
    except:
      pass

    await ctx.send(embed=embed, content=None)
    await ctx.send(embed=embed2, content=None)

  @commands.command(aliases=['logout', 'off', 'shutthefuckup', 'die'])
  @commands.is_owner()
  @commands.cooldown(1, 30, commands.BucketType.guild)
  async def shutdown(self, ctx):
    embed = discord.Embed(description=f'Are you sure you want to shut down the bot?\nTo confirm, please respond with `yes`')
    embed.set_footer(text='This request will expire in 15 seconds.')
    embed3 = discord.Embed(description=f'The bot is shutting down.')
    shut = await ctx.send(embed=embed, content=None, delete_after=15)

    def check(m):
      return m.content.startswith('yes') and m.author == ctx.author

    msg = await client.wait_for("message", check=check, timeout=20)
    await shut.edit(embed=embed3, content=None, delete_after=20)
    await msg.delete()
    await client.logout()

  @commands.command()
  @commands.is_owner()
  async def leave(self, ctx, guild: int=None):
    if guild == None:
      guild = client.get_guild(ctx.guild.id)
    else:
      guild = client.get_guild(guild)
    embed = discord.Embed(description=f'Are you sure you want to leave `{guild.name}`?\nTo confirm, please respond with `yes`')
    embed.set_footer(text='This request will expire in 15 seconds.')
    embed3 = discord.Embed(description=f'The bot has left `{guild.name}`.')
    shut = await ctx.send(embed=embed, content=None, delete_after=15)
    
    def check(m):
      return m.content.startswith('yes') and m.author == ctx.author
    
    msg = await client.wait_for("message", check=check, timeout=20)
    await shut.edit(embed=embed3, content=None, delete_after=20)
    await msg.delete()
    await guild.leave()

  @commands.command()
  @commands.is_owner()
  async def load(self, ctx, extension):
    try:
      self.client.load_extension(f'cogs.{extension}')
    except Exception as e:
      embed = discord.Embed(description=f'**`ERROR:`** ```python\n{type(e).__name__} - {e}\n```', color=0xFF2727)
      await ctx.send(embed=embed, content=None)
    else:
      embed = discord.Embed(description=f"```python\nExtension '{extension}' has been loaded.\n```", color=0x32FF1E)
      await ctx.send(embed=embed, content=None)

  @commands.command()
  @commands.is_owner()
  async def reload(self, ctx, extension: str):
    extension2 = extension.lower()
    try:
      self.client.reload_extension(f'cogs.{extension2}')
    except Exception as e:
      embed = discord.Embed(description=f'**`ERROR:`** ```python\n{type(e).__name__} - {e}\n```', color=0xFF2727)
      await ctx.send(embed=embed, content=None)
    else:
      embed = discord.Embed(description=f"```python\nExtension '{extension2}' has been reloaded.\n```", color=0x32FF1E)
      await ctx.send(embed=embed, content=None)

  @commands.command()
  @commands.is_owner()
  async def unload(self, ctx, extension):
    try:
      self.client.unload_extension(f'cogs.{extension}')
    except Exception as e:
      embed = discord.Embed(description=f'**`ERROR:`** ```python\n{type(e).__name__} - {e}\n```', color=0xFF2727)
      await ctx.send(embed=embed, content=None)
    else:
      embed = discord.Embed(description=f"```python\nExtension '{extension}' has been unloaded.\n```", color=0x32FF1E)
      await ctx.send(embed=embed, content=None)
  
  @commands.command()
  @commands.is_owner()
  async def cogs(self, ctx):
    cogs2 = len(listofcogs)
    cgs = []
    cgs.clear()
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        global nm
        nm += 1
        filename2 = filename.replace('.py', '')
        cgs.append(filename2)
        if nm == cogs2:
          nm = 0
          embed = discord.Embed(description=f"**`{client.user.name}'s cogs: ({cogs2})`**```python\n{cgs}```")
          await ctx.send(embed=embed, content=None)

  @commands.command()
  @commands.is_owner()
  async def servers(self, ctx, *, other: str=None):
    activeservers = client.guilds
    if other:
      server = client.get_guild(client.guilds[len(client.guilds) - 1].id)
      try:
        created_at = server.created_at
      except:
        created_at = None
        pass
      else:
        pass
        
      embed = discord.Embed(description=f'**About {server}**', color=discord.Color.random(), timestamp=created_at)
      embed.set_footer(text=f'Server ID: {server.id}\nServer created at:')
      embed.set_thumbnail(url=server.icon)
  
      if server.premium_subscription_count < 2:
        max_boosts = 2
      elif server.premium_subscription_count < 7:
        max_boosts = 7
      elif server.premium_subscription_count <= 14:
        max_boosts = 14
  
      embed.add_field(name='Information:', value=f'`Owner:` <@{server.owner_id}>\n`Name:` **{server}**\n`Verification level:` **{server.verification_level}**\n`Boosts:` **{server.premium_subscription_count} / {max_boosts}**\n`Boost level:` **{server.premium_tier}**\n`Afk timeout:` **{server.afk_timeout} seconds**\n`Description:` **{server.description}**\n`Afk channel:` **{server.afk_channel}**\n`Total members:` **{server.member_count}**')

      if ctx.author.guild_permissions.manage_roles:
        try:
          logs = get_db('guilds')[f'{ctx.guild.id}']['logs']['active']
        except:
          logs = "False"

        try:
          ai = get_db('guilds')[f'{ctx.guild.id}']['ai']['active']
        except:
          ai = "False"

        try:
          gc = get_db('guilds')[f'{ctx.guild.id}']['global_chat']['active']
        except:
          gc = "False"

        try:
          score = get_db('guilds')[f'{ctx.guild.id}']['score']
        except:
          score = "False"

        embed.add_field(name="Specific Information:", value=f"""`Logs Enabled?` **{logs}**\n`AI Enabled?` **{ai}**\n`Global Chat Enabled?` **{gc}**\n`Score Enabled?` **{score}**""", inline=True)

      await ctx.send(embed=embed, content=None)
      return
      
    for guild in activeservers:
      member = guild.get_member_named(f"{client.user.name}")
      join = member.joined_at
      gil.append(f"{guild.name} - ID: {guild.id}\nJoin Date: {fixtime(join)}\nOwner: {guild.owner}\nOwner ID: {guild.owner.id}")
      if len(gil) == 10:
        embed = discord.Embed(description=f"**`Guilds ({len(client.guilds)})`**")
        embed.add_field(name=empty, value=gil[0])
        embed.add_field(name=empty, value=gil[1])
        embed.add_field(name=empty, value=gil[2])
        embed.add_field(name=empty, value=gil[3])
        embed.add_field(name=empty, value=gil[4])
        embed.add_field(name=empty, value=gil[5])
        embed.add_field(name=empty, value=gil[6])
        embed.add_field(name=empty, value=gil[7])
        embed.add_field(name=empty, value=gil[8])
        embed.add_field(name=empty, value=gil[9])
          
        await ctx.send(embed=embed, content=None)
        gil.clear()
        pass
    else:
      gil2 = str(gil).replace("[", "")
      gil2 = gil2.replace("]", "")
      gil2 = gil2.replace(",", "\n")
      gil2 = gil2.replace("\n", "\n")
      gil2 = gil2.replace("'", "")
      embed = discord.Embed(description=f"**`Guilds ({len(client.guilds)})`**\n\n{gil2}")
      gil.clear()
      await ctx.send(embed=embed, content=None)
  
  @commands.command()
  @commands.is_owner()
  async def test(self, ctx):
    msg = ctx.message
    guild = client.get_guild(ctx.guild.id)
    ctg = discord.utils.get(guild.categories, name="bot staff")
    don = discord.utils.get(guild.roles, name="Donkey")
    overwrites = {
      guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    if ctg is None:
      if don is None:
        await guild.create_role(name="Donkey", permissions=discord.Permissions(send_messages=False, read_messages=True, read_message_history=True))
        category = await guild.create_category(name="bot staff", overwrites=overwrites)
        await guild.create_text_channel(name=logs_global, overwrites=overwrites, category=category)
        await guild.create_text_channel(name="logs-the-second", overwrites=overwrites, category=category)
        await guild.create_text_channel(name="bot-channel-staff", overwrites=overwrites, category=category)
      else:
        category = await guild.create_category(name="bot staff", overwrites=overwrites)
        await guild.create_text_channel(name=logs_global, overwrites=overwrites, category=category)
        await guild.create_text_channel(name="logs-the-second", overwrites=overwrites, category=category)
        await guild.create_text_channel(name="bot-channel-staff", overwrites=overwrites, category=category)
    else:
      if don is None:
        await guild.create_role(name="Donkey", permissions=discord.Permissions(send_messages=False, read_messages=True, read_message_history=True))
      else:
        await ctx.send(f"The {ctg} category and the Donkey role already exist.", delete_after=5)
        await msg.delete()

  @shutdown.error
  async def clear_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      embed= discord.Embed(description=f"{ctx.author.mention}, you aren't allowed to execute the {ctx.command} command.", color=discord.Color.from_rgb(r=255, g=0, b=0))
      await ctx.send(embed=embed, content=None, delete_after=5)

  @commands.command()
  @commands.is_owner()
  async def channels(self, ctx):
    msg = ctx.message
    guild = client.get_guild(ctx.guild.id)
    await ctx.author.send(f"**`{guild}'s text channels:`**\n`{guild.text_channels}`")
    await ctx.author.send(f"**`{guild}'s voice channels:`**\n`{guild.voice_channels}`")
    await msg.delete()

  @commands.command()
  @commands.is_owner()
  async def restart(self, ctx):
    msg = ctx.message
    embed = discord.Embed(description=f'Are you sure you want to restart down the bot?\nTo confirm, please respond with `yes`')
    embed.set_footer(text='This request will expire in 15 seconds.')
    embed3 = discord.Embed(description=f'The bot is restarting.')
    shut = await ctx.send(embed=embed, content=None, delete_after=15)

    def check(m):
      return m.content.startswith('yes') and m.author == ctx.author

    msg = await client.wait_for("message", check=check, timeout=20)
    await shut.edit(embed=embed3, content=None, delete_after=20)
    await msg.delete()
    await client.logout()
    await client.login(token, bot=True, reconnect=True)

  @commands.command()
  @commands.is_owner()
  async def roles(self, ctx):
    msg = ctx.message
    server = await client.fetch_guild(ctx.guild.id)
    await msg.delete()
    await ctx.author.send(f"`{server.roles}`")
  
  @commands.command()
  @commands.is_owner()
  async def gbchat(self, ctx):
    guild = client.get_guild(ctx.guild.id)
    rle = discord.utils.get(guild.roles, name="Lauren's Fax Machine")
    overwrites = {
      guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True),
      guild.get_role(rle.id): discord.PermissionOverwrite(send_messages=True, read_messages=True, manage_messages=True, embed_links=True, attach_files=True, read_message_history=True)
    }
    msg = ctx.message
    server = client.get_guild(ctx.guild.id)
    ctg = discord.utils.get(server.categories, name="bot staff")
    chann = discord.utils.get(server.channels, name="global-chat")
    await msg.delete()
    if chann == None:
      await server.create_text_channel(name="global-chat", category=ctg, overwrites=overwrites, slowmode_delay=10, topic=f"A Text Channel for all the servers that <@{client.user.id}> is in. Make sure to respect discord's TOS. This does not allow nsfw.")
    else:
      return
  
  @commands.command()
  @commands.is_owner()
  async def servunmute(self, ctx, user: discord.Member=None):
    if user == None:
      user = ctx.author
      await user.edit(mute=False, deafen=False)
      await ctx.message.delete()
    else:
      await user.edit(mute=False, deafen=False)
      await ctx.message.delete()
  
  @commands.command()
  @commands.is_owner()
  async def helpcounter(self, ctx):
    file = open("help.txt", "r")
    file2 = file.read()
    await ctx.send(file2)


def setup(client):
  client.add_cog(Owner(client))
