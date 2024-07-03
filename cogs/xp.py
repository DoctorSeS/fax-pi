from discord.ext import commands, tasks
import discord
import logging
import traceback
import asyncio
import datetime
import random
from random import randint
from main import client, bot_prefix, round_time, ses, currency, check_name, green, red, server_prefix
import fileinput
from discord.commands import slash_command
from discord import Option
from termcolor import cprint
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
import os
from cogs.score import check_currency
from database import *

def next_milestone(current):
  milestone = current + 10000
  milestone = int(str(milestone)[:-4]) * 10000
  return milestone
  
def add_time(time_add):
  current = datetime.datetime.now()
  add = datetime.timedelta(seconds=int(time_add))
  new_time = current + add

  return str(new_time)

class Xp(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.last_user = 0

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.guild:
      if not message.author.bot:

        #auto patreon #
        patron_check = list(get_db('misc')['all_patrons'])
        if str(message.author.id) in patron_check:
          pledge = get_db('misc')['all_patrons'][f'{message.author.id}']['pledge']
          if pledge == 1000:
            update_db('users', f"{message.author.id}", {f'role-{message.guild.id}': {"name": "Prophet", "multiplier": 2}})
          elif pledge == 500:
            update_db('users', f"{message.author.id}", {f'role-{message.guild.id}': {"name": "Daredevil", "multiplier": 1.75}})
          else:
            pass
        
        try:
          check_score = get_db('guilds')[f'{message.guild.id}']['score']
        except:
          return
        else:
          if check_score == False:
            return
          else:
            if self.last_user != message.author.id:
              try:
                guild_xp = get_db('guilds')[f'{message.guild.id}']['xp']
              except:
                update_db(f'guilds/{message.guild.id}', 'xp', {f"{message.author.id}": 0})

              current = datetime.datetime.now()
              last_talked = None
              try:
                last_talked = get_db('timers')[f'TimerXp-{message.author.id}={message.guild.id}']
              except:
                pass
              else:
                date_check = datetime.datetime.strptime(last_talked, '%Y-%m-%d %H:%M:%S.%f')
              if last_talked:
                if not current < date_check:
                  return
                else:
                  pass
              else:
                self.last_user = message.author.id

                try:
                  booster = get_db('users')[f'{message.author.id}']['xpbooster']
                except:
                  booster = 0

                try:
                  multiplier = float(get_db('users')[f'{message.author.id}'][f'role-{message.guild.id}']['multiplier'])
                except:
                  multiplier = 1

                edited_msg = str(message.content).replace(" ", "")
                if "https" in message.content:
                  edited_msg = "link"

                boost = 1
                if int(booster) > 0:
                  update_db('users', f'{message.author.id}', {"xpbooster": int(booster) - 1})
                  boost = 2
                calculated_score = round(((len(edited_msg) * round(random.uniform(0.75, 1.00), 1) * multiplier) * boost))

                try:
                  xp = get_db('users')[f'{message.author.id}'][f'xp-{message.guild.id}']
                except:
                  xp = 0
                finally:
                  final_xp = int(xp) + calculated_score
                  seconds = 120
                  update_db(f'timers',f'none' , {f"TimerXp-{message.author.id}={message.guild.id}": add_time(seconds)})
                  update_db(f'users',f'{message.author.id}' , {f"xp-{message.guild.id}": final_xp})

                  reward = None
                  the_next = next_milestone(int(xp))
                  if (final_xp >= 10000) and (int(xp) < 10000):
                    reward = "The Common Role (1.1x)"
                    update_db('users', f"{message.author.id}", {f'role-{message.guild.id}': {"name": "Common", "multiplier": 1.1}})
                  elif (final_xp >= 20000) and (int(xp) < 20000):
                    reward = "The Uncommon Role (1.2x)"
                    update_db('users', f"{message.author.id}", {f'role-{message.guild.id}': {"name": "Uncommon", "multiplier": 1.2}})
                  elif (final_xp >= 30000) and (int(xp) < 30000):
                    reward = "The Rare Role (1.3x)"
                    update_db('users', f"{message.author.id}", {f'role-{message.guild.id}': {"name": "Rare", "multiplier": 1.3}})
                  elif (final_xp >= 40000) and (int(xp) < 40000):
                    reward = "The Legendary Role (1.4x)"
                    update_db('users', f"{message.author.id}", {f'role-{message.guild.id}': {"name": "Legendary", "multiplier": 1.4}})
                  elif (final_xp >= 50000) and (int(xp) < 50000):
                    reward = "The Exotic Role (1.5x)"
                    update_db('users', f"{message.author.id}", {f'role-{message.guild.id}': {"name": "Exotic", "multiplier": 1.5}})
                  elif (final_xp >= next_milestone(int(xp))) and (int(xp) < next_milestone(int(xp))):
                    try:
                      score = get_db('user')[f'{message.author.id}'][f'xp-{message.guild.id}']
                    except:
                      score = 0

                    reward = int(the_next / 40)
                    final_reward = int(score) + reward
                    reward = f"{reward} {check_currency(message.guild.id)}"
                    update_db(f'users',f'{message.author.id}' , {f"xp-{message.guild.id}": final_reward})

                  if reward:
                    embed = discord.Embed(description=f"```ps\nYou have been rewarded with {reward} due to reaching {the_next} Xp.```\n\nYou can check your profile in **`{message.guild}`** by invoking `{server_prefix(message.guild.id)}profile`.", color=green)
                    embed.set_author(name=f"{message.guild}", icon_url=message.guild.icon)
                    await message.author.send(embed=embed, silent=True)


                  ### update leaderboard per server ###
                  update_db(f'guilds/{message.guild.id}', 'xp', {f"{message.author.id}": final_xp})

def setup(client):
  client.add_cog(Xp(client))