from discord.ext import commands, tasks
import discord
import logging
import traceback
import asyncio
import datetime
import random
from random import randint
from main import client, bot_prefix, currentDT, round_time, ses, currency, check_name, green, red, server_prefix
import fileinput
from discord.commands import slash_command
from discord import Option
from termcolor import cprint
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
import os

from characterai import PyCAI

messages_channel = 983395530866585702

class Ai(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_message(self, message):
    if (message.guild is None) and (not message.author.bot):
      ### DM Detection in bot-channel-staff ###
      channel = client.get_channel(messages_channel)
      embed = discord.Embed(description=f"Message from {message.author.mention}:\n{message.content}", timestamp=message.created_at, color=0x37ff00)
      embed.set_author(icon_url=message.author.avatar, name=message.author)
      if message.content.startswith("https://"):
        embed.set_image(url=f'{message.content}')
      elif message.attachments:
        embed.set_image(url=message.attachments[0].proxy_url)

      await channel.send(embed=embed)


      if not bot_prefix in str(message.content).lower(): 
        if message.author.id == 645660675334471680:
          ch_client = PyCAI(os.getenv('C.AI_TOKEN'))
          char = os.getenv('C.AI_FAX')
    
          chat = ch_client.chat.get_chat(char)
          mes = message.content
    
          participants = chat['participants']
          if not participants[0]['is_human']:
            tgt = participants[0]['user']['username']
          else:
            tgt = participants[1]['user']['username']
    
          data = ch_client.chat.send_message(chat['external_id'], tgt, mes)
    
          text = data['replies'][0]['text']
    
          response = f"{text}"
          await message.channel.send(response)
          
          embed2 = discord.Embed(description=f"Response to {message.author.mention}:\n\n{response}", color=0xff2a00)
          embed2.set_author(icon_url=message.author.avatar, name=message.author)
          await channel.send(embed=embed2)
          

def setup(client):
  client.add_cog(Ai(client))