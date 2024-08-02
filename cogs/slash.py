import discord
from discord.ext import commands, tasks
import random
from random import randint
import asyncio
from rea import sexres
from nword import *
import json
import requests
import math
from discord.commands import slash_command
from main import client, bot_prefix, round_time, ses, currency, red, green, check_name
from termcolor import cprint
from discord import Option
import datetime
from cogs.shop import role1emoji, role2emoji, role3emoji, role4emoji, role5emoji
from cogs.score import check_currency
from discord.ui import InputText, Modal
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
import os
import time
from database import *

def get_dominant_color(pil_img):
  img = pil_img.copy()
  img = img.convert("RGBA")
  img = img.resize((1, 1), resample=0)
  dominant_color = img.getpixel((0, 0))
  return dominant_color

def add_milestone(user, milestone, amount=None):
  try:
    all_milestones = get_db('users')[f'{user}']['milestones']
  except:
    all_milestones = {}

  if "game" in milestone:
    name = "Mini-Games Won"
    if all_milestones.get(name) is not None:
      total_amount = all_milestones[name]["amount"] + 1
    else:
      total_amount = 1

    if total_amount >= 1000:
      level2 = 6
    elif total_amount >= 750:
      level2 = 5
    elif total_amount >= 500:
      level2 = 4
    elif total_amount >= 250:
      level2 = 3
    elif total_amount >= 100:
      level2 = 2
    elif total_amount >= 50:
      level2 = 1
    else:
      level2 = 0

    filename = f"game_badge{level2}"

  if "gambl" in milestone:
    name = "Compulsive Gambler"
    if all_milestones.get(name) is not None:
      total_amount = all_milestones[name]["amount"] + 1
    else:
      total_amount = 1

    if total_amount >= 5000:
      level2 = 6
    elif total_amount >= 2500:
      level2 = 5
    elif total_amount >= 1000:
      level2 = 4
    elif total_amount >= 500:
      level2 = 3
    elif total_amount >= 250:
      level2 = 2
    elif total_amount >= 100:
      level2 = 1
    else:
      level2 = 0

    filename = f"gambler{level2}"


  all_milestones.update({f"{name}": {"level": level2, "amount": total_amount, "filename": filename}})
  update_db(f'users/{user}', f'milestones', all_milestones)


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


logs = 639513264522526769
logs_global = "logs"
empty = '\uFEFF'
guild_ids = [863561097604497438]
numbers = ["₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉"]

def add_time(time_add):
  current = datetime.datetime.now()
  add = datetime.timedelta(seconds=int(time_add))
  new_time = current + add

  return str(new_time)

def small_to_big(number):
  for num in numbers:
    if number == num:
      lenn = numbers.index(str(num))
      final = lenn
      return final
    else:
      pass
  else:
    return None

class Button(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=60)

  @discord.ui.button(label="Click me", style=discord.ButtonStyle.green, custom_id="some_id")
  async def button(self, button, interaction):
    embed2 = discord.Embed(description="hi")
    await interaction.message.channel.send("hi")
    await interaction.message.edit(content=None, embed=embed2, view=self)
    await interaction.response.defer()

class Pages(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=1500)
    self.value = 1

  @discord.ui.button(label="<", style=discord.ButtonStyle.green, custom_id="Previous Page", disabled=False)
  async def pagedown(self, button, interaction):
    embed1 = discord.Embed(description="Page1")
    embed2 = discord.Embed(description="Page2")
    embed3 = discord.Embed(description="Page3")
    embed4 = discord.Embed(description="Page4")
    self.value -= 1

    if self.value < 1:
      self.value += 1
      pass
    elif self.value > 4:
      self.value -= 1
      pass
    else:
      pass

    await interaction.message.channel.send(self.value)
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()
    if self.value == 1:
      await interaction.message.edit(content=None, embed=embed1, view=self)
      await interaction.response.defer()
      return
    elif self.value == 2:
      await interaction.message.edit(content=None, embed=embed2, view=self)
      await interaction.response.defer()
      return
    elif self.value == 3:
      await interaction.message.edit(content=None, embed=embed3, view=self)
      await interaction.response.defer()
      return

  @discord.ui.button(label=f"Moderator Commands", style=discord.ButtonStyle.grey, custom_id="Other Commands", disabled=False)
  async def current(self, button, interaction):
    mod = discord.Embed(description="Moderator Active")
    embed1 = discord.Embed(description="Page1")
    link = 863561097604497438
    link2 = client.get_guild(link)
    perms = False
    if interaction.message.guild != None:
      if interaction.message.author.guild_permissions.manage_messages == True:
        perms = True
    elif link != None:
      user = link2.get_member(interaction.message.author.id)
      if user.guild_permissions.manage_messages == True:
        perms = True
      else:
        pass
    else:
      pass
    #wait
    if perms == False:
      button.disabled = False
      if button.label == "Member Commands":
        button.label = f"Moderator Commands"
        await interaction.message.edit(content=None, embed=embed1, view=self)
        await interaction.response.defer()
        return
      elif button.label == "Moderator Commands":
        button.label = f"Member Commands"
        await interaction.message.edit(content=None, embed=mod, view=self)
        await interaction.response.defer()
        return
    else:
      button.disabled = True
      await interaction.message.edit(content=None, embed=embed1, view=self)
      await interaction.response.defer()
      return

  @discord.ui.button(label=">", style=discord.ButtonStyle.green, custom_id="Next Page")
  async def pageup(self, button, interaction):
    embed1 = discord.Embed(description="Page1")
    embed2 = discord.Embed(description="Page2")
    embed3 = discord.Embed(description="Page3")
    embed4 = discord.Embed(description="Page4")
    self.value += 1

    if self.value < 1:
      self.value += 1
      pass
    elif self.value > 4:
      self.value -= 1
      pass
    else:
      pass

    await interaction.message.channel.send(self.value)
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()
    if self.value == 3:
      await interaction.message.edit(content=None, embed=embed3, view=self)
      await interaction.response.defer()
      return
    elif self.value == 4:
      await interaction.message.edit(content=None, embed=embed4, view=self)
      await interaction.response.defer()
      return
    elif self.value == 1:
      await interaction.message.edit(content=None, embed=embed2, view=self)
      await interaction.response.defer()
      return

class Select(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=60)
    self.rps = ""

  #server2 = client.get_guild(710840786853429319)
  #emoji = discord.utils.get(server2.emojis, name="stone")
  #emoji2 = discord.utils.get(server2.emojis, name="paper")
  #emoji3 = discord.utils.get(server2.emojis, name="scissors1")
  #emoji4 = discord.utils.get(server2.emojis, name="sex")

  @discord.ui.select(placeholder="Choose your attack.", max_values=1, disabled=False, options=[
        discord.SelectOption(
            label=f"Rock"
        ),
        discord.SelectOption(
            label="Paper"
        ),
        discord.SelectOption(
            label="Scissors"
        ),
        discord.SelectOption(
            label="Random",
            description="Randomly Chosen."
        )
    ])
  async def sele(self, select, interaction):
    val = str(select.values)
    choose2 = ['rock',
               'paper',
               'scissors']
    stone = "<:stone:780724249815810058>"
    pep = "<:paper:780724297509371904>"
    sci = "<:scissors1:780724274762874890>"
    choose3 = random.choice(choose2)
    valre = val.replace("['", "")
    val2 = valre.replace("']", "")
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()

    if userid in embeddict['footer']['text']:
      if "Rock" in val:
        if choose3 == "rock":
          embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`It's a tie.`")
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
        elif choose3 == "scissors":
          embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
        elif choose3 == "paper":
          embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()

      elif "Scissors" in val:
        if choose3 == "rock":
          embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()

        elif choose3 == "scissors":
          embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`It's a tie.`")
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
          await interaction.response.defer()
        elif choose3 == "paper":
          embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()

      elif "Paper" in val:
        if choose3 == "rock":
          embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
        elif choose3 == "scissors":
          embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
        elif choose3 == "paper":
          embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`It's a tie.`")
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()

      elif "Random" in val:
        val2 = random.choice(choose2)
        if "rock" in val2:
          if choose3 == "rock":
            embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`It's a tie.`")
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.message.edit(embed=embed, content=None)
            await interaction.response.defer()
          elif choose3 == "scissors":
            embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.message.edit(embed=embed, content=None)
            await interaction.response.defer()
          elif choose3 == "paper":
            embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.message.edit(embed=embed, content=None)
            await interaction.response.defer()

        elif "scissors" in val2:
          if choose3 == "rock":
            embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.message.edit(embed=embed, content=None)
            await interaction.response.defer()
          elif choose3 == "scissors":
            embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`It's a tie.`")
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.message.edit(embed=embed, content=None)
            await interaction.response.defer()
          elif choose3 == "paper":
            embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.message.edit(embed=embed, content=None)
            await interaction.response.defer()

        elif "scissors" in val2:
          if choose3 == "rock":
            embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.message.edit(embed=embed, content=None)
            await interaction.response.defer()
          elif choose3 == "scissors":
            embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.message.edit(embed=embed, content=None)
            await interaction.response.defer()
          elif choose3 == "paper":
            embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`It's a tie.`")
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.message.edit(embed=embed, content=None)
            await interaction.response.defer()
    else:
      return

def emojies(play):
  if play == "Rock":
    return "<:stone:780724249815810058>"
  elif play == "Scissors":
    return "<:scissors1:780724274762874890>"
  elif play == "Paper":
    return "<:paper:780724297509371904>"
  else:
    return "Error."

class PlayAgain(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=30)

  @discord.ui.button(label="Play Again", style=discord.ButtonStyle.green, custom_id="play_again")
  async def playagain(self, button, interaction):
    playerids = get_db('minigames')['rps'][f'{interaction.message.id}']

    if (interaction.user.id == int(playerids["player1"]["id"])) or (interaction.user.id == int(playerids["player2"]["id"])):
      playerids['player1'].update({"pick": "None"})
      playerids['player2'].update({"pick": "None"})

      update_db('minigames/rps', f'{interaction.message.id}', playerids)

      asset = interaction.guild.get_member(int(playerids["player1"]["id"])).display_avatar
      data = BytesIO(await asset.read())
      player1_pfp = Image.open(data).convert("RGBA").resize((300, 300))

      asset = interaction.guild.get_member(int(playerids["player2"]["id"])).display_avatar
      data = BytesIO(await asset.read())
      player2_pfp = Image.open(data).convert("RGBA").resize((300, 300))

      TINT_COLOR = (0, 0, 0)
      TRANSPARENCY = .50
      OPACITY = int(255 * TRANSPARENCY)

      img = Image.open('images/assets/backgrounds/rps_background.png').convert("L")
      black = randint(0, 200), randint(0, 20), randint(0, 200)
      img = ImageOps.colorize(img, black=black, white="white")
      img = img.convert("RGBA")

      outline = Image.new('RGBA', (302, 302), (30, 30, 30))
      img.paste(smooth_corners(outline, 30), (59, 299), smooth_corners(outline, 30))
      outline = Image.new('RGBA', (302, 302), (30, 30, 30))
      img.paste(smooth_corners(outline, 30), (1139, 299), smooth_corners(outline, 30))

      img.paste(smooth_corners(player1_pfp, 30), (60, 300), smooth_corners(player1_pfp, 30))
      img.paste(smooth_corners(player2_pfp, 30), (1140, 300), smooth_corners(player2_pfp, 30))

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"{playerids['player1']['name']}", font=ImageFont.truetype("images/assets/que.otf", 70))
      draw.text(((450-w)/2, 220), f"{playerids['player1']['name']}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
      _, _, w, h = draw.textbbox((0, 0), f"{playerids['player2']['name']}", font=ImageFont.truetype("images/assets/que.otf", 70))
      draw.text(((2550-w)/2, 220), f"{playerids['player2']['name']}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)

      #picks
      overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
      draw3 = ImageDraw.Draw(overlay)

      outline = Image.new('RGBA', (220, 220), (30, 30, 30, 50))
      draw3.rounded_rectangle((380, 340, 600, 560), fill=TINT_COLOR + (OPACITY,), radius=20)
      draw3.rounded_rectangle((900, 340, 1120, 560), fill=TINT_COLOR + (OPACITY,), radius=20)
      img = Image.alpha_composite(img, overlay)

      if playerids['player1']['pick'] == "None":
        player1_pick = Image.open("images/assets/rps/waiting.png")
      else:
        player1_pick = Image.open(f"""images/assets/rps/{playerids['player1']['pick'].lower()}/{random.choice(os.listdir(f"images/assets/rps/{playerids['player1']['pick'].lower()}"))}""").convert("RGBA").resize((200, 200))

      if playerids['player2']['pick'] == "None":
        player2_pick = Image.open("images/assets/rps/waiting.png")
      else:
        player2_pick = Image.open(f"""images/assets/rps/{playerids['player2']['pick'].lower()}/{random.choice(os.listdir(f"images/assets/rps/{playerids['player2']['pick'].lower()}"))}""").convert("RGBA").resize((200, 200)).transpose(Image.FLIP_LEFT_RIGHT)

      img.paste(player1_pick, (390, 350), player1_pick)
      img.paste(player2_pick, (910, 350), player2_pick)

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"=== Rock, Paper, Scissors ===", font=ImageFont.truetype("images/assets/que.otf", 80))
      draw.text(((1500-w)/2, 20), f"=== Rock, Paper, Scissors ===", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

      overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
      draw3 = ImageDraw.Draw(overlay)

      outline = Image.new('RGBA', (220, 220), (30, 30, 30, 50))
      draw3.rounded_rectangle((650, 680, 850, 870), fill=TINT_COLOR + (OPACITY,), radius=20)
      img = Image.alpha_composite(img, overlay)

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"Bet:", font=ImageFont.truetype("images/assets/que.otf", 80))
      draw.text(((1500-w)/2, 690), f"Bet:", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

      _, _, w, h = draw.textbbox((0, 0), f"{playerids['bet']}", font=ImageFont.truetype("images/assets/que.otf", 80))
      draw.text(((1500-w)/2, 780), f"{playerids['bet']}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

      img.save(f"images/rps/{playerids['player1']['id']}.png")
      f = discord.File(f"{os.getcwd()}/images/rps/{playerids['player1']['id']}.png", filename=f"{playerids['player1']['id']}.png")

      embed = discord.Embed()
      embed.set_image(url=f"attachment://{playerids['player1']['id']}.png")
      await interaction.message.edit(content=None, embed=embed, view=Multi(), file=f)
      await interaction.response.defer()


def complete_transaction(inteid, winner):
  playerids = get_db('minigames')['rps'][f'{inteid}']
  bet = playerids['bet']
  if bet:
    try:
      player1_score = get_db('users')[f'{playerids["player1"]["id"]}']['score']
    except:
      player1_score = None

    try:
      player2_score = get_db('users')[f'{playerids["player2"]["id"]}']['score']
    except:
      player2_score = None

    if (player1_score != None) and (player2_score != None):
      if winner == 1:
        player1value = round(float(player1_score) + float(bet), 2)
        player2value = round(float(player2_score) - float(bet), 2)
      else:
        player1value = round(float(player1_score) - float(bet), 2)
        player2value = round(float(player2_score) + float(bet), 2)

      update_db('users', f'{playerids["player1"]["id"]}', {"score": player1value})
      update_db('users', f'{playerids["player2"]["id"]}', {"score": player2value})

    if (player1_score is None) or (player2_score is None):
      footer = "Could not complete transaction."
    else:
      footer = f"{playerids['player1']['name']}: {player1_score} ≫ {player1value}\n{playerids['player2']['name']}: {player2_score} ≫ {player2value}"

    return footer
  else:
    return


class Multi(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=120)

  @discord.ui.select(placeholder="Choose your attack.", max_values=1, disabled=False, options=[
        discord.SelectOption(
            label=f"Rock"
        ),
        discord.SelectOption(
            label="Paper"
        ),
        discord.SelectOption(
            label="Scissors"
        ),
        discord.SelectOption(
            label="Random",
            description="Randomly Chosen."
        )
    ])
  async def sele(self, select, interaction):
    playerids = get_db('minigames')['rps'][f'{interaction.message.id}']
    if (interaction.user.id == int(playerids["player1"]["id"])) or (interaction.user.id == int(playerids["player2"]["id"])):
      val = str(select.values[0])
      if interaction.user.id == int(playerids["player1"]["id"]):
        firstpick = val
        if "Random" in val:
          choose2 = ["Rock", "Paper", "Scissors"]
          firstpick = random.choice(choose2)

        update_db(f'minigames/rps/{interaction.message.id}', 'player1', {"pick": firstpick})

      if interaction.user.id == int(playerids["player2"]["id"]):
        secondpick = val
        if "Random" in val:
          choose2 = ["Rock", "Paper", "Scissors"]
          secondpick = random.choice(choose2)

        update_db(f'minigames/rps/{interaction.message.id}', 'player2', {"pick": secondpick})

      if (playerids['player1']['pick'] != "None") and (playerids['player2']['pick'] != "None"):

        asset = interaction.guild.get_member(int(playerids["player1"]["id"])).display_avatar
        data = BytesIO(await asset.read())
        player1_pfp = Image.open(data).convert("RGBA").resize((300, 300))

        asset = interaction.guild.get_member(int(playerids["player2"]["id"])).display_avatar
        data = BytesIO(await asset.read())
        player2_pfp = Image.open(data).convert("RGBA").resize((300, 300))

        TINT_COLOR = (0, 0, 0)
        TRANSPARENCY = .50
        OPACITY = int(255 * TRANSPARENCY)

        img = Image.open('images/assets/backgrounds/rps_background.png').convert("L")
        black = randint(0, 200), randint(0, 20), randint(0, 200)
        img = ImageOps.colorize(img, black=black, white="white")
        img = img.convert("RGBA")

        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), f"=== Rock, Paper, Scissors ===", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((1500-w)/2, 20), f"=== Rock, Paper, Scissors ===", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

        overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
        draw3 = ImageDraw.Draw(overlay)

        outline = Image.new('RGBA', (220, 220), (30, 30, 30, 50))
        draw3.rounded_rectangle((650, 680, 850, 870), fill=TINT_COLOR + (OPACITY,), radius=20)
        img = Image.alpha_composite(img, overlay)

        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), f"Bet:", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((1500-w)/2, 690), f"Bet:", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

        _, _, w, h = draw.textbbox((0, 0), f"{playerids['bet']}", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((1500-w)/2, 780), f"{playerids['bet']}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

        winner = 0
        embed = discord.Embed()
        firstpick = playerids['player1']['pick']
        secondpick = playerids['player2']['pick']
        if firstpick == secondpick:
          winner = 0
          pass

        if firstpick == "Rock":
          if secondpick == "Scissors":
            embed.set_footer(text=complete_transaction(interaction.message.id, 1))
            winner = 1
            update_db(f'minigames/rps/{interaction.message.id}', f'player{winner}', {"points": int(playerids[f'player{winner}']['points']) + 1})
            add_milestone(user=int(playerids["player1"]["id"]), milestone="mini-games, RPS", amount=1)
            pass

          elif secondpick == "Paper":
            embed.set_footer(text=complete_transaction(interaction.message.id, 2))
            winner = 2
            update_db(f'minigames/rps/{interaction.message.id}', f'player{winner}', {"points": int(playerids[f'player{winner}']['points']) + 1})
            add_milestone(user=int(playerids["player2"]["id"]), milestone="mini-games, RPS", amount=1)
            pass


        elif firstpick == "Scissors":
          if secondpick == "Rock":
            embed.set_image(url=f"attachment://{playerids['player1']['id']}.png")
            embed.set_footer(text=complete_transaction(interaction.message.id, 2))
            winner = 2
            update_db(f'minigames/rps/{interaction.message.id}', f'player{winner}', {"points": int(playerids[f'player{winner}']['points']) + 1})
            add_milestone(user=int(playerids["player2"]["id"]), milestone="mini-games, RPS", amount=1)
            pass

          elif secondpick == "Paper":
            embed.set_footer(text=complete_transaction(interaction.message.id, 1))
            winner = 1
            update_db(f'minigames/rps/{interaction.message.id}', f'player{winner}', {"points": int(playerids[f'player{winner}']['points']) + 1})
            add_milestone(user=int(playerids["player1"]["id"]), milestone="mini-games, RPS", amount=1)
            pass


        elif firstpick == "Paper":
          if secondpick == "Rock":
            embed.set_footer(text=complete_transaction(interaction.message.id, 1))
            winner = 1
            update_db(f'minigames/rps/{interaction.message.id}', f'player{winner}', {"points": int(playerids[f'player{winner}']['points']) + 1})
            add_milestone(user=int(playerids["player1"]["id"]), milestone="mini-games, RPS", amount=1)
            pass
          elif secondpick == "Scissors":
            embed.set_footer(text=complete_transaction(interaction.message.id, 2))
            winner = 2
            update_db(f'minigames/rps/{interaction.message.id}', f'player{winner}', {"points": int(playerids[f'player{winner}']['points']) + 1})
            add_milestone(user=int(playerids["player2"]["id"]), milestone="mini-games, RPS", amount=1)
            pass

        if winner == 0:
          win = Image.open("images/assets/rps/tie.png").convert("RGBA").resize((220, 220))
          player1_color = (50, 50, 50)
          player2_color = (50, 50, 50)
          win_text = "Tie"
        elif winner == 1:
          win = Image.open("images/assets/rps/player1_win.png").convert("RGBA").resize((220, 220))
          player1_color = (0, 180, 0)
          player2_color = (180, 0, 0)
          win_text = "Winner"
        elif winner == 2:
          win = Image.open("images/assets/rps/player2_win.png").convert("RGBA").resize((220, 220))
          player2_color = (0, 180, 0)
          player1_color = (180, 0, 0)
          win_text = "Winner"
        else:
          win = Image.open("images/assets/rps/waiting.png").convert("RGBA").resize((220, 220))
          player1_color = (50, 50, 50)
          player2_color = (50, 50, 50)
          win_text = "Error"

        _, _, w, h = draw.textbbox((0, 0), f"{win_text}", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((1500-w)/2, 570), f"{win_text}", (0, 150, 0), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

        img.paste(win, (640, 350), win)

        overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
        draw3 = ImageDraw.Draw(overlay)

        draw3.rounded_rectangle((10, 210, 610, 750), fill=player1_color + (OPACITY,), radius=20)
        draw3.rounded_rectangle((890, 210, 1490, 750), fill=player2_color + (OPACITY,), radius=20)
        img = Image.alpha_composite(img, overlay)

        #points
        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), f"Wins:", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((420-w)/2, 610), f"Wins:", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

        _, _, w, h = draw.textbbox((0, 0), f"{playerids['player1']['points']}", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((420-w)/2, 680), f"{playerids['player1']['points']}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

        _, _, w, h = draw.textbbox((0, 0), f"Wins:", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((2580-w)/2, 610), f"Wins:", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

        _, _, w, h = draw.textbbox((0, 0), f"{playerids['player2']['points']}", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((2580-w)/2, 680), f"{playerids['player2']['points']}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)


        outline = Image.new('RGBA', (302, 302), (30, 30, 30))
        img.paste(smooth_corners(outline, 30), (59, 299), smooth_corners(outline, 30))
        outline = Image.new('RGBA', (302, 302), (30, 30, 30))
        img.paste(smooth_corners(outline, 30), (1139, 299), smooth_corners(outline, 30))

        img.paste(smooth_corners(player1_pfp, 30), (60, 300), smooth_corners(player1_pfp, 30))
        img.paste(smooth_corners(player2_pfp, 30), (1140, 300), smooth_corners(player2_pfp, 30))

        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), f"{playerids['player1']['name']}", font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((450-w)/2, 220), f"{playerids['player1']['name']}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
        _, _, w, h = draw.textbbox((0, 0), f"{playerids['player2']['name']}", font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((2550-w)/2, 220), f"{playerids['player2']['name']}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)

        #picks
        overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
        draw3 = ImageDraw.Draw(overlay)

        outline = Image.new('RGBA', (220, 220), (30, 30, 30, 50))
        draw3.rounded_rectangle((380, 340, 600, 560), fill=TINT_COLOR + (OPACITY,), radius=20)
        draw3.rounded_rectangle((900, 340, 1120, 560), fill=TINT_COLOR + (OPACITY,), radius=20)
        img = Image.alpha_composite(img, overlay)

        if playerids['player1']['pick'] == "None":
          player1_pick = Image.open("images/assets/rps/waiting.png")
        else:
          player1_pick = Image.open(f"""images/assets/rps/{playerids['player1']['pick'].lower()}/{random.choice(os.listdir(f"images/assets/rps/{playerids['player1']['pick'].lower()}"))}""").convert("RGBA").resize((200, 200))

        if playerids['player2']['pick'] == "None":
          player2_pick = Image.open("images/assets/rps/waiting.png")
        else:
          player2_pick = Image.open(f"""images/assets/rps/{playerids['player2']['pick'].lower()}/{random.choice(os.listdir(f"images/assets/rps/{playerids['player2']['pick'].lower()}"))}""").convert("RGBA").resize((200, 200)).transpose(Image.FLIP_LEFT_RIGHT)

        img.paste(player1_pick, (390, 350), player1_pick)
        img.paste(player2_pick, (910, 350), player2_pick)

        img.save(f"images/rps/{playerids['player1']['id']}.png")
        f = discord.File(f"{os.getcwd()}/images/rps/{playerids['player1']['id']}.png", filename=f"{playerids['player1']['id']}.png")

        embed.set_image(url=f"attachment://{playerids['player1']['id']}.png")

        await interaction.message.edit(embed=embed, content=None, view=PlayAgain(), file=f)
        await interaction.response.defer()

      else:
        await interaction.response.defer()

class Join(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=60)

  @discord.ui.button(label="Join RPS game", style=discord.ButtonStyle.green, custom_id="Join")
  async def join(self, button, interaction):
    playerids = get_db('minigames')['rps'][f'{interaction.message.id}']

    if interaction.user.id == int(playerids["player2"]["id"]):
      asset = interaction.guild.get_member(int(playerids["player1"]["id"])).display_avatar
      data = BytesIO(await asset.read())
      player1_pfp = Image.open(data).convert("RGBA").resize((300, 300))

      asset = interaction.guild.get_member(int(playerids["player2"]["id"])).display_avatar
      data = BytesIO(await asset.read())
      player2_pfp = Image.open(data).convert("RGBA").resize((300, 300))

      TINT_COLOR = (0, 0, 0)
      TRANSPARENCY = .50
      OPACITY = int(255 * TRANSPARENCY)

      img = Image.open('images/assets/backgrounds/rps_background.png').convert("L")
      black = randint(0, 200), randint(0, 20), randint(0, 200)
      img = ImageOps.colorize(img, black=black, white="white")
      img = img.convert("RGBA")

      outline = Image.new('RGBA', (302, 302), (30, 30, 30))
      img.paste(smooth_corners(outline, 30), (59, 299), smooth_corners(outline, 30))
      outline = Image.new('RGBA', (302, 302), (30, 30, 30))
      img.paste(smooth_corners(outline, 30), (1139, 299), smooth_corners(outline, 30))

      img.paste(smooth_corners(player1_pfp, 30), (60, 300), smooth_corners(player1_pfp, 30))
      img.paste(smooth_corners(player2_pfp, 30), (1140, 300), smooth_corners(player2_pfp, 30))

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"{playerids['player1']['name']}", font=ImageFont.truetype("images/assets/que.otf", 70))
      draw.text(((450-w)/2, 220), f"{playerids['player1']['name']}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
      _, _, w, h = draw.textbbox((0, 0), f"{playerids['player2']['name']}", font=ImageFont.truetype("images/assets/que.otf", 70))
      draw.text(((2550-w)/2, 220), f"{playerids['player2']['name']}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)

      #picks
      overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
      draw3 = ImageDraw.Draw(overlay)

      outline = Image.new('RGBA', (220, 220), (30, 30, 30, 50))
      draw3.rounded_rectangle((380, 340, 600, 560), fill=TINT_COLOR + (OPACITY,), radius=20)
      draw3.rounded_rectangle((900, 340, 1120, 560), fill=TINT_COLOR + (OPACITY,), radius=20)
      img = Image.alpha_composite(img, overlay)

      if playerids['player1']['pick'] == "None":
        player1_pick = Image.open("images/assets/rps/waiting.png")
      else:
        player1_pick = Image.open(f"""images/assets/rps/{playerids['player1']['pick'].lower()}/{random.choice(os.listdir(f"images/assets/rps/{playerids['player1']['pick'].lower()}"))}""").convert("RGBA").resize((200, 200))

      if playerids['player2']['pick'] == "None":
        player2_pick = Image.open("images/assets/rps/waiting.png")
      else:
        player2_pick = Image.open(f"""images/assets/rps/{playerids['player2']['pick'].lower()}/{random.choice(os.listdir(f"images/assets/rps/{playerids['player2']['pick'].lower()}"))}""").convert("RGBA").resize((200, 200)).transpose(Image.FLIP_LEFT_RIGHT)

      img.paste(player1_pick, (390, 350), player1_pick)
      img.paste(player2_pick, (910, 350), player2_pick)

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"=== Rock, Paper, Scissors ===", font=ImageFont.truetype("images/assets/que.otf", 80))
      draw.text(((1500-w)/2, 20), f"=== Rock, Paper, Scissors ===", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

      overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
      draw3 = ImageDraw.Draw(overlay)

      outline = Image.new('RGBA', (220, 220), (30, 30, 30, 50))
      draw3.rounded_rectangle((650, 680, 850, 870), fill=TINT_COLOR + (OPACITY,), radius=20)
      img = Image.alpha_composite(img, overlay)

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"Bet:", font=ImageFont.truetype("images/assets/que.otf", 80))
      draw.text(((1500-w)/2, 690), f"Bet:", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

      _, _, w, h = draw.textbbox((0, 0), f"{playerids['bet']}", font=ImageFont.truetype("images/assets/que.otf", 80))
      draw.text(((1500-w)/2, 780), f"{playerids['bet']}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

      img.save(f"images/rps/{playerids['player1']['id']}.png")
      f = discord.File(f"{os.getcwd()}/images/rps/{playerids['player1']['id']}.png", filename=f"{playerids['player1']['id']}.png")

      embed = discord.Embed()
      embed.set_image(url=f"attachment://{playerids['player1']['id']}.png")
      await interaction.message.edit(content=None, embed=embed, view=Multi(), file=f)
      await interaction.response.defer()

  @discord.ui.button(label="Decline", style=discord.ButtonStyle.red, custom_id="decline")
  async def decline(self, button, interaction):
    playerids = get_db('minigames')['rps'][f'{interaction.message.id}']

    if interaction.user.id == int(playerids["player2"]["id"]):
      embed = discord.Embed(description=f"{interaction.user.mention} has declined your invitation.")
      f = discord.File(f"{os.getcwd()}/images/pixel.png", filename="pixel.png")
      embed.set_image(url="attachment://pixel.png")
      await interaction.message.edit(content=None, embed=embed, view=None, file=f)
      await interaction.response.defer()

def get_coords(count):
  coords = (150, 300)
  text_x = 550
  if count >= 7:
    coords_final = (-400, -400)
    text_x_final = -400
    return coords_final, text_x_final
  else:
    if count >= 4:
      coords_final = (coords[0]+450*(count-4), coords[1]+350)
      text_x_final = text_x+900*(count-4)
    else:
      text_x_final = text_x+900*(count-1)
      coords_final = (coords[0]+450*(count-1), coords[1])

  return coords_final, text_x_final

def give_to_winner(winner, all_ids, bet):
  for x in all_ids:
    try:
      score = get_db('users')[f'{x}']['score']
    except:
      continue
    else:
      if x == winner:
        score_final = round(float(score + bet*(len(all_ids)-1)), 2)
        update_db(f'users', f"{x}", {"score": score_final})
      else:
        score_final = round(float(score - bet), 2)
        update_db(f'users', f"{x}", {"score": score_final})

class Turns_rr(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(label="Shoot", style=discord.ButtonStyle.gray, custom_id="shoot", disabled=False)
  async def shoot(self, button, interaction):
    rrdata = get_db('minigames')['rr'][f'{interaction.message.id}']
    turn = rrdata['turn']
    next_turn = turn + 1

    if (interaction.user.id == rrdata[f'player{turn}']['id']) or (rrdata[f'player{turn}']['id'] == "bot"):
      embed_color = discord.Color.dark_theme()

      if rrdata.get(f"bullet") is None:
        bullet = randint(1, 6)
      else:
        bullet = int(rrdata['bullet'])

      outcome = "Error."
      if bullet == 1:
        bullet = randint(1, 6)
        rrdata.update({'bullet': bullet})
        rrdata.update({'player_count': rrdata['player_count'] - 1})
        rrdata[f'player{turn}'].update({'dead': True})
        update_db('minigames/rr', f"{interaction.message.id}", rrdata)
        embed_color = 0x960000
        outcome = "but they didn't make it."

      else:
        bullet -= 1
        rrdata.update({'bullet': bullet})
        update_db('minigames/rr', f"{interaction.message.id}", rrdata)
        outcome = "but the gun didn't go off."

      img = Image.open('images/assets/rr/rr_background.png').convert("RGBA")

      coords = (150, 300)
      count = 1
      text_x = 550
      while count <= 6:
        if count >= 4:
          coords_final = (coords[0]+450*(count-4), coords[1]+350)
          text_x_final = text_x+900*(count-4)
        else:
          text_x_final = text_x+900*(count-1)
          coords_final = (coords[0]+450*(count-1), coords[1])

        if rrdata.get(f"player{next_turn}") is None:
          next_turn += 1
        else:
          if rrdata[f'player{next_turn}']['dead'] is True:
            next_turn += 1

        if rrdata.get(f"player{count}") is None:
          outline = Image.new('RGBA', (262, 312), (30, 30, 30))
          img.paste(smooth_corners(outline, 30), (coords_final[0] - 6, coords_final[1] - 6), smooth_corners(outline, 30))
          unknown = Image.open("images/assets/rr/unknown.png").convert("RGBA").resize((250, 250))
          img.paste(unknown, coords_final, unknown)
          count += 1
          continue

        if rrdata[f'player{count}']['id'] == "bot":
          asset = requests.get(rrdata[f'player{count}']['avatar_url'])
          data = BytesIO(asset.content)
        else:
          asset = client.get_guild(interaction.guild.id).get_member(int(rrdata[f'player{count}']['id'])).display_avatar
          data = BytesIO(await asset.read())

        player_pfp = Image.open(data).convert("RGBA").resize((250, 250))

        if rrdata[f'player{count}']['dead'] is True:
          outline = Image.new('RGBA', (262, 312), (100, 0, 0))
          img.paste(smooth_corners(outline, 30), (coords_final[0] - 6, coords_final[1] - 6), smooth_corners(outline, 30))

          img.paste(smooth_corners(player_pfp, 30), coords_final, smooth_corners(player_pfp, 30))

          x = Image.open("images/assets/rr/x.png").convert("RGBA").resize((244, 244))
          img.paste(x, (coords_final[0]+3, coords_final[1]+3), x)
          blood = Image.open("images/assets/rr/blood.png").convert("RGBA").resize((252, 252))
          img.paste(blood, (coords_final[0]-2, coords_final[1]-1), blood)

          draw = ImageDraw.Draw(img)
          _, _, w, h = draw.textbbox((0, 0), f"{rrdata[f'player{count}']['name']}", font=ImageFont.truetype("images/assets/que.otf", 40))
          draw.text(((text_x_final - w) / 2, coords_final[1] + 260), f"{rrdata[f'player{count}']['name']}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 40), stroke_fill=(0, 0, 0), stroke_width=4)

          count += 1
          continue


        color = (30, 30, 30)

        outline = Image.new('RGBA', (262, 312), color)
        img.paste(smooth_corners(outline, 30), (coords_final[0]-6, coords_final[1]-6), smooth_corners(outline, 30))

        img.paste(smooth_corners(player_pfp, 30), coords_final, smooth_corners(player_pfp, 30))

        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), f"{rrdata[f'player{count}']['name']}", font=ImageFont.truetype("images/assets/que.otf", 40))
        draw.text(((text_x_final - w) / 2, coords_final[1]+260), f"{rrdata[f'player{count}']['name']}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 40), stroke_fill=(0, 0, 0), stroke_width=4)
        count += 1

      TINT_COLOR = (0, 0, 0)
      TRANSPARENCY = .50
      OPACITY = int(255 * TRANSPARENCY)

      overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
      draw3 = ImageDraw.Draw(overlay)

      draw3.rounded_rectangle((50, 110, 1450, 260), fill=TINT_COLOR + (OPACITY,), radius=20)
      img = Image.alpha_composite(img, overlay)

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"""=== Russian Roulette ===""", font=ImageFont.truetype("images/assets/que.otf", 80))
      draw.text(((1500 - w) / 2, 20), f"""=== Russian Roulette ===""", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

      rrdata.update({"total_turns": int(rrdata['total_turns']) + 1})
      all_nums = [1, 2, 3, 4, 5, 6]
      if next_turn > 6:
        for x in all_nums:
          if rrdata.get(f"player{x}") is None:
            continue
          else:
            if rrdata[f'player{x}']['dead'] is True:
              continue
            else:
              next_turn = x
              break

      rrdata.update({"turn": next_turn})

      winner = 0
      if rrdata['player_count'] == 1:
        for user in all_nums:
          if rrdata.get(f"player{user}") is None:
            continue
          else:
            if rrdata[f'player{user}']['dead'] is True:
              continue
            else:
              winner = user
              break
      if winner == 0:
        color = (0, 150, 0)
        gun = Image.open("images/assets/rr/gun.png").convert("RGBA").resize((180, 120))
        img.paste(gun, (get_coords(next_turn)[0][0] + 260, get_coords(next_turn)[0][1]+60), gun)
      else:
        color = (217, 196, 2)

      outline = Image.new('RGBA', (262, 312), color)

      if rrdata[f'player{next_turn}']['id'] == "bot":
        asset = requests.get(rrdata[f'player{next_turn}']['avatar_url'])
        data = BytesIO(asset.content)
      else:
        asset = client.get_guild(interaction.guild.id).get_member(int(rrdata[f'player{next_turn}']['id'])).display_avatar
        data = BytesIO(await asset.read())

      player_pfp = Image.open(data).convert("RGBA").resize((250, 250))

      img.paste(smooth_corners(outline, 30), (get_coords(next_turn)[0][0]-6, get_coords(next_turn)[0][1]-6), smooth_corners(outline, 30))

      img.paste(smooth_corners(player_pfp, 30), get_coords(next_turn)[0], smooth_corners(player_pfp, 30))

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"{rrdata[f'player{next_turn}']['name']}", font=ImageFont.truetype("images/assets/que.otf", 40))
      draw.text(((get_coords(next_turn)[1] - w) / 2, get_coords(next_turn)[0][1]+260), f"{rrdata[f'player{next_turn}']['name']}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 40), stroke_fill=(0, 0, 0), stroke_width=4)

      update_db('minigames/rr', f"{interaction.message.id}", rrdata)

      draw = ImageDraw.Draw(img)

      if winner == 0:
        _, _, w, h = draw.textbbox((0, 0), f"""{rrdata[f'player{turn}']['name']} decided to {button.label}...""", font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((1500 - w) / 2, 120), f"""{rrdata[f'player{turn}']['name']} decided to {button.label}...""", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
        _, _, w, h = draw.textbbox((0, 0), outcome, font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((1500 - w) / 2, 190), outcome, (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
      else:
        _, _, w, h = draw.textbbox((0, 0), f"{rrdata[f'player{winner}']['name']} wins.", font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((1500 - w) / 2, 120), f"{rrdata[f'player{winner}']['name']} wins.", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
        _, _, w, h = draw.textbbox((0, 0), f"Total winnings: {rrdata['bet'] * (rrdata['total_players'] - 1)}", font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((1500 - w) / 2, 190), f"Total winnings: {rrdata['bet'] * (rrdata['total_players'] - 1)}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)

        crown = Image.open("images/assets/rr/crown.png").convert("RGBA").resize((100, 100))
        img.paste(crown, (get_coords(winner)[0][0] + 80, get_coords(winner)[0][1] - 55), crown)
        embed_color = 0xd9c402
        if int(rrdata['bet']) > 0:
          give_to_winner(winner=rrdata[f'player{winner}']['id'], all_ids=list(rrdata['all_ids']), bet=int(rrdata['bet']))

      embed = discord.Embed(color=embed_color)

      img.save(f"images/rr/{rrdata['player1']['id']}.png")
      f = discord.File(f"{os.getcwd()}/images/rr/{rrdata['player1']['id']}.png", filename=f"{rrdata['player1']['id']}.png")

      embed.set_image(url=f"attachment://{rrdata['player1']['id']}.png")
      embed.set_footer(text=f"Total Turns: {int(rrdata['total_turns']) + 1}\nCurrent Bet: {rrdata['bet']} {check_currency(interaction.guild.id)}")
      if winner == 0:
        if rrdata[f'player{next_turn}']['id'] == "bot":
          time.sleep(2)
          random_shoot = 1
          fake_interaction = None
          if random_shoot == 1:
            await self.shoot.callback(self.shoot, fake_interaction)
          else:
            await self.spinshoot.callback(self.spinshoot, fake_interaction)

        else:
          await interaction.message.edit(content=None, embed=embed, view=Turns_rr(), file=f)
      else:
        self.spinshoot.disabled = True
        button.disabled = True
        await interaction.message.edit(content=None, embed=embed, view=self, file=f)
      try:
        await interaction.response.defer()
      except:
        return

    else:
      try:
        await interaction.response.defer()
      except:
        return


  @discord.ui.button(label="Spin & Shoot", style=discord.ButtonStyle.gray, custom_id="spinshoot", disabled=False)
  async def spinshoot(self, button, interaction):
    rrdata = get_db('minigames')['rr'][f'{interaction.message.id}']
    turn = rrdata['turn']
    next_turn = turn + 1

    if interaction.user.id == rrdata[f'player{turn}']['id']:
      embed_color = discord.Color.dark_theme()
      bullet = randint(1, 6)

      outcome = "Error."
      if bullet == 1:
        bullet = randint(1, 6)
        rrdata.update({'bullet': bullet})
        rrdata.update({'player_count': rrdata['player_count'] - 1})
        rrdata[f'player{turn}'].update({'dead': True})
        update_db('minigames/rr', f"{interaction.message.id}", rrdata)
        embed_color = 0x960000
        outcome = "but they didn't make it."

      else:
        bullet -= 1
        rrdata.update({'bullet': bullet})
        update_db('minigames/rr', f"{interaction.message.id}", rrdata)
        outcome = "but the gun didn't go off."

      img = Image.open('images/assets/rr/rr_background.png').convert("RGBA")

      coords = (150, 300)
      count = 1
      text_x = 550
      while count <= 6:
        if count >= 4:
          coords_final = (coords[0]+450*(count-4), coords[1]+350)
          text_x_final = text_x+900*(count-4)
        else:
          text_x_final = text_x+900*(count-1)
          coords_final = (coords[0]+450*(count-1), coords[1])

        if rrdata.get(f"player{next_turn}") is None:
          next_turn += 1
        else:
          if rrdata[f'player{next_turn}']['dead'] is True:
            next_turn += 1

        if rrdata.get(f"player{count}") is None:
          outline = Image.new('RGBA', (262, 312), (30, 30, 30))
          img.paste(smooth_corners(outline, 30), (coords_final[0] - 6, coords_final[1] - 6), smooth_corners(outline, 30))
          unknown = Image.open("images/assets/rr/unknown.png").convert("RGBA").resize((250, 250))
          img.paste(unknown, coords_final, unknown)
          count += 1
          continue

        asset = client.get_guild(interaction.guild.id).get_member(int(rrdata[f'player{count}']['id'])).display_avatar
        data = BytesIO(await asset.read())
        player_pfp = Image.open(data).convert("RGBA").resize((250, 250))

        if rrdata[f'player{count}']['dead'] is True:
          outline = Image.new('RGBA', (262, 312), (100, 0, 0))
          img.paste(smooth_corners(outline, 30), (coords_final[0] - 6, coords_final[1] - 6), smooth_corners(outline, 30))

          img.paste(smooth_corners(player_pfp, 30), coords_final, smooth_corners(player_pfp, 30))

          x = Image.open("images/assets/rr/x.png").convert("RGBA").resize((244, 244))
          img.paste(x, (coords_final[0]+3, coords_final[1]+3), x)
          blood = Image.open("images/assets/rr/blood.png").convert("RGBA").resize((252, 252))
          img.paste(blood, (coords_final[0]-2, coords_final[1]-1), blood)

          draw = ImageDraw.Draw(img)
          _, _, w, h = draw.textbbox((0, 0), f"{rrdata[f'player{count}']['name']}", font=ImageFont.truetype("images/assets/que.otf", 40))
          draw.text(((text_x_final - w) / 2, coords_final[1] + 260), f"{rrdata[f'player{count}']['name']}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 40), stroke_fill=(0, 0, 0), stroke_width=4)

          count += 1
          continue


        color = (30, 30, 30)

        outline = Image.new('RGBA', (262, 312), color)
        img.paste(smooth_corners(outline, 30), (coords_final[0]-6, coords_final[1]-6), smooth_corners(outline, 30))

        img.paste(smooth_corners(player_pfp, 30), coords_final, smooth_corners(player_pfp, 30))

        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), f"{rrdata[f'player{count}']['name']}", font=ImageFont.truetype("images/assets/que.otf", 40))
        draw.text(((text_x_final - w) / 2, coords_final[1]+260), f"{rrdata[f'player{count}']['name']}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 40), stroke_fill=(0, 0, 0), stroke_width=4)
        count += 1

      TINT_COLOR = (0, 0, 0)
      TRANSPARENCY = .50
      OPACITY = int(255 * TRANSPARENCY)

      overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
      draw3 = ImageDraw.Draw(overlay)

      draw3.rounded_rectangle((50, 110, 1450, 260), fill=TINT_COLOR + (OPACITY,), radius=20)
      img = Image.alpha_composite(img, overlay)

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"""=== Russian Roulette ===""", font=ImageFont.truetype("images/assets/que.otf", 80))
      draw.text(((1500 - w) / 2, 20), f"""=== Russian Roulette ===""", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

      rrdata.update({"total_turns": int(rrdata['total_turns']) + 1})
      all_nums = [1, 2, 3, 4, 5, 6]
      if next_turn > 6:
        for x in all_nums:
          if rrdata.get(f"player{x}") is None:
            continue
          else:
            if rrdata[f'player{x}']['dead'] == True:
              continue
            else:
              next_turn = x
              break

      rrdata.update({"turn": next_turn})

      winner = 0
      if rrdata['player_count'] == 1:
        for user in all_nums:
          if rrdata.get(f"player{user}") is None:
            continue
          else:
            if rrdata[f'player{user}']['dead'] == True:
              continue
            else:
              winner = user
              break
      if winner == 0:
        color = (0, 150, 0)
        gun = Image.open("images/assets/rr/gun.png").convert("RGBA").resize((180, 120))
        img.paste(gun, (get_coords(next_turn)[0][0] + 260, get_coords(next_turn)[0][1]+60), gun)
      else:
        color = (217, 196, 2)

      outline = Image.new('RGBA', (262, 312), color)

      asset = client.get_guild(interaction.guild.id).get_member(int(rrdata[f'player{next_turn}']['id'])).display_avatar
      data = BytesIO(await asset.read())
      player_pfp = Image.open(data).convert("RGBA").resize((250, 250))

      img.paste(smooth_corners(outline, 30), (get_coords(next_turn)[0][0]-6, get_coords(next_turn)[0][1]-6), smooth_corners(outline, 30))

      img.paste(smooth_corners(player_pfp, 30), get_coords(next_turn)[0], smooth_corners(player_pfp, 30))

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"{rrdata[f'player{next_turn}']['name']}", font=ImageFont.truetype("images/assets/que.otf", 40))
      draw.text(((get_coords(next_turn)[1] - w) / 2, get_coords(next_turn)[0][1]+260), f"{rrdata[f'player{next_turn}']['name']}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 40), stroke_fill=(0, 0, 0), stroke_width=4)

      update_db('minigames/rr', f"{interaction.message.id}", rrdata)

      draw = ImageDraw.Draw(img)

      if winner == 0:
        _, _, w, h = draw.textbbox((0, 0), f"""{rrdata[f'player{turn}']['name']} decided to {button.label}...""", font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((1500 - w) / 2, 120), f"""{rrdata[f'player{turn}']['name']} decided to {button.label}...""", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
        _, _, w, h = draw.textbbox((0, 0), outcome, font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((1500 - w) / 2, 190), outcome, (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
      else:
        _, _, w, h = draw.textbbox((0, 0), f"{rrdata[f'player{winner}']['name']} wins.", font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((1500 - w) / 2, 120), f"{rrdata[f'player{winner}']['name']} wins.", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
        _, _, w, h = draw.textbbox((0, 0), f"Total winnings: {rrdata['bet'] * (rrdata['total_players'] - 1)}", font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((1500 - w) / 2, 190), f"Total winnings: {rrdata['bet'] * (rrdata['total_players'] - 1)}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)

        crown = Image.open("images/assets/rr/crown.png").convert("RGBA").resize((100, 100))
        img.paste(crown, (get_coords(winner)[0][0] + 80, get_coords(winner)[0][1] - 55), crown)
        embed_color = 0xd9c402
        if int(rrdata['bet']) > 0:
          give_to_winner(winner=rrdata[f'player{winner}']['id'], all_ids=list(rrdata['all_ids']), bet=int(rrdata['bet']))

      embed = discord.Embed(color=embed_color)

      img.save(f"images/rr/{rrdata['player1']['id']}.png")
      f = discord.File(f"{os.getcwd()}/images/rr/{rrdata['player1']['id']}.png", filename=f"{rrdata['player1']['id']}.png")

      embed.set_image(url=f"attachment://{rrdata['player1']['id']}.png")
      embed.set_footer(text=f"Total Turns: {int(rrdata['total_turns']) + 1}\nCurrent Bet: {rrdata['bet']} {check_currency(interaction.guild.id)}")
      if winner == 0:
        await interaction.message.edit(content=None, embed=embed, view=Turns_rr(), file=f)
      else:
        self.spinshoot.disabled = True
        button.disabled = True
        await interaction.message.edit(content=None, embed=embed, view=self, file=f)
      try:
        await interaction.response.defer()
      except:
        return

    else:
      try:
        await interaction.response.defer()
      except:
        return

class Join_rr(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
    self.joined = 1
    self.value = "Timed out."
    self.msgid = int
    self.fs = False

  @discord.ui.button(label="Join RR Room", style=discord.ButtonStyle.green, custom_id="Join", disabled=False)
  async def join(self, button, interaction):
    rrdata = get_db('minigames')['rr'][f'{interaction.message.id}']
    if rrdata['total_players'] >= 6:
      return

    if interaction.user.id not in rrdata['all_ids']:
      img = Image.open(f'images/rr/{rrdata["player1"]["id"]}.png').convert("RGBA")

      coords_final = get_coords(int(rrdata['total_players']) + 1)[0]
      text_x_final = get_coords(int(rrdata['total_players']) + 1)[1]
      count = int(rrdata['total_players']) + 1

      if count >= 6:
        self.add_bot.disabled = True
        button.disabled = True

      asset = interaction.user.display_avatar
      data = BytesIO(await asset.read())
      player_pfp = Image.open(data).convert("RGBA").resize((250, 250))
      color = (30, 30, 30)

      outline = Image.new('RGBA', (262, 312), color)
      img.paste(smooth_corners(outline, 30), (coords_final[0] - 6, coords_final[1] - 6), smooth_corners(outline, 30))

      img.paste(smooth_corners(player_pfp, 30), coords_final, smooth_corners(player_pfp, 30))

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"{interaction.user.display_name}", font=ImageFont.truetype("images/assets/que.otf", 40))
      draw.text(((text_x_final - w) / 2, coords_final[1] + 260), f"{interaction.user.display_name}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 40), stroke_fill=(0, 0, 0), stroke_width=4)

      rrdata.update({'all_ids': rrdata['all_ids'].append(interaction.user.id)})
      rrdata.update({'player_count': int(rrdata['player_count']) + 1})
      rrdata.update({'total_players': int(rrdata['total_players']) + 1})
      self.joined += 1
      rrdata.update({f'player{count}': {'id': f'{interaction.user.id}', 'name': f"{interaction.user.display_name}", 'dead': False}})
      update_db('minigames/rr', f"{interaction.message.id}", rrdata)

      img.save(f"images/rr/{rrdata['player1']['id']}.png")

      f = discord.File(f"{os.getcwd()}/images/rr/{rrdata['player1']['id']}.png", filename=f"{rrdata['player1']['id']}.png")
      embed = discord.Embed()
      embed.set_footer(text=f"Current Bet: {rrdata['bet']} {check_currency(interaction.guild.id)}")
      embed.set_image(url=f"attachment://{rrdata['player1']['id']}.png")

      await interaction.message.edit(embed=embed, content=None, view=self, file=f)
      await interaction.response.defer()

  @discord.ui.button(label="Start", style=discord.ButtonStyle.green, custom_id="ForceStart", disabled=False)
  async def fs(self, button, interaction):
    rrdata = get_db('minigames')['rr'][f'{interaction.message.id}']
    if interaction.user.id == int(rrdata['player1']['id']):
      if int(rrdata['player_count']) == 1:
        await interaction.response.defer()
        return
      else:
        img = Image.open('images/assets/rr/rr_background.png').convert("RGBA")

        turn = rrdata['turn']
        coords = (150, 300)
        count = 1
        text_x = 550
        while count <= 6:
          if count >= 4:
            coords_final = (coords[0]+450*(count-4), coords[1]+350)
            text_x_final = text_x+900*(count-4)
          else:
            text_x_final = text_x+900*(count-1)
            coords_final = (coords[0]+450*(count-1), coords[1])

          if rrdata.get(f"player{count}") is None:
            outline = Image.new('RGBA', (262, 312), (30, 30, 30))
            img.paste(smooth_corners(outline, 30), (coords_final[0] - 6, coords_final[1] - 6), smooth_corners(outline, 30))
            unknown = Image.open("images/assets/rr/unknown.png").convert("RGBA").resize((250, 250))
            img.paste(unknown, coords_final, unknown)
            count += 1
            continue

          if rrdata[f'player{count}']['id'] == "bot":
            asset = requests.get(rrdata[f'player{count}']['avatar_url'])
            data = BytesIO(asset.content)
          else:
            asset = client.get_guild(interaction.guild.id).get_member(int(rrdata[f'player{count}']['id'])).display_avatar
            data = BytesIO(await asset.read())

          player_pfp = Image.open(data).convert("RGBA").resize((250, 250))

          #check for color
          if turn == count:
            color = (0, 150, 0)
            gun = Image.open("images/assets/rr/gun.png").convert("RGBA").resize((180, 120))
            img.paste(gun, (coords_final[0] + 260, coords_final[1]+60), gun)
          else:
            color = (30, 30, 30)

          outline = Image.new('RGBA', (262, 312), color)
          img.paste(smooth_corners(outline, 30), (coords_final[0]-6, coords_final[1]-6), smooth_corners(outline, 30))

          img.paste(smooth_corners(player_pfp, 30), coords_final, smooth_corners(player_pfp, 30))

          draw = ImageDraw.Draw(img)
          _, _, w, h = draw.textbbox((0, 0), f"{rrdata[f'player{count}']['name']}", font=ImageFont.truetype("images/assets/que.otf", 40))
          draw.text(((text_x_final - w) / 2, coords_final[1]+260), f"{rrdata[f'player{count}']['name']}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 40), stroke_fill=(0, 0, 0), stroke_width=4)
          count += 1

        TINT_COLOR = (0, 0, 0)
        TRANSPARENCY = .50
        OPACITY = int(255 * TRANSPARENCY)

        overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
        draw3 = ImageDraw.Draw(overlay)

        draw3.rounded_rectangle((100, 100, 1400, 250), fill=TINT_COLOR + (OPACITY,), radius=20)
        img = Image.alpha_composite(img, overlay)

        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), f"""It's {rrdata[f'player{turn}']['name']}'s turn...""", font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((1500 - w) / 2, 150), f"""It's {rrdata[f'player{turn}']['name']}'s turn...""", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
        _, _, w, h = draw.textbbox((0, 0), f"""=== Russian Roulette ===""", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((1500 - w) / 2, 20), f"""=== Russian Roulette ===""", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

        img.save(f"images/rr/{rrdata['player1']['id']}.png")

        f = discord.File(f"{os.getcwd()}/images/rr/{rrdata['player1']['id']}.png", filename=f"{rrdata['player1']['id']}.png")
        embed = discord.Embed()
        embed.set_image(url=f"attachment://{rrdata['player1']['id']}.png")
        embed.set_footer(text=f"Current Bet: {rrdata['bet']} {check_currency(interaction.guild.id)}")

        await interaction.message.edit(content=f"Game Started.", embed=embed, view=Turns_rr(), file=f)
        await interaction.response.defer()
        return
    else:
      return

  @discord.ui.button(label="Add Bot", style=discord.ButtonStyle.gray, custom_id="add_bot", disabled=False)
  async def add_bot(self, button, interaction):
    rrdata = get_db('minigames')['rr'][f'{interaction.message.id}']
    if rrdata['total_players'] >= 6:
      return

    if interaction.user.id == int(rrdata['player1']['id']):
      img = Image.open(f'images/rr/{interaction.user.id}.png').convert("RGBA")

      coords_final = get_coords(int(rrdata['total_players']) + 1)[0]
      text_x_final = get_coords(int(rrdata['total_players']) + 1)[1]
      count = int(rrdata['total_players']) + 1

      if count >= 6:
        button.disabled = True
        self.join.disabled = True

      cprint("reached else", 'green')
      url = "https://google-search83.p.rapidapi.com/google/search_image"

      pfp_to_search = ["neco arc", 'neco arc profile picture', 'neco arc chaos', 'neco arc chaos pfp', 'kratos face', 'neco arc face']
      querystring = {"query": f"{random.choice(pfp_to_search)}", "gl": "us", "lr": "en", "num": "1", "start": "0"}

      headers = {
        "X-RapidAPI-Key": "656579fde0msh1a659fc425536d6p163315jsn94162aa70de6",
        "X-RapidAPI-Host": "google-search83.p.rapidapi.com"
      }

      googleresponse = requests.request("GET", url, headers=headers, params=querystring)

      data = None
      while data is None:
        nmb = randint(0, 19)
        try:
          asset = requests.get(googleresponse.json()[nmb]['url'])
          data = BytesIO(asset.content)
        except:
          continue
        else:
          break

      player_pfp = Image.open(data).convert("RGBA").resize((250, 250))
      color = (30, 30, 30)

      outline = Image.new('RGBA', (262, 312), color)
      img.paste(smooth_corners(outline, 30), (coords_final[0] - 6, coords_final[1] - 6), smooth_corners(outline, 30))

      img.paste(smooth_corners(player_pfp, 30), coords_final, smooth_corners(player_pfp, 30))

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"Bot", font=ImageFont.truetype("images/assets/que.otf", 40))
      draw.text(((text_x_final - w) / 2, coords_final[1] + 260), f"Bot", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 40), stroke_fill=(0, 0, 0), stroke_width=4)

      cprint("reached append", 'red')
      rrdata.update({'all_ids': ['bot']})
      rrdata.update({'player_count': int(rrdata['player_count']) + 1})
      rrdata.update({'total_players': int(rrdata['total_players']) + 1})
      self.joined += 1
      rrdata.update({f'player{count}': {'id': 'bot', 'name': "Bot", 'dead': False, 'avatar_url': f"{googleresponse.json()[nmb]['url']}"}})
      update_db('minigames/rr', f"{interaction.message.id}", rrdata)

      img.save(f"images/rr/{rrdata['player1']['id']}.png")

      f = discord.File(f"{os.getcwd()}/images/rr/{rrdata['player1']['id']}.png",
                       filename=f"{rrdata['player1']['id']}.png")
      embed = discord.Embed()
      embed.set_footer(text=f"Current Bet: {rrdata['bet']} {check_currency(interaction.guild.id)}")
      embed.set_image(url=f"attachment://{rrdata['player1']['id']}.png")

      await interaction.message.edit(embed=embed, content=None, view=self, file=f)
      await interaction.response.defer()

class Select_slash(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=60)
    self.rps = ""

  #server2 = client.get_guild(710840786853429319)
  #emoji = discord.utils.get(server2.emojis, name="stone")
  #emoji2 = discord.utils.get(server2.emojis, name="paper")
  #emoji3 = discord.utils.get(server2.emojis, name="scissors1")
  #emoji4 = discord.utils.get(server2.emojis, name="sex")

  @discord.ui.select(placeholder="Choose your attack.", max_values=1, disabled=False, options=[
        discord.SelectOption(
            label=f"Rock"
        ),
        discord.SelectOption(
            label="Paper"
        ),
        discord.SelectOption(
            label="Scissors"
        ),
        discord.SelectOption(
            label="Random",
            description="Randomly Chosen."
        )
    ])
  async def sele(self, select, interaction):
    val = str(select.values)
    choose2 = ['rock',
               'paper',
               'scissors']
    stone = "<:stone:780724249815810058>"
    pep = "<:paper:780724297509371904>"
    sci = "<:scissors1:780724274762874890>"
    choose3 = random.choice(choose2)
    valre = val.replace("['", "")
    val2 = valre.replace("']", "")
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()

    if userid in embeddict['footer']['text']:
      if "Rock" in val:
        if choose3 == "rock":
          embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`It's a tie.`")
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.response.edit_message(embed=embed, content=None)
        elif choose3 == "scissors":
          embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.response.edit_message(embed=embed, content=None)
        elif choose3 == "paper":
          embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.response.edit_message(embed=embed, content=None)

      elif "Scissors" in val:
        if choose3 == "rock":
          embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.response.edit_message(embed=embed, content=None)
        elif choose3 == "scissors":
          embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`It's a tie.`")
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.response.edit_message(embed=embed, content=None)
        elif choose3 == "paper":
          embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.response.edit_message(embed=embed, content=None)

      elif "Paper" in val:
        if choose3 == "rock":
          embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.response.edit_message(embed=embed, content=None)
        elif choose3 == "scissors":
          embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.response.edit_message(embed=embed, content=None)
        elif choose3 == "paper":
          embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`It's a tie.`")
          embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
          await interaction.response.edit_message(embed=embed, content=None)

      elif "Random" in val:
        val2 = random.choice(choose2)
        if "rock" in val2:
          if choose3 == "rock":
            embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`It's a tie.`")
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=embed, content=None)
          elif choose3 == "scissors":
            embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=embed, content=None)
          elif choose3 == "paper":
            embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=embed, content=None)

        elif "scissors" in val2:
          if choose3 == "rock":
            embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=embed, content=None)
          elif choose3 == "scissors":
            embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`It's a tie.`")
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=embed, content=None)
          elif choose3 == "paper":
            embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=embed, content=None)

        elif "scissors" in val2:
          if choose3 == "rock":
            embed = discord.Embed(description=f"I picked {choose3} {stone}\n\n`You win.`", color=discord.Color.from_rgb(r=0, g=randint(50, 255), b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=embed, content=None)
          elif choose3 == "scissors":
            embed = discord.Embed(description=f"I picked {choose3} {sci}\n\n`I win.`", color=discord.Color.from_rgb(r=randint(50, 255), g=0, b=0))
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=embed, content=None)
          elif choose3 == "paper":
            embed = discord.Embed(description=f"I picked {choose3} {pep}\n\n`It's a tie.`")
            embed.set_footer(text=f"Your pick: {val2} ({interaction.user.id})", icon_url=interaction.user.avatar)
            await interaction.response.edit_message(embed=embed, content=None)
    else:
      return

def checkwin(msg, symbol):
  value = get_db('minigames')['ttt'][f'{msg}']

  if (f"1{symbol}" in value) and (f"2{symbol}" in value) and (f"3{symbol}" in value):
    return True

  if (f"1{symbol}" in value) and (f"4{symbol}" in value) and (f"7{symbol}" in value):
    return True

  if (f"1{symbol}" in value) and (f"5{symbol}" in value) and (f"9{symbol}" in value):
    return True

  if (f"2{symbol}" in value) and (f"5{symbol}" in value) and (f"8{symbol}" in value):
    return True

  if (f"3{symbol}" in value) and (f"6{symbol}" in value) and (f"9{symbol}" in value):
    return True

  if (f"3{symbol}" in value) and (f"5{symbol}" in value) and (f"7{symbol}" in value):
    return True

  if (f"4{symbol}" in value) and (f"5{symbol}" in value) and (f"6{symbol}" in value):
    return True

  if (f"7{symbol}" in value) and (f"8{symbol}" in value) and (f"9{symbol}" in value):
    return True

  return False

class Tic(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=180)
    self.rps = ""

  @discord.ui.button(label="1", style=discord.ButtonStyle.primary, custom_id="1", disabled=False, row=0)
  async def one(self, button, interaction):
    val = str(button.label)
    val2 = int(val)
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    comps = str(interaction.message.components)
    for embed in embeds:
      embeddict = embed.to_dict()

    bet = str(embeddict['description'])
    bet2 = bet.split('Bet: **`')[1].lstrip().split('`**')[0]
    betcheck = False
    if bet2 != "None":
      betcheck = True

    desc = embeddict["description"]
    footer = embeddict["footer"]
    footerpre = str(footer)[-3]
    footer2 = footerpre.replace(f"{footerpre}", f"{int(footerpre) + 1}")

    symbol = "None"
    footerpre2 = str(desc).replace("!", "")
    if (float(footer2) % 2) == 0:
      desc3 = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc2 = str(desc).replace(numbers[val2], "X")
      symbol = "X"
      lastturn = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
    else:
      lastturn = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc3 = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      desc2 = str(desc).replace(numbers[val2], "0")
      symbol = "0"

    if int(lastturn) != interaction.user.id:
      await interaction.response.defer()
      return

    pattern = "disabled=False"
    comps2 = comps.split(" ")
    count = 0
    for word in comps2:
      if pattern in word:
        count += 1
      else:
        pass

    value = get_db('minigames')['ttt'][f'{interaction.message.id}']
    value2 = value.split(f"{small_to_big(numbers[val2])}", 1)[1].lstrip().split('-')[0]
    value3 = value.replace(f"{small_to_big(numbers[val2])}{value2}", f"{small_to_big(numbers[val2])}{symbol}")
    update_db('minigames', 'ttt', {f"{interaction.message.id}": f"{value3}"})

    turn = interaction.guild.get_member(int(desc3))
    desc3a = str(desc).split("...", 1)[0]
    desc3 = desc2.replace(f"{desc3a}", f"```fix\nWaiting for {turn.display_name}")

    final = discord.Embed(description=f"{desc3}")
    final.set_footer(text=f"Turn number: {footer2}")
    if checkwin(str(interaction.message.id), symbol):
      desc3 = desc2.replace(f"{desc3a}", f"```fix\n{interaction.user.display_name} has won the game")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")

      if betcheck:
        uservalue = get_db('users')[f'{turn.id}']['score']
        yourvalue = get_db('users')[f'{interaction.user.id}']['score']
        uservalueint = float(uservalue)
        yourvalueint = float(yourvalue)
        uservaluefinal = uservalueint - int(bet2)
        yourvaluefinal = yourvalueint + int(bet2)
        update_db('users', f'{turn.id}', {"score": uservaluefinal})
        update_db('users', f'{interaction.user.id}', {"score": yourvaluefinal})
        final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}\n\n{interaction.user.name}: {yourvalue} ≫ {yourvaluefinal}\n{turn.name}: {uservalue} ≫ {uservaluefinal}")

      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
      await interaction.response.defer()

    elif count == 1:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      desc3 = desc2.replace(f"{desc3a}", f"```fix\nIt's a tie")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")
      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    else:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      await interaction.message.edit(embed=final, content=None, view=self)
      await interaction.response.defer()

  @discord.ui.button(label="2", style=discord.ButtonStyle.primary, custom_id="2", disabled=False, row=0)
  async def two(self, button, interaction):
    val = str(button.label)
    val2 = int(val)
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    comps = str(interaction.message.components)
    for embed in embeds:
      embeddict = embed.to_dict()

    bet = str(embeddict['description'])
    bet2 = bet.split('Bet: **`')[1].lstrip().split('`**')[0]
    betcheck = False
    if bet2 != "None":
      betcheck = True

    desc = embeddict["description"]
    footer = embeddict["footer"]
    footerpre = str(footer)[-3]
    footer2 = footerpre.replace(f"{footerpre}", f"{int(footerpre) + 1}")

    footerpre2 = str(desc).replace("!", "")
    if (float(footer2) % 2) == 0:
      desc3 = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc2 = str(desc).replace(numbers[val2], "X")
      lastturn = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      symbol = "X"
    else:
      lastturn = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc3 = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      desc2 = str(desc).replace(numbers[val2], "0")
      symbol = "0"

    if int(lastturn) != interaction.user.id:
      await interaction.response.defer()
      return

    pattern = "disabled=False"
    comps2 = comps.split(" ")
    count = 0
    for word in comps2:
      if pattern in word:
        count += 1
      else:
        pass

    value = get_db('minigames')['ttt'][f'{interaction.message.id}']
    value2 = value.split(f"{small_to_big(numbers[val2])}", 1)[1].lstrip().split('-')[0]
    value3 = value.replace(f"{small_to_big(numbers[val2])}{value2}", f"{small_to_big(numbers[val2])}{symbol}")
    update_db('minigames', 'ttt', {f"{interaction.message.id}": f"{value3}"})

    turn = interaction.guild.get_member(int(desc3))
    desc3a = str(desc).split("...", 1)[0]
    desc3 = desc2.replace(f"{desc3a}", f"```fix\nWaiting for {turn.display_name}")

    final = discord.Embed(description=f"{desc3}")
    final.set_footer(text=f"Turn number: {footer2}")
    if checkwin(str(interaction.message.id), symbol):
      desc3 = desc2.replace(f"{desc3a}", f"```fix\n{interaction.user.display_name} has won the game")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")

      if betcheck:
        uservalue = get_db('users')[f'{turn.id}']['score']
        yourvalue = get_db('users')[f'{interaction.user.id}']['score']
        uservalueint = float(uservalue)
        yourvalueint = float(yourvalue)
        uservaluefinal = uservalueint - int(bet2)
        yourvaluefinal = yourvalueint + int(bet2)
        update_db('users', f'{turn.id}', {"score": uservaluefinal})
        update_db('users', f'{interaction.user.id}', {"score": yourvaluefinal})
        final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}\n\n{interaction.user.name}: {yourvalue} ≫ {yourvaluefinal}\n{turn.name}: {uservalue} ≫ {uservaluefinal}")

      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)

    elif count == 1:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      desc3 = desc2.replace(f"{desc3a}", f"```fix\nIt's a tie")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")
      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    else:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      await interaction.message.edit(embed=final, content=None, view=self)
      await interaction.response.defer()

  @discord.ui.button(label="3", style=discord.ButtonStyle.primary, custom_id="3", disabled=False, row=0)
  async def three(self, button, interaction):
    val = str(button.label)
    val2 = int(val)
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    comps = str(interaction.message.components)
    for embed in embeds:
      embeddict = embed.to_dict()

    bet = str(embeddict['description'])
    bet2 = bet.split('Bet: **`')[1].lstrip().split('`**')[0]
    betcheck = False
    if bet2 != "None":
      betcheck = True

    desc = embeddict["description"]
    footer = embeddict["footer"]
    footerpre = str(footer)[-3]
    footer2 = footerpre.replace(f"{footerpre}", f"{int(footerpre) + 1}")

    footerpre2 = str(desc).replace("!", "")
    if (float(footer2) % 2) == 0:
      desc3 = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc2 = str(desc).replace(numbers[val2], "X")
      lastturn = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      symbol = "X"
    else:
      lastturn = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc3 = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      desc2 = str(desc).replace(numbers[val2], "0")
      symbol = "0"

    if int(lastturn) != interaction.user.id:
      await interaction.response.defer()
      return

    pattern = "disabled=False"
    comps2 = comps.split(" ")
    count = 0
    for word in comps2:
      if pattern in word:
        count += 1
      else:
        pass

    value = get_db('minigames')['ttt'][f'{interaction.message.id}']
    value2 = value.split(f"{small_to_big(numbers[val2])}", 1)[1].lstrip().split('-')[0]
    value3 = value.replace(f"{small_to_big(numbers[val2])}{value2}", f"{small_to_big(numbers[val2])}{symbol}")
    update_db('minigames', 'ttt', {f"{interaction.message.id}": f"{value3}"})

    turn = interaction.guild.get_member(int(desc3))
    desc3a = str(desc).split("...", 1)[0]
    desc3 = desc2.replace(f"{desc3a}", f"```fix\nWaiting for {turn.display_name}")

    final = discord.Embed(description=f"{desc3}")
    final.set_footer(text=f"Turn number: {footer2}")
    if checkwin(str(interaction.message.id), symbol):
      desc3 = desc2.replace(f"{desc3a}", f"```fix\n{interaction.user.display_name} has won the game")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")

      if betcheck:
        uservalue = get_db('users')[f'{turn.id}']['score']
        yourvalue = get_db('users')[f'{interaction.user.id}']['score']
        uservalueint = float(uservalue)
        yourvalueint = float(yourvalue)
        uservaluefinal = uservalueint - int(bet2)
        yourvaluefinal = yourvalueint + int(bet2)
        update_db('users', f'{turn.id}', {"score": uservaluefinal})
        update_db('users', f'{interaction.user.id}', {"score": yourvaluefinal})
        final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}\n\n{interaction.user.name}: {yourvalue} ≫ {yourvaluefinal}\n{turn.name}: {uservalue} ≫ {uservaluefinal}")

      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    elif count == 1:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      desc3 = desc2.replace(f"{desc3a}", f"```fix\nIt's a tie")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")
      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    else:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      await interaction.message.edit(embed=final, content=None, view=self)
      await interaction.response.defer()

  @discord.ui.button(label="4", style=discord.ButtonStyle.primary, custom_id="4", disabled=False, row=1)
  async def four(self, button, interaction):
    val = str(button.label)
    val2 = int(val)
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    comps = str(interaction.message.components)
    for embed in embeds:
      embeddict = embed.to_dict()

    bet = str(embeddict['description'])
    bet2 = bet.split('Bet: **`')[1].lstrip().split('`**')[0]
    betcheck = False
    if bet2 != "None":
      betcheck = True

    desc = embeddict["description"]
    footer = embeddict["footer"]
    footerpre = str(footer)[-3]
    footer2 = footerpre.replace(f"{footerpre}", f"{int(footerpre) + 1}")

    footerpre2 = str(desc).replace("!", "")
    if (float(footer2) % 2) == 0:
      desc3 = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc2 = str(desc).replace(numbers[val2], "X")
      lastturn = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      symbol = "X"
    else:
      lastturn = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc3 = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      desc2 = str(desc).replace(numbers[val2], "0")
      symbol = "0"

    if int(lastturn) != interaction.user.id:
      await interaction.response.defer()
      return

    pattern = "disabled=False"
    comps2 = comps.split(" ")
    count = 0
    for word in comps2:
      if pattern in word:
        count += 1
      else:
        pass

    value = get_db('minigames')['ttt'][f'{interaction.message.id}']
    value2 = value.split(f"{small_to_big(numbers[val2])}", 1)[1].lstrip().split('-')[0]
    value3 = value.replace(f"{small_to_big(numbers[val2])}{value2}", f"{small_to_big(numbers[val2])}{symbol}")
    update_db('minigames', 'ttt', {f"{interaction.message.id}": f"{value3}"})

    turn = interaction.guild.get_member(int(desc3))
    desc3a = str(desc).split("...", 1)[0]
    desc3 = desc2.replace(f"{desc3a}", f"```fix\nWaiting for {turn.display_name}")

    final = discord.Embed(description=f"{desc3}")
    final.set_footer(text=f"Turn number: {footer2}")
    if checkwin(str(interaction.message.id), symbol):
      desc3 = desc2.replace(f"{desc3a}", f"```fix\n{interaction.user.display_name} has won the game")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")

      if betcheck:
        uservalue = get_db('users')[f'{turn.id}']['score']
        yourvalue = get_db('users')[f'{interaction.user.id}']['score']
        uservalueint = float(uservalue)
        yourvalueint = float(yourvalue)
        uservaluefinal = uservalueint - int(bet2)
        yourvaluefinal = yourvalueint + int(bet2)
        update_db('users', f'{turn.id}', {"score": uservaluefinal})
        update_db('users', f'{interaction.user.id}', {"score": yourvaluefinal})
        final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}\n\n{interaction.user.name}: {yourvalue} ≫ {yourvaluefinal}\n{turn.name}: {uservalue} ≫ {uservaluefinal}")

      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    elif count == 1:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      desc3 = desc2.replace(f"{desc3a}", f"```fix\nIt's a tie")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")
      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    else:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      await interaction.message.edit(embed=final, content=None, view=self)
      await interaction.response.defer()

  @discord.ui.button(label="5", style=discord.ButtonStyle.primary, custom_id="5", disabled=False, row=1)
  async def five(self, button, interaction):
    val = str(button.label)
    val2 = int(val)
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    comps = str(interaction.message.components)
    for embed in embeds:
      embeddict = embed.to_dict()

    bet = str(embeddict['description'])
    bet2 = bet.split('Bet: **`')[1].lstrip().split('`**')[0]
    betcheck = False
    if bet2 != "None":
      betcheck = True

    desc = embeddict["description"]
    footer = embeddict["footer"]
    footerpre = str(footer)[-3]
    footer2 = footerpre.replace(f"{footerpre}", f"{int(footerpre) + 1}")

    footerpre2 = str(desc).replace("!", "")
    if (float(footer2) % 2) == 0:
      desc3 = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc2 = str(desc).replace(numbers[val2], "X")
      lastturn = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      symbol = "X"
    else:
      lastturn = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc3 = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      desc2 = str(desc).replace(numbers[val2], "0")
      symbol = "0"

    if int(lastturn) != interaction.user.id:
      await interaction.response.defer()
      return

    pattern = "disabled=False"
    comps2 = comps.split(" ")
    count = 0
    for word in comps2:
      if pattern in word:
        count += 1
      else:
        pass

    value = get_db('minigames')['ttt'][f'{interaction.message.id}']
    value2 = value.split(f"{small_to_big(numbers[val2])}", 1)[1].lstrip().split('-')[0]
    value3 = value.replace(f"{small_to_big(numbers[val2])}{value2}", f"{small_to_big(numbers[val2])}{symbol}")
    update_db('minigames', 'ttt', {f"{interaction.message.id}": f"{value3}"})

    turn = interaction.guild.get_member(int(desc3))
    desc3a = str(desc).split("...", 1)[0]
    desc3 = desc2.replace(f"{desc3a}", f"```fix\nWaiting for {turn.display_name}")

    final = discord.Embed(description=f"{desc3}")
    final.set_footer(text=f"Turn number: {footer2}")
    if checkwin(str(interaction.message.id), symbol):
      desc3 = desc2.replace(f"{desc3a}", f"```fix\n{interaction.user.display_name} has won the game")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")

      if betcheck:
        uservalue = get_db('users')[f'{turn.id}']['score']
        yourvalue = get_db('users')[f'{interaction.user.id}']['score']
        uservalueint = float(uservalue)
        yourvalueint = float(yourvalue)
        uservaluefinal = uservalueint - int(bet2)
        yourvaluefinal = yourvalueint + int(bet2)
        update_db('users', f'{turn.id}', {"score": uservaluefinal})
        update_db('users', f'{interaction.user.id}', {"score": yourvaluefinal})
        final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}\n\n{interaction.user.name}: {yourvalue} ≫ {yourvaluefinal}\n{turn.name}: {uservalue} ≫ {uservaluefinal}")

      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    elif count == 1:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      desc3 = desc2.replace(f"{desc3a}", f"```fix\nIt's a tie")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")
      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    else:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      await interaction.message.edit(embed=final, content=None, view=self)
      await interaction.response.defer()

  @discord.ui.button(label="6", style=discord.ButtonStyle.primary, custom_id="6", disabled=False, row=1)
  async def six(self, button, interaction):
    val = str(button.label)
    val2 = int(val)
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    comps = str(interaction.message.components)
    for embed in embeds:
      embeddict = embed.to_dict()

    bet = str(embeddict['description'])
    bet2 = bet.split('Bet: **`')[1].lstrip().split('`**')[0]
    betcheck = False
    if bet2 != "None":
      betcheck = True

    desc = embeddict["description"]
    footer = embeddict["footer"]
    footerpre = str(footer)[-3]
    footer2 = footerpre.replace(f"{footerpre}", f"{int(footerpre) + 1}")

    footerpre2 = str(desc).replace("!", "")
    if (float(footer2) % 2) == 0:
      desc3 = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc2 = str(desc).replace(numbers[val2], "X")
      lastturn = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      symbol = "X"
    else:
      lastturn = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc3 = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      desc2 = str(desc).replace(numbers[val2], "0")
      symbol = "0"

    if int(lastturn) != interaction.user.id:
      await interaction.response.defer()
      return

    pattern = "disabled=False"
    comps2 = comps.split(" ")
    count = 0
    for word in comps2:
      if pattern in word:
        count += 1
      else:
        pass

    value = get_db('minigames')['ttt'][f'{interaction.message.id}']
    value2 = value.split(f"{small_to_big(numbers[val2])}", 1)[1].lstrip().split('-')[0]
    value3 = value.replace(f"{small_to_big(numbers[val2])}{value2}", f"{small_to_big(numbers[val2])}{symbol}")
    update_db('minigames', 'ttt', {f"{interaction.message.id}": f"{value3}"})

    turn = interaction.guild.get_member(int(desc3))
    desc3a = str(desc).split("...", 1)[0]
    desc3 = desc2.replace(f"{desc3a}", f"```fix\nWaiting for {turn.display_name}")

    final = discord.Embed(description=f"{desc3}")
    final.set_footer(text=f"Turn number: {footer2}")
    if checkwin(str(interaction.message.id), symbol):
      desc3 = desc2.replace(f"{desc3a}", f"```fix\n{interaction.user.display_name} has won the game")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")

      if betcheck:
        uservalue = get_db('users')[f'{turn.id}']['score']
        yourvalue = get_db('users')[f'{interaction.user.id}']['score']
        uservalueint = float(uservalue)
        yourvalueint = float(yourvalue)
        uservaluefinal = uservalueint - int(bet2)
        yourvaluefinal = yourvalueint + int(bet2)
        update_db('users', f'{turn.id}', {"score": uservaluefinal})
        update_db('users', f'{interaction.user.id}', {"score": yourvaluefinal})
        final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}\n\n{interaction.user.name}: {yourvalue} ≫ {yourvaluefinal}\n{turn.name}: {uservalue} ≫ {uservaluefinal}")

      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    elif count == 1:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      desc3 = desc2.replace(f"{desc3a}", f"```fix\nIt's a tie")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")
      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    else:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      await interaction.message.edit(embed=final, content=None, view=self)
      await interaction.response.defer()

  @discord.ui.button(label="7", style=discord.ButtonStyle.primary, custom_id="7", disabled=False, row=2)
  async def seven(self, button, interaction):
    val = str(button.label)
    val2 = int(val)
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    comps = str(interaction.message.components)
    for embed in embeds:
      embeddict = embed.to_dict()

    bet = str(embeddict['description'])
    bet2 = bet.split('Bet: **`')[1].lstrip().split('`**')[0]
    betcheck = False
    if bet2 != "None":
      betcheck = True

    desc = embeddict["description"]
    footer = embeddict["footer"]
    footerpre = str(footer)[-3]
    footer2 = footerpre.replace(f"{footerpre}", f"{int(footerpre) + 1}")

    footerpre2 = str(desc).replace("!", "")
    if (float(footer2) % 2) == 0:
      desc3 = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc2 = str(desc).replace(numbers[val2], "X")
      lastturn = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      symbol = "X"
    else:
      lastturn = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc3 = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      desc2 = str(desc).replace(numbers[val2], "0")
      symbol = "0"

    if int(lastturn) != interaction.user.id:
      await interaction.response.defer()
      return

    pattern = "disabled=False"
    comps2 = comps.split(" ")
    count = 0
    for word in comps2:
      if pattern in word:
        count += 1
      else:
        pass

    value = get_db('minigames')['ttt'][f'{interaction.message.id}']
    value2 = value.split(f"{small_to_big(numbers[val2])}", 1)[1].lstrip().split('-')[0]
    value3 = value.replace(f"{small_to_big(numbers[val2])}{value2}", f"{small_to_big(numbers[val2])}{symbol}")
    update_db('minigames', 'ttt', {f"{interaction.message.id}": f"{value3}"})

    turn = interaction.guild.get_member(int(desc3))
    desc3a = str(desc).split("...", 1)[0]
    desc3 = desc2.replace(f"{desc3a}", f"```fix\nWaiting for {turn.display_name}")

    final = discord.Embed(description=f"{desc3}")
    final.set_footer(text=f"Turn number: {footer2}")
    if checkwin(str(interaction.message.id), symbol):
      desc3 = desc2.replace(f"{desc3a}", f"```fix\n{interaction.user.display_name} has won the game")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")

      if betcheck:
        uservalue = get_db('users')[f'{turn.id}']['score']
        yourvalue = get_db('users')[f'{interaction.user.id}']['score']
        uservalueint = float(uservalue)
        yourvalueint = float(yourvalue)
        uservaluefinal = uservalueint - int(bet2)
        yourvaluefinal = yourvalueint + int(bet2)
        update_db('users', f'{turn.id}', {"score": uservaluefinal})
        update_db('users', f'{interaction.user.id}', {"score": yourvaluefinal})
        final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}\n\n{interaction.user.name}: {yourvalue} ≫ {yourvaluefinal}\n{turn.name}: {uservalue} ≫ {uservaluefinal}")

      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    elif count == 1:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      desc3 = desc2.replace(f"{desc3a}", f"```fix\nIt's a tie")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")
      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    else:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      await interaction.message.edit(embed=final, content=None, view=self)
      await interaction.response.defer()

  @discord.ui.button(label="8", style=discord.ButtonStyle.primary, custom_id="8", disabled=False, row=2)
  async def eight(self, button, interaction):
    val = str(button.label)
    val2 = int(val)
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    comps = str(interaction.message.components)
    for embed in embeds:
      embeddict = embed.to_dict()

    bet = str(embeddict['description'])
    bet2 = bet.split('Bet: **`')[1].lstrip().split('`**')[0]
    betcheck = False
    if bet2 != "None":
      betcheck = True

    desc = embeddict["description"]
    footer = embeddict["footer"]
    footerpre = str(footer)[-3]
    footer2 = footerpre.replace(f"{footerpre}", f"{int(footerpre) + 1}")

    footerpre2 = str(desc).replace("!", "")
    if (float(footer2) % 2) == 0:
      desc3 = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc2 = str(desc).replace(numbers[val2], "X")
      lastturn = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      symbol = "X"
    else:
      lastturn = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc3 = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      desc2 = str(desc).replace(numbers[val2], "0")
      symbol = "0"

    if int(lastturn) != interaction.user.id:
      await interaction.response.defer()
      return

    pattern = "disabled=False"
    comps2 = comps.split(" ")
    count = 0
    for word in comps2:
      if pattern in word:
        count += 1
      else:
        pass

    value = get_db('minigames')['ttt'][f'{interaction.message.id}']
    value2 = value.split(f"{small_to_big(numbers[val2])}", 1)[1].lstrip().split('-')[0]
    value3 = value.replace(f"{small_to_big(numbers[val2])}{value2}", f"{small_to_big(numbers[val2])}{symbol}")
    update_db('minigames', 'ttt', {f"{interaction.message.id}": f"{value3}"})

    turn = interaction.guild.get_member(int(desc3))
    desc3a = str(desc).split("...", 1)[0]
    desc3 = desc2.replace(f"{desc3a}", f"```fix\nWaiting for {turn.display_name}")

    final = discord.Embed(description=f"{desc3}")
    final.set_footer(text=f"Turn number: {footer2}")
    if checkwin(str(interaction.message.id), symbol):
      desc3 = desc2.replace(f"{desc3a}", f"```fix\n{interaction.user.display_name} has won the game")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")

      if betcheck:
        uservalue = get_db('users')[f'{turn.id}']['score']
        yourvalue = get_db('users')[f'{interaction.user.id}']['score']
        uservalueint = float(uservalue)
        yourvalueint = float(yourvalue)
        uservaluefinal = uservalueint - int(bet2)
        yourvaluefinal = yourvalueint + int(bet2)
        update_db('users', f'{turn.id}', {"score": uservaluefinal})
        update_db('users', f'{interaction.user.id}', {"score": yourvaluefinal})
        final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}\n\n{interaction.user.name}: {yourvalue} ≫ {yourvaluefinal}\n{turn.name}: {uservalue} ≫ {uservaluefinal}")

      del_db('minigames/ttt', f"{interaction.message.id}")
      add_milestone(user=interaction.user.id, milestone="mini-games, TTT", amount=1)
      await interaction.message.edit(emrbed=final, content=None, view=None)
    elif count == 1:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      desc3 = desc2.replace(f"{desc3a}", f"```fix\nIt's a tie")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")
      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    else:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      await interaction.message.edit(embed=final, content=None, view=self)
      await interaction.response.defer()

  @discord.ui.button(label="9", style=discord.ButtonStyle.primary, custom_id="9", disabled=False, row=2)
  async def nine(self, button, interaction):
    val = str(button.label)
    val2 = int(val)
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    comps = str(interaction.message.components)
    for embed in embeds:
      embeddict = embed.to_dict()

    bet = str(embeddict['description'])
    bet2 = bet.split('Bet: **`')[1].lstrip().split('`**')[0]
    betcheck = False
    if bet2 != "None":
      betcheck = True

    desc = embeddict["description"]
    footer = embeddict["footer"]
    footerpre = str(footer)[-3]
    footer2 = footerpre.replace(f"{footerpre}", f"{int(footerpre) + 1}")

    footerpre2 = str(desc).replace("!", "")
    if (float(footer2) % 2) == 0:
      desc3 = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc2 = str(desc).replace(numbers[val2], "X")
      lastturn = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      symbol = "X"
    else:
      lastturn = footerpre2.split("┅\n<@", 1)[1].lstrip().split('> ⋙ **`0`**')[0]
      desc3 = footerpre2.split("<@", 1)[1].lstrip().split('> ⋙ **`X`**')[0]
      desc2 = str(desc).replace(numbers[val2], "0")
      symbol = "0"

    if int(lastturn) != interaction.user.id:
      await interaction.response.defer()
      return

    pattern = "disabled=False"
    comps2 = comps.split(" ")
    count = 0
    for word in comps2:
      if pattern in word:
        count += 1
      else:
        pass

    value = get_db('minigames')['ttt'][f'{interaction.message.id}']
    value2 = value.split(f"{small_to_big(numbers[val2])}", 1)[1].lstrip().split('-')[0]
    value3 = value.replace(f"{small_to_big(numbers[val2])}{value2}", f"{small_to_big(numbers[val2])}{symbol}")
    update_db('minigames', 'ttt', {f"{interaction.message.id}": f"{value3}"})

    turn = interaction.guild.get_member(int(desc3))
    desc3a = str(desc).split("...", 1)[0]
    desc3 = desc2.replace(f"{desc3a}", f"```fix\nWaiting for {turn.display_name}")

    final = discord.Embed(description=f"{desc3}")
    final.set_footer(text=f"Turn number: {footer2}")
    if checkwin(str(interaction.message.id), symbol):
      desc3 = desc2.replace(f"{desc3a}", f"```fix\n{interaction.user.display_name} has won the game")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")

      if betcheck:
        uservalue = get_db('users')[f'{turn.id}']['score']
        yourvalue = get_db('users')[f'{interaction.user.id}']['score']
        uservalueint = float(uservalue)
        yourvalueint = float(yourvalue)
        uservaluefinal = uservalueint - int(bet2)
        yourvaluefinal = yourvalueint + int(bet2)
        update_db('users', f'{turn.id}', {"score": uservaluefinal})
        update_db('users', f'{interaction.user.id}', {"score": yourvaluefinal})
        final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}\n\n{interaction.user.name}: {yourvalue} ≫ {yourvaluefinal}\n{turn.name}: {uservalue} ≫ {uservaluefinal}")

      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    elif count == 1:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      desc3 = desc2.replace(f"{desc3a}", f"```fix\nIt's a tie")
      final = discord.Embed(description=f"{desc3}")
      final.set_footer(text=f"Game concluded.\nNumber of turns: {footerpre}")
      del_db('minigames/ttt', f"{interaction.message.id}")
      await interaction.message.edit(embed=final, content=None, view=None)
    else:
      button.disabled = True
      button.style = discord.ButtonStyle.gray
      await interaction.message.edit(embed=final, content=None, view=self)
      await interaction.response.defer()

class Join_TTT(discord.ui.View):
  def __init__(self, user, author):
    super().__init__(timeout=60)
    self.value = 0
    self.user = user
    self.author = author

  @discord.ui.button(label="Join TTT game", style=discord.ButtonStyle.green, custom_id="Join")
  async def join(self, button, interaction):
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()

    footer = embeddict['footer']['text']
    bet = str(embeddict['description'])
    bet2 = bet.split('Bet: ')[1]
    self.value += 1
    if self.value == 1:
      if str(interaction.user.id) == self.user:
        author2 = interaction.guild.get_member(int(self.author))

        random = randint(1, 2)
        if random == 1:
          first = author2
          second = interaction.user
        else:
          first = interaction.user
          second = author2

        view = Tic()
        embed = discord.Embed(description=f"""```fix\nWaiting for {first.display_name}...```\nCurrent Bet: {bet2} {check_currency(interaction.guild.id)}\n
```ml
┌─────────┐
  ₁│ ₂ │₃
  ─┼───┼─
  ₄│ ₅ │₆
  ─┼───┼─
  ₇│ ₈ │₉
└─────────┘```\n{first.mention} ⋙ **`X`**\n┅┅┅┅┅┅┅┅┅┅\n{second.mention} ⋙ **`0`**""")
        embed.set_footer(text="Turn number: 1")
        msg = await interaction.message.edit(embed=embed, view=view)
        update_db('minigames', "ttt", {f"{msg.id}": "0None-1None-2None-3None-4None-5None-6None-7None-8None-9None"})
        await interaction.response.defer()
      else:
        self.value = 0
        return

  @discord.ui.button(label="Decline", style=discord.ButtonStyle.red, custom_id="decline")
  async def decline(self, button, interaction):
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()

    footer = embeddict['footer']['text']
    bet = str(embeddict['description'])
    bet2 = bet.split('Current')[1]
    self.value += 1
    if self.value == 1:
      if str(interaction.user.id) == self.user:
        embed2 = discord.Embed(description=f"{interaction.user.mention} has declined your invitation.")
        await interaction.message.edit(content=None, embed=embed2, view=None)
        await interaction.response.defer()
      else:
        self.value = 0
        return

  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    else:
      await self.message.edit(view=self, content="Timed out.")

### commands ###
class Slash(commands.Cog):
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

  async def disable(self, ctx):
    ### internally disabled ###
    if ctx.author.id != int(ses):
      raise discord.ext.commands.CommandError(f"Sorry, this command is currently internally disabled, as it is being worked on.")


  @slash_command(name="print", description="Print any image you want. 5 Minute Cooldown, Forced ephemeral.")
  async def print(self, ctx, *, input:Option(str, "Anything you want to search on google.", required=True)):
    cooldown = False
    try:
      global value
      value = get_db('timers')[f"TimerPrint-{ctx.author.id}"]
      cooldown = True
    except:
      cooldown = False

    if cooldown == False:
      try:
        channel = discord.utils.get(ctx.guild.channels, name="logs-the-second")
      except:
        pass
      else:
        embed = discord.Embed(description=f"Slash Command used in <#{ctx.channel.id}>.", color=discord.Color.random())
        embed.add_field(name=f'Command used:', value=f"/print {input}")
        embed.set_author(name=f"{check_name(ctx.author)} • ID: {ctx.author.id}", icon_url=ctx.author.avatar)
        embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)
        await channel.send(embed=embed, content=None)
        pass

      await ctx.defer(ephemeral=True)
      nmb = randint(0, 19)
      url = "https://google-search83.p.rapidapi.com/google/search_image"

      querystring = {"query":f"{input}","gl":"us","lr":"en","num":"1","start":"0"}

      headers = {
      	"X-RapidAPI-Key": "656579fde0msh1a659fc425536d6p163315jsn94162aa70de6",
      	"X-RapidAPI-Host": "google-search83.p.rapidapi.com"
      }

      googleresponse = requests.request("GET", url, headers=headers, params=querystring)
      res2 = googleresponse.json()[nmb]['url']
      finalembed = discord.Embed(description=f"Searched for **`{input}`**.\nEntry Number: `{nmb}`")
      finalembed.set_image(url=res2)
      await ctx.respond(embed=finalembed, content=None, ephemeral=True)
      time = 300
      update_db('timers', f"none", {f"TimerPrint-{ctx.author.id}": add_time(time)})
    else:
      finalembed = discord.Embed(description=f"You're on Cooldown.\n```\nTime left: {value} seconds.```")
      await ctx.respond(embed=finalembed, content=None, ephemeral=True)

  @commands.command(aliases=["russianroulette", "russian", "roulette"])
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 120, commands.BucketType.guild)
  async def rr(self, ctx, bet: int=None):
    img = Image.open('images/assets/rr/rr_background.png').convert("RGBA")

    turn = 1
    coords = (150, 300)
    count = 1
    text_x = 550
    while count <= 6:
      if count >= 4:
        coords_final = (coords[0]+450*(count-4), coords[1]+350)
        text_x_final = text_x+900*(count-4)
      else:
        text_x_final = text_x+900*(count-1)
        coords_final = (coords[0]+450*(count-1), coords[1])

      if count > 1:
        outline = Image.new('RGBA', (262, 312), (30, 30, 30))
        img.paste(smooth_corners(outline, 30), (coords_final[0] - 6, coords_final[1] - 6), smooth_corners(outline, 30))
        unknown = Image.open("images/assets/rr/unknown.png").convert("RGBA").resize((250, 250))
        img.paste(unknown, coords_final, unknown)
        count += 1
        continue

      asset = ctx.author.display_avatar
      data = BytesIO(await asset.read())
      player_pfp = Image.open(data).convert("RGBA").resize((250, 250))

      #check for color
      color = (30, 30, 30)

      outline = Image.new('RGBA', (262, 312), color)
      img.paste(smooth_corners(outline, 30), (coords_final[0]-6, coords_final[1]-6), smooth_corners(outline, 30))

      img.paste(smooth_corners(player_pfp, 30), coords_final, smooth_corners(player_pfp, 30))

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"{ctx.author.display_name}", font=ImageFont.truetype("images/assets/que.otf", 40))
      draw.text(((text_x_final - w) / 2, coords_final[1]+260), f"{ctx.author.display_name}", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 40), stroke_fill=(0, 0, 0), stroke_width=4)
      count += 1

    TINT_COLOR = (0, 0, 0)
    TRANSPARENCY = .50
    OPACITY = int(255 * TRANSPARENCY)

    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)

    draw3.rounded_rectangle((100, 100, 1400, 250), fill=TINT_COLOR + (OPACITY,), radius=20)
    img = Image.alpha_composite(img, overlay)

    draw = ImageDraw.Draw(img)
    _, _, w, h = draw.textbbox((0, 0), f"""Waiting for players...""", font=ImageFont.truetype("images/assets/que.otf", 70))
    draw.text(((1500 - w) / 2, 145), f"""Waiting for players...""", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
    _, _, w, h = draw.textbbox((0, 0), f"""=== Russian Roulette ===""", font=ImageFont.truetype("images/assets/que.otf", 80))
    draw.text(((1500 - w) / 2, 20), f"""=== Russian Roulette ===""", (200, 200, 200), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)


    embed = discord.Embed()
    try:
      firstvalue = get_db('users')[f'{ctx.author.id}']['score']
    except:
      firstvalue = 0

    if bet:
      if bet <= 0:
        embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you can not bet below 1 {check_currency(ctx.guild.id)}.```", color=red)
        await ctx.send(embed=embed2, content=None, delete_after=30)
        return
      elif bet > 1000:
        embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you can not bet above 1000 {check_currency(ctx.guild.id)}.```", color=red)
        await ctx.send(embed=embed2, content=None, delete_after=30)
        return
      elif float(firstvalue) < bet:
        embed2 = discord.Embed(description=f"**`ERROR:`** ```\n{ctx.author.name}, you do not have enough {check_currency(ctx.guild.id)}.\n\nYour bet: {bet}\nYour {check_currency(ctx.guild.id)}: {firstvalue}```", color=red)
        await ctx.send(embed=embed2, content=None, delete_after=30)
        return
    else:
      bet = 0

    img.save(f"images/rr/{ctx.author.id}.png")
    f = discord.File(f"{os.getcwd()}/images/rr/{ctx.author.id}.png", filename=f"{ctx.author.id}.png")

    join = Join_rr()
    embed.set_footer(text=f"Current Bet: {bet} {check_currency(ctx.guild.id)}")
    embed.set_image(url=f"attachment://{ctx.author.id}.png")
    msgid = await ctx.send(embed=embed, view=join, file=f)

    update_db("minigames/rr", f"{msgid.id}", {'turn': 1, 'total_turns': 0, 'total_players': 1, 'player_count': 1, 'bet': bet, 'all_ids': [ctx.author.id], 'player1': {'id': ctx.author.id, 'name': ctx.author.display_name, 'dead': False}})

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 30, commands.BucketType.guild)
  async def rps(self, ctx, user: discord.User=None, bet: int=None):
    if user is None:
      embed = discord.Embed(description="Waiting...")
      embed.set_footer(text=f"{ctx.author.id}")
      await ctx.send(embed=embed, view=Select())
    else:
      if user.bot:
        embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, bots cannot fight you.```", color=red)
        await ctx.send(embed=embed2, content=None, delete_after=30)
        return
      else:
        if user == int or user.mention:
          pass
        else:
          user = ctx.guild.get_member_named(user)
        if ctx.author.id == user.id:
          embed = discord.Embed(description="Waiting...")
          embed.set_footer(text=f"{ctx.author.id}")
          await ctx.send(embed=embed, view=Select())
          return
        else:
          pass
        if bet != None:
          try:
            firstvalue = get_db('users')[f'{ctx.author.id}']['score']
          except:
            firstvalue = 0

          try:
            secondvalue = get_db('users')[f'{user.id}']['score']
          except:
            secondvalue = 0

          if bet <= 0:
            embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you can not bet below 1 {check_currency(ctx.guild.id)}.```", color=red)
            await ctx.send(embed=embed2, content=None, delete_after=15)
            return
          elif float(firstvalue) < bet:
            embed2 = discord.Embed(description=f"**`ERROR:`** ```\n{ctx.author.name}, you do not have enough {check_currency(ctx.guild.id)}.\n\nYour bet: {bet}\nYour {check_currency(ctx.guild.id)}: {firstvalue}```", color=red)
            await ctx.send(embed=embed2, content=None, delete_after=15)
            return
          elif bet > 1000:
            bet = 1000
            pass
          elif float(secondvalue) < bet:
            embed2 = discord.Embed(description=f"**`ERROR:`** ```\n{ctx.author.name}, {user.name} does not have enough {check_currency(ctx.guild.id)}.\n\nYour bet: {bet}\n{user.name}'s {check_currency(ctx.guild.id)}: {secondvalue}```", color=red)
            await ctx.send(embed=embed2, content=None, delete_after=15)
            return
        else:
          bet = 0


        asset = ctx.author.display_avatar
        data = BytesIO(await asset.read())
        player1_pfp = Image.open(data).convert("RGBA").resize((300, 300))

        TINT_COLOR = (0, 0, 0)
        TRANSPARENCY = .50
        OPACITY = int(255 * TRANSPARENCY)

        img = Image.open('images/assets/backgrounds/rps_background.png').convert("L")
        black = randint(0, 200), randint(0, 20), randint(0, 200)
        img = ImageOps.colorize(img, black=black, white="white")
        img = img.convert("RGBA")

        outline = Image.new('RGBA', (302, 302), (30, 30, 30))
        img.paste(smooth_corners(outline, 30), (59, 299), smooth_corners(outline, 30))
        outline = Image.new('RGBA', (302, 302), (30, 30, 30))
        img.paste(smooth_corners(outline, 30), (1139, 299), smooth_corners(outline, 30))

        img.paste(smooth_corners(player1_pfp, 30), (60, 300), smooth_corners(player1_pfp, 30))

        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), f"{ctx.author.display_name}", font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((450-w)/2, 220), f"{ctx.author.display_name}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
        _, _, w, h = draw.textbbox((0, 0), f"{user.display_name}", font=ImageFont.truetype("images/assets/que.otf", 70))
        draw.text(((2550-w)/2, 220), f"{user.display_name}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=4)


        _, _, w, h = draw.textbbox((0, 0), f"=== Rock, Paper, Scissors ===", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((1500-w)/2, 20), f"=== Rock, Paper, Scissors ===", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

        overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
        draw3 = ImageDraw.Draw(overlay)

        outline = Image.new('RGBA', (220, 220), (30, 30, 30, 50))
        draw3.rounded_rectangle((650, 680, 850, 870), fill=TINT_COLOR + (OPACITY,), radius=20)
        img = Image.alpha_composite(img, overlay)

        draw = ImageDraw.Draw(img)
        _, _, w, h = draw.textbbox((0, 0), f"Bet:", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((1500-w)/2, 690), f"Bet:", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

        _, _, w, h = draw.textbbox((0, 0), f"{bet}", font=ImageFont.truetype("images/assets/que.otf", 80))
        draw.text(((1500-w)/2, 780), f"{bet}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=4)

        img.save(f"images/rps/{ctx.author.id}.png")
        f = discord.File(f"{os.getcwd()}/images/rps/{ctx.author.id}.png", filename="{ctx.author.id}.png")

        embed = discord.Embed(description=f"Waiting for {user.mention} to join...\nCurrent Bet: **`{bet}`** **`{check_currency(ctx.guild.id)}`**")
        embed.set_image(url=f"attachment://{ctx.author.id}.png")
        mesid = await ctx.send(embed=embed, view=Join(), file=f)

        update_db("minigames/rps", f"{mesid.id}", {"player1": {"id": f"{ctx.author.id}", "name": f"{ctx.author.display_name}", "pick": "None", "points": 0}, "player2": {"id": f"{user.id}", "name": f"{user.display_name}", "pick": "None", "points": 0}, "bet": f"{bet}"})
        return


  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 30, commands.BucketType.guild)
  async def ttt(self, ctx, user: discord.User, bet: int=None):
    if user is None:
      embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, Fax can not fight you. yet.```", color=red)
      await ctx.send(embed=embed2, content=None, delete_after=30)
      return
    else:
      if user.bot:
        embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, bots can not fight you.```", color=red)
        await ctx.send(embed=embed2, content=None, delete_after=30)
        return
      else:
        if user == int or user.mention:
          pass
        else:
          user = ctx.guild.get_member_named(user)
        if ctx.author.id == user.id:
          embed = discord.Embed(description="Waiting...")
          embed.set_footer(text=f"{ctx.author.id}")
          await ctx.send(embed=embed, view=Select())
          return
        else:
          pass
        if bet != None:
          try:
            firstvalue = get_db('users')[f'{ctx.author.id}']['score']
          except:
            firstvalue = 0

          try:
            secondvalue = get_db('users')[f'{user.id}']['score']
          except:
            secondvalue = 0

          if bet <= 0:
            embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you can not bet below 1 {check_currency(ctx.guild.id)}.```", color=red)
            await ctx.send(embed=embed2, content=None, delete_after=30)
            return
          elif bet > 1000:
            embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you can not bet above 1000 {check_currency(ctx.guild.id)}.```", color=red)
            await ctx.send(embed=embed2, content=None, delete_after=30)
            return
          elif float(firstvalue) < bet:
            embed2 = discord.Embed(description=f"**`ERROR:`** ```\n{ctx.author.name}, you do not have enough {check_currency(ctx.guild.id)}.\n\nYour bet: {bet}\nYour {check_currency(ctx.guild.id)}: {firstvalue}```", color=red)
            await ctx.send(embed=embed2, content=None, delete_after=30)
            return
          elif float(secondvalue) < bet:
            embed2 = discord.Embed(description=f"**`ERROR:`** ```\n{ctx.author.name}, {user.name} does not have enough {check_currency(ctx.guild.id)}.\n\nYour bet: {bet}\n{user.name}'s {check_currency(ctx.guild.id)}: {secondvalue}```", color=red)
            await ctx.send(embed=embed2, content=None, delete_after=30)
            return
          else:
            embed = discord.Embed(description=f"Waiting for {user.mention} to join...\nCurrent Bet: **`{bet}`**")
            embed.set_footer(text=f"Gamemode: Tic Tac Toe")
            user2 = str(user.id)
            author = str(ctx.author.id)
            await ctx.send(embed=embed, view=Join_TTT(user2, author))
        else:
          embed = discord.Embed(description=f"Waiting for {user.mention} to join...\nCurrent Bet: **`None`**")
          embed.set_footer(text=f"Gamemode: Tic Tac Toe")
          user2 = str(user.id)
          author = str(ctx.author.id)
          await ctx.send(embed=embed, view=Join_TTT(user2, author))


def setup(client):
  client.add_cog(Slash(client))
  