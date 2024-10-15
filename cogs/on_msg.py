import asyncio
import datetime
import random
import re
from random import randint

import discord
from discord.ext import commands

from database import *
from main import bot_prefix
from main import client
from main import ses

mess = 0
alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "'", "[", "]", "{", "}", ";", ":", '"', ",", "<", ".", ">", "/", "?", "|", "-", "_", "=", "+", "`", "~", "/", "*", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "A", "B", "C", 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ["0", '1', '2', '3', '4', '5', '6', '7', '8', '9']
currentDT = datetime.datetime.now()

def file_len():
  with open("ai.txt") as f:
    for i, l in enumerate(f):
      pass
  return i + 1

def letter(word):
  return [char for char in word]

def emoji(name):
  emoji2 = None
  num = 0
  while emoji2 == None:
    server = client.get_guild(client.guilds[num].id)
    emoji2 = discord.utils.get(server.emojis, name=name)
    num += 1
  else:
    return emoji2


class On_msg(commands.Cog):
  def __init__(self, client):
    self.client = client
    global nm4, words3, words4

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
  
  @commands.Cog.listener()
  async def on_message(self, message):
    ### Golila ###
    num = randint(1, 10000)
    if num == 1:
      server = client.get_guild(715956039182319637)
      emoji = discord.utils.get(server.emojis, name="golira")
      await message.add_reaction(emoji) 
      pass
    ### aritificial intelligence lol ###
    #collect messages
    if message.guild:
      if str(message.guild.id) in get_db('misc')['ai_collect_servers']:
        if not ("@everyone" in message.content) and not ("@here" in message.content) and not ("@here" in message.content) and not ("<@&" in message.content) and not (message.author.bot) and not (bot_prefix in message.content):
          with open('ai.txt', "a", encoding='utf-8') as f:
            if message.attachments:
              text = f"{message.content}\n{message.attachments[0].url}\n"
            else:
              text = f"{message.content}\n"

            f.write(f"{text}")
            f.close()
            pass

      #send messages
      try:
        value = get_db('guilds')['ai']
      except:
        pass
      else:
        if value.get("active") is not None:
          if value["active"] is True:
            chance = 0
            if value.get("channels") is not None:
              if value["channels"].get(f"{message.channel.id}") is not None:
                if value.get('advanced') is not None:
                  if value.get('advanced') is True:
                    chance = int(value["channels"][f"{message.channel.id}"])
              else:
                chance = 0
            else:
              if value.get("global_chance") is not None:
                chance = int(value["global_chance"])
              else:
                chance = 1
                update_db(f'guilds/{message.guild.id}', f"ai", {"global_chance": chance})

            if chance != 0:
              final_chance = randint(1, 100)
              if final_chance <= chance:
                with open('ai.txt', "r") as f:
                  random_line = random.choice(f.readlines())
                  f.close()
                try:
                  await message.channel.send(random_line)
                except:
                  pass
        
          
  
    ### nickname check ###
    if message.guild is not None:
      try:
        guild_data = get_db('guilds')[str(message.guild.id)]
      except:
        return
      else:
        if guild_data.get('nick') is True:
          user = message.guild.get_member(message.author.id)
          if user is None:
            return
          name = str(user.name)
          name2 = name.strip()
          nick = str(user.nick)
          nick2 = nick.strip()
          numb = randint(0, 1000)
          stringname = letter(name2)
          stringnick = letter(nick2)
          if name == nick:
            for let in stringname:
              if let in alpha:
                break
              else:
                await message.author.edit(nick=f"Unpingable Name #{numb}", reason="Non-Latin Name.")
                break
            else:
              pass
          else:
            for let in stringnick:
              if let in alpha:
                break
              else:
                for let in stringname:
                  if let in alpha:
                    break
                  else:
                    await message.author.edit(nick=f"Unpingable Name #{numb}", reason="Non-Latin Name.")
                    break
  
  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.is_owner()
  async def aicollect(self, ctx):
    update_db('misc', 'none', {'ai_collect_servers': f"{get_db('misc')['ai_collect_servers']}{ctx.guild.id},"})
    embed = discord.Embed(description=f"The bot is collecting messages from the following servers:\n{get_db('misc')['ai_collect_servers']}")
    await ctx.send(embed=embed, content=None)

  @commands.command(aliases=['msgs', 'mes'])
  @commands.before_invoke(disabled_check)
  @commands.has_permissions(manage_messages=True)
  async def messages(self, ctx):
    embed = discord.Embed(title=f"Total Messages:", description=f"From {len(client.guilds)} guilds.", color=0x58ab55, timestamp=currentDT)
    embed.add_field(name="`Count:`", value=f"**`{mess}`** messages")
    embed.set_footer(text="Last restart:", icon_url=client.user.avatar)
    await ctx.send(embed=embed, content=None)

  @commands.command(aliases=['speak'])
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 30, commands.BucketType.guild)
  async def talk(self, ctx, shit: str=None):
    global nm2, words
    rand = randint(0, file_len())
    lines = open("ai.txt", "r").readlines() 
    chan = ctx.message.channel
    line = lines[rand]
    if shit == None:
      async with ctx.message.channel.typing():
        await asyncio.sleep(2)
        await ctx.message.channel.send(line)
        nm2 = 0
        words.clear()
    else:
      for line2 in lines:
        if re.search(f'{shit}', line2):
          if line2 in words:
            async with chan.typing():
              number = nm2 - 1
              words2 = randint(0, number)
              await asyncio.sleep(2)
              await chan.send(words[words2])
              nm2 = 0
              words.clear()
              break
          else:
            line3 = str(line2)
            words.append(line3)
            nm2 += 1

  @commands.command(aliases=['you', "are you", 'are'])
  @commands.cooldown(1, 30, commands.BucketType.guild)
  async def ok(self, ctx):
    await ctx.invoke(self.client.get_command('talk'))

          
def setup(client):
  client.add_cog(On_msg(client))
