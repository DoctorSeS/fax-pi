#Score (Fax Machine's Communist Republic of Lauren's Lair's Social Credit Score)
from discord.ext import commands
import discord
import datetime
import random
from random import randint
from main import client, bot_prefix, ses, currency, check_name, green, red
from discord import Option
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
from database import *
from cogs.events import check_logs

role1emoji = "<:Common:1126127286484205598>"
role2emoji = "<:Uncommon:1126127291089563728>"
role3emoji = "<:Rare:1126127295736840242>"
role4emoji = "<:Legendary:1126127297678807151>"
role5emoji = "<:Exotic:1126127301717917757>"
role6emoji = "<:Daredevil:1126127310148481115>"
role7emoji = "<:Prophet:1126127316544794716>"

prefixes = ["0", '1', '2', '3', '4', '5', '6', '7', '8', '9']
fixed_chance = 60
formats = ["gif", "png", "jpg", "jpeg"]

def check_currency(guild_id):
  try:
    value = get_db('guilds')[f'{guild_id}']['currency']
  except:
    return currency
  else:
    return value

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
    return "Common Role (1.1x)"
  elif current < 20000:
    return "Uncommon Role (1.2x)"
  elif current < 30000:
    return "Rare Role (1.3x)"
  elif current < 40000:
    return "Legendary Role (1.4x)"
  elif current < 50000:
    return "Exotic Role (1.5x)"
  else:
    return f"{int(to / 40)} {check_currency(guild_id)}"


def check_level(name, userid):
  milestones = get_db('users')[f'{userid}']['milestones']
  if "gamble" in name.lower():
    num = milestones['Compulsive Gambler']['amount']
    if num >= 10000:
      return {'level': 6, "next": f"{num}"}
    elif num >= 5000:
      return {'level': 5, "next": f"{num}/10000"}
    elif num >= 2500:
      return {'level': 4, "next": f"{num}/5000"}
    elif num >= 1000:
      return {'level': 3, "next": f"{num}/2500"}
    elif num >= 500:
      return {'level': 2, "next": f"{num}/1000"}
    elif num >= 100:
      return {'level': 1, "next": f"{num}/500"}
    else:
      return {'level': 0, "next": f"{num}/100"}
  if "game" in name.lower():
    num = milestones['Mini-Games Won']['amount']
    if num >= 1000:
      return {'level': 6, "next": f"{num}"}
    elif num >= 750:
      return {'level': 5, "next": f"{num}/1000"}
    elif num >= 500:
      return {'level': 4, "next": f"{num}/750"}
    elif num >= 250:
      return {'level': 3, "next": f"{num}/500"}
    elif num >= 100:
      return {'level': 2, "next": f"{num}/250"}
    elif num >= 50:
      return {'level': 1, "next": f"{num}/100"}
    else:
      return {'level': 0, "next": f"{num}/50"}

  elif "role" in name:
    num = milestones['Beta Role']['level']
    return num

  else:
    return {'level': 0, "next": "Error."}

def check_role(name):
  if "None" in name:
    return "pixel"
  elif "Common" in name:
    return "role1"
  elif "Uncommon" in name:
    return "role2"
  elif "Rare" in name:
    return "role3"
  elif "Legendary" in name:
    return "role4"
  elif "Exotic" in name:
    return "role5"
  elif "Daredevil" in name:
    return "role6"
  elif "Prophet" in name:
    return "role7"


def check_folder(name):
  bgs = get_db('misc')['shop']['backgrounds']
  for x in bgs:
    for x2 in bgs[x]["filename"]:
      if name == x2:
        return f"{x}/{x2}"
  else:
    if ("1" in name) or ("2" in name) or ("3" in name) or ("4" in name) or ("5" in name) or ("6" in name) or ("7" in name) or ("8" in name) or ("9" in name) or ("0" in name):
      return f"custom/{name}"
    else:
      return "default_background"


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

class Edit_Profile(discord.ui.View):
  def __init__(self, ctx):
    super().__init__(timeout=30)
    self.ctx = ctx

  @discord.ui.button(label="Edit Profile", style=discord.ButtonStyle.secondary, custom_id="Edit")
  async def edit(self, button, interaction):
    await self.ctx.invoke(client.get_command("inventory"))
    await interaction.message.delete()


class Confirm(discord.ui.View):
  def __init__(self, ctx, amount, user, yourvaluefinal, uservaluefinal, yourvalueint, uservalueint):
    super().__init__(timeout=30)
    self.value = 0
    self.ctx = ctx
    self.amount = amount
    self.user = user
    self.yourvaluefinal = yourvaluefinal
    self.uservaluefinal = uservaluefinal
    self.yourvalueint = yourvalueint
    self.uservalueint = uservalueint

  @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="Yes")
  async def yes(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:
      update_db('users', f"{self.user.id}", {"score": self.uservaluefinal})
      update_db('users', f"{interaction.user.id}", {"score": self.yourvaluefinal})

      finalembed = discord.Embed(description=f"```ini\n[ {check_currency(interaction.guild.id)} has been wired successfully. ]\n\n{interaction.user.name}'s {check_currency(interaction.guild.id)}: {self.yourvalueint} ≫ {self.yourvaluefinal}\n{self.user.name}'s {check_currency(interaction.guild.id)}: {self.uservalueint} ≫ {self.uservaluefinal}```", color=green)
      await interaction.message.edit(embed=finalembed, content=None, view=None)

      finalembed2 = discord.Embed(description=f"```ini\n[ {check_currency(interaction.guild.id)} has been wired successfully. ]\n\n{interaction.user.name}'s {check_currency(interaction.guild.id)}: {self.yourvalueint} ≫ {self.yourvaluefinal}\n{self.user.name}'s {check_currency(interaction.guild.id)}: {self.uservalueint} ≫ {self.uservaluefinal}\n\nYou have received {self.amount} {check_currency(interaction.guild.id)} from {interaction.user.name}.```\n[Jump to the message]({interaction.message.jump_url})", color=green)
      await self.user.send(embed=finalembed2, content=None, view=None)
    else:
      return

  @discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="No")
  async def no(self, button, interaction):
    if interaction.user.id == self.ctx.author.id:
      finalembed = discord.Embed(description=f"```ini\n[ {check_currency(interaction.guild.id)} transaction cancelled. ]\n\nPlease try again if you mentioned the wrong amount of {check_currency(interaction.guild.id)}.```", color=red)
      await interaction.message.edit(embed=finalembed, content=None, view=None)
    else:
      return

  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    else:
      await self.message.edit(view=self, content="Timed out.")

class Scores(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.lastmessage = " "

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
  @commands.is_owner()
  async def scores(self, ctx):
    try:
      active = get_db('guilds')[f'{ctx.guild.id}']['score']
    except:
      update_db('guilds', f"{ctx.guild.id}", {"score": True})
      embed = discord.Embed(description=f"Score and Xp tracking has been activated.\nUse {bot_prefix}profile to check both your xp and score.", color=green)
      await ctx.send(embed=embed)
    else:
      if not active:
        update_db('guilds', f"{ctx.guild.id}", {"score": True})
        embed = discord.Embed(description=f"Score and Xp tracking has been activated.\nUse {bot_prefix}profile to check both your xp and score.", color=green)
      else:
        update_db('guilds', f"{ctx.guild.id}", {"score": False})
        embed = discord.Embed(description=f"Score and Xp tracking has been deactivated.", color=red)

      await ctx.send(embed=embed)

  @commands.command(aliases=["transfer", "give"])
  @commands.before_invoke(disabled_check)
  async def transmit(self, ctx, user: discord.User=None, amount: int=None):
    if user == None:
      embed2 = discord.Embed(description=f"**`ERROR:`** ```python\nInvalid method.\nValid Methods: g!transmit <user> <amount>(+)```", color=red)
      await ctx.send(embed=embed2, content=None, delete_after=10)
      return
    else:
      if user.id == ctx.author.id:
        embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you can not give {check_currency(ctx.guild.id)} to yourself.```", color=red)
        await ctx.send(embed=embed2, content=None, delete_after=10)
        return
      else:
        pass
      if amount == None:
        embed2 = discord.Embed(description=f"**`ERROR:`** ```python\nInvalid method.\nValid Methods: g!transmit <user> <amount>(+)```", color=red)
        await ctx.send(embed=embed2, content=None, delete_after=10)
        return
      else:
        try:
          uservalue = get_db('users')[f'{user.id}']['score']
        except:
          uservalue = 0

        try:
          yourvalue = get_db('users')[f'{ctx.author.id}']['score']
        except:
          yourvalue = 0

        uservalueint = float(uservalue)
        yourvalueint = float(yourvalue)
        amountstr = str(amount)
        if amountstr.startswith("-"):
          embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you can not give someone negative {check_currency(ctx.guild.id)}.```", color=red)
          await ctx.send(embed=embed2, content=None, delete_after=30)
          return
        elif yourvalueint < amount:
          embed2 = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you can not give someone something you do not have.\n\nYour {check_currency(ctx.guild.id)}: {yourvalueint}\nAmount needed: {amount}```", color=red)
          await ctx.send(embed=embed2, content=None, delete_after=30)
          return
        else:
          uservaluefinal = uservalueint + amount
          yourvaluefinal = yourvalueint - amount
          buttonembed = discord.Embed(description=f"```ini\n[ Are you sure you want to wire {amount} {check_currency(ctx.guild.id)} to {user.name}? ]\n\nThe values below will proceed if confirmation is received.\n{ctx.author.name}'s {check_currency(ctx.guild.id)}: {yourvalueint} ≫ {yourvaluefinal}\n{user.name}'s {check_currency(ctx.guild.id)}: {uservalueint} ≫ {uservaluefinal}```", color=0xedbc1c)
          view = Confirm(ctx, amount, user, yourvaluefinal, uservaluefinal, yourvalueint, uservalueint)
          await ctx.send(embed=buttonembed, content=None, view=view)

  @commands.command()
  @commands.is_owner()
  async def dbadd(self, ctx, id: str, id2: str, *, value: str):
    if "/" in id2:
      embed = discord.Embed(description=f"Incorrect placements.\nExample: {bot_prefix}dbadd users/{ctx.author.id} child value(dict)")
      await ctx.send(embed=embed)
      return

    update_db(f'{id}', f"{id2}", eval(value))
    await ctx.send(f"""Database entry {id} created:\nValue: {value} """)

  @commands.command(aliases=["dbdel"])
  @commands.is_owner()
  async def dbdelete(self, ctx, id: str, id2: str):
    if "/" in id2:
      embed = discord.Embed(description=f"Incorrect placements.\nExample: {bot_prefix}dbdel users/{ctx.author.id} child(thing to delete)")
      await ctx.send(embed=embed)
      return

    del_db(f'{id}', f"{id2}")
    await ctx.send("Database key Deleted.")

  @commands.command(aliases=['dbval'])
  @commands.is_owner()
  async def dbvalue(self, ctx, id: str):
    try:
      if "/" in id:
        id2 = id.split('/')
        value = get_db(f'{id2[0]}')
        id2.pop(0)
        for x in id2:
          value = value[x]
      else:
        value = get_db(f"{id}")
    except:
      embed = discord.Embed(description=f"Database {id} doesn't exist.")
      await ctx.send(embed=embed)
    else:
      await ctx.send(value)

  #score adding on_message
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.guild != None:
      if message.author.bot:
        return
      else:
        try:
          score_tracking = get_db('guilds')[f"{message.guild.id}"]['score']
        except:
          score_tracking = False

        if score_tracking is True:
          try:
            profile = get_db('users')[f'{message.author.id}']['profile']
          except:
            profile = f"{check_name(message.author)}/"

          try:
            score = float(get_db('users')[f'{message.author.id}']['score'])
          except:
            score = 1.00

          try:
            role_multiplier = float(get_db('users')[f'{message.author.id}'][f'role-{message.guild.id}']['multiplier'])
          except:
            role_multiplier = 1.0

          try:
            booster2 = int(get_db('users')[f"{message.author.id}"]['moneybooster'])
          except:
            booster = 0
            booster2 = 0
          else:
            booster = 1

          if booster <= 0:
            booster = 0
          else:
            booster = 1

          if role_multiplier > 1.5:
            patrons = list(get_db('misc')['all_patrons'])
            if not str(message.author.id) in patrons:
              try:
                previous = get_db('users')[f'{message.author.id}']['previous_role']
              except:
                pass
              else:
                update_db(f'users', f"{message.author.id}", {f'role-{message.guild.id}': {"name": previous['name'], "multiplier": previous['multiplier']}})
                del_db(f'users/{message.author.id}', 'previous_role')


          if score <= -0.01:
            score3b = str(str(score).replace("-", ""))
            score = float(score3b)
            percent = 100
            earn1 = round((1 * (float(score) / (fixed_chance / 0.9)) * role_multiplier), 2)
            earn2 = round((2.5 * (float(score) / (fixed_chance / 0.9)) * role_multiplier), 2)
            earning = round(random.uniform(earn1, earn2), 2)
          elif score < 10:
            percent = 100
            earn1 = round((1 * (float(score) / (fixed_chance / 0.9)) * role_multiplier), 2)
            earn2 = round((2.5 * (float(score) / (fixed_chance / 0.9)) * role_multiplier), 2)

            if earn1 == earn2:
              earn2 += 0.1

            if earn1 == 0.0:
              earn1 += 0.01

            earning = round(random.uniform(earn1, earn2), 2)
          else:
            if booster >= 1:
              percent = round((fixed_chance / round((float(score) / 225), 2) * 2), 4)
            else:
              percent = round((fixed_chance / round((float(score) / 225), 2) * 1), 4)

            #EDIT THE NUMBERS AFTER ROUND() TO INCREASE AMOUNT PER MESSAGE
            earn1 = round((0.5 * (float(score) / (fixed_chance / 0.9)) * role_multiplier), 2)
            earn2 = round((1.25 * (float(score) / (fixed_chance / 0.9)) * role_multiplier), 2)
            earning = round(random.uniform(earn1, earn2), 2)


          if percent > 100:
            percent = 100

          percent2 = round(random.uniform(1.00, 100.00), 4)

          update_db('users', f"{message.author.id}", {'profile': f"{check_name(message.author)}/{percent}-{earn1}={earn2}"})

          if booster == 1:
            boost2 = int(booster2) - 1
            update_db('users', f'{message.author.id}', {'moneybooster': boost2})


          if percent >= percent2:
            finalscore = round(float(score) + earning, 2)
            update_db('users', f'{message.author.id}', {'score': finalscore})

            update_db('misc', "all_scores", {f'{message.author.id}': finalscore})

          else:
            update_db('misc', "all_scores", {f'{message.author.id}': score})

  @commands.command(aliases=[f"{currency}", "money", "wallet", "balance", "bal"])
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 20, commands.BucketType.user)
  async def score(self, ctx: commands.Context):
    try:
      money = get_db('users')[f'{ctx.author.id}']['score']
    except:
      money = 0

    try:
      rep = get_db('users')[f'{ctx.author.id}']['reputation']
    except:
      text3 = f"No rep"
      position3 = (140, 520)
    else:
      if rep <= 0:
        text3 = f"No rep"
        position3 = (140, 520)
      else:
        text3 = f"+{rep} rep"

      if int(rep) < 10:
        position3 = (140, 520)
      else:
        position3 = (130, 520)

    color = 255, 255, 255
    img_width = 1500
    img_height = 600

    asset = ctx.author.display_avatar
    data = BytesIO(await asset.read())
    pfp = Image.open(data).convert("RGBA")
    pfp = pfp.resize((410, 410))

    try:
      bought_background = get_db('users')[f'{ctx.guild.id}']['background']
    except:
      img = Image.open('images/assets/backgrounds/default_background.png')
    else:
      img = Image.open(f'images/assets/backgrounds/{check_folder(bought_background)}.png')
    img = img.resize((1500, 660))

    try:
      edited_background = get_db('users')[f'{ctx.guild.id}']['edited_background']
    except:
      pass
    else:
      if "random" in edited_background:
        img = img.convert("L")
        black = randint(0, 200), randint(0, 200), randint(0, 200)
        img = ImageOps.colorize(img, black=black, white="white")
      else:
        img = img.convert("L")
        black = (int(edited_background[0]), int(edited_background[1]), int(edited_background[2]))
        img = ImageOps.colorize(img, black=black, white="white")

    img = img.convert("RGBA")
    font = ImageFont.truetype("images/assets/que.otf", 90)

    TINT_COLOR = (0, 0, 0)
    TRANSPARENCY = .40  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)

    overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
    draw2 = ImageDraw.Draw(overlay)
    draw2.rectangle((60, 0, 480, 660), fill=TINT_COLOR+(OPACITY,))
    img = Image.alpha_composite(img, overlay)

    """overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    draw3.rounded_rectangle((30, 750, 1470, 970), fill=TINT_COLOR + (OPACITY,), radius=20)
    img = Image.alpha_composite(img, overlay)"""

    img.paste(smooth_corners(pfp, 50), (66, 86), smooth_corners(pfp, 50))

    draw = ImageDraw.Draw(img)
    draw.text((500, 130), f"Wallet:", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((550, 260), f"{round(float(money), 2)} {check_currency(ctx.guild.id)}", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text(position3, text3, color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)

    try:
      current = get_db('users')[f'{ctx.author.id}'][f'xp-{ctx.guild.id}']
    except:
      pass
    else:
      current = int(current)
      to = next_milestone(current)

      if len(str(current)) > 4:
        current2 = str(current)[:-4]
        current3 = int(str(current)[len(current2):])
      else:
        current3 = current

      try:
        xpboost = get_db('users')[f'{ctx.author.id}']['xpbooster']
      except:
        xpbooster = ""
      else:
        if xpboost >= 1:
          xpbooster = "(2x)"
        else:
          xpbooster = ""

      overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
      draw3 = ImageDraw.Draw(overlay)
      draw3.rectangle((546, 476, 1424, 584), fill=(173, 173, 173) + (int(255 * .90),), outline=(100, 100, 100), width=4)
      draw3.rectangle((550, 480, 550 + divmod(current3, 11.55)[0], 580), fill=(206, 206, 206) + (int(255 * .90),))
      img = Image.alpha_composite(img, overlay)

      draw = ImageDraw.Draw(img)
      draw.text((550, 425), f"Next Reward: {next_reward(current=current, to=to, guild_id=ctx.guild.id)} ", color, font=ImageFont.truetype("images/assets/que.otf", 50), stroke_fill=(0, 0, 0), stroke_width=3)
      _, _, w, h = draw.textbbox((0, 0), f"{current} / {to} {xpbooster}", font=ImageFont.truetype("images/assets/que.otf", 70))
      draw.text(((2000-w)/2, 500), f"{current} / {to} {xpbooster}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=2)

    img.save("images/wallet.png")
    f = discord.File(f"{os.getcwd()}/images/wallet.png", filename="wallet.png")

    #embed = discord.Embed(description=f"> **Viewing current balance • [** {ctx.author.name} **]**", color=ctx.author.color)
    #embed.set_image(url="attachment://wallet.png")

    await ctx.send(f"> **Viewing current balance • [** {ctx.author.name} **]**", file=f)

  @discord.slash_command(name="score", description="Display your score.")
  async def score_slash(self, ctx):
    if ctx.guild:
      if check_logs(ctx.guild.id)[0] is True:
        logs2 = check_logs(ctx.guild.id)[2]
        embed = discord.Embed(description=f"Slash Command used in <#{ctx.channel.id}>.", color=discord.Color.random())
        embed.add_field(name=f'Command used:', value=f"/score")
        embed.set_author(name=f"{ctx.author} • ID: {ctx.author.id}", icon_url=ctx.author.avatar)
        embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)
        await logs2.send(embed=embed, content=None)

    try:
      money = get_db('users')[f'{ctx.author.id}']['score']
    except:
      money = 0

    try:
      rep = get_db('users')[f'{ctx.author.id}']['reputation']
    except:
      text3 = f"No rep"
      position3 = (140, 520)
    else:
      text3 = f"+{rep} rep"

      if int(rep) < 10:
        position3 = (140, 520)
      else:
        position3 = (130, 520)

    color = 255, 255, 255
    img_width = 1500
    img_height = 600

    asset = ctx.author.display_avatar
    data = BytesIO(await asset.read())
    pfp = Image.open(data).convert("RGBA")
    pfp = pfp.resize((410, 410))

    try:
      bought_background = get_db('users')[f'{ctx.guild.id}']['background']
    except:
      img = Image.open('images/assets/backgrounds/default_background.png')
    else:
      img = Image.open(f'images/assets/backgrounds/{check_folder(bought_background)}.png')
    img = img.resize((1500, 660))

    try:
      edited_background = get_db('users')[f'{ctx.guild.id}']['edited_background']
    except:
      pass
    else:
      if "random" in edited_background:
        img = img.convert("L")
        black = randint(0, 200), randint(0, 200), randint(0, 200)
        img = ImageOps.colorize(img, black=black, white="white")
      else:
        img = img.convert("L")
        black = (int(edited_background[0]), int(edited_background[1]), int(edited_background[2]))
        img = ImageOps.colorize(img, black=black, white="white")

    img = img.convert("RGBA")
    font = ImageFont.truetype("images/assets/que.otf", 90)

    TINT_COLOR = (0, 0, 0)
    TRANSPARENCY = .40  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)

    overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
    draw2 = ImageDraw.Draw(overlay)
    draw2.rectangle((60, 0, 480, 660), fill=TINT_COLOR+(OPACITY,))
    img = Image.alpha_composite(img, overlay)

    """overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    draw3.rounded_rectangle((30, 750, 1470, 970), fill=TINT_COLOR + (OPACITY,), radius=20)
    img = Image.alpha_composite(img, overlay)"""

    img.paste(smooth_corners(pfp, 50), (66, 86), smooth_corners(pfp, 50))

    draw = ImageDraw.Draw(img)
    draw.text((500, 130), f"Wallet:", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((550, 260), f"{money} {check_currency(ctx.guild.id)}", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text(position3, text3, color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)

    try:
      current = get_db('users')[f'{ctx.author.id}'][f'xp-{ctx.guild.id}']
    except:
      pass
    else:
      current = int(current)
      to = next_milestone(current)

      if len(str(current)) > 4:
        current2 = str(current)[:-4]
        current3 = int(str(current)[len(current2):])
      else:
        current3 = current

      try:
        xpboost = get_db('users')[f'{ctx.author.id}']['xpbooster']
      except:
        xpbooster = ""
      else:
        if xpboost >= 1:
          xpbooster = "(2x)"
        else:
          xpbooster = ""

      overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
      draw3 = ImageDraw.Draw(overlay)
      draw3.rectangle((546, 476, 1424, 584), fill=(173, 173, 173) + (int(255 * .90),), outline=(100, 100, 100), width=4)
      draw3.rectangle((550, 480, 550 + divmod(current3, 11.55)[0], 580), fill=(206, 206, 206) + (int(255 * .90),))
      img = Image.alpha_composite(img, overlay)

      draw = ImageDraw.Draw(img)
      draw.text((550, 425), f"Next Reward: {next_reward(current=current, to=to, guild_id=ctx.guild.id)} ", color, font=ImageFont.truetype("images/assets/que.otf", 50), stroke_fill=(0, 0, 0), stroke_width=3)
      _, _, w, h = draw.textbbox((0, 0), f"{current} / {to} {xpbooster}", font=ImageFont.truetype("images/assets/que.otf", 70))
      draw.text(((2000-w)/2, 500), f"{current} / {to} {xpbooster}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=2)

    img.save("images/wallet.png")
    f = discord.File(f"{os.getcwd()}/images/wallet.png", filename="wallet.png")

    #embed = discord.Embed(description=f"> **Viewing current balance • [** {ctx.author.name} **]**", color=ctx.author.color)
    #embed.set_image(url="attachment://wallet.png")

    await ctx.respond(f"> **Viewing current balance • [** {ctx.author.name} **]**", file=f, ephemeral=True)

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def rep(self, ctx):
    await ctx.message.reply("The **rep** command has been moved to a slash command.\nPlease type **/rep** to collect your reward.", delete_after=10)
    await ctx.message.delete(delay=10)

  @commands.slash_command(name='rep', description='Give a reputation point to someone.', default_permissions=True)
  async def rep(self, ctx, *, member: Option(discord.Member, "The person you give a reputation point to.", required=True)):
    time_add = 86400

    if member.bot:
      embed = discord.Embed(description=f"**`ERROR:`** ```python\nYou can't give reputation points to a bot.```", color=red)
      await ctx.send(embed=embed, content=None)
      return

    if ctx.author.id == member.id:
      embed = discord.Embed(description=f"**`ERROR:`** ```python\nYou can't give reputation points to yourself.```", color=red)
      await ctx.send(embed=embed, content=None)
      return

    rep = 0
    try:
      rep = get_db('users')[f'{member.id}']['reputation']
    except:
      rep = 0
    finally:

      try:
        check = get_db('timers')[f'TimerRep-{ctx.author.id}']
      except:
        amount = 1

        embed = discord.Embed(description=f"**{ctx.author.mention} has given {member.mention} a reputation point!** `({int(rep)} >> {int(rep) + 1})`", color=green)

        patron_check = get_db('misc')['all_patrons']
        if str(ctx.author.id) in list(patron_check):
          pledge = int(patron_check[f"{ctx.author.id}"]["pledge"])
          if pledge == 1000:
            amount = 2
            embed = discord.Embed(description=f"**{ctx.author.mention}{role7emoji} has given {member.mention} a reputation point!** `({rep} >> {int(rep) + 2})`", color=green)

        elif str(member.id) in patron_check:
          pledge = int(patron_check[f"{member.id}"]["pledge"])
          if pledge == 1000:
            amount = 2
            embed = discord.Embed(description=f"**{ctx.author.mention} has given {member.mention}{role7emoji} a reputation point!** `({rep} >> {int(rep) + 2})`", color=green)

        elif ctx.author.id == ses:
          amount = 2
          embed = discord.Embed(description=f"**{ctx.author.mention}{role7emoji} has given {member.mention} a reputation point!** `({rep} >> {int(rep) + 2})`", color=green)

        update_db('users', f"{member.id}", {'reputation': rep + amount})

        update_db('misc', 'all_rep', {f'{member.id}': rep + amount})

        await ctx.respond(embed=embed, content=None)
        update_db("timers", f"none", {f"TimerRep-{ctx.author.id}": f"{add_time(time_add)}"})

      else:
        current = datetime.datetime.now()
        value2 = str(check)
        date_check = datetime.datetime.strptime(value2, '%Y-%m-%d %H:%M:%S.%f')
        new_time = date_check - current

        embed = discord.Embed(description=f"**`ERROR:`** ```python\nYou are unable to give out anymore reputation points at this time.\nTime left: {new_time}.\n```", color=red)
        await ctx.respond(embed=embed, content=None)

  @commands.slash_command(name="daily", description="Claim your daily reward.", default_permissions=True)
  async def daily_slash(self, ctx):
    earning = round(random.uniform(20.00, 60.00), 2)

    time_add = 86400
    time_add2 = 172800

    try:
      check = get_db('timers')[f'TimerDaily-{ctx.author.id}']
    except:
      try:
        streak = get_db('timers')[f'TimerStreak-{ctx.author.id}']
      except:
        streak = f"0/{add_time(time_add2)}"
      else:
        pass

      multiplier = int(streak.split('/')[0])

      if multiplier < 7:
        m3 = multiplier + 1
      else:
        m3 = multiplier

      final_earning = round(earning * m3, 2)

      m4 = ""
      patron_check = get_db('misc')['all_patrons']
      if str(ctx.author.id) in list(patron_check):
        pledge = int(patron_check[f"{ctx.author.id}"]["pledge"])
        if pledge == 100:
          final_earning = final_earning * 1.25
          m4 = " * 1.25"
        elif pledge == 300:
          final_earning = final_earning * 1.5
          m4 = " * 1.5"
        elif pledge == 500:
          final_earning = final_earning * 1.75
          m4 = f" * 1.75 {role6emoji}"
        elif pledge == 1000:
          final_earning = final_earning * 2
          m4 = f" * 2 {role7emoji}"
      elif ctx.author.id == ses:
        final_earning = final_earning * 2
        m4 = f" * 2 {role7emoji}"

      update_db('timers', 'none', {f"TimerStreak-{ctx.author.id}": f"{m3}/{add_time(time_add2)}"})

      if m3 == 1:
        daily = f"{role1emoji} > "
        color = 0xb3b3b3
      elif m3 == 2:
        daily = f"{role1emoji} > {role2emoji} > "
        color = 0x43b512
      elif m3 == 3:
        daily = f"{role1emoji} > {role2emoji} > {role3emoji} > "
        color = 0x005bb5
      elif m3 == 4:
        daily = f"{role1emoji} > {role2emoji} > {role3emoji} > {role4emoji} > "
        color = 0x7300bf
      elif m3 == 5:
        daily = f"{role1emoji} > {role2emoji} > {role3emoji} > {role4emoji} > {role5emoji}"
        color = 0xffdd00
      elif m3 == 6:
        daily = f"{role1emoji} > {role2emoji} > {role3emoji} > {role4emoji} > {role5emoji} > {role6emoji}"
        color = 0xf29305
      elif m3 == 7:
        daily = f"{role1emoji} > {role2emoji} > {role3emoji} > {role4emoji} > {role5emoji} > {role6emoji} > {role7emoji}"
        color = 0xcf0000
      elif m3 == 8:
        m3 -= 1
        daily = f"{role1emoji} > {role2emoji} > {role3emoji} > {role4emoji} > {role5emoji} > {role6emoji} > {role7emoji}"
        color = 0xcf0000

      embed = discord.Embed(description=f"**`Daily Reward Collected`**\n\n{final_earning} {check_currency(ctx.guild.id)} has been added to your wallet. (Base: {earning} * {round(float(m3), 2)}{m4})\n**`Streak: {m3}/7 Days`**\n{daily}", color=color)
      try:
        value = get_db('users')[f'{ctx.author.id}']['score']
      except:
        update_db('users', f'{ctx.author.id}', {"score": final_earning})
        embed.set_footer(text=f"Wallet: {final_earning}")
      else:
        final_money = round(float(value) + float(final_earning), 2)
        embed.set_footer(text=f"Wallet: {value} >> {round(final_money, 2)}")
        update_db('users', f'{ctx.author.id}', {"score": final_money})

      update_db('timers', "none", {f"TimerDaily-{ctx.author.id}": f"{add_time(time_add)}"})
      await ctx.respond(embed=embed, content=None)

    else:
      current = datetime.datetime.now()
      value2 = str(check)
      date_check = datetime.datetime.strptime(value2, '%Y-%m-%d %H:%M:%S.%f')
      new_time = date_check - current

      if "-1 day" in str(new_time):
        del_db('timers', f'TimerDaily-{ctx.author.id}')
        embed = discord.Embed(description=f"**`ERROR:`** ```python\nBad date detected, please try again.```", color=red)
      else:
        embed = discord.Embed(description=f"**`ERROR:`** ```python\nYou are unable to claim your daily reward at this time.\nTime left: {new_time}.\n```", color=red)

      await ctx.respond(embed=embed, content=None, delete_after=5)

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 20, commands.BucketType.user)
  async def daily(self, ctx):
    await ctx.message.reply("The **daily** command has been moved to a slash command.\nPlease type **/daily** to collect your reward.", delete_after=10)
    await ctx.message.delete(delay=10)

  @discord.slash_command(name="profile", description="Check your profile.")
  async def profile_slash(self, ctx):
    try:
      role = get_db('users')[f'{ctx.author.id}'][f'role-{ctx.guild.id}']
    except:
      role = {"name": "None", "multiplier": 1.0}

    try:
      profile = get_db('users')[f'{ctx.author.id}'][f'profile']
    except:
      profile = f"{ctx.author.name}/0-0=0"

    try:
      score = get_db('users')[f'{ctx.author.id}'][f'score']
    except:
      score = 0

    try:
      rep = get_db('users')[f'{ctx.author.id}'][f'reputation']
    except:
      rep = "No"
      rep2 = 0
    else:
      rep2 = int(rep)
      rep = f"+{rep}"

    color = 255, 255, 255

    asset = ctx.author.display_avatar
    data = BytesIO(await asset.read())
    pfp = Image.open(data).convert("RGBA")
    pfp = pfp.resize((250, 250))

    formatter = "png"

    try:
      bought_background = get_db('users')[f'{ctx.author.id}'][f'background']
    except:
      img = Image.open('images/assets/backgrounds/default_background.png')
    else:
      if not "custom" in check_folder(bought_background):
        img = Image.open(f'images/assets/backgrounds/{check_folder(bought_background)}.png')
      else:
        for filename in os.listdir('./images/assets/backgrounds/custom'):
          if f"{ctx.author.id}" in filename:
            formatter = filename.split(".")[1]
            img = Image.open(f'images/assets/backgrounds/custom/{filename}')

    img = img.resize((1500, 1000))

    try:
      edited_background = get_db('users')[f'{ctx.author.id}'][f'edited_background']
    except:
      pass
    else:
      if "random" in str(edited_background):
        img = img.convert("L")
        black = randint(0, 200), randint(0, 200), randint(0, 200)
        img = ImageOps.colorize(img, black=black, white="white")
      else:
        img = img.convert("L")
        black = (int(edited_background[0]), int(edited_background[1]), int(edited_background[2]))
        img = ImageOps.colorize(img, black=black, white="white")

    img = img.convert("RGBA")
    font = ImageFont.truetype("images/assets/que.otf", 70)

    role2 = role['name']
    role_emoji = Image.open(f'images/assets/roles/{check_role(role2)}.png')
    role_emoji = role_emoji.convert("RGBA")

    TINT_COLOR = (0, 0, 0)  # Black
    TRANSPARENCY = .40  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)

    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    draw3.rounded_rectangle((30, 30, 860, 400), fill=TINT_COLOR + (OPACITY,), radius=10)
    img = Image.alpha_composite(img, overlay)

    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    draw3.rounded_rectangle((30, 440, 860, 690), fill=TINT_COLOR + (OPACITY,), radius=20)
    img = Image.alpha_composite(img, overlay)

    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    draw3.rounded_rectangle((30, 750, 1470, 970), fill=TINT_COLOR + (OPACITY,), radius=20)
    img = Image.alpha_composite(img, overlay)

    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    draw3.rounded_rectangle((950, 70, 1430, 600), fill=TINT_COLOR + (OPACITY,), radius=20)
    img = Image.alpha_composite(img, overlay)

    new_size = (252, 252)
    outline = Image.new('RGBA', new_size, (30, 30, 30))
    img.paste(smooth_corners(outline, 20), (45, 45), smooth_corners(outline, 20))

    img.paste(smooth_corners(pfp, 20), (46, 46), smooth_corners(pfp, 20))
    img.paste(role_emoji, role_pos(role2), role_emoji)

    no_badge = Image.open("images/assets/badges/no_badge.png")

    badges = [(1000, 150), (1250, 150), (1000, 300), (1250, 300), (1000, 450), (1250, 450)]
    try:
      badge_placements = get_db('users')[f'{ctx.author.id}'][f'badge_slots']
    except:
      for x in badges:
        img.paste(no_badge, x, no_badge)
      pass
    else:
      del badge_placements['holder']
      for the_badge in badge_placements:
        if "role" in badge_placements[str(the_badge)]:
          num = int(str(badge_placements[str(the_badge)])[-1])
          if (num == 1) or (num == 2):
            x = badges[int(the_badge) - 1][0] - 15
            y = badges[int(the_badge) - 1][1] + 15
          else:
            x = badges[int(the_badge) - 1][0] - 15
            y = badges[int(the_badge) - 1][1]

          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png")
          img.paste(badge, (x, y), badge)

        elif ("game" in badge_placements[str(the_badge)]) or ("gambl" in badge_placements[str(the_badge)]):
          num = str(badge_placements[str(the_badge)])[-1]
          if num == 6:
            x = badges[int(the_badge) - 1][0] - 41
            y = badges[int(the_badge) - 1][1]
          elif (num == 4) or (num == 3):
            x = badges[int(the_badge) - 1][0] - 36
            y = badges[int(the_badge) - 1][1]
          else:
            x = badges[int(the_badge) - 1][0]
            y = badges[int(the_badge) - 1][1]

          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png")
          img.paste(badge, (x, y), badge)

        elif "dumbass" in badge_placements[str(the_badge)]:
          x = badges[int(the_badge) - 1][0] - 10
          y = badges[int(the_badge) - 1][1]

          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png")
          img.paste(badge, (x, y), badge)

        elif "owner" in badge_placements[str(the_badge)]:
          x = badges[int(the_badge) - 1][0] - 11
          y = badges[int(the_badge) - 1][1] + 5

          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png").convert("RGBA")
          badge = badge.resize((142, 130))
          img.paste(badge, (x, y), badge)

        elif "patreon" in badge_placements[str(the_badge)]:
          x = badges[int(the_badge) - 1][0] - 15
          y = badges[int(the_badge) - 1][1] - 10
          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png").convert("RGBA")
          badge = badge.resize((int(120*1.25), int(132*1.25)))
          img.paste(badge, (x, y), badge)

        elif ("hunter" in badge_placements[str(the_badge)]) or ("arg1" in badge_placements[str(the_badge)]):
          x = badges[int(the_badge) - 1][0] - 15
          y = badges[int(the_badge) - 1][1]
          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png")
          img.paste(badge, (x, y), badge)

        else:
          img.paste(no_badge, badges[int(the_badge) - 1], no_badge)

    if rep2 < 10:
      position4 = (75, 310)
    else:
      position4 = (65, 310)


    draw = ImageDraw.Draw(img)
    _, _, w, h = draw.textbbox((0, 0), f">> Badges <<", font=ImageFont.truetype("images/assets/que.otf", 60))
    draw.text(((2380-w)/2, 80), f">> Badges <<", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 60), stroke_fill=(0, 0, 0), stroke_width=3)
    draw.text((320, 80), f"{check_name(ctx.author)}", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((320, 210), f"{role['name']}\n({role['multiplier']}x)", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text(position4, f"{rep} rep", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((40, 540), f"Chance: {profile.split('/')[1].lstrip().split('-')[0]}%\nEarning: {round(float(profile.split('-')[1].lstrip().split('=')[0]), 1)} - {round(float(profile.split('=')[1]), 1)}", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((40, 470), f"Wallet: {score} {check_currency(ctx.guild.id)}", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)

    try:
      current = get_db('users')[f'{ctx.author.id}'][f'xp-{ctx.guild.id}']
    except:
      pass
    else:
      current = int(current)
      to = next_milestone(current)

      if len(str(current)) > 4:
        current2 = str(current)[:-4]
        current3 = int(str(current)[len(current2):])
      else:
        current3 = current

      overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
      draw3 = ImageDraw.Draw(overlay)
      draw3.rectangle((76, 836, 1424, 944), fill=(173, 173, 173) + (int(255 * .90),), outline=(100, 100, 100), width=4)
      draw3.rectangle((80, 840, 80 + divmod(current3, 7.4)[0], 940), fill=(206, 206, 206) + (int(255 * .90),))
      img = Image.alpha_composite(img, overlay)

      draw = ImageDraw.Draw(img)
      draw.text((100, 770), f"Next Reward: {next_reward(current=current, to=to, guild_id=ctx.guild.id)} ", color, font=ImageFont.truetype("images/assets/que.otf", 60), stroke_fill=(0, 0, 0), stroke_width=4)
      _, _, w, h = draw.textbbox((0, 0), f"{current} / {to}", font=ImageFont.truetype("images/assets/que.otf", 70))
      draw.text(((1500-w)/2, 860), f"{current} / {to}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=2)



    img.save(f"images/profile.{formatter}")
    f = discord.File(f"{os.getcwd()}/images/profile.{formatter}", filename=f"profile.{formatter}")

    #embed = discord.Embed(description=f"**Viewing profile card • [** {ctx.author.name} **]**", color=ctx.author.color)
    #embed.set_image(url="attachment://profile.png")

    await ctx.respond(f"> **Viewing profile card • [** {ctx.author.name} **]**", file=f, view=Edit_Profile(ctx))


  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 20, commands.BucketType.user)
  async def profile(self, ctx):
    try:
      role = get_db('users')[f'{ctx.author.id}'][f'role-{ctx.guild.id}']
    except:
      role = {"name": "None", "multiplier": 1.0}


    try:
      profile = get_db('users')[f'{ctx.author.id}'][f'profile']
    except:
      profile = f"{ctx.author.name}/0-0=0"

    try:
      score = get_db('users')[f'{ctx.author.id}'][f'score']
    except:
      score = 0

    try:
      rep = get_db('users')[f'{ctx.author.id}'][f'reputation']
    except:
      rep = "No"
      rep2 = 0
    else:
      rep2 = int(rep)
      rep = f"+{rep}"

    color = 255, 255, 255

    asset = ctx.author.display_avatar
    data = BytesIO(await asset.read())
    pfp = Image.open(data).convert("RGBA")
    pfp = pfp.resize((250, 250))

    formatter = "png"

    try:
      bought_background = get_db('users')[f'{ctx.author.id}'][f'background']
    except:
      img = Image.open('images/assets/backgrounds/default_background.png')
    else:
      if not "custom" in check_folder(bought_background):
        img = Image.open(f'images/assets/backgrounds/{check_folder(bought_background)}.png')
      else:
        for filename in os.listdir('./images/assets/backgrounds/custom'):
          if f"{ctx.author.id}" in filename:
            formatter = filename.split(".")[1]
            img = Image.open(f'images/assets/backgrounds/custom/{filename}')

    img = img.resize((1500, 1000))

    try:
      edited_background = get_db('users')[f'{ctx.author.id}'][f'edited_background']
    except:
      pass
    else:
      if "random" in str(edited_background):
        img = img.convert("L")
        black = randint(0, 200), randint(0, 200), randint(0, 200)
        img = ImageOps.colorize(img, black=black, white="white")
      else:
        img = img.convert("L")
        black = (int(edited_background[0]), int(edited_background[1]), int(edited_background[2]))
        img = ImageOps.colorize(img, black=black, white="white")

    img = img.convert("RGBA")
    font = ImageFont.truetype("images/assets/que.otf", 70)

    role2 = role['name']
    role_emoji = Image.open(f'images/assets/roles/{check_role(role2)}.png')
    role_emoji = role_emoji.convert("RGBA")

    TINT_COLOR = (0, 0, 0)  # Black
    TRANSPARENCY = .40  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)

    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    draw3.rounded_rectangle((30, 30, 860, 400), fill=TINT_COLOR + (OPACITY,), radius=10)
    img = Image.alpha_composite(img, overlay)

    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    draw3.rounded_rectangle((30, 440, 860, 690), fill=TINT_COLOR + (OPACITY,), radius=20)
    img = Image.alpha_composite(img, overlay)

    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    draw3.rounded_rectangle((30, 750, 1470, 970), fill=TINT_COLOR + (OPACITY,), radius=20)
    img = Image.alpha_composite(img, overlay)

    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    draw3.rounded_rectangle((950, 70, 1430, 600), fill=TINT_COLOR + (OPACITY,), radius=20)
    img = Image.alpha_composite(img, overlay)

    new_size = (252, 252)
    outline = Image.new('RGBA', new_size, (30, 30, 30))
    img.paste(smooth_corners(outline, 20), (45, 45), smooth_corners(outline, 20))

    img.paste(smooth_corners(pfp, 20), (46, 46), smooth_corners(pfp, 20))
    img.paste(role_emoji, role_pos(role2), role_emoji)

    no_badge = Image.open("images/assets/badges/no_badge.png")

    badges = [(1000, 150), (1250, 150), (1000, 300), (1250, 300), (1000, 450), (1250, 450)]
    try:
      badge_placements = get_db('users')[f'{ctx.author.id}'][f'badge_slots']
    except:
      for x in badges:
        img.paste(no_badge, x, no_badge)
      pass
    else:
      del badge_placements['holder']
      for the_badge in badge_placements:
        if "role" in badge_placements[str(the_badge)]:
          num = int(str(badge_placements[str(the_badge)])[-1])
          if (num == 1) or (num == 2):
            x = badges[int(the_badge) - 1][0] - 15
            y = badges[int(the_badge) - 1][1] + 15
          else:
            x = badges[int(the_badge) - 1][0] - 15
            y = badges[int(the_badge) - 1][1]

          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png")
          img.paste(badge, (x, y), badge)

        elif ("game" in badge_placements[str(the_badge)]) or ("gambl" in badge_placements[str(the_badge)]):
          num = str(badge_placements[str(the_badge)])[-1]
          if num == 6:
            x = badges[int(the_badge) - 1][0] - 41
            y = badges[int(the_badge) - 1][1]
          elif (num == 4) or (num == 3):
            x = badges[int(the_badge) - 1][0] - 36
            y = badges[int(the_badge) - 1][1]
          else:
            x = badges[int(the_badge) - 1][0]
            y = badges[int(the_badge) - 1][1]

          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png")
          img.paste(badge, (x, y), badge)

        elif "dumbass" in badge_placements[str(the_badge)]:
          x = badges[int(the_badge) - 1][0] - 10
          y = badges[int(the_badge) - 1][1]

          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png")
          img.paste(badge, (x, y), badge)

        elif "owner" in badge_placements[str(the_badge)]:
          x = badges[int(the_badge) - 1][0] - 11
          y = badges[int(the_badge) - 1][1] + 5

          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png").convert("RGBA")
          badge = badge.resize((142, 130))
          img.paste(badge, (x, y), badge)

        elif "patreon" in badge_placements[str(the_badge)]:
          x = badges[int(the_badge) - 1][0] - 15
          y = badges[int(the_badge) - 1][1] - 10
          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png").convert("RGBA")
          badge = badge.resize((int(120 * 1.25), int(132 * 1.25)))
          img.paste(badge, (x, y), badge)

        elif ("hunter" in badge_placements[str(the_badge)]) or ("arg1" in badge_placements[str(the_badge)]):
          x = badges[int(the_badge) - 1][0] - 15
          y = badges[int(the_badge) - 1][1]
          badge = Image.open(f"images/assets/badges/{badge_placements[str(the_badge)]}.png")
          img.paste(badge, (x, y), badge)


        else:
          img.paste(no_badge, badges[int(the_badge) - 1], no_badge)

    if rep2 < 10:
      position4 = (75, 310)
    else:
      position4 = (65, 310)

    draw = ImageDraw.Draw(img)
    _, _, w, h = draw.textbbox((0, 0), f">> Badges <<", font=ImageFont.truetype("images/assets/que.otf", 60))
    draw.text(((2380 - w) / 2, 80), f">> Badges <<", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 60), stroke_fill=(0, 0, 0), stroke_width=3)
    draw.text((320, 80), f"{check_name(ctx.author)}", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((320, 210), f"{role['name']}\n({role['multiplier']}x)", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text(position4, f"{rep} rep", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((40, 540), f"Chance: {profile.split('/')[1].lstrip().split('-')[0]}%\nEarning: {round(float(profile.split('-')[1].lstrip().split('=')[0]), 1)} - {round(float(profile.split('=')[1]), 1)}", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((40, 470), f"Wallet: {score} {check_currency(ctx.guild.id)}", color, font=font, stroke_fill=(0, 0, 0), stroke_width=4)

    try:
      current = int(get_db('users')[f'{ctx.author.id}'][f'xp-{ctx.guild.id}'])
    except:
      current = 0
    else:
      to = next_milestone(current)

      if len(str(current)) > 4:
        current2 = str(current)[:-4]
        current3 = int(str(current)[len(current2):])
      else:
        current3 = current

      overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
      draw3 = ImageDraw.Draw(overlay)
      draw3.rectangle((76, 836, 1424, 944), fill=(173, 173, 173) + (int(255 * .90),), outline=(100, 100, 100), width=4)
      draw3.rectangle((80, 840, 80 + divmod(current3, 7.4)[0], 940), fill=(206, 206, 206) + (int(255 * .90),))
      img = Image.alpha_composite(img, overlay)

      draw = ImageDraw.Draw(img)
      draw.text((100, 770), f"Next Reward: {next_reward(current=current, to=to, guild_id=ctx.guild.id)} ", color, font=ImageFont.truetype("images/assets/que.otf", 60), stroke_fill=(0, 0, 0), stroke_width=4)
      _, _, w, h = draw.textbbox((0, 0), f"{current} / {to}", font=ImageFont.truetype("images/assets/que.otf", 70))
      draw.text(((1500 - w) / 2, 860), f"{current} / {to}", (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 70), stroke_fill=(0, 0, 0), stroke_width=2)

    img.save(f"images/profile.{formatter}")
    f = discord.File(f"{os.getcwd()}/images/profile.{formatter}", filename=f"profile.{formatter}")

    # embed = discord.Embed(description=f"**Viewing profile card • [** {ctx.author.name} **]**", color=ctx.author.color)
    # embed.set_image(url="attachment://profile.png")

    await ctx.send(f"> **Viewing profile card • [** {ctx.author.name} **]**", file=f, view=Edit_Profile(ctx))

def setup(client):
  client.add_cog(Scores(client))
