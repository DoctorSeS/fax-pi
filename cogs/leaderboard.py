from discord.ext import commands, tasks
import discord
from main import client, bot_prefix, round_time, ses, currency, check_name, red, green
import time
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageEnhance
import os
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


class Rep_and_Score(discord.ui.View):
  def __init__(self, ctx):
    super().__init__(timeout=None)
    self.ctx = ctx

  @discord.ui.button(label="Rep Leaderboard", style=discord.ButtonStyle.secondary, custom_id="rep")
  async def rep(self, button, interaction):
    await self.ctx.invoke(client.get_command("leaderboard"), the_db="All_Rep")
    await interaction.message.delete()

  @discord.ui.button(label=f"{currency} Leaderboard", style=discord.ButtonStyle.secondary, custom_id="score")
  async def score(self, button, interaction):
    await self.ctx.invoke(client.get_command("leaderboard"), the_db=None)
    await interaction.message.delete()

    
class Xp_and_Score(discord.ui.View):
  def __init__(self, ctx):
    super().__init__(timeout=None)
    self.ctx = ctx

  @discord.ui.button(label=f"{currency} Leaderboard", style=discord.ButtonStyle.secondary, custom_id="score")
  async def score(self, button, interaction):
    await self.ctx.invoke(client.get_command("leaderboard"), the_db=None)
    await interaction.message.delete()

  @discord.ui.button(label="Xp Leaderboard", style=discord.ButtonStyle.secondary, custom_id="xp")
  async def xp(self, button, interaction):
    try:
      xp = get_db('guilds')[f'{interaction.guild.id}']['xp']
    except:
      self.button.disabled = True
      await interaction.message.edit(view=self)
    else:
      await self.ctx.invoke(client.get_command("leaderboard"), the_db="GuildXp")
      await interaction.message.delete()


class Rep_and_Xp(discord.ui.View):
  def __init__(self, ctx):
    super().__init__(timeout=None)
    self.ctx = ctx

  @discord.ui.button(label="Rep Leaderboard", style=discord.ButtonStyle.secondary, custom_id="rep")
  async def rep(self, button, interaction):
    await self.ctx.invoke(client.get_command("leaderboard"), the_db="All_Rep")
    await interaction.message.delete()

  @discord.ui.button(label="Xp Leaderboard", style=discord.ButtonStyle.secondary, custom_id="xp")
  async def xp(self, button, interaction):
    try:
      xp = get_db('guilds')[f'{interaction.guild.id}']['xp']
    except:
      self.button.disabled = True
      await interaction.message.edit(view=self)
    else:
      await self.ctx.invoke(client.get_command("leaderboard"), the_db="GuildXp")
      await interaction.message.delete()


class Leaderboard(commands.Cog):
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
  
  @commands.command(aliases=["lb", "scorelb", "scoreleaderboard", "top"])
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 60, commands.BucketType.guild)
  async def leaderboard(self, ctx, the_db=None):
    if the_db is None:
      scores = get_db('misc')['all_scores']
      title = f"Global {currency} Leaderboard"
      view = Rep_and_Xp(ctx)
      
    elif the_db == "All_Rep":
      scores = get_db('misc')['all_rep']
      title = f"Global Rep Leaderboard"
      view = Xp_and_Score(ctx)
      
    elif the_db == "GuildXp":
      scores = get_db('guilds')[f'{ctx.guild.id}']['xp']
      title = f"Server Xp Leaderboard"
      view = Rep_and_Score(ctx)
      
    else:
      scores = get_db('misc')['all_scores']
      title = f"Global {currency} Leaderboard"
      view = Rep_and_Xp(ctx)
      
    scores2 = {val[0] : val[1] for val in sorted(scores.items(), key = lambda x: (-x[1], x[0]))}

    img = Image.open('images/assets/leaderboard.png').convert("RGBA")
    font = ImageFont.truetype("images/assets/que.otf", 60)
    
    TINT_COLOR = (0, 0, 0)  # Black
    TRANSPARENCY = .40  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)
    
    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    x1 = 50
    y1 = 150
    x2 = 1450
    y2 = 220
    #slots
    draw3.rounded_rectangle((250, 20, 1250, 130), fill=TINT_COLOR + (int(255 * 0.70),), radius=10)
    draw3.rounded_rectangle((x1, y1, x2, y2), fill=TINT_COLOR + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80, x2, y2+80), fill=TINT_COLOR + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*2, x2, y2+80*2), fill=TINT_COLOR + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*3, x2, y2+80*3), fill=TINT_COLOR + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*4, x2, y2+80*4), fill=TINT_COLOR + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*5, x2, y2+80*5), fill=TINT_COLOR + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*6, x2, y2+80*6), fill=TINT_COLOR + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*7, x2, y2+80*7), fill=TINT_COLOR + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*8, x2, y2+80*8), fill=TINT_COLOR + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*9, x2, y2+80*9), fill=TINT_COLOR + (OPACITY,), radius=10)
    img = Image.alpha_composite(img, overlay)
    
    #colors
    x2 = 100
    TINT_COLOR2 = (255, 255, 255)
    overlay = Image.new('RGBA', img.size, TINT_COLOR + (0,))
    draw3 = ImageDraw.Draw(overlay)
    draw3.rounded_rectangle((x1, y1, x2, y2), fill=(255, 179, 0) + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80, x2, y2+80), fill=(212, 212, 212) + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*2, x2, y2+80*2), fill=(133, 65, 13) + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*3, x2, y2+80*3), fill=TINT_COLOR2 + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*4, x2, y2+80*4), fill=TINT_COLOR2 + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*5, x2, y2+80*5), fill=TINT_COLOR2 + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*6, x2, y2+80*6), fill=TINT_COLOR2 + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*7, x2, y2+80*7), fill=TINT_COLOR2 + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*8, x2, y2+80*8), fill=TINT_COLOR2 + (OPACITY,), radius=10)
    draw3.rounded_rectangle((x1, y1+80*9, x2, y2+80*9), fill=TINT_COLOR2 + (OPACITY,), radius=10)
    img = Image.alpha_composite(img, overlay)
    
    img = ImageEnhance.Brightness(img).enhance(1.5)
    
    draw = ImageDraw.Draw(img)
    draw.text((x1+60, 160), f"#1", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((x1+60, 160+80), f"#2", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((x1+60, 160+80*2), f"#3", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((x1+60, 160+80*3), f"#4", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((x1+60, 160+80*4), f"#5", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((x1+60, 160+80*5), f"#6", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((x1+60, 160+80*6), f"#7", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((x1+60, 160+80*7), f"#8", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((x1+60, 160+80*8), f"#9", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    draw.text((x1+60, 160+80*9), f"#10", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
    
    add_x = 180
    this_y = 160
    second_x = 1300
    num = 0
    for new_s, new_val in scores2.items():
      if num == 0:
        _, _, w, h = draw.textbbox((0, 0), f"{scores2[new_s]}", font=font)
        draw.text(((2500 - w) / 2, this_y), f"{scores2[new_s]}", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=2)
    
        user_name = check_name(client.get_user(int(new_s)))
        draw.text((x1+add_x, this_y), f"{user_name}", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
        num += 1
        continue
        
      if num == 10:
        break
      else:
        #score
        _, _, w, h = draw.textbbox((0, 0), f"{scores2[new_s]}", font=font)
        draw.text(((2500 - w) / 2, this_y+80*num), f"{scores2[new_s]}", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=2)
        
        #name
        user_name = check_name(client.get_user(int(new_s)))
        draw.text((x1+add_x, this_y+80*num), f"{user_name}", (255, 255, 255), font=font, stroke_fill=(0, 0, 0), stroke_width=4)
        num += 1
    
    _, _, w, h = draw.textbbox((0, 0), title, font=ImageFont.truetype("images/assets/que.otf", 80))
    draw.text(((1500-w)/2, 40), title, (255, 255, 255), font=ImageFont.truetype("images/assets/que.otf", 80), stroke_fill=(0, 0, 0), stroke_width=2)
    

    img.save("images/leaderboard_used.png")
    f = discord.File(f"{os.getcwd()}/images/leaderboard_used.png", filename="leaderboard_used.png")
    
    #embed = discord.Embed(color=discord.Color.dark_theme())
    #embed.set_image(url="attachment://leaderboard_used.png")
    
    await ctx.send(file=f, view=view)


def setup(client):
  client.add_cog(Leaderboard(client))