import discord
from discord.ext import commands, tasks
import logging
import traceback
from random import randint
from main import client, currentDT, bot_prefix, ses, red, green, site_link
import difflib
import random
from termcolor import cprint
from database import *

def check_patron(user_id):
  patrons = get_db('misc')['all_patrons']
  if int(user_id) == ses:
    return True
  
  elif str(user_id) in patrons:
    pledge = patrons[str(user_id)]["pledge"]
    if int(pledge) > 100:
      return True
    else:
      return False
  else:
    return False

class Errors(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.command_list.start()

  @tasks.loop(hours=10)
  async def command_list(self):
    commands = [c.name for c in client.commands]
    remove_comms = ["embedtest", "emp", "gc", "rate", "perms", "view_test", "add_badge", "gbchat", "gbchat_select", "dbvalue", "dbpref", "dbdelete", "dbadd", "dbkeys", "channel_select", "choose_the_welcome", "extend_shorten_time", "lastMessage", "ai_selection", "aicollect", "dm", "say", "globalsay", "wipe", "cmd", "killswitch", "humble", "suggestionban", "suggestionunban", "msgdata", "leave", "shutdown", "reload", "load", "unload", "cogs", "servers", "botreply", "channels", "restart", "move", "servunmute", "helpcounter", "messages", "roles", "nick_change", "patrons", "starboard_settings", "read", "join", "calc", "fax", "dbmassdel", "print", "ok", "comms"]
    for word in remove_comms:
      try:
        commands.remove(word)
      except:
        pass
      else:
        pass
    else:
      commandsfinal = str(commands)
      update_db('misc', 'none', {"all_commands": commandsfinal})
      return

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
  async def on_command_completion(self, ctx):
    comm = ctx.command.name
    value = get_db('misc')['all_used_commands']
    if str(comm) in value:
      try:
        number = value.split(f"{comm}:")[1].lstrip().split(",")[0]
      except:
        pass
      else:
        replacement = value.replace(f"{comm}:{number}", f"{comm}:{int(number) + 1}")
        update_db('misc', "none", {"all_used_commands": str(replacement)})
        pass
    else:
      update_db('misc', "none", {"all_used_commands": f"{value}{comm}:1,"})
      pass
      
    try:
      value = get_db("guilds")[f'{ctx.guild.id}']['logs']['logs2']
    except:
      return
    else:
      global comms2
      embed = discord.Embed(description=f"Command used in {ctx.channel.mention}.\n[Jump to the message]({ctx.message.jump_url})", color=0x038211, timestamp=ctx.message.created_at)
      embed.add_field(name=f'Command used:', value=f"{ctx.message.content}")
      embed.set_author(name=f"{ctx.author} • ID: {ctx.author.id}", icon_url=ctx.author.avatar)
      embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)

      logs2 = ctx.guild.get_channel(int(value))
      try:
        await logs2.send(embed=embed, content=None)
        comms2 += 1
      except:
        return
      else:
        return

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    msg = ctx.message
    if isinstance(error, commands.MissingRequiredArgument):
      if f"mute" in ctx.command.name:
        return
      elif f"dm" in ctx.command.name:
        return
      elif f"purge" in ctx.command.name:
        return
      elif f"say" in ctx.command.name:
        return
      elif f"lock" in ctx.command.name:
        return
      elif f"role" in ctx.command.name:
        return
      else:
        embed = discord.Embed(description=f"**`ERROR:`** ```python\nMissing required arguments.\n```", color=red)
        await msg.delete(delay=5)
        await ctx.send(embed=embed, content=None, delete_after=10)
        ctx.command.reset_cooldown(ctx)

    elif isinstance(error, commands.CommandNotFound):
      words = str(get_db('misc')["all_commands"]).split(",")
      command = ctx.message.content[2:]
      closest = difflib.get_close_matches(command, words)
      
      if "[]" in str(closest):
        mean = ""
      else:
        mean = f'\nDid you mean: "{random.choice(closest)}"?'
      embed = discord.Embed(description=f"**`ERROR:`** ```python\nInvalid command.\n{mean}```", color=red)
      await ctx.send(embed=embed, content=None, delete_after=10)

    elif isinstance(error, commands.CommandOnCooldown):
      if check_patron(ctx.author.id) == True:
        ctx.command.reset_cooldown(ctx)
        try:
          await ctx.invoke(client.get_command(f"{ctx.command}"))
        except:
          return
        else:
          return
      
      time = error.retry_after
      time2 = round(time)
      embed = discord.Embed(description=f"**`ERROR:`** ```python\nThe '{ctx.command}' command is on cooldown.\nTime left: {time:.2f} seconds.\n```", color=red)
      if time2 > 20:
        await msg.delete(delay=5)
        await ctx.send(embed=embed, content=None, delete_after=10)
      else:
        await msg.delete(delay=time2)
        await ctx.send(embed=embed, content=None, delete_after=time2)

    elif isinstance(error, commands.MissingPermissions):
      embed = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you do not have the required permissions to execute the '{ctx.command}' command.\n```", color=red)
      await msg.delete(delay=5)
      await ctx.send(embed=embed, content=None, delete_after=10)
      ctx.command.reset_cooldown(ctx)

    elif isinstance(error, commands.BotMissingPermissions):
      embed = discord.Embed(description=f"**`ERROR:`** ```python\nThe bot is missing the required permissions to execute the `{ctx.command}` command.\n```", color=red)
      await msg.delete(delay=5)
      await ctx.send(embed=embed, content=None, delete_after=10)
      ctx.command.reset_cooldown(ctx)

    elif isinstance(error, commands.DisabledCommand):
      embed = discord.Embed(description=f"**`ERROR:`** ```python\nThe '{ctx.command}' command is disabled.\n```", color=red)
      await msg.delete(delay=5)
      await ctx.send(embed=embed, content=None, delete_after=10)

    elif isinstance(error, commands.NoPrivateMessage):
      try:
        embed = discord.Embed(description=f"**`ERROR:`** ```python\nThe '{ctx.command}' command cannot be used in Private Messages.\n```", color=red)
        await ctx.author.send(embed=embed, content=None)
      except discord.HTTPException:
        pass
    elif isinstance(error, commands.TooManyArguments):
      embed = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you passed too many arguments for the '{ctx.command}' command.\n```", color=discord.Color.from_rgb(r=255, g=0, b=0))
      await msg.delete(delay=5)
      await ctx.send(embed=embed, content=None, delete_after=10)
      ctx.command.reset_cooldown(ctx)

    elif isinstance(error, commands.UserNotFound):
      embed = discord.Embed(description=f"**`ERROR:`** ```python\n{error}\n```", color=red)
      await msg.delete(delay=5)
      await ctx.send(embed=embed, content=None, delete_after=10)
      ctx.command.reset_cooldown(ctx)

    elif isinstance(error, commands.EmojiNotFound):
      if f"{bot_prefix}e" in ctx.message.content:
        return
      else:
        embed = discord.Embed(description=f"**`ERROR:`** ```python\n{error}\n```", color=red)
        await msg.delete(delay=5)
        await ctx.send(embed=embed, content=None, delete_after=10)
        ctx.command.reset_cooldown(ctx)

    elif isinstance(error, commands.NotOwner):
      embed = discord.Embed(description=f"**`ERROR:`** ```python\n{ctx.author.name}, you are not the owner of this bot.\n```", color=red)
      await msg.delete(delay=5)
      await ctx.send(embed=embed, content=None, delete_after=10)
      ctx.command.reset_cooldown(ctx)

    elif isinstance(error, commands.BadArgument):
      if f"{bot_prefix}e" in ctx.message.content:
        return
      else:
        embed = discord.Embed(description=f"**`ERROR:`** ```python\n{error}\n```", color=red)
        await msg.delete(delay=5)
        await ctx.send(embed=embed, content=None, delete_after=10)
        ctx.command.reset_cooldown(ctx)

    else:
      embed = discord.Embed(description=f"**`ERROR:`** ```md\n{error}```", color=red)
      await ctx.send(embed=embed, content=None, delete_after=10)
      ctx.command.reset_cooldown(ctx)

  @commands.command(aliases=['ping', 'statutus'])
  @commands.has_permissions(kick_members=True)
  async def bot(self, ctx):
    server = client.get_guild(ctx.message.guild.id)
    fax = client.get_user(client.user.id)
    ver = str(discord.version_info)
    ver2 = ver.replace("VersionInfo", '')
    ver3 = ver2.replace("(", "```python\n")
    ver4 = ver3.replace(")", '\n```')
    ver5 = ver4.replace("releaselevel", "\nreleaselevel")
    embed = discord.Embed(description=f"The bot is running.\n`Ping:` {round(client.latency * 1000)} ms\n`Guild:` {server}\n`Status:` [online]({site_link})\n`Version:` {discord.__version__}", color=discord.Color.from_rgb(r=0, g=randint(1, 255), b=0), timestamp=currentDT)
    embed.add_field(name=f"`Version Info:`", value=f"{ver5}")
    embed.set_footer(text=f'Last restart:', icon_url=fax.avatar)
    await ctx.send(embed=embed, content=None)

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def comms(self, ctx):
    value = get_db('misc')['all_used_commands']
    value2 = value.replace(",", "\n`")
    value3 = value2.replace(":", ":` ")
    embed = discord.Embed(description=f"**{comms2}** commands used.", color=discord.Color.from_rgb(r=0, g=randint(1, 255), b=0), timestamp=currentDT)
    embed.add_field(name="Total:", value=f"{value3}")
    embed.set_footer(text="Last restart:", icon_url=client.user.avatar)
    await ctx.send(embed=embed, content=None)


def setup(client):
    client.add_cog(Errors(client))
