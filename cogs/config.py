import discord
from discord.ext import commands, tasks
from random import randint
from main import client, currentDT, bot_prefix, ses, round_time, red, green
import fileinput
from termcolor import cprint
from discord.ui import InputText, Modal
import random
import os
from database import *

currency = "Kromer"

class channel_chance_modal(Modal):
  def __init__(self, ctx, channel_id) -> None:
    self.ctx = ctx
    self.channel_id = channel_id
    super().__init__(title="Channel Response Chance")
    self.add_item(InputText(label="Type in a number (1-100)", placeholder=f"Ex: {randint(1, 100)}"))

  async def callback(self, interaction: discord.Interaction):
    serverid = interaction.guild.id
    channelid = interaction.channel.id

    response = str(self.children[0].value).lower()
    if "/" in response:
      response2 = int(response.split("/")[0])
    else:
      try:
        response2 = int(response)
      except:
        response2 = str("None")
        pass

    if isinstance(response2, int):
      embed = discord.Embed(title="Channel Response Chance", description=f"Set to {response2}% chance per message for <#{self.channel_id}>.", color=green)
      if response2 > 100:
        response2 = 100
      elif response2 < 1:
        response2 = 1

      update_db(f'guilds/{serverid}/ai', 'channels', {f"{self.channel_id}": response2})

    else:
      embed = discord.Embed(title="Channel Response Chance", description=f"There was an error setting the chance. Please try again.\n\n`{response}` could not be identified as an integer.", color=red)

    await interaction.message.edit(embed=embed, content=None, view=ai_first_select(self.ctx))
    await interaction.response.defer()
        

class global_chance_modal(Modal):
  def __init__(self, ctx) -> None:
    self.ctx = ctx
    super().__init__(title="Global Response Chance")
    self.add_item(InputText(label="Type in a number (1-100)", placeholder=f"Ex: {randint(1, 100)}"))

  async def callback(self, interaction: discord.Interaction):
    serverid = interaction.guild.id
    channelid = interaction.channel.id

    response = str(self.children[0].value).lower()
    if "/" in response:
      response2 = int(response.split("/")[0])
    else:
      try:
        response2 = int(response)
      except:
        response2 = str("None")
        pass

    if isinstance(response2, int):
      embed = discord.Embed(title="Global Chance", description=f"Set to {response2}% chance per message.", color=green)
      if response2 > 100:
        response2 = 100
      elif response2 < 1:
        response2 = 1
        
      try:
        value = get_db('guilds')[f"{serverid}"]['ai']['active']
      except:
        embed.set_footer(text="The Module has been activated automatically.")
        update_db(f'guilds/{serverid}', 'ai', {"active": True})
      else:
        if not value:
          state = "Deactivated"
        else:
          state = "Activated"
            
        embed.set_footer(text=f"This Module is currently {state}.")

    else:
      embed = discord.Embed(title="Global Chance", description=f"There was an error setting the chance. Please try again.\n\n`{response}` could not be identified as an integer.", color=red)

    await interaction.message.edit(embed=embed, content=None, view=ai_first_select(self.ctx))
    await interaction.response.defer()

class All_Channels(discord.ui.Select):
  def __init__(self, options, ctx, category_id):
    super().__init__(
      placeholder="Select a channel",
      max_values=1,
      options=options
      )
    self.options = options
    self.ctx = ctx
    self.author = self.ctx.author.id
    self.category_id = category_id
  
  async def callback(self, interaction: discord.Interaction):
    val = str(self.values[0])

    if val == "back":
      options = []
      for category in interaction.guild.categories:
        try:
          options.append(discord.SelectOption(label=category.name, value=f"{category.id}", emoji="<:__:1180910705013166281>"))
        except:
          continue
      else:    
        options.append(discord.SelectOption(label="Go Back", value="back", emoji="<:go_back:1180929157203513384>"))
        embed = discord.Embed(title="Choose Category", description=f"Make sure you know in which category the channel you want to edit is in.")

      await interaction.message.edit(embed=embed, view=categories_before(self.ctx, options))
      await interaction.response.defer()
      return
  
    embed = discord.Embed(title="Channel Selected", description=f"Select what you want to edit about <#{val}>.")

    await interaction.message.edit(embed=embed, content=None, view=Ai_select(self.ctx, int(val), self.category_id))
    await interaction.response.defer()

class channels_before(discord.ui.View):
  def __init__(self, ctx, options, category_id):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.options = options
    self.category_id = category_id
    self.add_item(All_Channels(self.options, self.ctx, self.category_id))

class All_Categories(discord.ui.Select):
  def __init__(self, options, ctx):
    super().__init__(
      placeholder="Select a category",
      max_values=1,
      options=options
      )
    self.options = options
    self.ctx = ctx
    self.author = self.ctx.author.id

  async def callback(self, interaction: discord.Interaction):
    val = str(self.values[0])

    if val == "back":
      try:
        value = get_db('guilds')[f"{interaction.guild.id}"]['ai']['active']
      except:
        state = "Deactivated"
      else:
        if value is not None:
          if value == True:
            state = "Activated"
          else:
            state = "Deactivated"
        else:
          state = "Deactivated"

      embed = discord.Embed(title="Beta Ai Settings", description="Please select what you want to do with this module.")
      embed.set_footer(text=f"This module is currently {state}.")
      
      await interaction.message.edit(embed=embed, view=ai_first_select(self.ctx))
      await interaction.response.defer()
      return
      
    options = []
    for channel in discord.utils.get(interaction.guild.categories, id=int(val)).text_channels:
      try:
        options.append(discord.SelectOption(label=channel.name, value=f"{channel.id}", emoji="<:__:1180910705013166281>"))
      except:
        continue
    else:    
      options.append(discord.SelectOption(label="Go Back", value="back", emoji="<:go_back:1180929157203513384>"))
      embed = discord.Embed(title="Category Selected", description=f"Select the channel you want to edit.")
  
      await interaction.message.edit(embed=embed, content=None, view=channels_before(self.ctx, options, int(val)))
      await interaction.response.defer()

class categories_before(discord.ui.View):
  def __init__(self, ctx, options):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.options = options
    self.add_item(All_Categories(self.options, self.ctx))

class ai_first_select(discord.ui.View):
  def __init__(self, ctx):
    super().__init__(timeout=120)
    self.ctx = ctx
    
  @discord.ui.button(label="Activate/Deactivate", style=discord.ButtonStyle.primary, custom_id="activate")
  async def activate(self, button, interaction):
    try:
      value = get_db('guilds')[f"{interaction.guild.id}"]['ai']
    except:
      value = {}

    if value.get('global_chance') is None:
      update_db(f'guilds/{interaction.guild.id}', 'ai', {"global_chance": 1})
      chance = "\n\nGlobal Response Chance has been set to 1%."
    else:
      chance = f"""\n\nGlobal Response Chance is currently set to {value['global_chance']}%."""
  
    if value.get('active') is not None:
      if value["active"]:
        update_db(f'guilds/{interaction.guild.id}', 'ai', {"active": False})
        state = "Deactivated"
      else:
        update_db(f'guilds/{interaction.guild.id}', 'ai', {"active": True})
        state = "Activated"
    else:
      update_db(f'guilds/{interaction.guild.id}', 'ai', {"active": True})
      state = "Activated"
      
    embed = discord.Embed(title="Activate/Deactivate", description=f"The Beta Ai has been {state}.{chance}")
    embed.set_footer(text=f"This Module is currently {state}.")
    
    await interaction.message.edit(embed=embed, content=None, view=ai_first_select(self.ctx))
    await interaction.response.defer()

  @discord.ui.button(label="Global Chance", style=discord.ButtonStyle.primary, custom_id="chance")
  async def chance(self, button, interaction):
    embed = discord.Embed(title="Global Chance", description="Edit the chance of the bot responding on the whole server.")

    modal = global_chance_modal(self.ctx)
    await interaction.message.edit(embed=embed, content=None)
    await interaction.response.send_modal(modal)

  @discord.ui.button(label="Add Channels", style=discord.ButtonStyle.primary, custom_id="channel")
  async def channel(self, button, interaction):
    options = []
    for category in interaction.guild.categories:
      try:
        options.append(discord.SelectOption(label=category.name, value=f"{category.id}", emoji="<:__:1180910705013166281>"))
      except:
        continue
    else:    
      options.append(discord.SelectOption(label="Go Back", value="back", emoji="<:go_back:1180929157203513384>"))
      embed = discord.Embed(title="Choose Category", description=f"Make sure you know in which category the channel you want to edit is in.")
      
      await interaction.message.edit(embed=embed, view=categories_before(self.ctx, options))
      await interaction.response.defer()

async def on_timeout(self):
  for child in self.children:
    child.disabled = True
  else:
    await self.message.edit(view=self, content="Timed out.") 

class Currency_Choice(discord.ui.View):
  def __init__(self, response):
    super().__init__(timeout=60)
    self.response = response
  
  @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="Yes")
  async def yes(self, button, interaction):
    if " " in self.response:
      self.response = self.response.split(" ", 1)[0]

    update_db(f'guilds/{interaction.guild.id}', 'currency',f"{self.response[0].upper()}{self.response[1:]}")
    
    if ("reset" in self.response) or ("default" in self.response):
      self.response = currency
      del_db(f'guilds/{interaction.guild.id}', 'currency')
      
    embed = discord.Embed(description=f"""```ps\nThe name of the currency has been set to "{self.response[0].upper()}{self.response[1:]}".```""", color=green)
    
    await interaction.message.edit(embed=embed, content=None, view=None)

  @discord.ui.button(label="No", style=discord.ButtonStyle.danger, custom_id="No")
  async def no(self, button, interaction):
    embed = discord.Embed(description=f"""```ps\n[Currency configuration cancelled.]```""", color=red)
    
    await interaction.message.edit(embed=embed, content=None, view=None)

  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    else:
      await self.message.edit(view=self, content="Timed out.")
    

class Config_Modal(Modal):
  def __init__(self, ctx, command, title, label, placeholder) -> None:
    self.ctx = ctx
    self.command = command
    self.title = title
    self.label = label
    self.placeholder = placeholder
    super().__init__(title=self.title)
    self.add_item(InputText(label=self.label, placeholder=self.placeholder))

  async def callback(self, interaction: discord.Interaction):
    response = str(self.children[0].value).lower()

    names = []
    channels = client.get_guild(interaction.guild.id).text_channels
    channels = str(channels).split(",")
    for x in channels:
      if "name=" in x:
        name = x.split("name='")[1].lstrip().split("' ")[0]
        names.append(name)
    
    if self.command == "disable":
      await self.ctx.invoke(client.get_command(self.command), cmd2=response)
      await interaction.response.defer()

    elif self.command == "prefix":
      if ("reset" in response) or ("default" in response):
        await self.ctx.invoke(client.get_command(self.command))
        await interaction.response.defer()
      else:
        await self.ctx.invoke(client.get_command(self.command), prefix=response)
        await interaction.response.defer()

    elif self.command == "raid":
      try:
        if int(response):
          await self.ctx.invoke(client.get_command(self.command), days=int(response))
          await interaction.response.defer()
        else:
          await self.ctx.invoke(client.get_command(self.command))
          await interaction.response.defer()
      except:
        await self.ctx.invoke(client.get_command(self.command))
        await interaction.response.defer()
    
    elif self.command == "ignore":
      try:
        chan = discord.utils.get(interaction.guild.text_channels, name=response)
      except:
        embed = discord.Embed(description=f"**`ERROR:`** ```md\nThe channel <{response}> could not be found.\n```", color=red)
        await interaction.channel.send(embed=embed, content=None, delete_after=20)
        await interaction.response.defer()
      else:
        if response in str(names):
          await self.ctx.invoke(client.get_command(self.command), channel=chan)
          await interaction.response.defer()
        else:
          embed = discord.Embed(description=f"**`ERROR:`** ```md\nThe channel <{response}> could not be found.\n```", color=red)
          await interaction.channel.send(embed=embed, content=None, delete_after=20)
          await interaction.response.defer()
        
    elif self.command == "logs":
      if f"'{response}'" in str(names):
        chan = discord.utils.get(interaction.guild.text_channels, name=response)
        await self.ctx.invoke(client.get_command(self.command), channel=chan)
        await interaction.response.defer()
      else:
        await self.ctx.invoke(client.get_command(self.command))
        await interaction.response.defer()

    elif self.command == "ai":
      if f"'{response}'" in str(names):
        chan = discord.utils.get(interaction.guild.text_channels, name=response)
        await self.ctx.invoke(client.get_command(self.command), chan=chan.id)
        await interaction.response.defer()
      elif ("disable" in response) or ("enable" in response):
        await self.ctx.invoke(client.get_command(self.command))
        await interaction.response.defer()
      elif int(response) <= 100:
        await self.ctx.invoke(client.get_command(self.command), chan=int(response))
        await interaction.response.defer()
      else:
        await self.ctx.invoke(client.get_command(self.command))
        await interaction.response.defer()

    elif self.command == "currency":
      if ("reset" in response) or ("default" in response):
        embed = discord.Embed(description=f"""```ps\nAre you sure that you want to [reset] the name of the currency back to "{currency}"?```""", color=0xf7e300)
        await interaction.channel.send(embed=embed, content=None, view=Currency_Choice(response))
        await interaction.response.defer()
      else:
        response = response.split(" ", 1)[0]
        embed = discord.Embed(description=f"""```ps\nAre you sure that you want to [set] the name of the currency to "{response[0].upper()}{response[1:]}"?```""", color=0xf7e300)
        await interaction.channel.send(embed=embed, content=None, view=Currency_Choice(response))
        await interaction.response.defer()

perm_embed = discord.Embed(description="```ps\n[Sorry, but you do not have the required permissions to invoke this module.]\n```")

class Select_Command(discord.ui.View):
  def __init__(self, ctx, author):
    super().__init__(timeout=60)
    self.selected = ""
    self.ctx = ctx
    self.author = author

  @discord.ui.select(placeholder="Choose what command you want to invoke.", max_values=1, disabled=False, options=[
        discord.SelectOption(
          label="Enable/Disable (Manage_Roles)",
          description="Enable/Disable any command from the bot."
        ),
        discord.SelectOption(
          label="Welcome Message (Administrator)",
          description="Customize a message that greets new members."
        ),
        discord.SelectOption(
          label="Ignore Channel (Manage_Roles)",
          description="Select a channel to make it ignore commands."
        ),
        discord.SelectOption(
          label="Set up Logging (Administrator)",
          description="Select a channel and choose what that channel will log."
        ),
        discord.SelectOption(
          label="Nickname Check (Manage_Roles)",
          description="Automatically changes any non-latin names to a random name."
        ),
        discord.SelectOption(
          label="Change Prefix (Administrator)",
          description=f"Change the prefix used by The Fax Machine"
        ),
        discord.SelectOption(
          label="Configure AI (Administrator)",
          description=f"Change the chances/channel where Fax can talk in."
        ),
        discord.SelectOption(
          label="Anti Raid (Administrator)",
          description=f"Configure an automatic timeout on newer accounts."
        ),
        discord.SelectOption(
          label="Score & Xp Tracking (Administrator)",
          description=f"Enable/Disable adding score & Xp to members that are active."
        ),
        discord.SelectOption(
          label="Global Chat (Administrator)",
          description=f"Configurate the Global Chat."
        ),
        discord.SelectOption(
          label="Starboard (Administrator)",
          description=f"Configurate the Starboard."
        ),
        discord.SelectOption(
          label="Currency (Administrator)",
          description=f"Configurate the name of the bot's currency."
        )
    ])
  async def sele(self, select, interaction):
    val = str(select.values[0])
    if interaction.user.id == self.author:
      if "Enable/Disable" in val:
        perms = "Manage_Roles"
        if not interaction.user.guild_permissions.manage_roles:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return
          
        commands = get_db('misc')['all_commands']
        commands = commands.split(",")
        command = "disable"
        title = "Disabling/Enabling a command"
        label = "Type in any command."
        placeholder = f"Ex: {random.choice(commands)}"
        
        modal = Config_Modal(self.ctx, command, title, label, placeholder)
        await interaction.response.send_modal(modal)
        await interaction.message.delete()

      elif "Currency" in val:
        perms = "Administrator"
        if not interaction.user.guild_permissions.administrator:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return

        command = "currency"
        title = "Configuring Currency"
        label = "Change the name of fax's currency."
        placeholder = f"{currency} OR reset/default"
        
        modal = Config_Modal(self.ctx, command, title, label, placeholder)
        await interaction.response.send_modal(modal)
        await interaction.message.delete()

      elif "Prefix" in val:
        perms = "Administrator"
        if not interaction.user.guild_permissions.administrator:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return
          
        prefixes = [",", ";", "?", ">", "!", ":", ".", "=", "+", "-", "_", "^", "%", "$", "&", "*", "#", "@"]
        command = "prefix"
        title = "Changing prefix"
        label = "Type in the prefix you want the bot to use."
        placeholder = f"Ex: {random.choice(prefixes)}{random.choice(prefixes)} OR <reset>/<default>."
        
        modal = Config_Modal(self.ctx, command, title, label, placeholder)
        await interaction.response.send_modal(modal)
        await interaction.message.delete()

      elif "Raid" in val:
        perms = "Administrator"
        if not interaction.user.guild_permissions.administrator:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return
          
        command = "raid"
        title = "Configuring Anti-Raid"
        label = "How many days old should an account be?"
        placeholder = f"Ex: {randint(1, 100)} OR anything else to change."
        
        modal = Config_Modal(self.ctx, command, title, label, placeholder)
        await interaction.response.send_modal(modal)
        await interaction.message.delete()
      
      elif "Welcome" in val:
        perms = "Administrator"
        if not interaction.user.guild_permissions.administrator:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return

        p = discord.Embed(description="This configuration has been moved to the site, to make it easier to set up.\nPlease click (here)[CONFIGSITE]")
        await interaction.message.edit(embed=p, content=None, view=None)
        return

      elif "Score" in val:
        perms = "Administrator"
        if not interaction.user.guild_permissions.administrator:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return
          
        command = "scores"
        await self.ctx.invoke(client.get_command(command))
        await interaction.message.delete()

      elif "Global" in val:
        perms = "Administrator"
        if not interaction.user.guild_permissions.administrator:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return
          
        command = "gc"
        await self.ctx.invoke(client.get_command(command))
        await interaction.message.delete()

      elif "Starboard" in val:
        perms = "Administrator"
        if not interaction.user.guild_permissions.administrator:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return
          
        command = "starboard"
        await self.ctx.invoke(client.get_command(command))
        await interaction.message.delete()

      elif "Nick" in val:
        perms = "Manage_Roles"
        if not interaction.user.guild_permissions.manage_roles:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return
        
        command = "nickcheck"
        await self.ctx.invoke(client.get_command(command))
        await interaction.message.delete()
        
      elif "Ignore" in val:
        perms = "Manage_Roles"
        if not interaction.user.guild_permissions.manage_roles:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return
          
        names = []
        channels = client.get_guild(interaction.guild.id).text_channels
        channels = str(channels).split(",")
        for x in channels:
          if "name=" in x:
            name = x.split("name='")[1].lstrip().split("' ")[0]
            names.append(name)
        
        command = "ignore"
        title = "Ignoring a channel"
        label = "Type in a channel name."
        placeholder = f"Ex: {random.choice(names)}"
        
        modal = Config_Modal(self.ctx, command, title, label, placeholder)
        await interaction.response.send_modal(modal)
        await interaction.message.delete()

      elif "Logging" in val:
        perms = "Administrator"
        if not interaction.user.guild_permissions.administrator:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return
          
        names = []
        channels = client.get_guild(interaction.guild.id).text_channels
        channels = str(channels).split(",")
        for x in channels:
          if "name=" in x:
            name = x.split("name='")[1].lstrip().split("' ")[0]
            names.append(name)
            
        command = "logs"
        title = "Setting up Logging"
        label = "Type in a channel name."
        placeholder = f"Ex: {random.choice(names)} OR anything else to change."
        
        modal = Config_Modal(self.ctx, command, title, label, placeholder)
        await interaction.response.send_modal(modal)
        await interaction.message.delete()

      elif "Configure AI" in val:
        perms = "Administrator"
        if not interaction.user.guild_permissions.administrator:
          perm_embed.add_field(name="Required Permissions:", value=f"```md\n<{perms}>```")
          await interaction.message.edit(embed=perm_embed, content=None, delete_after=20, view=None)
          return

        command = "ai"
        await self.ctx.invoke(client.get_command(command))
        await interaction.message.delete()


def saveFilterToFile(filterList):
    f = open("bans.txt", "a")
    f.write('%d' % filterList + ", ")
    f.close()


def loadFilterFromFile():
    f = open("bans.txt", "r")
    filterList = f.readlines()

    for i in range(0, len(filterList)):
      filterList[i] = filterList[i][:len(filterList[i])-1] 

    f.close()
    return filterList

def saveservers(filterList):
    f = open("servers2.txt", "a")
    f.write('%d' % filterList + "\n")
    f.close()

def removeservers(word):
    with open("servers2.txt", "r") as f:
      lines = f.readlines()
    with open("servers2.txt", "w") as f:
      for line in lines:
        if line.strip("\n") != word:
          f.write(line)

def savenickserver(filterList):
    f = open("nick.txt", "a")
    f.write('%d' % filterList + "\n")
    f.close()

def removenickserver(word):
    with open("nick.txt", "r") as f:
      lines = f.readlines()
    with open("nick.txt", "w") as f:
      for line in lines:
        if line.strip("\n") != word:
          f.write(line)

def ai2save(filterList):
    f = open("ai2.txt", "a")
    f.write('%d' % filterList + "\n")
    f.close()

def ai2remove(word):
    with open("ai2.txt", "r") as f:
      lines = f.readlines()
    with open("ai2.txt", "w") as f:
      for line in lines:
        if line.strip("\n") != word:
          f.write(line)

class Ignore_Select(discord.ui.View):
  def __init__(self, ctx, channel, author, name):
    super().__init__(timeout=60)
    self.selected = ""
    self.ctx = ctx
    self.channel = channel
    self.name = name
    self.author = author

  @discord.ui.select(placeholder=f"Choose what you want to do with this channel.", max_values=1, disabled=False, options=[
        discord.SelectOption(
            label="Ignore Channel",
            description="Disallow the usage of commands in the channel."
        ),
        discord.SelectOption(
            label="Unignore Channel",
            description="Allow the usage of commands in the channel."
        ),
        discord.SelectOption(
            label="Check Database",
            description="Check what channels are ignored in your server."
        )
    ])
  async def sele2(self, select, interaction):
    val = str(select.values[0])
    if interaction.user.id == self.author:
      try:
        value = get_db('guilds')[f'{interaction.guild.id}']['ignore']
      except:
        value = ''

      if "Ignore" in val:
        if str(self.channel) in value:
          embed = discord.Embed(description=f"""```md\n<#{self.name}> is already being ignored.\n```""")
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
        else:
          update_db(f'guilds', f'{interaction.guild.id}', {"ignore": f"{value}{self.channel},"})
          embed = discord.Embed(description=f"""```md\n<#{self.name}> is now being ignored.\n```""")
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
      elif "Unignore" in val:
        if str(self.channel) in value:
          valuefinal = str(value).replace(f"{self.channel},", "")
          update_db(f'guilds', f'{interaction.guild.id}', {"ignore": f"{valuefinal}"})
          embed = discord.Embed(description=f"""```md\n<#{self.name}> is now not being ignored.\n```""")
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
        else:
          embed = discord.Embed(description=f"""```md\n<#{self.name}> is already not ignored.\n```""")
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
      elif "Check" in val:
        if value == '':
          embed = discord.Embed(description=f"""No channels selected to ignore commands.""")
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
        else:
          channels = value.replace("-", ">\n<#")
          embed = discord.Embed(description=f"""**`Currently ignored channels`**:\n\n<#{channels[:-2]}""")
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
    else:
      await interaction.response.defer()
      return

class Disable_Select(discord.ui.View):
  def __init__(self, ctx, cmd, author):
    super().__init__(timeout=60)
    self.selected = ""
    self.ctx = ctx
    self.cmd = cmd
    self.author = author

  @discord.ui.select(placeholder=f"Choose what you want to do with this command.", max_values=1, disabled=False, options=[
        discord.SelectOption(
            label="Disable Command",
            description="Disallow the usage of this command in your server."
        ),
        discord.SelectOption(
            label="Enable Command",
            description="Allow the usage of this command in your server."
        ),
        discord.SelectOption(
            label="View Commands",
            description="View all the commands you can disable/enable."
        ),
        discord.SelectOption(
            label="Check Database",
            description="Check what commands are disabled in your server."
        )
    ])
  async def sele(self, select, interaction):
    val = str(select.values[0])
    if interaction.user.id == self.author:
      try:
        value = get_db('guilds')[f'{interaction.guild.id}']['disable']
      except:
        value = ''

      if "Disable" in val:
        if f"<{self.cmd}>" in value:
          embed = discord.Embed(description=f"""```md\nThe <{self.cmd}> command is already disabled.\n```""")
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
        else:
          embed = discord.Embed(description=f"""```md\nThe <{self.cmd}> command has been disabled.```""")
          update_db('guilds', f'{interaction.guild.id}', {"disable": f"{value}<{self.cmd}>,"})

          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()

      elif "Enable" in val:
        if f"<{self.cmd}>" in value:
          embed = discord.Embed(description=f"""```md\nThe <{self.cmd}> command has been enabled.```""")
          new_val = value.replace(f"<{self.cmd}>,", "")
          update_db('guilds', f'{interaction.guild.id}', {"disable": f"{new_val}"})

          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()
        else:
          embed = discord.Embed(description=f"""```md\nThe <{self.cmd}> command is not disabled.\n```""")
          await interaction.message.edit(embed=embed, content=None)
          await interaction.response.defer()

      elif "View" in val:
        await interaction.message.delete()
        await self.ctx.invoke(client.get_command('help'))

      elif "Check" in val:
        if value == '':
          embed = discord.Embed(description=f"""```fix\nNo commands are currently disabled.```""")
        else:
          cmds = value.replace(",", "\n")
          embed = discord.Embed(description=f"""**`Currently disabled commands`**:\n```fix\n{cmds}```""")

        await interaction.message.edit(embed=embed, content=None)
        await interaction.response.defer()


class Select_channel(discord.ui.View):
  def __init__(self, ctx, channel, author):
    super().__init__(timeout=60)
    self.selected = ""
    self.ctx = ctx
    self.channel = channel
    self.author = author

  @discord.ui.select(placeholder="Choose what you want to edit.", max_values=1, disabled=False, options=[
        discord.SelectOption(
            label="Normal Logs",
            description="Logs important things, like users joining, messages getting deleted/edited, etc."
        ),
        discord.SelectOption(
            label="Command Logs",
            description="Logs the commands used from the bot and reports it in the channel."
        )
    ])
  async def sele(self, select, interaction):
    val = str(select.values[0])
    if interaction.user.id == self.author:
      try:
        if "Normal" in val:
          await interaction.message.delete()
          await self.ctx.invoke(client.get_command("channel_select"), chosen="normal", chosen2=self.channel)
          return
        elif "Command" in val:
          await interaction.message.delete()
          await self.ctx.invoke(client.get_command("channel_select"), chosen="command", chosen2=self.channel)
          return
      except:
        return

class Ai_select(discord.ui.View):
  def __init__(self, ctx, chan, category_id):
    super().__init__(timeout=60)
    self.selected = ""
    self.ctx = ctx
    self.channel = int(chan)
    self.category_id = category_id

  @discord.ui.select(placeholder="Choose what you want to edit.", max_values=1, disabled=False, options=[
        discord.SelectOption(
          label="Change channel chance",
          description=f"Change the chance of the bot responding in the selected channel."
        ),
        discord.SelectOption(
          label="Reset",
          description="Reset the settings made."
        ),
        discord.SelectOption(
          label=f"Add Channel",
          description="Add a channel the bot will be able to respond in. It will only respond in the added channels."
        ),
        discord.SelectOption(
          label="Remove Channel",
          description="Remove a channel from the list."
        ),
        discord.SelectOption(
          label="Check Settings",
          description="Check the current settings."
        ),
        discord.SelectOption(
          label="Go Back",
          description="Choose another channel from the list.",
          emoji="<:go_back:1180929157203513384>"
        )
    ])
  async def sele(self, select, interaction):
    val = str(select.values[0])
    if interaction.user.id == self.ctx.author.id:
      try:
        value = get_db('guilds')[f'{interaction.guild.id}']['ai']
      except:
        value = {}
        
      if "Change " in val:
        embed = discord.Embed(title="Change Channel Chance", description=f"Set the chance of response per channel.")

        modal = channel_chance_modal(self.ctx, self.channel)
        await interaction.message.edit(embed=embed, content=None)
        await interaction.response.send_modal(modal)
        
      elif "Reset" in val:
        if value.get("channels") is not None:
          del_db(f'guilds/{interaction.guild.id}/ai', 'channels')
        
        embed = discord.Embed(description=f"All Channels have been removed from the database.")
        
        await interaction.message.edit(embed=embed, content=None, view=self)
        await interaction.response.defer()
      elif "Add " in val:
        if value.get("channels") is not None:
          if value["channels"].get(str(self.channel)) is not None:
            embed = discord.Embed(description=f"<#{self.channel}> is already in the database.\n\nCurrent set chance: {value['channels'][str(self.channel)]}%")
          else:
            value["channels"].update({f"{self.channel}": 1})
            update_db(f'guilds/{interaction.guild.id}', 'ai', {"channels": value['channels']})

            embed = discord.Embed(description=f"<#{self.channel}> has been added to the database.\n\nCurrent set chance: 1%")
        else:
          value.update({"channels": {f"{self.channel}": 1}})
          update_db(f'guilds/{interaction.guild.id}', 'ai', {"channels": value['channels']})

          embed = discord.Embed(description=f"<#{self.channel}> has been added to the database.\n\nCurrent set chance: 1%")

        await interaction.message.edit(embed=embed, content=None, view=self)
        await interaction.response.defer()
          
      elif "Remove " in val:
        if value.get("channels") is not None:
          if value["channels"].get(str(self.channel)) is not None:
            embed = discord.Embed(description=f"<#{self.channel}> has been deleted from the database.")
            del_db(f'guilds/{interaction.guild.id}/ai/channels', f'{self.channel}')

          else:
            embed = discord.Embed(description=f"<#{self.channel}> could not be found in the database.")
        else:
          embed = discord.Embed(description=f"<#{self.channel}> could not be found in the database.")

        await interaction.message.edit(embed=embed, content=None, view=self)
        await interaction.response.defer()
        
      elif "Check" in val:
        chance = "Not Set"
        active = False
        channels = "None"
        all_chans = ""
        if value.get("global_chance") is not None:
          if value.get("channels") is not None:
            chance = f"{value['global_chance']}% (Does nothing when individual channels are set)"
          else:
            chance = f"{value['global_chance']}%"

        if value.get("active") is not None:
          active = value['active']

        if value.get("channels") is not None:
          channels = value['channels']
          all_chans = ""
          for x in channels:
            all_chans += f"<#{x}> - {value['channels'][x]}%\n"
          
        embed = discord.Embed(title="Current Settings", description=f"Active? **{active}**\nGlobal Chance: **{chance}**\n\n{all_chans}")
        await interaction.message.edit(embed=embed, content=None, view=self)
        await interaction.response.defer()
          
      elif "Back" in val:
        options = []
        for channel in discord.utils.get(interaction.guild.categories, id=int(self.category_id)).text_channels:
          try:
            options.append(discord.SelectOption(label=channel.name, value=f"{channel.id}", emoji="<:__:1180910705013166281>"))
          except:
            continue
        else:    
          options.append(discord.SelectOption(label="Go Back", value="back", emoji="<:go_back:1180929157203513384>"))
          embed = discord.Embed(title="All Channels", description=f"Select a channel you want to edit.")

          await interaction.message.edit(embed=embed, view=channels_before(self.ctx, options, self.category_id))
          await interaction.response.defer()

class Config(commands.Cog):
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
  @commands.has_permissions(administrator=True) 
  async def channel_select(self, ctx, chosen: str, chosen2: int):
    try:
      channel = ctx.guild.get_channel(int(chosen2))
    except:
      embed2 = discord.Embed(title="Failed to edit module", description=f"The provided channel ({chosen2}) does not exist.", color=red)
      await ctx.send(embed=embed2, content=None)
      return

    if chosen == "normal":
      update_db(f'guilds/{ctx.guild.id}', 'logs', {'logs1': f"{channel.id}"})
      embed = discord.Embed(title="Module Enabled", description=f"{channel.mention} has been set the logs for important matters.", color=green)
      await ctx.send(embed=embed, content=None)

    elif chosen == "command":
      update_db(f'guilds/{ctx.guild.id}', 'logs', {'logs2': f"{channel.id}"})
      embed = discord.Embed(title="Module Enabled", description=f"{channel.mention} has been set the logs for commands that have been invoked.", color=green)
      await ctx.send(embed=embed, content=None)

  ### ACTUAL COMMANDS ###

  @commands.command()
  @commands.has_permissions(manage_roles=True)
  async def config(self, ctx):
    author = ctx.author.id
    view = Select_Command(ctx, author)
    embed = discord.Embed(title="Configurate your server", description="Please select what command you want to invoke.", color=green) 
    await ctx.send(embed=embed, content=None, view=view)

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.is_owner()
  async def prefix(self, ctx, prefix: str=None):
    try:
      value = get_db(f"guilds")[f'{ctx.guild.id}']['prefix']
    except:
      if prefix is None:
        embed2 = discord.Embed(description=f"**`ERROR:`** ```k\nYou need to add an argument of a prefix to activate this module.\n```", color=0xc40000)
        await ctx.send(embed=embed2, content=None)
      else:
        embed2 = discord.Embed(description=f"**`SUCCESS:`** ```k\nThe prefix of this bot has been changed from <{bot_prefix}> to <{prefix}>.\nYou can reset this by invoking this command again, with no argument.```", color=0x1bd13a)  
        update_db(f'guilds', f"{ctx.guild.id}", {"prefix": f"{prefix}"})
        await ctx.send(embed=embed2, content=None)
    else:
      if prefix is None:
        embed2 = discord.Embed(description=f"**`SUCCESS:`** ```k\nThe prefix of this bot has been reset back to <{bot_prefix}>.\nYou can change this by invoking this command again, with an argument.```", color=0xc40000)
        del_db(f'guilds/{ctx.guild.id}', "prefix")
        await ctx.send(embed=embed2, content=None)
      else:
        embed2 = discord.Embed(description=f"**`SUCCESS:`** ```k\nThe prefix of this bot has been changed from <{value}> to <{prefix}>.\nYou can reset this by invoking this command again, with no argument.```", color=0x1bd13a)  
        update_db(f'guilds', f"{ctx.guild.id}", {"prefix": f"{prefix}"})
        await ctx.send(embed=embed2, content=None)

  @commands.command(aliases=['enable'])
  @commands.is_owner()
  async def disable(self, ctx, cmd2: str=None):
    ids = ctx.guild.id
    ids2 = str(ids)
    if cmd2 == None:
      await ctx.invoke(self.client.get_command('help'))
    else:
      if cmd2.startswith("g!"):
        cmd2 = cmd2.replace("g!", "")
      else:
        pass
      cmd = cmd2.lower()
      if f"'{cmd}'" in str(client.all_commands):
        view = Disable_Select(ctx, cmd, ctx.author.id)
        embed = discord.Embed(description=f"""```md\nThe <{cmd}> command has been found.\nPlease select an option from the menu below.```""")
        await ctx.send(embed=embed, content=None, view=view)
      else:
        embed = discord.Embed(description=f"""```md\nThe <{cmd}> command does not exist.\n```""")
        await ctx.send(embed=embed, content=None)

  @commands.command(aliases=['unignore'])
  @commands.is_owner()
  async def ignore(self, ctx, channel : discord.TextChannel):
    if channel:
      embed = discord.Embed(description=f"""```md\n<#{channel.name}> has been found.\nPlease select an option from the menu below.```""")
      view = Ignore_Select(ctx, channel.id, ctx.author.id, channel.name)
      await ctx.send(embed=embed, content=None, view=view)
    else:
      embed = discord.Embed(description=f"""```diff\n- Channel could not be found.```""", color=red)
      await ctx.send(embed=embed, content=None, view=None)
  
  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.is_owner()
  async def logs(self, ctx, channel: discord.TextChannel):
    author = ctx.author.id
    view = Select_channel(ctx, channel.id, author)

    embed = discord.Embed(description="**Channel Found**\n\nPlease select what you want this channel to log.")
    await ctx.send(embed=embed, content=None, view=view)

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.is_owner()
  async def ai(self, ctx):
    try:
      value = get_db('guilds')[f"{ctx.guild.id}"]['ai']
    except:
      state = "Deactivated"
    else:
      if value.get("active") is not None:
        if value["active"]:
          state = "Activated"
        else:
          state = "Deactivated"
      else:
        state = "Deactivated"
        
    embed = discord.Embed(title="Beta Ai Settings", description="Please select what you want to do with this module.")
    embed.set_footer(text=f"This module is currently {state}.")
    await ctx.send(embed=embed, content=None, view=ai_first_select(ctx))

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.is_owner()
  async def nickcheck(self, ctx):
    file = open("nick.txt", "r")
    file2 = file.read()
    ids = ctx.guild.id
    ids2 = str(ids)
    if ids2 in file2:
      embed2 = discord.Embed(description=f"**`SUCCESS:`** ```k\nThe server has been removed from the list.\nYou can re-enable this at anytime with the {bot_prefix}nickcheck command.\n```", color=green)
      removenickserver(ids2)
      await ctx.send(embed=embed2, content=None)
    else:
      embed2 = discord.Embed(description=f"**`SUCCESS:`** ```k\nThe server has been added to the list.\nThe bot will now rename anyone with a non-latin name to 'Unpingable Name #num'. You can disable this at anytime with the {bot_prefix}nickcheck command.\n```", color=green)
      savenickserver(ids)
      await ctx.send(embed=embed2, content=None)

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.is_owner()
  async def raid(self, ctx, days: int=None):
    if not days:
      days = 10

    try:
      value = get_db('guilds')[f"{ctx.guild.id}"]['raid']
    except:
      update_db(f'guilds/{ctx.guild.id}', 'raid', {"active": True, "days": days})
      embed2 = discord.Embed(description=f"**`SUCCESS:`** ```k\nThe server has been added to the database.\nIf any person with an account that is less than {days} days old joins, that account will get timed out for one hour.```", color=green)
      embed2.set_footer(text="The Module is now enabled.")
      await ctx.send(embed=embed2, content=None)
    else:
      value2 = str(value['active']).lower()
      update_db(f'guilds/{ctx.guild.id}', 'raid', {"days": days})

      if "true" in value2:
        status = "enabled"
      else:
        status = "disabled"
        
      embed2 = discord.Embed(description=f"**`SUCCESS:`** ```k\nThe server has been added to the database.\nIf any person with an account that is less than {days} days old joins, that account will get timed out for one hour.```", color=green)
      embed2.set_footer(text=f"The Module is currently {status}.")
      await ctx.send(embed=embed2, content=None)
        

def setup(client):
    client.add_cog(Config(client))