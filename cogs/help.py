import discord
from discord.ext import commands, tasks
import random
from random import randint
import asyncio
from main import client, bot_prefix, currentDT, round_time, ses, faxname, faxpfp, currency, red, green
import requests
from database import *
from discord.commands import slash_command

def check_logs(guild):
  try:
    value = get_db('guilds')[f"{guild}"]['logs']
  except:
    return False
  else:
    logs = [False, "None", "None"]

    try:
      logs[0] = get_db('guilds')[f"{guild}"]['logs']['active']
    except:
      pass

    try:
      logs[1] = get_db('guilds')[f"{guild}"]['logs']['logs1']
    except:
      pass

    try:
      logs[2] = get_db('guilds')[f"{guild}"]['logs']['logs2']
    except:
      pass

    return logs

ses2 = client.get_user(ses)

### embed1 ###
footer = f"Cooldowns are listed as the number after the command, in seconds."

embed1 = discord.Embed(title=f"Help with {faxname}", description="`Commands Available:`\n **`Fun`**", color=discord.Color.green())
embed1.add_field(name=f"{bot_prefix}battleship `60`", value="Minigame based on the real battleship board game.")
embed1.add_field(name=f"{bot_prefix}ask `10`", value="Ask any question.")
embed1.add_field(name=f"{bot_prefix}gayrate `10`", value="Randomly chosen.")
embed1.add_field(name=f"{bot_prefix}sexyrate `10`", value="Randomly chosen.")
embed1.add_field(name=f"{bot_prefix}hilo `30`", value=f'Ex: {bot_prefix}hilo 10 20 (10 max number, 20 bet)')
embed1.add_field(name=f"{bot_prefix}rps `30`", value=f"Ex: {bot_prefix}rps @person 100 (arguments are optional.)")
embed1.add_field(name=f"{bot_prefix}talk `30`", value="Makes the bot say something random. Can be followed by a topic. One word only.")
embed1.add_field(name=f"{bot_prefix}rr `120`", value=f"Creates a room for anyone to join, and play Russian Roulette for {currency}.")
embed1.set_footer(text=footer + "\nPage 1/5")
embed1.set_thumbnail(url=faxpfp)

### embed2 ###
embed2 = discord.Embed(title=f"Help with {faxname}", description="`Commands Available:`\n **`Utility`**", color=discord.Color.green())
embed2.add_field(name=f"{bot_prefix}userinfo `15`", value="Mention someone.")
embed2.add_field(name=f"{bot_prefix}roleinfo `15`", value="Mention someone.")
embed2.add_field(name=f"{bot_prefix}av `10`", value="Shows you anyone's avatar.")
embed2.add_field(name=f"{bot_prefix}e `10`", value="Show you any emoji of your choosing. Must be from a server the bot is in.")
embed2.add_field(name=f"{bot_prefix}s `10`", value="Show you any sticker of your choosing. Must be from a server the bot is in.")
embed2.add_field(name=f"{bot_prefix}snipe `5`", value=f"Snipe the earliest deleted message from the server.")
embed2.add_field(name=f"{bot_prefix}profile `20`", value='Displays your profile.')
embed2.set_footer(text=footer + "\nPage 2/5")
embed2.set_thumbnail(url=faxpfp)

### embed3 ###
embed3 = discord.Embed(title=f"Help with {faxname}", description="`Commands Available:`\n **`Utility #2`**", color=discord.Color.green())
embed3.add_field(name=f"{bot_prefix}afk `60`", value="Marks you as AFK. The next message sent will remove this.")
embed3.add_field(name=f"{bot_prefix}rep `30`", value="Award anyone with a reputation point.")
embed3.set_footer(text=footer + "\nPage 3/5")
embed3.set_thumbnail(url=faxpfp)

### embed4 ###
embed4 = discord.Embed(title=f"Help with {faxname}", description="`Commands Available:`\n **`Score-Based`**", color=discord.Color.green())
embed4.add_field(name=f"{bot_prefix}score `20`", value='Displays your score.')
embed4.add_field(name=f"{bot_prefix}leaderboard `30`", value='Displays the top 10 scores on both sides.')
embed4.add_field(name=f"{bot_prefix}transmit `None`", value=f"Give someone an amount of {currency} you can afford.")
embed4.add_field(name=f"{bot_prefix}daily `20`", value=f'Gain a random amount of {currency} instantly, every 24 hours.')
embed4.add_field(name=f"{bot_prefix}inventory `30`", value='Check/Use the items that you have in your inventory.')
embed4.add_field(name=f"{bot_prefix}shop `60`", value='A store to buy items.')
embed4.add_field(name=f"{bot_prefix}ttt `30`", value=f'Tic Tac Toe, can bet {currency}.')
embed4.add_field(name=f"{bot_prefix}slots `60`", value=f'A slots machine, must bet {currency}.')
embed4.set_footer(text=footer + "\nPage 4/5")
embed4.set_thumbnail(url=faxpfp)

### embed5 ###
embed5 = discord.Embed(title=f"Help with {faxname}", description="`Commands Available:`\n **`Other`**", color=discord.Color.green())
embed5.add_field(name=f"{bot_prefix}ses `None`", value="The bot's owner.")
embed5.add_field(name=f"{bot_prefix}cats `30`", value="Cats.")
embed5.add_field(name=f"{bot_prefix}monkey `30`", value="Monkeys.")
embed5.add_field(name=f"{bot_prefix}suggest `120`", value="Suggest an idea for the bot.")
embed5.add_field(name=f"{bot_prefix}random `10`", value=f"Roll between 2 numbers. Invoke with no argument to roll 1-6.")
embed5.set_footer(text=footer + "\nPage 5/5")
embed5.set_thumbnail(url=faxpfp)

### mod1 ###
footer3 = """The Permissions required to invoke the command are listed after the command itself, just as the cooldowns on the member tab.\nAll commands can be disabled."""

mod1 = discord.Embed(title=f"Help with {faxname}", description="`Moderator Commands:`\n **`Member-Based`**", color=discord.Color.dark_green())
mod1.add_field(name=f"{bot_prefix}ban/{bot_prefix}unban\n`Ban Members`", value="Ban/Unban someone.")
mod1.add_field(name=f"{bot_prefix}kick\n`Kick Members`", value="Kick someone.")
mod1.add_field(name=f"{bot_prefix}members\n`Manage Messages`", value="Member count.")
mod1.set_footer(text=footer3 + "\nPage 1/3")

### mod2 ###
mod2 = discord.Embed(title=f"Help with {faxname}", description="`Moderator Commands:`\n **`Member-Based #2`**", color=discord.Color.dark_green())
mod2.add_field(name=f"{bot_prefix}addtime\n`Manage Roles`", value="Add/Shorten a mute or lockdown timer.")
mod2.add_field(name=f"{bot_prefix}warn/{bot_prefix}unwarn\n`Manage Roles`", value="Warn/Unwarn any member, with a reason.")
mod2.set_footer(text=footer3 + "\nPage 2/3")

### mod3 ###
mod3 = discord.Embed(title=f"Help with {faxname}", description="`Moderator Commands:`\n **`Server Management`**", color=discord.Color.dark_green())
mod3.add_field(name=f"{bot_prefix}purge\n`Manage Messages`", value='Ex: g!purge 10 / g!purge 10 @member')
mod3.add_field(name=f"{bot_prefix}lock/unlock\n`Manage Roles`", value="Lock/unlock any channel of your choosing.")
mod3.add_field(name=f"{bot_prefix}invites\n`Manage Roles`", value="Request all invites from the guild.")
mod3.add_field(name=f"{bot_prefix}config\n`Manage Roles`", value="A command that has every configuration option.")
mod3.set_footer(text=footer3 + "\nPage 3/3")

### mod4 ###
mod4 = discord.Embed(title=f"Help with {faxname}", description="`Moderator Commands:`\n **`Configuration #1`**", color=discord.Color.dark_green())
mod4.set_footer(text=footer3 + "\nPage 4/5")

### mod5 ###
mod5 = discord.Embed(title=f"Help with {faxname}", description="`Moderator Commands:`\n **`Configuration #2`**", color=discord.Color.dark_green())
mod5.set_footer(text=footer3 + "\nPage 5/5") 
    
class Pages(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=300)
    self.value = 1
  
  def sescheck(self):
    global ses2
    ses2 = client.get_user(ses)     
    return ses2
  
  def setauthor(self):
    Pages.sescheck()
    #set author#
    embed1.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    embed2.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    embed3.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    embed4.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    embed5.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    
    mod1.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    mod2.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    mod3.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    mod4.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    mod5.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    #######

  @discord.ui.button(label="<", style=discord.ButtonStyle.green, custom_id="Previous Page", disabled=False)
  async def pagedown(self, button, interaction):
    ### set pfp ##
    mod1.set_thumbnail(url=interaction.user.avatar)
    mod2.set_thumbnail(url=interaction.user.avatar)
    mod3.set_thumbnail(url=interaction.user.avatar)
    mod4.set_thumbnail(url=interaction.user.avatar)
    mod5.set_thumbnail(url=interaction.user.avatar)
    ###
    self.value -= 1
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()
      embedstr = str(embeddict)

    if self.value < 1:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        self.value = 5
        await interaction.message.edit(content=None, embed=embed5, view=self)
        await interaction.response.defer()
        return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        self.value = 3
        await interaction.message.edit(content=None, embed=mod3, view=self)
        await interaction.response.defer()
        return
    elif self.value > 5:
      self.value -= 1
      pass
    else:
      pass

    if self.value == 1:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.message.edit(content=None, embed=embed1, view=self)
        await interaction.response.defer()
        return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        button.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.defer()
        return
    if self.value == 2:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.message.edit(content=None, embed=embed2, view=self)
        await interaction.response.defer()
        return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        await interaction.message.edit(content=None, embed=mod2, view=self)
        await interaction.response.defer()
        return
    if self.value == 3:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.message.edit(content=None, embed=embed3, view=self)
        await interaction.response.defer()
        return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        await interaction.message.edit(content=None, embed=mod3, view=self)
        await interaction.response.defer()
        return
    if self.value == 4:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.message.edit(content=None, embed=embed4, view=self)
        await interaction.response.defer()
        return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        await interaction.message.edit(content=None, embed=mod4, view=self)
        await interaction.response.defer()
        return
  
  @discord.ui.button(label=f"Moderator Commands", style=discord.ButtonStyle.grey, custom_id="Other Commands", disabled=False)
  async def mod(self, button, interaction):
    ### set pfp ##
    mod1.set_thumbnail(url=interaction.user.avatar)
    mod2.set_thumbnail(url=interaction.user.avatar)
    mod3.set_thumbnail(url=interaction.user.avatar)
    mod4.set_thumbnail(url=interaction.user.avatar)
    mod5.set_thumbnail(url=interaction.user.avatar)
    ###
    global perms
    matches = db.prefix(f"help-{interaction.user.id}")
    if "help-" in str(matches):
      perms = True
      pass
    else:
      perms = False
      button.disabled = True
      self.value = 1
      button.label = f"Unavailable"
      await interaction.message.edit(content=None, embed=embed1, view=self)
      await interaction.response.defer()
      return
    #wait
    if perms == True:
      button.disabled = False
      if button.label == "Member Commands":
        button.label = f"Moderator Commands"
        self.value = 1
        await interaction.message.edit(content=None, embed=embed1, view=self)
        await interaction.response.defer()
        return
      elif button.label == "Moderator Commands":
        button.label = f"Member Commands"
        self.value = 1
        await interaction.message.edit(content=None, embed=mod1, view=self)
        await interaction.response.defer()
        return
    else:
      button.disabled = True
      button.label = f"Unavailable"
      self.value = 1
      await interaction.message.edit(content=None, embed=embed1, view=self)
      await interaction.response.defer()
      return

  @discord.ui.button(label=">", style=discord.ButtonStyle.green, custom_id="Next Page")
  async def pageup(self, button, interaction):
    ### set pfp ##
    mod1.set_thumbnail(url=interaction.user.avatar)
    mod2.set_thumbnail(url=interaction.user.avatar)
    mod3.set_thumbnail(url=interaction.user.avatar)
    mod4.set_thumbnail(url=interaction.user.avatar)
    mod5.set_thumbnail(url=interaction.user.avatar)
    ###
    self.value += 1
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()
      embedstr = str(embeddict)

    if self.value < 1:
      self.value += 1
      pass
    elif self.value > 3:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        if self.value > 5:
          self.value = 1
          await interaction.message.edit(content=None, embed=embed1, view=self)
          await interaction.response.defer()
          return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        self.value = 1
        await interaction.message.edit(content=None, embed=mod1, view=self)
        await interaction.response.defer()
        return
    else:
      pass
   
    if self.value == 5:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.message.edit(content=None, embed=embed5, view=self)
        await interaction.response.defer()
        return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        button.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.defer()
        return
    if self.value == 3:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.message.edit(content=None, embed=embed3, view=self)
        await interaction.response.defer()
        return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        await interaction.message.edit(content=None, embed=mod3, view=self)
        await interaction.response.defer()
        return
    if self.value == 4:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.message.edit(content=None, embed=embed4, view=self)
        await interaction.response.defer()
        return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        button.disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.defer()
        return
    if self.value == 2:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.message.edit(content=None, embed=embed2, view=self)
        await interaction.response.defer()
        return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        await interaction.message.edit(content=None, embed=mod2, view=self)
        await interaction.response.defer()
        return 
  
  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    else:
      await self.message.edit(view=self, content="Timed out.")

class Pages_slash(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=300)
    self.value = 1
  
  def sescheck(self):
    global ses2
    ses2 = client.get_user(ses)     
    return ses2
  
  def setauthor(self):
    Pages.sescheck()
    #set author#
    embed1.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    embed2.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    embed3.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    embed4.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    
    mod1.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    mod2.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    mod3.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    mod4.set_author(name=f"Consider supporting this project on patreon", icon_url=f"{ses2.avatar}", url="https://www.patreon.com/doctorses")
    #######

  @discord.ui.button(label="<", style=discord.ButtonStyle.green, custom_id="Previous Page", disabled=False)
  async def pagedown(self, button, interaction):
    ### set pfp ##
    mod1.set_thumbnail(url=interaction.user.avatar)
    mod2.set_thumbnail(url=interaction.user.avatar)
    mod3.set_thumbnail(url=interaction.user.avatar)
    mod4.set_thumbnail(url=interaction.user.avatar)
    ###
    self.value -= 1
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()
      embedstr = str(embeddict)

    if self.value < 1:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        self.value = 5
        await interaction.message.edit(content=None, embed=embed5, view=self)
        await interaction.response.defer()
        return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        self.value = 3
        await interaction.message.edit(content=None, embed=mod3, view=self)
        await interaction.response.defer()
        return
    elif self.value > 5:
      self.value -= 1
      pass
    else:
      pass

    if self.value == 1:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.response.edit_message(content=None, embed=embed1, view=self)
      elif embedstr.startswith("{'footer': {'text': 'The"):
        await interaction.response.edit_message(content=None, embed=mod1, view=self)
        return
    elif self.value == 2:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.response.edit_message(content=None, embed=embed2, view=self)
      elif embedstr.startswith("{'footer': {'text': 'The"):
        await interaction.response.edit_message(content=None, embed=mod2, view=self)
        await interaction.response.defer()
        return
    elif self.value == 3:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.response.edit_message(content=None, embed=embed3, view=self)
      elif embedstr.startswith("{'footer': {'text': 'The"):
        await interaction.response.edit_message(content=None, embed=mod3, view=self)
  
  @discord.ui.button(label=f"Moderator Commands", style=discord.ButtonStyle.grey, custom_id="Other Commands", disabled=False)
  async def mod(self, button, interaction):
    ### set pfp ##
    mod1.set_thumbnail(url=interaction.user.avatar)
    mod2.set_thumbnail(url=interaction.user.avatar)
    mod3.set_thumbnail(url=interaction.user.avatar)
    mod4.set_thumbnail(url=interaction.user.avatar)
    ###
    global perms
    matches = db.prefix(f"help-{interaction.user.id}")
    if "help-" in str(matches):
      perms = True
      pass
    else:
      perms = False
      button.disabled = True
      self.value = 1
      button.label = f"Unavailable"
      await interaction.response.edit_message(content=None, embed=embed1, view=self)
    #wait
    if perms == True:
      button.disabled = False
      if button.label == "Member Commands":
        button.label = f"Moderator Commands"
        self.value = 1
        await interaction.response.edit_message(content=None, embed=embed1, view=self)
      elif button.label == "Moderator Commands":
        button.label = f"Member Commands"
        self.value = 1
        await interaction.response.edit_message(content=None, embed=mod1, view=self)
    else:
      button.disabled = True
      button.label = f"Unavailable"
      self.value = 1
      await interaction.response.edit_message(content=None, embed=embed1, view=self)

  @discord.ui.button(label=">", style=discord.ButtonStyle.green, custom_id="Next Page")
  async def pageup(self, button, interaction):
    ### set pfp ##
    mod1.set_thumbnail(url=interaction.user.avatar)
    mod2.set_thumbnail(url=interaction.user.avatar)
    mod3.set_thumbnail(url=interaction.user.avatar)
    mod4.set_thumbnail(url=interaction.user.avatar)
    ###
    self.value += 1
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()
      embedstr = str(embeddict)

    if self.value < 1:
      self.value += 1
      pass
    elif self.value > 3:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        if self.value > 5:
          self.value = 1
          await interaction.message.edit(content=None, embed=embed1, view=self)
          await interaction.response.defer()
          return
      elif embedstr.startswith("{'footer': {'text': 'The"):
        self.value = 1
        await interaction.message.edit(content=None, embed=mod1, view=self)
        await interaction.response.defer()
        return
    else:
      pass

    if self.value == 3:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.response.edit_message(content=None, embed=embed3, view=self)
      elif embedstr.startswith("{'footer': {'text': 'The"):
        await interaction.response.edit_message(content=None, embed=mod3, view=self)
    elif self.value == 4:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.response.edit_message(content=None, embed=embed4, view=self)
      elif embedstr.startswith("{'footer': {'text': 'The"):
        await interaction.response.edit_message(content=None, embed=mod4, view=self)
    elif self.value == 2:
      if embedstr.startswith("{'footer': {'text': 'Cooldowns"):
        await interaction.response.edit_message(content=None, embed=embed2, view=self)
      elif embedstr.startswith("{'footer': {'text': 'The"):
        await interaction.response.edit_message(content=None, embed=mod2, view=self)
  
  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    else:
      await self.message.edit(view=self, content="Timed out.")

class Help(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['cmds', 'commands'])
  async def help(self, ctx):
    Pages.setauthor()
    Pages.sescheck()

    value = get_db('misc')['helped']
    update_db('misc', 'none', {'helped': int(value) + 1})
    
    if ctx.guild:
      await ctx.message.delete()
      if ctx.author.guild_permissions.manage_messages == True:
        await asyncio.sleep(0.5)
        #wait
        await ctx.author.send(embed=embed1, view=Pages())
        return
      else:
        await asyncio.sleep(0.5)
        #wait
        await ctx.author.send(embed=embed1, view=Pages())
        return
    else:
      await ctx.author.send(embed=embed1, view=Pages())
  
  @slash_command(name="help", description=f"Help with {faxname}")
  async def help_slash(self, ctx):
    Pages.setauthor()
    Pages.sescheck()
    if ctx.guild:
      if check_logs(ctx.guild.id)[0] == True:
        logs2 = ctx.guild.get_channel(int(check_logs(ctx.guild.id)[2]))
        embed = discord.Embed(description=f"Slash Command used in <#{ctx.channel.id}>.", color=discord.Color.random())
        embed.add_field(name=f'Command used:', value=f"/help")
        embed.set_author(name=f"{ctx.author} • ID: {ctx.author.id}", icon_url=ctx.author.avatar)
        embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)
        await logs2.send(embed=embed, content=None)

    value = get_db('misc')['helped']
    update_db('misc', 'none', {'helped': int(value) + 1})
    
    if ctx.guild:
      if ctx.author.guild_permissions.manage_messages == True:
        await asyncio.sleep(0.5)
        #wait
        await ctx.respond(embed=embed1, view=Pages_slash(), ephemeral=True)
        return
      else:
        await asyncio.sleep(0.5)
        #wait
        await ctx.respond(embed=embed1, view=Pages_slash(), ephemeral=True)
        return
    else:
      await ctx.respond(embed=embed1, view=Pages_slash(), ephemeral=True)


def setup(client):
  client.add_cog(Help(client))