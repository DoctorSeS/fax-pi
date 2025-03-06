import math

import discord
from discord.ext import commands, tasks
import random
from random import randint
from main import client, bot_prefix, round_time, ses, currency, red, green, check_name
from cogs.shop import role1emoji, role2emoji, role3emoji, role4emoji, role5emoji
from cogs.score import check_currency
from discord.ui import InputText, Modal
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
from cogs.mini_games import add_milestone
import os
import time
from database import *

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
  
role_list = ["role5", "role4", "role3", "role2", "role1"]
emojies2 = f"role1,role1,role1,role1,role1,role2,role2,role2,role2,role2,role3,role3,role3,role4,role4,role5"
emojilist2 = emojies2.split(",")
preview_emoji = role5emoji
no_emoji = role1emoji
empty = '\uFEFF'

common_multiplier = 0.75
uncommon_multiplier = 1.25
rare_multiplier = 2
legendary_multiplier = 3
exotic_multiplier = 5

### slots embed1 ###
slots_footer = f'When you press the "Change" button, you have to type a number right after you press it to change the amount of money you want to bet.'

slots_embed1 = discord.Embed(title=f"Slots Guide", description="""```asciidoc\nAll Possible Patterns for wins\n==============================```""", color=0x5927b8)
slots_embed1.add_field(name="Rarity Multipliers:", value=f"{role1emoji} > **`{common_multiplier}x`**\n{role2emoji} > **`{uncommon_multiplier}x`**\n{role3emoji} > **`{rare_multiplier}x`**\n{role4emoji} > **`{legendary_multiplier}x`**\n{role5emoji} > **`{exotic_multiplier}x`**", inline=False)

slots_embed1.add_field(name="Normal 1\nPayout:\n(Bet * 1.5) * Rarity", value=f"{preview_emoji} {no_emoji} {no_emoji}\n{preview_emoji} {no_emoji} {no_emoji}\n{preview_emoji} {no_emoji} {no_emoji}")
slots_embed1.add_field(name="Normal 2\nPayout:\n(Bet * 1.5) * Rarity", value=f"{no_emoji} {preview_emoji} {no_emoji}\n{no_emoji} {preview_emoji} {no_emoji}\n{no_emoji} {preview_emoji} {no_emoji}")
slots_embed1.add_field(name="Normal 3\nPayout:\n(Bet * 1.5) * Rarity", value=f"{no_emoji} {no_emoji} {preview_emoji}\n{no_emoji} {no_emoji} {preview_emoji}\n{no_emoji} {no_emoji} {preview_emoji}")

slots_embed1.add_field(name="Normal 4\nPayout:\n(Bet * 1.5) * Rarity", value=f"{preview_emoji} {preview_emoji} {preview_emoji}\n{no_emoji} {no_emoji} {no_emoji}\n{no_emoji} {no_emoji} {no_emoji}")
slots_embed1.add_field(name="Normal 5\nPayout:\n(Bet * 1.5) * Rarity", value=f"{no_emoji} {no_emoji} {no_emoji}\n{preview_emoji} {preview_emoji} {preview_emoji}\n{no_emoji} {no_emoji} {no_emoji}")
slots_embed1.add_field(name="Normal 6\nPayout:\n(Bet * 1.5) * Rarity", value=f"{no_emoji} {no_emoji} {no_emoji}\n{no_emoji} {no_emoji} {no_emoji}\n{preview_emoji} {preview_emoji} {preview_emoji}")

slots_embed1.add_field(name="Normal 7\nPayout:\n(Bet * 1.5) * Rarity", value=f"{preview_emoji} {no_emoji} {no_emoji}\n{no_emoji} {preview_emoji} {no_emoji}\n{no_emoji} {no_emoji} {preview_emoji}")
slots_embed1.add_field(name="Normal 8\nPayout:\n(Bet * 1.5) * Rarity", value=f"{no_emoji} {no_emoji} {preview_emoji}\n{no_emoji} {preview_emoji} {no_emoji}\n{preview_emoji} {no_emoji} {no_emoji}")
slots_embed1.add_field(name=empty, value=empty)

slots_embed1.add_field(name="Full board\nPayout:\n(Bet * 50) * Rarity", value=f"{preview_emoji} {preview_emoji} {preview_emoji}\n{preview_emoji} {preview_emoji} {preview_emoji}\n{preview_emoji} {preview_emoji} {preview_emoji}")
slots_embed1.add_field(name="Big Ass 2\nPayout:\n(Bet * 10) * Rarity", value=f"{preview_emoji} {no_emoji} {preview_emoji}\n{no_emoji} {preview_emoji} {no_emoji}\n{preview_emoji} {no_emoji} {preview_emoji}")
slots_embed1.add_field(name="Big Ass 3\nPayout:\n(Bet * 10) * Rarity", value=f"{no_emoji} {preview_emoji} {no_emoji}\n{preview_emoji} {preview_emoji} {preview_emoji}\n{no_emoji} {preview_emoji} {no_emoji}")

slots_embed1.add_field(name="Big Line 1\nPayout:\n(Bet * 5) * Rarity", value=f"{preview_emoji} {preview_emoji} {preview_emoji}\n{preview_emoji} {preview_emoji} {preview_emoji}\n{no_emoji} {no_emoji} {no_emoji}")
slots_embed1.add_field(name="Big Line 2\nPayout:\n(Bet * 5) * Rarity", value=f"{no_emoji} {no_emoji} {no_emoji}\n{preview_emoji} {preview_emoji} {preview_emoji}\n{preview_emoji} {preview_emoji} {preview_emoji}")
slots_embed1.add_field(name="Big Line 3\nPayout:\n(Bet * 5) * Rarity", value=f"{no_emoji} {no_emoji} {no_emoji}\n{preview_emoji} {preview_emoji} {preview_emoji}\n{preview_emoji} {preview_emoji} {preview_emoji}")
slots_embed1.add_field(name="Big Line 4\nPayout:\n(Bet * 5) * Rarity", value=f"{preview_emoji} {preview_emoji} {no_emoji}\n{preview_emoji} {preview_emoji} {no_emoji}\n{preview_emoji} {preview_emoji} {no_emoji}")
slots_embed1.add_field(name="Big Line 5\nPayout:\n(Bet * 5) * Rarity", value=f"{no_emoji} {preview_emoji} {preview_emoji}\n{no_emoji} {preview_emoji} {preview_emoji}\n{no_emoji} {preview_emoji} {preview_emoji}")
slots_embed1.add_field(name="Big Line 6\nPayout:\n(Bet * 5) * Rarity", value=f"{preview_emoji} {no_emoji} {preview_emoji}\n{preview_emoji} {no_emoji} {preview_emoji}\n{preview_emoji} {no_emoji} {preview_emoji}")
slots_embed1.set_footer(text=slots_footer)

class Change_Modal(Modal):
  def __init__(self, ctx, amount, start) -> None:
    self.ctx = ctx
    self.amount = amount
    self.start = start
    super().__init__(title="Change bet amount")
    self.add_item(InputText(label="Type in your bet", placeholder=f"Ex: {randint(1, 1000)}"))

  async def callback(self, interaction: discord.Interaction):
    response = int(self.children[0].value)

    value = get_db('minigames')['Slots'][f"{interaction.message.id}"]
    ev_else = value.split("/")[1]

    update_db('minigames', 'Slots', {f'{interaction.message.id}': f"{response}/{ev_else}"})

    f = discord.File(f"{os.getcwd()}/images/assets/slots2.png", filename="slots2.png")
    embed = discord.Embed(color=0x36393F)
    embed.set_image(url=f"attachment://slots2.png")

    await interaction.message.edit(embed=embed, view=Slots_Button(self.ctx, self.amount, self.start), file=f)
    await interaction.response.defer()

def replace_name(x):
  if x == role_list[4]:
    return "Common"
  elif x == role_list[3]:
    return "Uncommon"
  elif x == role_list[2]:
    return "Rare"
  elif x == role_list[1]:
    return "Legendary"
  elif x == role_list[0]:
    return "Exotic"


def check_win_slots(randomizer):
  if_win = randomizer.split(',')
  for x in role_list:
    if (if_win[0] == x) and (if_win[1] == x) and (if_win[2] == x) and (if_win[3] == x) and (if_win[4] == x) and (if_win[5] == x) and (if_win[6] == x) and (if_win[7] == x) and (if_win[8] == x):
      return f"full board {replace_name(x)}"

    elif (if_win[0] == x) and (if_win[3] == x) and (if_win[6] == x) and (if_win[1] == x) and (if_win[4] == x) and (if_win[7] == x):
      return f"big line 1 {replace_name(x)}"

    elif (if_win[0] == x) and (if_win[3] == x) and (if_win[6] == x) and (if_win[2] == x) and (if_win[5] == x) and (if_win[8] == x):
      return f"big line 2 {replace_name(x)}"

    elif (if_win[0] == x) and (if_win[1] == x) and (if_win[2] == x) and (if_win[3] == x) and (if_win[4] == x) and (if_win[5] == x):
      return f"big line 3 {replace_name(x)}"

    elif (if_win[3] == x) and (if_win[4] == x) and (if_win[5] == x) and (if_win[6] == x) and (if_win[7] == x) and (if_win[8] == x):
      return f"big line 4 {replace_name(x)}"

    elif (if_win[0] == x) and (if_win[3] == x) and (if_win[6] == x) and (if_win[2] == x) and (if_win[5] == x) and (if_win[8] == x):
      return f"big line 5 {replace_name(x)}"

    elif (if_win[0] == x) and (if_win[2] == x) and (if_win[4] == x) and (if_win[6] == x) and (if_win[8] == x):
      return f"big ass 2 {replace_name(x)}"

    elif (if_win[1] == x) and (if_win[3] == x) and (if_win[4] == x) and (if_win[5] == x) and (if_win[7] == x):
      return f"big ass 3 {replace_name(x)}"


    elif (if_win[0] == x) and (if_win[1] == x) and (if_win[2] == x):
      return f"normal 1 {replace_name(x)}"

    elif (if_win[0] == x) and (if_win[4] == x) and (if_win[8] == x):
      return f"normal 2 {replace_name(x)}"

    elif (if_win[2] == x) and (if_win[4] == x) and (if_win[6] == x):
      return f"normal 2 {replace_name(x)}"

    elif (if_win[0] == x) and (if_win[3] == x) and (if_win[6] == x):
      return f"normal 3 {replace_name(x)}"

    elif (if_win[1] == x) and (if_win[4] == x) and (if_win[7] == x):
      return f"normal 4 {replace_name(x)}"

    elif (if_win[2] == x) and (if_win[5] == x) and (if_win[8] == x):
      return f"normal 5 {replace_name(x)}"

    elif (if_win[3] == x) and (if_win[4] == x) and (if_win[5] == x):
      return f"normal 6 {replace_name(x)}"

    elif (if_win[6] == x) and (if_win[7] == x) and (if_win[8] == x):
      return f"normal 7 {replace_name(x)}"

  else:
    return "You lost"

class Slots_Button(discord.ui.View):
  def __init__(self, ctx, amount, start):
    super().__init__(timeout=None)
    self.value = 0
    self.ctx = ctx
    self.amount = amount
    self.start = start

  @discord.ui.button(label="Spin", style=discord.ButtonStyle.green, custom_id="Spin")
  async def spin(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:
      randomizer = f"{random.choice(emojilist2)},{random.choice(emojilist2)},{random.choice(emojilist2)},{random.choice(emojilist2)},{random.choice(emojilist2)},{random.choice(emojilist2)},{random.choice(emojilist2)},{random.choice(emojilist2)},{random.choice(emojilist2)}"
      randomizer_list = randomizer.split(",")
      current_money = get_db('users')[f'{interaction.user.id}']['score']

      try:
        info = get_db('minigames')['Slots'][f"{interaction.message.id}"]
      except:
        update_db('minigames', 'Slots', {f"{interaction.message.id}": f"{self.amount}/1|{self.start}"})
        bet = self.amount
        spins = 0
        starting_money = self.start
      else:
        bet = info.split("/")[0]
        spins = int(info.split("/")[1].lstrip().split("|")[0])
        starting_money = info.split("|")[1]

      spins += 1
      update_db('minigames', 'Slots', {f"{interaction.message.id}": f"{bet}/{spins}|{starting_money}"})

      if "lost" in check_win_slots(randomizer).lower():
        win = 0 - float(bet)
      else:
        multiplier = common_multiplier
        if "Common" in check_win_slots(randomizer):
          multiplier = common_multiplier
        elif "Uncommon" in check_win_slots(randomizer):
          multiplier = uncommon_multiplier
        elif "Rare" in check_win_slots(randomizer):
          multiplier = rare_multiplier
        elif "Legendary" in check_win_slots(randomizer):
          multiplier = legendary_multiplier
        elif "Exotic" in check_win_slots(randomizer):
          multiplier = exotic_multiplier

        if "full board" in check_win_slots(randomizer):
          win = round((float(bet) * 50) * multiplier, 2)
        elif "big ass 2" in check_win_slots(randomizer):
          win = round((float(bet) * 10) * multiplier, 2)
        elif "big ass 3" in check_win_slots(randomizer):
          win = round((float(bet) * 10) * multiplier, 2)
        elif "big line" in check_win_slots(randomizer):
          win = round((float(bet) * 5) * multiplier, 2)
        elif "normal" in check_win_slots(randomizer):
          win = round((float(bet) * 1.5) * multiplier, 2)
        else:
          win = round((float(bet) * 2) * multiplier, 2)

      if float(current_money) < float(bet):
        no_money = discord.Embed(description=f"**`ERROR:`** ```\n{interaction.user.name}, you do not have enough {check_currency(interaction.guild.id)}.\n\nYour bet: {bet}\nYour {check_currency(interaction.guild.id)}: {check_currency(interaction.guild.id)}```", color=red)
        await interaction.message.edit(embed=no_money, content=None, view=None)
        return

      if win < 0:
        win2 = 0
      else:
        win2 = win

      calculated_value = (round(float(current_money), 2) + float(win2)) - float(bet)
      update_db('users', f"{interaction.user.id}", {"score": calculated_value})

      progress = round(float(calculated_value) - float(starting_money), 2)

      img = Image.open('images/assets/slots2.png')

      if len(check_currency(interaction.guild.id)) <= 3:
        short_currency = check_currency(interaction.guild.id)
      else:
        short_currency = f"{check_currency(interaction.guild.id)[0]}{check_currency(interaction.guild.id)[1]}."

      coords1 = 390
      coords2 = 305
      num = 1
      for x in randomizer_list:
        if num == 4:
          coords1 = 390
          coords2 = 555
        elif num == 7:
          coords1 = 390
          coords2 = 815

        role = Image.open(f'images/assets/roles/{x}.png')
        role = role.resize((210, 240))
        role = role.convert("RGBA")
        img.paste(role, (coords1, coords2), role)
        num += 1
        coords1 += 255

      draw = ImageDraw.Draw(img)
      _, _, w, h = draw.textbbox((0, 0), f"{check_win_slots(randomizer)}", font=ImageFont.truetype("images/assets/milk.ttf", 70))
      draw.text(((1500-w)/2, 110), f"{check_win_slots(randomizer)}", (255, 255, 255), font=ImageFont.truetype("images/assets/milk.ttf", 70), stroke_fill=(0, 0, 0), stroke_width=4)

      if win > 0:
        _, _, w2, h = draw.textbbox((0, 0), f"+ {win}", font=ImageFont.truetype("images/assets/milk.ttf", 70))
        draw.text(((1500 - w2) / 2, 180), f"+ {win}", (0, 150, 0), font=ImageFont.truetype("images/assets/milk.ttf", 70), stroke_fill=(0, 0, 0), stroke_width=4)
      else:
        _, _, w2, h = draw.textbbox((0, 0), f"- {str(win)[1:]}", font=ImageFont.truetype("images/assets/milk.ttf", 70))
        draw.text(((1500 - w2) / 2, 180), f"- {str(win)[1:]}", (150, 0, 0), font=ImageFont.truetype("images/assets/milk.ttf", 70), stroke_fill=(0, 0, 0), stroke_width=4)

      draw.text((1200, 132), f"Wallet:\n{round(calculated_value, 2)} {short_currency}", (255, 255, 255), font=ImageFont.truetype("images/assets/milk.ttf", 50), stroke_fill=(0, 0, 0), stroke_width=4)
      draw.text((1200, 320), f"Spins: {spins}", (255, 255, 255), font=ImageFont.truetype("images/assets/milk.ttf", 50), stroke_fill=(0, 0, 0), stroke_width=4)
      draw.text((1200, 530), f"Current Bet:\n{bet} {short_currency}", (255, 255, 255), font=ImageFont.truetype("images/assets/milk.ttf", 45), stroke_fill=(0, 0, 0), stroke_width=4)
      draw.text((50, 475), f"Progress:", (255, 255, 255), font=ImageFont.truetype("images/assets/milk.ttf", 45), stroke_fill=(0, 0, 0), stroke_width=4)

      if progress > 0:
        higher = Image.open('images/assets/higher2.png')
        higher = higher.resize((60, 60))
        img.paste(higher, (236, 477), higher)
        draw.text((50, 475), f"\n+ {progress} {short_currency}", (0, 150, 0), font=ImageFont.truetype("images/assets/milk.ttf", 45), stroke_fill=(0, 0, 0), stroke_width=4)
      elif progress < 0:
        lower = Image.open('images/assets/lower2.png')
        lower = lower.resize((60, 60))
        img.paste(lower, (236, 477), lower)
        draw.text((50, 475), f"\n- {str(progress)[1:]} {short_currency}", (150, 0, 0), font=ImageFont.truetype("images/assets/milk.ttf", 45), stroke_fill=(0, 0, 0), stroke_width=4)
      else:
        draw.text((50, 475), f"\n{progress} {short_currency}", (255, 255, 255), font=ImageFont.truetype("images/assets/milk.ttf", 45), stroke_fill=(0, 0, 0), stroke_width=4)

      asset = interaction.user.display_avatar
      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      pfp = pfp.resize((246, 246))
      pfp = pfp.convert("RGBA")

      img.paste(smooth_corners(pfp, 20), (37, 141), smooth_corners(pfp, 20))

      img.save(f"images/slots/{interaction.user.id}.png")
      f = discord.File(f"{os.getcwd()}/images/slots/{interaction.user.id}.png", filename=f"{interaction.user.id}.png")

      embed = discord.Embed(color=0x36393F)
      embed.set_image(url=f"attachment://{interaction.user.id}.png")

      await interaction.response.defer()
      time.sleep(0.5)
      add_milestone(user=interaction.user.id, milestone="gambler", amount=1)
      await interaction.message.edit(embed=embed, view=Slots_Button(self.ctx, self.amount, self.start), file=f)
    else:
      return

  @discord.ui.button(label="Change", style=discord.ButtonStyle.gray, custom_id="Change")
  async def Change(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:

      modal = Change_Modal(self.ctx, self.amount, self.start)
      await interaction.response.send_modal(modal)

  @discord.ui.button(label="Guide", style=discord.ButtonStyle.gray, custom_id="Guide")
  async def guide(self, button, interaction):
    await interaction.user.send(embed=slots_embed1, content=None)

    await interaction.message.edit(view=Slots_Button(self.ctx, self.amount, self.start))
    await interaction.response.defer()

  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    else:
      await self.message.edit(view=self)

class Slots(commands.Cog):
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

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 15, commands.BucketType.guild)
  async def slots(self, ctx, amount: float):
    amount = math.floor(amount)
    try:
      user_money = get_db('users')[f'{ctx.author.id}']['score']
    except:
      user_money = 0

    if amount <= 0:
      embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you cannot bet below 1 {check_currency(ctx.guild.id)}.```", color=red)
      await ctx.send(embed=embed2, content=None, delete_after=30)
      return
    #elif amount > 50000:
      #embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you cannot bet above 50000 {check_currency(ctx.guild.id)}.```", color=red)
      #await ctx.send(embed=embed2, content=None, delete_after=30)
      #return
    elif int(user_money) < amount:
      embed2 = discord.Embed(description=f"**`ERROR:`** ```\n{ctx.author.name}, you do not have enough {check_currency(ctx.guild.id)}.\n\nYour bet: {amount}\nYour {check_currency(ctx.guild.id)}: {user_money}```", color=red)
      await ctx.send(embed=embed2, content=None, delete_after=30)
      return
    else:
      start = int(user_money)

      f = discord.File(f"{os.getcwd()}/images/assets/slots2.png", filename="slots2.png")
      embed = discord.Embed(color=0x36393F)
      embed.set_image(url=f"attachment://slots2.png")

      await ctx.send(embed=embed, view=Slots_Button(ctx, amount, start), file=f)

def setup(client):
  client.add_cog(Slots(client))