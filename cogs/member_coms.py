import discord
from discord.ext import commands, tasks
import random
from random import randint
import asyncio
from rea import sexres
import datetime
from nword import *
import requests
import math
from main import client, bot_prefix, round_time, ses, currency, red, green, check_name
from discord import Option
from termcolor import colored, cprint
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
import os
import patreon
from discord.ui import InputText, Modal
from cogs.score import check_currency
from cogs.mini_games import add_milestone
from database import *

from cogs.events import check_logs

logs = 639513264522526769
logs_global = "logs"
empty = '\uFEFF'
fetch = None
words4 = []
words3 = []
words5 = []
color = 255, 255, 255

def check_tier(tier):
  if tier < 100:
    return "Tier 0"
  elif tier == 100:
    return "Tier 1"
  elif tier == 300:
    return "Tier 2"
  elif tier == 500:
    return "Tier 3"
  elif tier == 1000:
    return "Tier 4"

def higher_or_lower(chosen, id):
  value = get_db('minigames')['hilo'][f'{id}']
  number = int(value.split("-", 1)[0])

  if int(chosen) < int(number):
    return "higher"
  elif int(chosen) > int(number):
    return "lower"
  else:
    return

def check_payout(chosen, id, bet):
  value = get_db('minigames')['hilo'][f'{id}']
  number = int(value.split("-", 1)[0])
  final_percent = float(value.split("-")[1].lstrip().split("-")[0])
  # payout (if available) #
  if bet == 0:
    if int(chosen) != number:
      if f"{str(chosen)}," in value:
        percent = value.split(f"{chosen},")[1].lstrip().split("/")[0]
        return f"0 close"
      else:
        return "None"
    else:
      return f"0 exact"
  
  if int(chosen) != number:
    if f"{str(chosen)}," in value:
      percent = value.split(f"{chosen},")[1].lstrip().split("/")[0]
      return f"{bet * float(percent) / 100} close"
    else:
      return "None"
  else:
    return f"{bet * final_percent / 100} exact"

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

def fact_generator():
  limit = 1
  fact_api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
  fact_token = os.environ.get("API_NINJAS_KEY")
  fact_response = requests.get(fact_api_url, headers={'X-Api-Key': f'{fact_token}'})
  response2 = fact_response.text.replace('"', "")
  response2 = response2.replace('}', "")
  response2 = response2.replace(']', "")
  response3 = response2.split(": ")[1]
  if fact_response.status_code == requests.codes.ok:
    return response3
  else:
    return

def joke_generator():
  limit = 1
  joke_api_url = 'https://api.api-ninjas.com/v1/jokes?limit={}'.format(limit)
  fact_token = os.environ.get("API_NINJAS_KEY")
  joke_response = requests.get(joke_api_url, headers={'X-Api-Key': f'{fact_token}'})
  response2 = joke_response.text.replace('"', "")
  response2 = response2.replace('}', "")
  response2 = response2.replace(']', "")
  response3 = response2.split(": ")[1]
  if joke_response.status_code == requests.codes.ok:
    return response3
  else:
    return

def file_len():
  with open("ai.txt") as f:
    for i, l in enumerate(f):
      pass
  return i + 1

def add_time(time_add):
  current = datetime.datetime.now()
  add = datetime.timedelta(seconds=int(time_add))
  new_time = current + add

  return str(new_time)

def fixtime(dt):
  dt2 = str(dt)
  timelen = len(dt2)

  dt = dt2[:timelen - 13]
  return dt

class back(discord.ui.View):
  def __init__(self, ctx):
    super().__init__(timeout=None)
    self.ctx = ctx

  @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, custom_id="back", disabled=False)
  async def back(self, button, interaction):
    f = discord.File(f"{os.getcwd()}/images/pixel.png", filename="pixel.png")
    embed = discord.Embed(description=f"If you wish to support this project,\nyou can do so by supporting me on [patreon](https://www.patreon.com/doctorses).\nIf you do not want to subscribe to my patreon, you can always send a one time tip on [paypal](https://paypal.me/faxmachinebot).", color=discord.Color.from_rgb(r=0, g=200, b=0))
    embed.set_footer(text="Your support is greatly appriciated.")
    embed.set_image(url="attachment://pixel.png")
    view = patrons(self.ctx)
    await interaction.message.edit(embed=embed, content=None, view=view, file=f)
    await interaction.response.defer()

class patrons(discord.ui.View):
  def __init__(self, ctx):
    super().__init__(timeout=None)
    self.ctx = ctx

  @discord.ui.button(label="Active Patrons", style=discord.ButtonStyle.green, custom_id="patrons", disabled=False)
  async def patrons(self, button, interaction):
    img = Image.open('images/assets/backgrounds/patreon_background.png').convert("L")
    black = randint(0, 255), randint(0, 255), randint(0, 255)
    img = ImageOps.colorize(img, black=black, white="white")
    img = img.convert("RGBA")
    font = ImageFont.truetype("images/assets/milk.ttf", 70)
    
    active = get_db('misc')['all_patrons']
    coords1 = 50
    coords2 = 50
    for x in active:
      tier = int(active[x]["pledge"])
      user = await client.fetch_user(int(x))
      name = check_name(user.name)
      asset = user.avatar
      data = BytesIO(await asset.read())
      pfp = Image.open(data).convert("RGBA")
      pfp = pfp.resize((200, 200))
      img.paste(smooth_corners(pfp, 50), (coords1, coords2), smooth_corners(pfp, 50))
      position = (270, coords2 + 30)
      draw = ImageDraw.Draw(img)
      draw.text(position, f"{name} • {check_tier(tier)}", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
      coords2 += 250

    img.save("images/patreon.png")
    f = discord.File(f"{os.getcwd()}/images/patreon.png", filename="patreon.png")

    embed = discord.Embed(description=f"Active supporters on [patreon](https://www.patreon.com/doctorses).", color=green)
    embed.set_image(url="attachment://patreon.png")
    embed.set_footer(text="Thank you to everyone involved in supporting me for making this bot.")

    await interaction.message.edit(embed=embed, content=None, file=f, view=back(self.ctx))
    await interaction.response.defer()
    

class Warnings(discord.ui.View):
  def __init__(self, ctx, auth):
    super().__init__(timeout=60)
    self.ctx = ctx
    self.auth = auth

  @discord.ui.button(label="Warnings", style=discord.ButtonStyle.primary, custom_id="warns", disabled=False)
  async def warns(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:
      try:
        warnings = get_db('users')[f"{self.ctx.author.id}"][f'warnings-{interaction.guild.id}']
      except:
        result = "No warnings here, yet."
      else:
        warn_val = []
        num = 1
        for x in warnings:
          warn_val.append(f"**{num} >** {warnings[x]}")
          num += 1
        else:
          warn_val2 = [str(element) for element in warn_val]
          result = "\n".join(warn_val2)
        
      warns = discord.Embed(title=f"**`Information about {self.auth.name}`**", color=self.auth.color)
      warns.add_field(name="**`Warnings:`**", value=result)
      warns.set_footer(icon_url=interaction.user.avatar, text=f'Requested by {interaction.user}')
      view = Info(self.ctx, self.auth)
      await interaction.message.edit(embed=warns, content=None, view=view)
      await interaction.response.defer()
    else:
      return

class Info(discord.ui.View):
  def __init__(self, ctx, auth):
    super().__init__(timeout=60)
    self.ctx = ctx
    self.auth = auth

  @discord.ui.button(label="General Information", style=discord.ButtonStyle.primary, custom_id="info", disabled=False)
  async def info(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:
      member = self.auth
      global hype, voice
      if member.premium_since == None:
        nitro = "None"
      else:
        nitro = f"Since <t:{round(member.premium_since.timestamp())}:f>"
      if member.public_flags.hypesquad_bravery == True:
        hype = "Bravery"
      elif member.public_flags.hypesquad_brilliance == True:
        hype = "Brilliance"
      elif member.public_flags.hypesquad_balance == True:
        hype = "Balance"
      else:
        hype = "None"
      if member.voice != None:
        voice = member.voice.channel
      else:
        voice = "None"
      embed = discord.Embed(title=f"**`Information about {member.name}`**", color=member.color, timestamp=member.created_at)
      embed.set_thumbnail(url=member.avatar)
      embed.set_footer(text=f'Account age:')
      embed.add_field(name='ID:', value=f"{member.id}")
      embed.add_field(name='Nickname:', value=f'{member.display_name}')
      embed.add_field(name='Bot?', value=member.bot)
      embed.add_field(name='Joined:', value=f"<t:{round(member.joined_at.timestamp())}:f>")
      embed.add_field(name='Status:', value=member.status)
      embed.add_field(name='Boost:', value=nitro)
      embed.add_field(name='On Mobile?', value=member.is_on_mobile())
      embed.add_field(name='Voice status:', value=f"Channel: `{voice}`")
      embed.add_field(name='Hypesquad:', value=hype)
      view = Warnings(self.ctx, self.auth)
      await interaction.message.edit(embed=embed, content=None, view=view)
      await interaction.response.defer()
    else:
      return

class Avatar2(discord.ui.View):
  def __init__(self, ctx, auth2):
    super().__init__(timeout=60)
    self.ctx = ctx
    self.auth2 = auth2
    self.value = 1

  @discord.ui.button(label="Global Avatar", style=discord.ButtonStyle.primary, custom_id="Avatar2", disabled=False)
  async def svav2(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:
      avatar = discord.Embed(title=f"{self.auth2.name}'s avatar:", description=f"[Avatar Url]({self.auth2.avatar})\n{self.auth2.mention} - ID: {self.auth2.id}", color=self.auth2.color)
      avatar.set_image(url=f'{self.auth2.avatar}')
      
      view = Avatar(self.ctx, self.auth2)
      try:
        await interaction.message.edit(embed=avatar, content=None, view=view)
        await interaction.response.defer()
      except:
        await interaction.response.edit_message(embed=avatar, content=None, view=view)
        await interaction.response.defer()
      finally:
        return
    else:
      return
  
  @discord.ui.button(label="Banner", style=discord.ButtonStyle.primary, custom_id="Banner", disabled=False)
  async def banner(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:
      global fetch
      if fetch != None:
        if fetch.id == self.auth2.id:
          pass
        else:
          fetch = await client.fetch_user(self.auth2.id)
      else:
        fetch = await client.fetch_user(self.auth2.id)
        if fetch.id == self.auth2.id:
          pass
        else:
          fetch = await client.fetch_user(self.auth2.id)
      if fetch.banner == None:
        button.disabled = True
        try:
          await interaction.message.edit(view=self)
          await interaction.response.defer()
        except:
          await interaction.response.edit_message(view=self)
          await interaction.response.defer()
        finally:
          return
      else:
        avatar = discord.Embed(title=f"{self.auth2.name}'s banner:", description=f"[Banner Url]({fetch.banner})\n{self.auth2.mention} - ID: {self.auth2.id}", color=self.auth2.color)
        avatar.set_image(url=f'{fetch.banner}')
        
        view = Avatar2(self.ctx, self.auth2)
        try:
          await interaction.message.edit(embed=avatar, content=None, view=view)
          await interaction.response.defer()
        except:
          await interaction.response.edit_message(embed=avatar, content=None, view=view)
          await interaction.response.defer()
        finally:
          return
    else:
      return
  
  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    else:
      await self.message.edit(view=self, content="Timed out.")

class Avatar(discord.ui.View):
  def __init__(self, ctx, auth2):
    super().__init__(timeout=60)
    self.ctx = ctx
    self.auth2 = auth2
    self.value = 1

  @discord.ui.button(label="Server Avatar", style=discord.ButtonStyle.primary, custom_id="Avatar", disabled=False)
  async def svav(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:
      if (self.ctx.guild == None) or (self.auth2.guild_avatar == None):
        button.disabled = True
        try:
          await interaction.message.edit(view=self)
          await interaction.response.defer()
        except:
          await interaction.response.edit_message(view=self)
          await interaction.response.defer()
        finally:
          return
      else:
        avatar = discord.Embed(title=f"{self.auth2.name}'s server avatar:", description=f"[Avatar Url]({self.auth2.guild_avatar})\n{self.auth2.mention} - ID: {self.auth2.id}", color=self.auth2.color)
        avatar.set_image(url=f'{self.auth2.guild_avatar}')
        
        view = Avatar2(self.ctx, self.auth2)
        try:
          await interaction.message.edit(embed=avatar, content=None, view=view)
          await interaction.response.defer()
        except:
          await interaction.response.edit_message(embed=avatar, content=None, view=view)
          await interaction.response.defer()
        finally:
          return
    else:
      await interaction.response.defer()
      return
  
  @discord.ui.button(label="Banner", style=discord.ButtonStyle.primary, custom_id="Banner", disabled=False)
  async def banner(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:
      global fetch
      if fetch != None:
        if fetch.id == self.auth2.id:
          pass
        else:
          fetch = await client.fetch_user(self.auth2.id)
      else:
        fetch = await client.fetch_user(self.auth2.id)
        if fetch.id == self.auth2.id:
          pass
        else:
          fetch = await client.fetch_user(self.auth2.id)
      if fetch.banner == None:
        button.disabled = True
        try:
          await interaction.message.edit(view=self)
          await interaction.response.defer()
        except:
          await interaction.response.edit_message(view=self)
          await interaction.response.defer()
        finally:
          return
      else:
        avatar = discord.Embed(title=f"{self.auth2.name}'s banner:", description=f"[Banner Url]({fetch.banner})\n{self.auth2.mention} - ID: {self.auth2.id}", color=self.auth2.color)
        avatar.set_image(url=f'{fetch.banner}')
        
        view = Avatar2(self.ctx, self.auth2)
        try:
          await interaction.message.edit(embed=avatar, content=None, view=view)
          await interaction.response.defer()
        except:
          await interaction.response.edit_message(embed=avatar, content=None, view=view)
          await interaction.response.defer()
        finally:
          return
    else:
      return
  
  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    else:
      await self.message.edit(view=self, content="Timed out.")

class Hilo_Modal(Modal):
  def __init__(self, ctx, max) -> None:
    super().__init__(title="Make your guess")
    self.ctx = ctx
    self.max = max
    self.add_item(InputText(label=f"Type in your guess.", placeholder=f"Between 1 and {self.max}"))
  
  async def callback(self, interaction: discord.Interaction):
    view = Hi_lo(self.ctx)
    footer2 = int(self.children[0].value)
      
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()

    desc = embeddict['description']
    field1 = embeddict['fields'][0]['value']
    field2 = embeddict['fields'][1]['value']

    max = int(str(field1).split("1-")[1])
      
    if "`Bet:` 0" in field2:
      bet = 0
    else:
      bet = int(str(field2).split("`Bet:` ")[1])

    asset = self.ctx.author.display_avatar
    data = BytesIO(await asset.read())
    pfp = Image.open(data).convert("RGBA")
    pfp = pfp.resize((250, 250))
      
    img = Image.open('images/assets/minigame.png')
      
    font = ImageFont.truetype("images/assets/milk.ttf", 60)
    font2 = ImageFont.truetype("images/assets/milk.ttf", 45)

    draw2 = ImageDraw.Draw(img)
    position = (170, 380)
    position2 = (425, 150)
    position3 = (170, 580)

    value = get_db('minigames')['hilo'][f'{self.ctx.message.id}']
    final_percent = value.split("-")[1].lstrip().split("-")[0]
    tries = int(value.split(f"{final_percent}-")[1].lstrip().split("/")[0])
    number = int(value.split("-")[0])

    value2 = value.replace(f"-{tries}/", f"-{tries - 1}/")

    tries -= 1
    update_db('minigames', f"hilo", {f"{self.ctx.message.id}": value2})
      
    bet2 = bet * float(final_percent) / 100
      
    img.paste(smooth_corners(pfp, 50), (75, 50), smooth_corners(pfp, 50))
    draw2.text(position, f"{footer2}", color, font=font, stroke_fill=(0, 0, 0), stroke_width=6)
    draw2.text(position2, f"{bet2} {check_currency(interaction.guild.id)} ({final_percent}%)", color, font=font2, stroke_fill=(0, 0, 0), stroke_width=6)
    draw2.text(position3, f"{tries}", color, font=font, stroke_fill=(0, 0, 0), stroke_width=6)
      
    if "exact" in check_payout(footer2, self.ctx.message.id, bet):
      win = Image.open('images/assets/win.png')
      img.paste(win, (520, 250), win)
      draw2.text((585, 600), "YOU WIN!", (0, 200, 0), font=font, stroke_fill=(0, 0, 0), stroke_width=6)
        
      img.save("images/minigame2.png")
      f = discord.File(f"{os.getcwd()}/images/minigame2.png", filename="minigame2.png")
          
      embed = discord.Embed(description=desc, color=0xf7c200)
      embed.add_field(name=empty, value=field1)
      embed.add_field(name=empty, value=field2)
      embed.set_image(url="attachment://minigame2.png")

      payout = float(check_payout(footer2, self.ctx.message.id, bet).split(" exact")[0])
      if payout > 0:
        score = get_db('users')[f'{interaction.user.id}']['score']
        new_score = float(score) + float(payout)
        update_db('users', f"{interaction.user.id}", {'score': new_score})

      add_milestone(user=self.ctx.author.id, milestone="mini-games, Hi-Lo", amount=1)
      await interaction.message.edit(embed=embed, content=None, view=None, file=f)
      await interaction.response.defer()
        
    else:
      if tries <= 0:
        lost = Image.open('images/assets/lost.png')
        img.paste(lost, (500, 230), lost)
        view = None
        draw2.text((540, 570), "Game Over", (150, 0, 0), font=font, stroke_fill=(0, 0, 0), stroke_width=6)

        if "close" in check_payout(footer2, self.ctx.message.id, bet):
          payout = float(check_payout(footer2, self.ctx.message.id, bet).split(" close")[0])
        else:
           payout = 0
            
        draw2.text((465, 645), f"You got: {payout} {check_currency(interaction.guild.id)}\nThe Number was {number}", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=6)

        img.save("images/minigame2.png")
        f = discord.File(f"{os.getcwd()}/images/minigame2.png", filename="minigame2.png")

        embed = discord.Embed(description=desc, color=red)
        embed.add_field(name=empty, value=field1)
        embed.add_field(name=empty, value=field2)
        embed.set_image(url="attachment://minigame2.png")

        if payout > 0:
          score = get_db('users')[f'{interaction.user.id}']['score']
          new_score = float(score) + float(payout)
          update_db('users', f"{interaction.user.id}", {'score': new_score})
          
        await interaction.message.edit(embed=embed, content=None, view=view, file=f)
        await interaction.response.defer()
        
      elif "higher" in higher_or_lower(footer2, self.ctx.message.id):
        
        higher = Image.open('images/assets/higher2.png')
        img.paste(higher, (500, 250), higher)
        draw2.text((595, 600), "HIGHER", color, font=font, stroke_fill=(0, 0, 0), stroke_width=6)

        img.save("images/minigame2.png")
        f = discord.File(f"{os.getcwd()}/images/minigame2.png", filename="minigame2.png")

        embed = discord.Embed(description=desc, color=green)
        embed.add_field(name=empty, value=field1)
        embed.add_field(name=empty, value=field2)
        embed.set_image(url="attachment://minigame2.png")
        
          
        await interaction.message.edit(embed=embed, content=None, view=view, file=f)
        await interaction.response.defer()
        
      elif "lower" in higher_or_lower(footer2, self.ctx.message.id):
          
        lower = Image.open('images/assets/lower2.png')
        img.paste(lower, (500, 250), lower)
        draw2.text((590, 600), "LOWER", color, font=font, stroke_fill=(0, 0, 0), stroke_width=6)

        img.save("images/minigame2.png")
        f = discord.File(f"{os.getcwd()}/images/minigame2.png", filename="minigame2.png")
          
        embed = discord.Embed(description=desc, color=red)
        embed.add_field(name=empty, value=field1)
        embed.add_field(name=empty, value=field2)
        embed.set_image(url="attachment://minigame2.png")
        
      
        await interaction.message.edit(embed=embed, content=None, view=view, file=f)
        await interaction.response.defer()
      else:
        embed2 = discord.Embed(description=f"Error.", color=red)
        await interaction.message.edit(embed=embed2, content=None, delete_after=30, view=view)
        await interaction.response.defer()
        

class Hi_lo(discord.ui.View):
  def __init__(self, ctx):
    super().__init__(timeout=60)
    self.ctx = ctx
 
  @discord.ui.button(label="Press to guess", style=discord.ButtonStyle.green, custom_id="guess", disabled=False)
  async def guess(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:
      embeds = interaction.message.embeds
      for embed in embeds:
        embeddict = embed.to_dict()
  
      desc = embeddict['description']
      field1 = embeddict['fields'][0]['value']
      field2 = embeddict['fields'][1]['value']
  
      max = int(str(field1).split("1-")[1])
      modal = Hilo_Modal(self.ctx, max)
      await interaction.response.send_modal(modal)
          

class Member_coms(commands.Cog):
  def __init__(self, client):
    self.client = client

  async def disabled_check(self, ctx):
    ### disabled check ###
    try:
      value = get_db('guilds')[f'{ctx.guild.id}']['disable']
    except:
      return
    else:
      if f"<{str(ctx.command.name)}>" in value:
        raise discord.ext.commands.CommandError(f"The <{ctx.command.name}> command is disabled in this server.")
      else:
        ### ignored check ###
        try:
          value = get_db('guilds')[f'{ctx.guild.id}']['ignore']
        except:
          return
        else:
          if str(ctx.channel.id) in value:
            raise discord.ext.commands.CommandError(f"Commands are not allowed in this channel.")
          else:
            pass

  ###commands##

  @commands.command(aliases=['guess', 'guessing', 'random', 'high', 'low'])
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 30, commands.BucketType.guild)
  async def hilo(self, ctx, max_num: int, bet: int = None):
    if max_num < 20:
      tries = 2
      numbers = 2
    if max_num > 1000:
      max_num = 1000

    if max_num > 100:
      numbers = int(max_num / 10)
      tries = int(max_num / 20)
    else:
      numbers = int(max_num / 10)
      tries = int(max_num / 10)
    
    number = randint(1, max_num)
    final_percent = 100
    plus = ""
    minus = ""

    # percentages #
    max2 = max_num
    while max2 != 4:
      max2 -= 1
      final_percent += 1.5
    else:
      final_percent2 = final_percent
      number2 = number
      number3 = number
      while numbers != 0:
        plus = plus + f"{number2 + 1},{final_percent2 - 20}/"
        minus = minus + f"{number3 - 1},{final_percent2 - 20}/"
        numbers -= 1
        final_percent2 -= 20
        number2 += 1
        number3 -= 1
      else:
        pass

    if bet:
      if bet > 10000:
        bet = 10000
      bet2 = bet
      bet3 = bet * final_percent / 10
      score = get_db('users')[f'{ctx.author.id}']['score']
      new_score = float(score) - int(bet)
      update_db('users', f'{ctx.author.id}', {"score": new_score})
    else:
      bet2 = 0
      bet3 = 0

    f = discord.File(f"{os.getcwd()}/images/assets/minigame.png", filename="minigame.png")
    
    update_db("minigames", "hilo", {f"{ctx.message.id}": f"{number}-{final_percent}-{tries}/{plus}/{minus}"})
    embed = discord.Embed(description=f"```ini\n[ ============ Higher or Lower ============ ]\n```")
    embed.add_field(name=empty, value=f"`Min-Max:` 1-{max}", inline=True)
    embed.add_field(name=empty, value=f"`Bet:` {bet2}", inline=True)
    
    embed.set_image(url="attachment://minigame.png")

    view = Hi_lo(ctx)
    await ctx.send(embed=embed, file=f, view=view)
      
  
  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 30, commands.BucketType.guild)
  async def cats(self, ctx):
    nmb = randint(0, 19)
    cats = ['funny cats',
            'cats',
            'kitten',
            'fluffy cat',
            'cute cat',
            'cat meme',
            'ugly cat',
            'furless cat',
            'british cat',
            'jinx cat',
            'jinx cat eyes']
    cats2 = random.choice(cats)
    url = "https://google-search83.p.rapidapi.com/google/search_image"

    querystring = {"query":f"{cats2}","gl":"us","lr":"en","num":"1","start":"0"}
    
    headers = {
    	"X-RapidAPI-Key": "656579fde0msh1a659fc425536d6p163315jsn94162aa70de6",
    	"X-RapidAPI-Host": "google-search83.p.rapidapi.com"
    }
    
    googleresponse = requests.request("GET", url, headers=headers, params=querystring)
    res2 = googleresponse.json()[nmb]['url']
    embed = discord.Embed()
    embed.set_image(url=res2)
    await ctx.send(embed=embed, content=None)

  @commands.command(aliases=["suggest", "botsuggestion"])
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 300, commands.BucketType.guild)
  async def suggestion(self, ctx, *, content: str):
    bans = get_db('misc')['suggestion_bans']

    lencontent = len(content)
    if str(ctx.guild.id) in bans:
      embed = discord.Embed(title="Failed to send.", description=f"Your suggestion: `{content}`\n\n**`Reason:`** You have been banned from using this feature.", color=0xb52005)
      await ctx.message.delete()
      await ctx.author.send(embed=embed, content=None)
    else:
      if lencontent <= 20:
        embed = discord.Embed(title="Failed to send.", description=f"Your suggestion: `{content}`\n\n**`Reason:`** Suggestion does not meet the minimum requirements of being at least 20 letters long.", color=0xb52005)
        await ctx.message.delete()
        await ctx.author.send(embed=embed, content=None)
      else:
        embed = discord.Embed(title="Successfully sent.", description=f"Your suggestion: `{content}`\n\nThank you for your contribution.", color=0x178a00)
        await ctx.message.delete()

        update_db('misc', 'suggestions', {f'suggestion-{ctx.author.id}': content})
        await ctx.author.send(embed=embed, content=None)

  @commands.command(aliases=['hi', 'hey'])
  async def hello(self, ctx):
    hy = ['Hello',
          'Hi',
          'Hey',
          'Hello there',
          'Fuck you',
          'No',
          'Hey sexy',
          'He\ny',
          'w',
          'bruh',
          'Hello',
          'Hi',
          'Hey',
          'Hello there',
          'Fuck you',
          'No',
          'Hey sexy',
          'He\ny',
          'w',
          'bruh',
          "The pain, It's unbearable, please end it"]
    async with ctx.typing():
      await asyncio.sleep(1)
      await ctx.send(random.choice(hy))
  
  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 10, commands.BucketType.guild)
  async def nword(self, ctx, cont: str=None):
    if cont != None:
      cont2 = cont.lower()
      if cont2 == "count":
        await ctx.send(f"`Out of {nword2} words, you got:` {random.choice(n_word)}")
      else:
        await ctx.send(random.choice(n_word))
    else:
      await ctx.send(random.choice(n_word))
    
  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 10, commands.BucketType.guild)
  async def shanky(self, ctx, *, add=None):
    shank2 = get_db("misc")['shanky']
    if add:
      if ctx.author.id == ses:
        update_db('misc', 'none', {'shanky': f"{shank2}{add}+"})
        await ctx.send("Added to the database.")
      else:
        shank = shank2.split("+")
        await ctx.send(random.choice(shank))
    else:
      shank = shank2.split("+")
      await ctx.send(random.choice(shank))

  @commands.command()
  async def invite(self, ctx):
    embed = discord.Embed(description="If you want to invite the bot to your server, use the invite link on [this site](https://fax-machine.doctorses.repl.co/).", color=discord.Color.green())
    await ctx.send(embed=embed, content=None)

  @commands.command(aliases=['hollowses', 'doctorses', 'owner', 'creator'])
  async def ses(self, ctx, *, add=None):
    ses3 = randint(1, 4)
    ses4 = get_db('misc')['ses']
    ses5 = ses4.split("+")
    ses = await client.fetch_user(645660675334471680)
    embed = discord.Embed(description=f"{ses.name}, the creator of this bot.\nIf you found any errors, you can just message the bot itself, and if you want to support this project, you can do so on [patreon](https://www.patreon.com/doctorses).\nIf you do not want to subscribe to my patreon, you can always send a one time tip on [paypal](https://paypal.me/faxmachinebot).\nThe bot's site can be viewed [here](https://fax-machine.doctorses.repl.co).", color=discord.Color.from_rgb(r=50, g=0, b=0))
    embed.set_author(name=check_name(ses), icon_url=ses.avatar)
    if add:
      if ctx.author.id == ses.id:
        update_db('misc', 'none', {'ses': f"{ses4}{add}+"})
        await ctx.send("Added to the database.")
      else:
        if ses3 > 1:
          await ctx.send(embed=embed, content=None)
        else:
          await ctx.send(random.choice(ses5))

    else:
      if ses3 > 1:
        await ctx.send(embed=embed, content=None)
      else:
        await ctx.send(random.choice(ses5))

  @commands.command(aliases=['support', 'dono', 'donat', 'patreon', 'paypal', 'pay'])
  async def donate(self, ctx):
    embed = discord.Embed(description=f"If you wish to support this project,\nyou can do so by supporting me on [patreon](https://www.patreon.com/doctorses).\nIf you do not want to subscribe to my patreon, you can always send a one time tip on [paypal](https://paypal.me/faxmachinebot).", color=discord.Color.from_rgb(r=0, g=200, b=0))
    embed.set_footer(text="Your support is greatly appriciated.")
    view = patrons(ctx)
    await ctx.send(embed=embed, content=None, view=view)
  
  @commands.command(aliases=['faxmachine', 'thefaxmachine', "lauren's fax machine"])
  @commands.before_invoke(disabled_check)
  async def fax(self, ctx, yes=None):
    if not yes:
      await ctx.send("me")
    elif yes == "flip":
      embed = discord.Embed(color=discord.Color.from_rgb(r=0, g=randint(0, 255), b=0))
      embed.set_image(url="https://cdn.discordapp.com/attachments/521281908768899093/775754956841811978/flip.gif")
      await ctx.send(embed=embed, content=None)
    elif yes == "backflip":
      embed = discord.Embed(color=discord.Color.from_rgb(r=0, g=randint(0, 255), b=0))
      embed.set_image(url="https://cdn.discordapp.com/attachments/521281908768899093/775754956841811978/flip.gif")
      await ctx.send(embed=embed, content=None)
    elif yes == "pyramid":
      embed = discord.Embed(color=discord.Color.from_rgb(r=0, g=randint(0, 255), b=0))
      embed.set_image(url="https://cdn.discordapp.com/attachments/521281908768899093/775752767008145418/pyramids.gif")
      await ctx.send(embed=embed, content=None)
    elif yes == "donut":
      embed = discord.Embed(color=discord.Color.from_rgb(r=0, g=randint(0, 255), b=0))
      embed.set_image(url="https://cdn.discordapp.com/attachments/521281908768899093/775753134148288512/donut.gif")
      await ctx.send(embed=embed, content=None)
    elif yes == "planet":
      embed = discord.Embed(color=discord.Color.from_rgb(r=0, g=randint(0, 255), b=0))
      embed.set_image(url="https://cdn.discordapp.com/attachments/521281908768899093/775752415713820672/sun_n_planet.gif")
      await ctx.send(embed=embed, content=None)
    elif yes == "spin":
      embed = discord.Embed(color=discord.Color.from_rgb(r=0, g=randint(0, 255), b=0))
      embed.set_image(url="https://cdn.discordapp.com/attachments/521281908768899093/775752209157062716/spin.gif")
      await ctx.send(embed=embed, content=None)
    elif yes == "cube":
      embed = discord.Embed(color=discord.Color.from_rgb(r=0, g=randint(0, 255), b=0))
      embed.set_image(url="https://media.discordapp.net/attachments/521281908768899093/775719252774092800/cubefax.gif")
      await ctx.send(embed=embed, content=None)
    else:
      await ctx.send("no")

  @commands.command()
  @commands.cooldown(1, 15, commands.BucketType.user)
  @commands.before_invoke(disabled_check)
  @commands.guild_only()
  async def userinfo(self, ctx, *, member: discord.Member=None):
    server = client.get_guild(ctx.guild.id)
    if not member:
      member = ctx.author
      global hype, voice
      if member.premium_since == None:
        nitro = "None"
      else:
        nitro = f"Since <t:{round(member.premium_since.timestamp())}:f>"
      if member.public_flags.hypesquad_bravery == True:
        hype = "Bravery"
      elif member.public_flags.hypesquad_brilliance == True:
        hype = "Brilliance"
      elif member.public_flags.hypesquad_balance == True:
        hype = "Balance"
      else:
        hype = "None"
      if member.voice != None:
        voice = member.voice.channel
      else:
        voice = "None"
      embed = discord.Embed(title=f"**`Information about {member.name}`**", color=member.color, timestamp=member.created_at)
      embed.set_thumbnail(url=member.avatar)
      embed.set_footer(text=f'Account age:')
      embed.add_field(name='ID:', value=f"{member.id}")
      embed.add_field(name='Nickname:', value=f'{member.display_name}')
      embed.add_field(name='Bot?', value=member.bot)
      embed.add_field(name='Joined:', value=f"<t:{round(member.joined_at.timestamp())}:f>")
      embed.add_field(name='Status:', value=member.status)
      embed.add_field(name='Boost:', value=nitro)
      embed.add_field(name='On Mobile?', value=member.is_on_mobile())
      embed.add_field(name='Voice status:', value=f"Channel: `{voice}`")
      embed.add_field(name='Hypesquad:', value=hype)
      async with ctx.typing():
        await asyncio.sleep(1)
        auth = member
        view = Warnings(ctx, auth)
        await ctx.send(embed=embed, content=None, view=view)
    else:
      if member == int or member.mention:
        pass
      else:
        member = server.get_member_named(member)
      if member.premium_since == None:
        nitro = "None"
      else:
        nitro = f"Since <t:{round(member.premium_since.timestamp())}:f>"
      if member.public_flags.hypesquad_bravery == True:
        hype = "Bravery"
      elif member.public_flags.hypesquad_brilliance == True:
        hype = "Brilliance"
      elif member.public_flags.hypesquad_balance == True:
        hype = "Balance"
      else:
        hype = "None"
      if member.voice != None:
        voice = member.voice.channel
      else:
        voice = "None"
      embed = discord.Embed(title=f"**`Information about {member.name}`**", color=member.color, timestamp=member.created_at)
      embed.set_thumbnail(url=member.avatar)
      embed.set_footer(text=f'Account age:')
      embed.add_field(name='ID:', value=f"{member.id}")
      embed.add_field(name='Nickname:', value=f'{member.display_name}')
      embed.add_field(name='Bot?', value=member.bot)
      embed.add_field(name='Joined:', value=f"<t:{round(member.joined_at.timestamp())}:f>")
      embed.add_field(name='Status:', value=member.status)
      embed.add_field(name='Boost:', value=nitro)
      embed.add_field(name='On Mobile?', value=member.is_on_mobile())
      embed.add_field(name='Voice status:', value=f"Channel: `{voice}`")
      embed.add_field(name='Hypesquad:', value=hype)
      async with ctx.typing():
        await asyncio.sleep(1)
        auth = member
        view = Warnings(ctx, auth)
        await ctx.send(embed=embed, content=None, view=view)

  @commands.command()
  @commands.cooldown(1, 15, commands.BucketType.user)
  @commands.before_invoke(disabled_check)
  @commands.guild_only()
  async def roleinfo(self, ctx, *, member: discord.Member=None):
    if not member:
      member = ctx.author
      roles = [role for role in ctx.author.roles]
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
      embed.add_field(name='Top role:', value=member.top_role.mention, inline=True)
      if member.id == member.guild.owner.id:
        embed.add_field(name='Important:', value=f"**`Server Owner`**", inline=True)
      else:
        pass
      async with ctx.typing():
        await asyncio.sleep(1)
        await ctx.send(embed=embed, content=None)
    else:
      if member == int or member.mention:
        pass
      else:
        member = ctx.guild.get_member_named(member)
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
      embed.add_field(name='Top role:', value=member.top_role.mention, inline=True)
      if member.id == member.guild.owner.id:
        embed.add_field(name='Important:', value=f"**`Server Owner`**", inline=True)
      else:
        pass
      async with ctx.typing():
          await asyncio.sleep(1)
          await ctx.send(embed=embed, content=None)
  

  @commands.command()
  @commands.cooldown(1, 60, commands.BucketType.guild)
  @commands.before_invoke(disabled_check)
  async def monkey(self, ctx):
    nmb = randint(0, 19)
    monky = ['funny monkey',
            'monkey',
            'gorilla',
            'cute monkey',
            'orangutan',
            'monkey meme',
            'fat monkey']
    monky2 = random.choice(monky)
    url = "https://google-search83.p.rapidapi.com/google/search_image"

    querystring = {"query":f"{monky2}","gl":"us","lr":"en","num":"1","start":"0"}
    
    headers = {
    	"X-RapidAPI-Key": "656579fde0msh1a659fc425536d6p163315jsn94162aa70de6",
    	"X-RapidAPI-Host": "google-search83.p.rapidapi.com"
    }
    
    googleresponse = requests.request("GET", url, headers=headers, params=querystring)
    ress2 = googleresponse.json()[nmb]['url']
    embed = discord.Embed(description=f"Here's a {monky2}, just for you.")
    embed.set_image(url=ress2)
    await ctx.send(embed=embed, content=None)

  @commands.command(aliases=['gayrate'])
  @commands.cooldown(1, 10, commands.BucketType.guild)
  @commands.before_invoke(disabled_check)
  async def gay(self, ctx, member=None):
    msg = ctx.message
    gay1 = randint(0, 100)
    gay3 = randint(0, 25)
    if gay1 == 100:
      gay2 = 00
    else:
      gay2 = randint(0, 99)
      if not member:
        member = ctx.author

      embed = discord.Embed(description=f"{member.name} is {gay1}.{gay2}% gay", colour=discord.Color.random())
      embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/765631657926852608.webp")
        
      await ctx.send(content=None, embed=embed)

  @commands.command(aliases=['sexy'])
  @commands.cooldown(1, 10, commands.BucketType.guild)
  @commands.before_invoke(disabled_check)
  async def sexyrate(self, ctx, member=None):
    sexy = ["https://cdn.discordapp.com/emojis/866750216950513665.webp",
            "https://cdn.discordapp.com/emojis/733779618573713429.webp",
            "https://cdn.discordapp.com/emojis/1015376082326802513.webp",
            "https://cdn.discordapp.com/emojis/755828831172034582.webp"]
    msg = ctx.message
    first = randint(0, 100)
    first2 = randint(90, 100)
    if first == 100:
      second = 00
    elif first2 == 100:
      second = 00
    else:
      second = randint(0, 99)
      if not member:
        embed = discord.Embed(description=f"** **\nYou are {first}.{second}% sexy", colour=discord.Color.random())
        embed.set_thumbnail(url=random.choice(sexy))
        await ctx.send(content=None, embed=embed)
      else:
        if member == f'<@!{client.user.id}>':
          embed = discord.Embed(description=f"I'm too sexy for you", colour=discord.Color.random())
          embed.set_thumbnail(url=random.choice(sexy))
          await ctx.send(content=None, embed=embed)
        elif "fax" in member:
          embed = discord.Embed(description=f"I'm too sexy for you", colour=discord.Color.random())
          embed.set_thumbnail(url=random.choice(sexy))
          await ctx.send(content=None, embed=embed)
        else:
          embed = discord.Embed(description=f"** **\n{member} is {first}.{second}% sexy", colour=discord.Color.random())
          embed.set_thumbnail(url=random.choice(sexy))
          await ctx.send(content=None, embed=embed)

  @commands.command()
  @commands.before_invoke(disabled_check)
  async def sex(self, ctx):
    value = get_db('misc')['all_patrons']
    if str(ctx.author.id) in list(value):
      pledge = int(value[str(ctx.author.id)]['pledge'])
      if pledge == 1000:
        sexres2 = get_db('misc')['sex_all_yes']
        sexres3 = sexres2.split("/")
        await ctx.send(random.choice(sexres3))
        return
    elif ctx.author.id == ses:
      sexres2 = get_db('misc')['sex_all_yes']
      sexres3 = sexres2.split("/")
      await ctx.send(random.choice(sexres3))
      return
    
    await ctx.send(random.choice(sexres))

  @commands.command()
  @commands.cooldown(1, 10, commands.BucketType.guild)
  @commands.before_invoke(disabled_check)
  async def pet(self, ctx):
      msg = ctx.message
      e = ['<:laurflushed:700019121345134695>',
          '<:laurpleading:700601833521152091>',
          '<:laurahegao:755546270139154433>']
      embed = discord.Embed(description=f'{random.choice(e)}')
      embed.set_image(url='https://media.discordapp.net/attachments/608091112162328657/753676727816945664/faxing.gif')
      await ctx.send(embed=embed, content=None)
      await msg.delete()

  @commands.command(aliases=['avatar', 'avater', 'pfp'])
  @commands.cooldown(1, 20, commands.BucketType.user)
  @commands.before_invoke(disabled_check)
  async def av(self, ctx, *, member: discord.User=None):
    auth2 = ctx.author
    if member:
      auth2 = member
      avatar = discord.Embed(title=f"{auth2.name}'s avatar:", description=f"[Avatar Url]({auth2.avatar})\n{auth2.mention} - ID: {auth2.id}", color=auth2.color)
      avatar.set_footer(icon_url=ctx.author.avatar, text=f'Requested by {ctx.author}')

    avatar = discord.Embed(title=f"{auth2.name}'s avatar:", description=f"[Avatar Url]({auth2.avatar})\n{auth2.mention} - ID: {auth2.id}", color=auth2.color)
    avatar.set_image(url=f'{auth2.avatar}')
    view = Avatar(ctx, auth2)
    
    await ctx.send(embed=avatar, content=None, view=view)

  @commands.command(aliases=['emoji', 'em', 'emote'])
  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.before_invoke(disabled_check)
  async def e(self, ctx, emoji: discord.PartialEmoji):
    emojistring = str(emoji)
    if emojistring.startswith("<"):
      embed = discord.Embed(description=f"{emoji.name} - `ID: {emoji.id}`\n\n[Download link]({emoji.url})")
      embed.set_thumbnail(url=f'{emoji.url}')
      embed.set_footer(text=f'Created at: {fixtime(emoji.created_at)}')
      await ctx.send(embed=embed, content=None)
  
  @e.error
  async def clear_error(self, ctx, error):
    emoji = str(ctx.message.content).split(f'{ctx.command} ', 1)[1]
    for x in client.guilds:
        emojis = client.get_guild(x.id)
        emoji_id = discord.utils.get(emojis.emojis, name=emoji)
        if emoji_id:
          break
        
    if emoji_id == None:
      embed = discord.Embed(description=f"**`ERROR:`** ```python\n{error}\n```", color=red)
      await ctx.send(embed=embed, content=None, delete_after=10)
    else:
      embed = discord.Embed(description=f"{emoji_id.name} - `ID: {emoji_id.id}`\n\n[Download link]({emoji_id.url})")
      embed.set_thumbnail(url=f'{emoji_id.url}')
      embed.set_footer(icon_url=emoji_id.guild.icon, text=f'From: {emoji_id.guild.name}\nCreated at: {fixtime(emoji_id.created_at)}')
      await ctx.send(embed=embed, content=None)
  
  @commands.command(aliases=["s"])
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def sticker(self, ctx, *, sticker: str = None):
    if ctx.message.stickers:
      format = str(ctx.message.stickers[0].format).replace("StickerFormatType.", "")
      embed = discord.Embed(description=f"{ctx.message.stickers[0].name} - `ID: {ctx.message.stickers[0].id}`\nFormat: `{format}`\n\n[Download link]({ctx.message.stickers[0].url})")
      embed.set_thumbnail(url=f"{ctx.message.stickers[0].url}")
      await ctx.send(embed=embed, content=None)
    elif sticker:
      for x in client.guilds:
        stickers = client.get_guild(x.id).stickers
        if sticker in str(stickers):
          sticker_id = str(str(stickers).split(f"{sticker}' id=")[1].lstrip().split(" ")[0]) + f"-{x.id}"
          break
          
      if sticker_id != None:
        id = sticker_id.split("-")[0]
        id2 = sticker_id.split("-")[1]
        server = client.get_guild(int(id2))

        get = await server.fetch_sticker(int(id))
        
        format = str(get.format).replace("StickerFormatType.", "")
        embed = discord.Embed(description=f"{get.name} - `ID: {get.id}`\nFormat: `{format}`\n\n[Download link]({get.url})")
        embed.set_thumbnail(url=f"{get.url}")
        await ctx.send(embed=embed, content=None)
      else:
        embed = discord.Embed(description=f'Could not find sticker "{sticker}"', color=red)
        await ctx.send(embed=embed, content=None)
    else:
      embed = discord.Embed(description=f'Error.', color=red)
      await ctx.send(embed=embed, content=None)

  @commands.command()
  @commands.cooldown(1, 20, commands.BucketType.user)
  @commands.before_invoke(disabled_check)
  async def ask(self, ctx, *, question):
      guild = client.get_guild(ctx.message.guild.id)
      ids = [member for member in guild.members]
      us = random.choice(ids)
      msg = ctx.message
      question2 = question.lower()
      responses = ["It is certain.",
                  "It is decidedly so.",
                  "Without a doubt.",
                  "Yes - definitely.",
                  "You may rely on it.",
                  "As I see it, yes.",
                  "Most likely.",
                  "Outlook good.",
                  "Yes.",
                  "Fuck yeah",
                  "Of course.",
                  "Yeah.",
                  "Obviously",
                  "Signs point to yes.",
                  "Better not tell you now.",
                  "My reply is no.",
                  "My sources say no.",
                  "Outlook not so good.",
                  "Very doubtful.",
                  "No.",
                  "Fuck no",
                  "What? No.",
                  "No wtf",
                  "Monkey.",
                  "what",
                  f"{question}"]
      when = ['Now.',
              'In a bit.',
              'In 5 minutes.',
              'Right fucking now',
              "Right now.",
              "Never.",
              "Not even in a year.",
              "When the sun will collapse",
              "uhhhhhhhhhhhhhhhhh never",
              "In like 10 years."]
      where = ['Behind you.',
              'Right behind you.',
              'Like 100 feet away.',
              'At the other side of the fucking planet',
              "In Nessie's ass.",
              "In Shaggy's porn stash.",
              "In Brazil.",
              "Somewhere in Romania."]
      how = ["I don't even know.",
            "No clue.",
            "No fucking idea.",
            "You have to be a monkey to know how",
            "Monkies are always the answer.",
            "I still don't know.",
            "how",
            "Ask SeS"]
      who = ["You.",
            "Me.",
            "You, obviously.",
            "Someone.",
            "Not me",
            f"{us}"]
      what = ["A monkey.",
              "A retard",
              "A water balloon.",
              "A deformed trollface.",
              "<:showernow:941641965039140904>",
              "A disappointment.",
              "Black.",
              "Asian.",
              "Twink.",
              "A Gypsy.",
              "Romanian.",
              "A huge fucking dumbass.",
              "A gigantic retard.",
              "A Jew.",
              "A Chinese immigrant.",
              "A Mongolian chad."]
      huh = ['Huh?',
             "What?",
             "The fuck?",
             "Hm?",
             "what"]
      embed = discord.Embed(title=f'Question: {question}', colour=ctx.author.color, timestamp=ctx.message.created_at)
      embed.set_footer(icon_url=ctx.author.avatar, text=f'Requested by {ctx.author}')
    
      if "when " in question2:
        embed.add_field(name='**Answer:**', value=f'{random.choice(when)}')
      elif "where" in question2:
        embed.add_field(name='**Answer:**', value=f'{random.choice(where)}')
      elif question.startswith("how"):
        embed.add_field(name='**Answer:**', value=f'{random.choice(how)}')
      elif "why " in question2:
        embed.add_field(name='**Answer:**', value=f'{random.choice(how)}')
      elif "who " in question2:
        embed.add_field(name='**Answer:**', value=f'{random.choice(who)}')
      elif "what" in question2:
        if "is" in question2:
          embed.add_field(name='**Answer:**', value=f'{random.choice(what)}')
        elif "am i" in question2:
          embed.add_field(name='**Answer:**', value=f'{random.choice(what)}')
        else:
          embed.add_field(name='**Answer:**', value=f'{random.choice(responses)}')
      elif "http" in question2:
        embed.add_field(name='**Answer:**', value=f'{random.choice(huh)}')
      elif question.startswith("g!"):
        embed.add_field(name='**Answer:**', value=f'Command moment')
      elif "fact" in question2:
        embed.add_field(name='**Fact:**', value=fact_generator())
      elif "joke" in question2:
        embed.add_field(name='**Joke:**', value=joke_generator())
      else:
        embed.add_field(name='**Answer:**', value=f'{random.choice(responses)}')
        
      async with ctx.typing():
        await asyncio.sleep(0.5)
        await ctx.send(content=None, embed=embed)

def setup(client):
  client.add_cog(Member_coms(client))
