import discord
from discord.ext import commands, tasks
import logging
import traceback
import random
from random import randint
from main import client, currentDT, bot_prefix, ses, round_time, check_name, green, red
import fileinput
from termcolor import cprint
import os
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
from discord.ui import InputText, Modal
from database import *

def get_channels(guild):
  names = []
  channels = client.get_guild(int(guild)).text_channels
  channels = str(channels).split(",")
  for x in channels:
    if "name=" in x:
      name = x.split("name='")[1].lstrip().split("' ")[0]
      names.append(name)
  else:
    thing = random.choice(names)
    return thing

def if_100(guild):
  n = 100
  value = get_db('guilds')[f'{guild}']['starboard_messages']
  value2 = value.split(",")
  if len(value2) >= n:
    del_db(f'guilds/{guild}', 'starboard_messages')
  else:
    return None
    

class Starboard_Modal(Modal):
  def __init__(self, ctx, label, which) -> None:
    self.ctx = ctx
    self.label = label
    self.which = which
    if which == "channel":
      example = get_channels(self.ctx.guild.id)
    else:
      example = randint(1, 100)
    super().__init__(title="Configure Starboard")
    self.add_item(InputText(label=self.label, placeholder=f"Ex: {example}"))

  async def callback(self, interaction: discord.Interaction):
    response = self.children[0].value
    try:
      value = get_db('guilds')[f'{interaction.guild.id}']['starboard']
    except:
      value = {"active": False, "channel": "None", "count": 5}
      
    if "channel" in self.which:
      names = []
      channels = client.get_guild(interaction.guild.id).text_channels
      channels = str(channels).split(",")
      for x in channels:
        if "name=" in x:
          name = x.split("name='")[1].lstrip().split("' ")[0]
          names.append(name)
      
      try:
        channel = discord.utils.get(interaction.guild.text_channels, name=response)
      except:
        embed = discord.Embed(description=f"**`ERROR:`** ```md\nThe channel <{response}> could not be found.\n```", color=red)
        await interaction.message.edit(embed=embed, content=None, delete_after=20)
        await interaction.response.defer()
      else:
        if f"{response}" in names:
          embed2 = discord.Embed(title="Module Enabled", description=f"The starboard channel has been set to {channel.mention}", color=green)
          update_db(f'guilds/{interaction.user.id}', 'starboard', {"count": value['count'], "channel": str(channel.id)})
          await interaction.message.edit(embed=embed2, content=None)
          await interaction.response.defer()
          
        else:
          embed = discord.Embed(description=f"**`ERROR:`** ```md\nThe channel <{response}> could not be found.\n```", color=red)
          await interaction.message.edit(embed=embed, content=None, delete_after=20)
          await interaction.response.defer()
    else:
      try:
        if int(response) > 1:
          embed2 = discord.Embed(title="Reaction Amount Set", description=f"The starboard channel reaction amount has been set to **{response}**.", color=green)
          update_db(f'guilds/{interaction.user.id}', 'starboard', {"count": int(response)})
          await interaction.message.edit(embed=embed2, content=None)
          await interaction.response.defer()
      except:
        embed = discord.Embed(description=f"**`ERROR:`** ```md\nCould not set '{response}' as a number.\n```", color=red)
        await interaction.message.edit(embed=embed, content=None, delete_after=20)
        await interaction.response.defer()


class Select(discord.ui.View):
  def __init__(self, ctx, author):
    super().__init__(timeout=60)
    self.selected = ""
    self.ctx = ctx
    self.author = author

  @discord.ui.select(placeholder="Choose the starboard settings.", max_values=1, disabled=False, options=[
        discord.SelectOption(
          label="Enable/Disable",
          description="Enable/Disable the starboard."
        ),
        discord.SelectOption(
            label="Set Channel",
            description="Set the channel for the starboard."
        ),
        discord.SelectOption(
            label=f"Set Reaction Count",
            description="Set the amount of a reaction needed to pin the message in the starboard."
        )
    ])
  async def sele(self, select, interaction):
    val = str(select.values)
    valre = val.replace("['", "")
    val2 = valre.replace("']", "")
    if interaction.user.id == self.author:
      try:
        if "Enable/Disable" in val2:
          await interaction.message.delete()
          await self.ctx.invoke(client.get_command("starboard_settings"), chosen="enable")
          return
        elif "Reaction Count" in val2:
          embed = discord.Embed(title="Awaiting Response...", description=f"Your response will be set as the amount of reactions needed per message to send the message to the set channel.", color=green)
          label = "Change the amount of needed reactions."
          which = "count"
          modal = Starboard_Modal(self.ctx, label, which)
          await interaction.message.edit(embed=embed, content=None, view=None)
          await interaction.response.send_modal(modal)
        elif "Channel" in val2:
          embed = discord.Embed(title="Awaiting Response...", description=f"Your response will be set as the channel for the starboard to send messages in.", color=green)
          label = "Type in the name of the channel."
          which = "channel"
          modal = Starboard_Modal(self.ctx, label, which)
          await interaction.message.edit(embed=embed, content=None, view=None)
          await interaction.response.send_modal(modal)
          
      except discord.HTTPException as error:
        return

class Starboard(commands.Cog):
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
      raise discord.ext.commands.CommandError(
        f"Sorry, this command is currently internally disabled, as it is being worked on.")

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def starboard_settings(self, ctx, chosen: str):
    serverid = ctx.guild.id
    channelid = ctx.channel.id

    if chosen == "enable":
      try:
        active = get_db('guilds')[f'{serverid}']['starboard']['active']
      except:
        try:
          channel = int(get_db('guilds')[f'{serverid}']['starboard']['channel'])
        except:
          embed = discord.Embed(title="Module Enabled", description=f"The starboard has been enabled for this server.\nPlease consider adding a channel using the same command to make this module work.", color=0x00d10a)
        else:
          embed = discord.Embed(title="Module Enabled", description=f"The starboard has been enabled for this server.\nChannel: <#{channel}>", color=0x00d10a)


        update_db(f'guilds/{serverid}', 'starboard', {"active": True})
        await ctx.send(embed=embed, content=None)
      else:
        embed = discord.Embed(title="Module Disabled", description=f"The starboard has been disabled for this server.", color=0xd10000)
        update_db(f'guilds/{serverid}', 'starboard', {"active": False})
        await ctx.send(embed=embed, content=None)
        
    elif chosen == "count":
      embed = discord.Embed(title="Awaiting Response...", description=f"Your next message will be set as the amount of reactions needed to send a message to the starboard.\nPlease Reply to this message with a number above 1.", color=0x00d10a)
      mes = await ctx.send(embed=embed, content=None)

      def check(m):
        global msg1
        msg1 = m.content
        return m.content and m.author == ctx.author

      msg = await client.wait_for("message", check=check, timeout=60)
      await msg.delete()
      
      if int(msg1) > 1:
        embed2 = discord.Embed(title="Reaction Amount Set", description=f"The starboard channel reaction amount has been set to **{msg1}**.", color=0x00d10a)
        try:
          sg = get_db('guilds')[f'{serverid}']['starboard']
        finally:
          update_db(f'guild/{serverid}', 'starboard', {'count': int(msg1)})

        await mes.edit(embed=embed2, content=None)
      else:
        embed2 = discord.Embed(title="Failed to Set", description=f'Could not find a number in "{msg1}".', color=0xd10000)
        await mes.edit(embed=embed2, content=None)
      
    elif chosen == "channel":
      embed = discord.Embed(title="Awaiting Response...", description=f"Your next message will be set as the channel for the starboard.\nPlease Reply to this message with the mention/id/name of the channel you want to use for the starboard.", color=green)
      mes = await ctx.send(embed=embed, content=None)

      def check(m):
        global msg1
        msg1 = m.content
        return m.content and m.author == ctx.author

      msg = await client.wait_for("message", check=check, timeout=60)
      await msg.delete()
      try:
        msg2 = msg1.replace("<", "")
        msg3 = msg2.replace(">", "")
        msg4 = msg3.replace("!", "")
        msg5 = msg4.replace("#", "")
        msg6 = int(msg5)
      except:
        channel = discord.utils.get(ctx.guild.channels, name=msg5)
      else:
        channel = discord.utils.get(ctx.guild.channels, id=msg6)
      
      embed2 = discord.Embed(title="Channel Successfully Set", description=f"The starboard channel has been set to {channel.mention}", color=0x00d10a)
      try:
        sg = get_db('guilds')[f'{serverid}']['starboard']
      finally:
        update_db(f'guild/{serverid}', 'starboard', {'channel': str(channel.id)})
        
      await mes.edit(embed=embed2, content=None)

  @commands.command(aliases=['board'])
  @commands.before_invoke(disabled_check)
  @commands.is_owner()
  async def starboard(self, ctx):
    try:
      author = ctx.author.id
      view = Select(ctx, author)
      embed = discord.Embed(title="Starboard Module", description="Please select what you want to do with this module.") 
      await ctx.send(embed=embed, content=None, view=view)
    except:
      return

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, member):
    message = reaction.message
    if not message.guild:
      return


    try:
      active = get_db('guilds')[f'{reaction.guild.id}']['starboard']['active']
    except:
      return
      
    if active is True:
      if message.channel.is_nsfw():
        return
      if message.channel.is_news():
        return
      if message.is_system():
        return
      if message.author.bot:
        return

      
      counter = 5
      try:
        count = get_db('guilds')[f'{reaction.guild.id}']['starboard']['count']
      except:
        pass
      else:
        counter = int(count)
        pass

      try:
        editor = get_db('guilds')[f'{reaction.guild.id}']['starboard_messages']
      except:
        pass
      else:
        if str(message.id) in editor:
          try:
            find_channel = int(get_db('guilds')[f'{reaction.guild.id}']['starboard']['channel'])
          except:
            return
          
          editor2 = editor.split(f"{message.id}-")[1].lstrip().split("+")[0]
          emoji_id = editor.split(f"{message.id}-{editor2}+")[1].lstrip().split("/")[0]
          emoji_name = editor.split(f"{message.id}-{editor2}+{emoji_id}/")[1].lstrip().split(",")[0]

          number = None
          reactions = str(message.reactions).split(",")
          for x in reactions:
            if str(emoji_id) in str(x):
              number = str(x).split("count=")[1].lstrip().split(">")[0]
              break

          if number != None:
            msg = message.guild.get_channel(find_channel).get_partial_message(int(editor2))
            await msg.edit(content=f"<:{emoji_name}:{emoji_id}> **{number}**")
            return
          else:
            return
      
      if f"count={counter}" in str(message.reactions):
        try:
          find_channel = int(get_db('guilds')[f'{reaction.guild.id}']['starboard']['channel'])
        except:
          return

        if message.channel.id == find_channel:
          return

        try:
          find_mes = get_db('guilds')[f'{reaction.guild.id}']['starboard_messages']
        except:
          find_mes = ""

        if str(message.id) in find_mes: 
          return
        
        content = None
        channel = message.guild.get_channel(find_channel)
        embed = discord.Embed(description=message.content, timestamp=message.created_at, color=member.color)
        embed.set_author(name=check_name(message.author), icon_url=message.author.avatar)
        embed.add_field(name="Source:", value=f"[Jump]({message.jump_url})")
        embed.set_footer(text=f"{message.id}")

        if message.attachments:
          if ".mp4" in str(message.attachments[0].url):
            content = f"{message.attachments[0].url}"
          elif ".mov" in str(message.attachments[0].url):
            content = f"{message.attachments[0].url}"
          else:
            embed.set_image(url=f"{message.attachments[0].url}")

        if message.stickers:
          embed.set_thumbnail(url=f"{message.stickers[0].url}")
        
        if "http" in message.content:
          if "/tenor.co" in str(message.content):
            content = f"{message.content}"
            pass
          elif "twitter.com" in str(message.content):
            content = f"{message.content}"
                              
          else:
            if " " in str(message.content):
              if ".mp4" in str(message.content):
                mes = str(message.content).split("http")[1].lstrip().split(' ')[0]
                content = f"http{mes}"
              elif ".mov" in str(message.content):
                mes = str(message.content).split("http")[1].lstrip().split(' ')[0]
                content = f"http{mes}"
              else:
                mes = str(message.content).split("http")[1].lstrip().split(' ')[0]
                embed.set_image(url=f"http{mes}")
            else:
              embed.set_image(url=f"{message.content}")
                
        msg2 = await channel.send(embed=embed, content=f"{reaction.emoji} **{counter}**")

        try:
          editor = get_db('guilds')[f'{message.guild.id}']['starboard_messages']
        except:
          update_db(f'guilds', f"{message.guild.id}", {"starboard_messages": f"{reaction.message.id}-{msg2.id}+{reaction.emoji.id}/{reaction.emoji.name},"})
        else:
          update_db(f'guilds', f"{message.guild.id}", {"starboard_messages": f"{editor}{reaction.message.id}-{msg2.id}+{reaction.emoji.id}/{reaction.emoji.name},"})

        if_100(message.guild.id)

        if content == None:
          return
        else:
          await channel.send(content)
  

def setup(client):
    client.add_cog(Starboard(client))