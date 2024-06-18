import discord
from discord.ext import commands, tasks
from random import randint
import asyncio
import datetime
from datetime import date
from main import client, bot_prefix, currentDT, ses, red, green, check_name
from discord import slash_command
from termcolor import colored, cprint
import os
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
from discord.ui import InputText, Modal
from database import *


logs = 639513264522526769
channels2 = []

def add_time(time_add):
  current = datetime.datetime.now()
  add = datetime.timedelta(hours=int(time_add))
  new_time = current + add

  return new_time

def anti_raid(member, guild):
  date1 = member.created_at
  date1 = str(date1).split(" ")[0]
  date2 = datetime.datetime.now()
  date2 = str(date2).split(" ")[0]
  try:
    value = get_db("guilds")[f'{guild}']['raid']
  except:
    return "False"
  else:
    if bool(value['active']) is False:
      return "False"

    date1a = date1.split("-")
    date2a = date2.split("-")

    d1 = date(int(date1a[0]), int(date1a[1]), int(date1a[2]))
    d2 = date(int(date2a[0]), int(date2a[1]), int(date2a[2]))

    if d1 == d2:
      return "True Kick"
    else:
      delta = d2 - d1
      days = delta.days
      days2 = int(value['days'])
      if int(days) < days2:
        return "True"
      else:
        return "False"

def fixtime(dt):
  dt2 = str(dt)
  timelen = len(dt2)

  dt = dt2[:timelen - 13]
  return dt

def checkwm(serverid, channelid):
  try:
    value = get_db('guilds')[f'{serverid}']['welcome_message']
  except:
    update_db(f'guilds/{serverid}', f"welcome_message", {"active": True, "channel": f"{channelid}", "message": f"Welcome to [server], [member.mention].\nEnjoy your stay and please read the rules.", "image": None})
    return

def check_logs(guild):
  logs = [False, "None", "None"]
  try:
    value = get_db('guilds')[f"{guild}"]['logs']
  except:
    return logs
  else:
    try:
      logs[0] = value['active']
    except:
      pass

    try:
      logs[1] = value['logs1']
    except:
      pass

    try:
      logs[2] = value['logs2']
    except:
      pass

    return logs

class Events(commands.Cog):
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
  
  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    data = {'text_channels': len(guild.text_channels), 'voice_channels': len(guild.voice_channels), 'members': guild.member_count, "roles": len(guild.roles)}
    update_db('guilds', f'{guild.id}', data)

    serv = str(guild.id)
    l1 = discord.utils.get(guild.channels, name="logs")
    l2 = discord.utils.get(guild.channels, name="logs-the-second")
    rle = guild.get_member(client.user.id)
    ctg = discord.utils.get(guild.categories, name="bot staff")
    if ctg == None:
      global category
      category = await guild.create_category(name="bot staff")
      await category.set_permissions(guild.default_role, read_messages=False)
      await category.set_permissions(rle, send_messages=True, read_messages=True, manage_messages=True, embed_links=True, attach_files=True, read_message_history=True)
      pass
    else:
      pass
    if l1 == None:
      log = await guild.create_text_channel(name="logs", category=category)
      await log.set_permissions(guild.default_role, read_messages=False)
      await log.set_permissions(rle, send_messages=True, read_messages=True, manage_messages=True, embed_links=True, attach_files=True, read_message_history=True)
      pass
    else:
      pass
    if l2 == None:
      log2 = await guild.create_text_channel(name="logs-the-second", category=category)
      await log2.set_permissions(guild.default_role, read_messages=False)
      await log2.set_permissions(rle, send_messages=True, read_messages=True, manage_messages=True, embed_links=True, attach_files=True, read_message_history=True)
      pass
    else:
      pass
      
    l1 = discord.utils.get(guild.channels, name="logs")
    l2 = discord.utils.get(guild.channels, name="logs-the-second")
    rle = guild.get_member(client.user.id)
    ctg = discord.utils.get(guild.categories, name="bot staff")
    update_db(f'guilds/{serv}', 'logs', {"logs1": str(l1.id), "logs2": str(l2.id)})
  
  @commands.Cog.listener()
  async def on_interaction(self, interaction):
    button_final = int(get_db('misc')['buttons']) + 1
    update_db('misc', 'none', {"buttons": button_final})

    try:
      if interaction.user.guild is not None:
        if check_logs(interaction.user.guild.id)[0] is True:
          logs2 = check_logs(interaction.user.guild.id)[2]
          if logs2 != "None":
            if str(interaction.type) == "InteractionType.application_command":
              try:
                logs2 = discord.utils.get(interaction.message.guild.channels, id=int(logs2))
                embed = discord.Embed(description=f"Command used in <#{interaction.message.channel.id}>.\n[Jump to the message]({interaction.message.jump_url})", color=discord.Color.random(), timestamp=interaction.message.created_at)
                embed.add_field(name=f'Command used:', value=f"{interaction.message.content}")
                embed.set_author(name=f"{interaction.user} • ID: {interaction.user.id}", icon_url=interaction.message.author.avatar)
                embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)
                await logs2.send(embed=embed, content=None)
              except:
                return
    except:
      return

  @commands.Cog.listener()
  async def on_guild_unavailable(self, guild):
    ses2 = client.get_user(ses)
    try:
      global unguilds
      unguilds += 1
      embed = discord.Embed(description=f"Guild {guild.name} • ID: {guild.id} has become unavailable.\n`Reason:` Unknown.", timestamp=currentDT)
      embed.set_footer(text="Last restart:", icon_url=client.user.avatar)
      await ses2.send(embed=embed, content=None)
    except discord.HTTPException as error:
      embed = discord.Embed(description=f"**`Error:`**\n```python\n{error}```", timestamp=currentDT)
      embed.set_footer(text="Last restart:", icon_url=client.user.avatar)
      await ses2.send(embed=embed, content=None)
  
  @commands.Cog.listener()
  async def on_member_join(self, member):
    update_db('guilds', f'{member.guild.id}', {'members': member.guild.member_count})
    date1 = member.created_at
    date1 = str(date1).split(" ")[0]
    if "True" in anti_raid(member, member.guild.id):
      if "Kick" in anti_raid(member, member.guild.id):
        embed = discord.Embed(title=f"You have been kicked from {member.guild}", description="Due to anti-raid detection, your accounts needs to be at least one day old to join.", color=red)
        await member.send(embed=embed, content=None)
        await member.kick(reason=f"Account was created today ({date1}), Anti-raid function invoked.")
        return
      else:
        embed = discord.Embed(title=f"You have been timed out on {member.guild}", description="Your account has invoked the anti-raid function, which timed you out for one hour.\n\nYou can wait this out or contact a moderator about it if you are not a threat to the server.", color=red)
        await member.send(embed=embed, content=None)
        await member.timeout(until=add_time(1), reason=f"Account was created on {date1}, Anti-raid function invoked.")
        pass

    try:
      value = get_db('guilds')[f'{member.guild.id}']['welcome_message']
    except:
      return
    else:
      if 'active' in value:
        if value['active'] is True:

          if 'channel' in value:
            chan = value['channel']
          else:
            return

          try:
            wm_channel = member.guild.get_channel(int(chan))
          except:
            return
          else:
            if 'message' in value:
              mess = value['message']
            else:
              mess = "Welcome to [server], [member.mention]."

            if 'image' in value:
              image = value['image']
            else:
              image = None

            if 'color' in value:
              color = str(value['color']).replace('#', "0x")
            else:
              color = discord.Color.random()

            to_change = ['[member.mention]', '[member.id]', '[member.name]', '[server]']
            change_to = [f'{member.mention}', f'{member.id}', f'{member.name}', f'{member.guild}']

            for x in to_change:
              index = to_change.index(x)
              mess = mess.replace(x, change_to[index])

            welcome = discord.Embed(title="New Member!", description=f"{mess}", color=color)
            welcome.set_footer(text=f"{member} • ID: {member.id}", icon_url=member.avatar)
            if image != "None":
              welcome.set_image(url=f"{image}")

            await wm_channel.send(embed=welcome, content=None)
            await wm_channel.send(member.mention, delete_after=0.1)

    logs_global = list(check_logs(member.guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        channel2 = discord.utils.get(member.guild.channels, id=int(logs_global[1]))

        if channel2:
          logger = discord.Embed(title="New Member.", description=f"{member.mention} - {member}")
          logger.set_thumbnail(url=member.avatar)
          logger.set_author(name=f"ID: {member.id}", icon_url=member.avatar)
          await channel2.send(embed=logger, content=None)
  

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    update_db('guilds', f'{member.guild.id}', {'members': member.guild.member_count})
    logs_global = list(check_logs(member.guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(member.guild.channels, id=int(logs_global[1]))
        except:
          return

        embed = discord.Embed(description=f'{member.mention} left the server.', color=discord.Color.random(), timestamp=member.created_at)
        embed.set_footer(text=f'{member} • ID: {member.id}', icon_url=f"{member.avatar}")
        await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_member_ban(self, guild, user):
    logs_global = list(check_logs(guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(guild.channels, id=int(logs_global[1]))
        except:
          return

        async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=1, oldest_first=False):
          embed = discord.Embed(description=f'{user.mention} has been **banned** from the server.', color=discord.Color.from_rgb(r=randint(1, 255), g=randint(1, 255),b=randint(1, 255)))
          embed.set_author(name=f'{user} • ID: {user.id}', icon_url=user.avatar)
          embed.set_footer(text=f"Banned by {entry.user} • ID: {entry.user.id}", icon_url=entry.user.avatar)
          await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_member_unban(self, guild, user):
    logs_global = list(check_logs(guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(guild.channels, id=int(logs_global[1]))
        except:
          return

        async for entry in guild.audit_logs(action=discord.AuditLogAction.unban, limit=1, oldest_first=False):
          embed = discord.Embed(description=f'{user.mention} has been **unbanned** from the server.', color=discord.Color.random())
          embed.set_author(name=f'{user} • ID: {user.id}', icon_url=user.avatar)
          embed.set_footer(text=f"Unbanned by {entry.user} • ID: {entry.user.id}", icon_url=entry.user.avatar)
          await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_guild_channel_create(self, channel):
    update_db('guilds', f'{channel.guild.id}', {'text_channels': len(channel.guild.text_channels)})
    update_db('guilds', f'{channel.guild.id}', {'voice_channels': len(channel.guild.voice_channels)})
    logs_global = list(check_logs(channel.guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(channel.guild.channels, id=int(logs_global[1]))
        except:
          return

        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_create, limit=1, oldest_first=False):
          embed = discord.Embed(description=f'<#{channel.id}> has been created.\nID: {channel.id}', color=discord.Color.random(), timestamp=channel.created_at)
          embed.set_footer(text=f'Created by {entry.user} • ID: {entry.user.id}', icon_url=entry.user.avatar)
          await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_guild_channel_delete(self, channel):
    update_db('guilds', f'{channel.guild.id}', {'text_channels': len(channel.guild.text_channels)})
    update_db('guilds', f'{channel.guild.id}', {'voice_channels': len(channel.guild.voice_channels)})
    logs_global = list(check_logs(channel.guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(channel.guild.channels, id=int(logs_global[1]))
        except:
          return

        async for entry in channel.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1, oldest_first=False):
          embed = discord.Embed(description=f'`#{channel}` has been deleted.\nID: {channel.id}', color=discord.Color.random(), timestamp=channel.created_at)
          embed.set_footer(text=f'Deleted by {entry.user} • ID: {entry.user.id}', icon_url=f"{entry.user.avatar}")
          await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_guild_channel_update(self, before, after):
    logs_global = list(check_logs(before.guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(before.guild.channels, id=int(logs_global[1]))
        except:
          return

        if before == after:
          return
        else:
          if before != None:
            async for entry in before.guild.audit_logs(action=discord.AuditLogAction.channel_update, limit=1, oldest_first=False):
              embed = discord.Embed(description=f"<#{before.id}> has been updated.", color=discord.Color.random(), timestamp=before.created_at)
              embed.set_footer(text=f'Edited by {entry.user} • ID: {entry.user.id}', icon_url=entry.user.avatar)
              embed.add_field(name=f"Before:", value=f"`Name:` {before}\n`ID:` {before.id}\n`Position:` {before.position}\n`Slowmode delay:` {before.slowmode_delay}\n`Category:` {before.category}")
              embed.add_field(name=f"After:", value=f"`Name:` {after}\n`ID:` {after.id}\n`Position:` {after.position}\n`Slowmode delay:` {after.slowmode_delay}\n`Category:` {after.category}")
              await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    if message.author.bot is False:
      if message.content.startswith(f"{bot_prefix}"):
        return
      else:
        if message.guild != None:
          try:
            server = client.get_guild(message.guild.id)
          except:
            return
          mess = str(message.content)
          mess2 = mess.lower()

          embed = discord.Embed(description=f'A message in {message.channel.mention} has been deleted.\n[Jump to the message]({message.jump_url})\n**Content:** {message.content}', color=0xc40000, timestamp=message.created_at)
          embed.set_author(name=f'{check_name(message.author)} • ID:{message.author.id}', icon_url=f"{message.author.display_avatar}")
          
          if message.content.startswith(":"):
            if message.content.endswith(":"):
              return
            else:
              pass

          elif message.attachments:
            embed = discord.Embed(description=f'A message in {message.channel.mention} has been deleted.\n[Jump to the message]({message.jump_url})\n**Content:** {message.attachments[0].proxy_url}', color=0xc40000, timestamp=message.created_at)
            embed.set_author(name=f'{check_name(message.author)} • ID:{message.author.id}', icon_url=message.author.display_avatar)
            embed.set_image(url=message.attachments[0].proxy_url)
            update_db(f'minigames/snipe/{message.guild.id}', f"{message.channel.id}",  {"name": f"{message.author.display_name}", "id": f"{message.author.id}", "avatar": f"{message.author.display_avatar}", "time": f"{datetime.datetime.now()}", "message": f"{message.content}\n{message.attachments[0].proxy_url}"})

          else:
            update_db(f'minigames/snipe/{message.guild.id}', f"{message.channel.id}",  {"name": f"{message.author.display_name}", "id": f"{message.author.id}", "avatar": f"{message.author.display_avatar}", "time": f"{datetime.datetime.now()}", "message": f"{message.content}"})


          logs_global = list(check_logs(message.guild.id))
          if logs_global[0] is True:
            if logs_global[1] != "None":
              try:
                channel = discord.utils.get(message.guild.channels, id=int(logs_global[1]))
              except:
                return

              await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_reaction_clear(self, message, reactions: discord.Emoji):
    logs_global = list(check_logs(message.guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(message.guild.channels, id=int(logs_global[1]))
        except:
          return

        channel2 = discord.utils.get(message.guild.channels, id=message.channel.id)
        embed = discord.Embed(description=f'Reactions removed from a message in <#{channel2.id}> • Message ID: {message.id}\n[Jump to the message](https://discordapp.com/channelsᚋ{message.guild.id}ᚋ{channel2.id}ᚋ{message.id})', color=discord.Color.random(), timestamp=message.created_at)
        embed.add_field(name='Reactions removed:', value=f'{reactions}')
        embed.set_footer(text=f'Message Author: {message.author} • ID: {message.author.id}')
        embed.set_author(name=f'{message.author} • ID:{message.author.id}', icon_url=message.author.avatar)
        await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_message_edit(self, before, after):
    if before.guild != None:
      logs_global = list(check_logs(before.guild.id))
      if logs_global[0] is True:
        if logs_global[1] != "None":
          try:
            channel = discord.utils.get(before.guild.channels, id=int(logs_global[1]))
          except:
            return

          if before.author.bot is False:
            if before.guild != None:
              if "http" in before.content:
                return
              else:
                if before.content != after.content:
                  embed = discord.Embed(description=f"**A message has been edited in {before.channel.mention}.**\n[Jump to the message]({after.jump_url})", color=0x0023e8, timestamp=after.created_at)
                  embed.set_author(name=f'{before.author} • ID:{before.author.id}', icon_url=before.author.avatar)
                  embed.set_footer(text=f"Message ID: {before.id}")
                  embed.add_field(name='Before:', value=before.content + "\u200b")
                  embed.add_field(name="After:", value=after.content + "\u200b")
                  await channel.send(embed=embed, content=None)
                  if after.content.startswith(f"{bot_prefix}"):
                    await client.process_commands(after)
                  elif after.content.startswith(f"G!"):
                    await client.process_commands(after)
                  elif after.content.startswith(f"<@!{client.user.id}>"):
                    await client.process_commands(after)

  @commands.Cog.listener()
  async def on_guild_role_create(self, role):
    update_db('guilds', f'{role.guild.id}', {"roles": len(role.guild.roles)})
    logs_global = list(check_logs(role.guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(role.guild.channels, id=int(logs_global[1]))
        except:
          return

        async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_create, limit=1, oldest_first=False):
          embed = discord.Embed(description=f'<@&{role.id}> has been created.\nID: {role.id}', color=role.color, timestamp=role.created_at)
          embed.set_footer(text=f"Created by {entry.user} • ID: {entry.user.id}", icon_url=entry.user.avatar)
          await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_guild_role_delete(self, role):
    update_db('guilds', f'{role.guild.id}', {"roles": len(role.guild.roles)})
    logs_global = list(check_logs(role.guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(role.guild.channels, id=int(logs_global[1]))
        except:
          return

        async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_delete, limit=1, oldest_first=False):
          embed = discord.Embed(description=f'`@{role}` has been deleted.', color=role.color, timestamp=role.created_at)
          embed.set_footer(text=f'Role ID: {role.id}')
          embed.set_footer(text=f"Deleted by {entry.user} • ID: {entry.user.id}", icon_url=entry.user.avatar)
          await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_guild_update(self, before, after):
    logs_global = list(check_logs(before.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(before.channels, id=int(logs_global[1]))
        except:
          return

        async for entry in before.audit_logs(action=discord.AuditLogAction.guild_update, limit=1, oldest_first=False):
          embed = discord.Embed(description=f'**The server has been edited.**', color=discord.Color.random(), timestamp=after.created_at)
          embed.set_footer(text=f"Edited by {entry.user} • ID: {entry.user.id}\nServer ID: {before.id}", icon_url=entry.user.avatar)
          embed.add_field(name='Before:', value=f'`Name:` **{before}**\n`VL:` **{before.verification_level}**\n`Boosts:` **{before.premium_subscription_count}**')
          embed.add_field(name='After:', value=f'`Name:` **{after}**\n`VL:` **{after.verification_level}**\n`Boosts:` **{after.premium_subscription_count}**')
          embed.set_thumbnail(url=after.icon.url)
          await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_invite_create(self, invite):
    logs_global = list(check_logs(invite.guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(invite.guild.channels, id=int(logs_global[1]))
        except:
          return

        embed = discord.Embed(description=f"**A new invite has been created.**", color=discord.Color.random(), timestamp=invite.created_at)
        embed.set_footer(text=f'Invite created by {invite.inviter}\n{invite.url}', icon_url=invite.inviter.avatar)
        embed.add_field(name=f'Invite properties:', value=f"`Code:` {invite.code}\n`Channel:` {invite.channel}\n`Time left:` {invite.max_age} seconds\n`Max uses:` {invite.max_uses}", inline=False)
        await channel.send(embed=embed, content=None)

  @commands.Cog.listener()
  async def on_invite_delete(self, invite):
    logs_global = list(check_logs(invite.guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(invite.guild.channels, id=int(logs_global[1]))
        except:
          return

        embed = discord.Embed(description=f"**An invite has been deleted.**", color=discord.Color.random())
        embed.set_footer(text=f'Invite link: {invite.url}')
        embed.add_field(name=f'Invite properties:', value=f"`Code:` {invite.code}\n`Channel:` {invite.channel}\n`Time left:` {invite.max_age} seconds\n`Max uses:` {invite.max_uses}\n`Uses:` {invite.uses}", inline=False)
        await channel.send(embed=embed, content=None)

  @commands.command()
  @commands.before_invoke(disabled_check)
  async def snipe(self, ctx):
    try:
      msg = get_db('minigames')['snipe'][f'{ctx.guild.id}'][f'{ctx.channel.id}']
    except:
      embed = discord.Embed(description=f"There's nothing to snipe.")
      await ctx.send(embed=embed, content=None, delete_after=10)
    else:
      embed = discord.Embed(description=f"{msg['message']}")
      embed.set_author(name=f"{msg['name']} • ID: {msg['id']}", icon_url=f"{msg['avatar']}")
      embed.set_footer(text=f"Message sent at: {msg['time']}")
      del_db(f'minigames/snipe/{ctx.guild.id}', f'{ctx.channel.id}')

      await ctx.send(embed=embed, content=None)

  @slash_command(name='snipe', description="Snipe the latest deleted message from the current server.")
  async def snipe_slash(self, ctx):
    try:
      msg = get_db('minigames')['snipe'][f'{ctx.guild.id}'][f'{ctx.channel.id}']
    except:
      embed = discord.Embed(description=f"There's nothing to snipe.")
      await ctx.send(embed=embed, content=None, delete_after=10)
    else:
      embed = discord.Embed(description=f"{msg['message']}")
      embed.set_author(name=f"{msg['name']} • ID: {msg['id']}", icon_url=f"{msg['avatar']}")
      embed.set_footer(text=f"Message sent at: {msg['time']}")
      del_db(f'minigames/snipe/{ctx.guild.id}', f'{ctx.channel.id}')

      await ctx.respond(embed=embed, content=None)
      pass

    logs_global = list(check_logs(ctx.guild.id))
    if logs_global[0] is True:
      if logs_global[1] != "None":
        try:
          channel = discord.utils.get(ctx.guild.channels, id=int(logs_global[1]))
        except:
          return

        embed = discord.Embed(description=f"Slash Command used in <#{ctx.channel.id}>.", color=discord.Color.random())
        embed.add_field(name=f'Command used:', value=f"/snipe")
        embed.set_author(name=f"{ctx.author} • ID: {ctx.author.id}", icon_url=ctx.author.avatar)
        embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)
        await channel.send(embed=embed, content=None)

def setup(client):
  client.add_cog(Events(client))
