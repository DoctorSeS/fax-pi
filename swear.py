from discord.ext import commands, tasks
import discord
import logging
import traceback
import asyncio
from random import randint
from main import client, bot_prefix, currentDT, round_time, ses
import fileinput
from replit import db

def saveservers(filterList):
  f = open("blacklist_servers.txt", "a")
  f.write('%d' % filterList + "\n")
  f.close()

def removeservers(word):
  with open("blacklist_servers.txt", "r") as f:
    lines = f.readlines()
  with open("blacklist_servers.txt", "w") as f:
    for line in lines:
      if line.strip("\n") != word:
        f.write(line)

class Swear(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  async def check(self, ctx):
    #cooldown
    if ctx.author.guild_permissions.administrator:
      ctx.command.reset_cooldown(ctx)
      patreoncount = 0
      pass
    elif ctx.author.id == ses:
      ctx.command.reset_cooldown(ctx)
      patreoncount = 0
      pass
    elif ctx.author.id in roles2:
      ctx.command.reset_cooldown(ctx)
      patreoncount = 0
      pass
    else:
      matches = db.prefix(f"{ctx.guild.id}-cooldowns")
      if str(matches) != "()":
        value = db[f"{ctx.guild.id}-cooldowns"]
        if str(ctx.channel.id) in value:
          ctx.command.reset_cooldown(ctx)
          patreoncount = 0
          pass
        else:
          patreoncount = 0
          pass
      else:
        patreoncount = 0
        pass
    ###disabled
    disvalue = db.prefix(f"{ctx.guild.id}-disabled")
    disvalue2 = str(disvalue)
    if disvalue2 == "()":
      db[f"{ctx.guild.id}-disabled"] = ""
      pass
    else:
      value = db[f"{ctx.guild.id}-disabled"]
      message = str(ctx.message.content)
      first = message.split()[0]
      second = first.replace("g!", "")
      third = second.replace("G!", "")
      if third in value:
        raise discord.ext.commands.CommandError(f"The <{third}> command is disabled in this server.")
      else:
        pass
  
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return
    else:
      file = open("blacklist_servers.txt", "r")
      file2 = file.read()
      file3 = open("blacklist_channels.txt", "r")
      file4 = file3.read()
      ids = message.guild.id
      ids2 = str(ids)
      channel = message.channel.id
      channel2 = str(channel)
      if ids2 in file2:
        if channel2 in file4:
          return
        else:
          mes = str(message.content.lower())
          mes2 = mes.split(" ")
          check = open("blacklist.txt", "r")
          check2 = check.read()
          for word in mes2:
            if word in check2:
              await message.delete()
              return
            else:
              pass
          else:
            pass
      else:
        return
  
  @commands.command()
  @commands.before_invoke(check)
  @commands.has_permissions(administrator=True)
  async def blacklistenable(self, ctx):
    file = open("blacklist_servers.txt", "r")
    file2 = file.read()
    ids = ctx.guild.id
    ids2 = str(ids)
    if ids2 in file2:
      embed = discord.Embed(description=f"**`ERROR:`** ```python\nThe server is already in the list for blacklisting messages.\n```", color=0xc40000)
      await ctx.send(embed=embed, content=None)
    else:
      embed2 = discord.Embed(description=f"**`SUCCESS:`** ```python\nThe server has been added to the list.\nThe bot can now delete messages of any offenders, you can disable this at anytime with the {bot_prefix}blacklistdisable command.\n```", color=0x1bd13a)
      saveservers(ids)
      await ctx.send(embed=embed2, content=None)

  @commands.command()
  @commands.before_invoke(check)
  @commands.has_permissions(administrator=True)
  async def blacklistdisable(self, ctx):
    file = open("blacklist_servers.txt", "r")
    file2 = file.read()
    ids = ctx.guild.id
    ids2 = str(ids)
    if ids2 in file2:
      embed2 = discord.Embed(description=f"**`SUCCESS:`** ```python\nThe server has been removed from the list.\nYou can re-enable this at anytime with the {bot_prefix}scoreenable command.\n```", color=0x1bd13a)
      removeservers(ids2)
      await ctx.send(embed=embed2, content=None)
    else:
      embed = discord.Embed(description=f"**`ERROR:`** ```python\nThe server is not in the list. Cosider invoking the {bot_prefix}scoreenable command to enable this feature.\n```", color=0xc40000)
      await ctx.send(embed=embed, content=None)

  @commands.command(aliases=["swears", "wordblacklist"])
  @commands.before_invoke(check)
  @commands.has_permissions(administrator=True)
  async def blacklist(self, ctx, way: str, *, word: str=None):
    way2 = way.lower()
    check = open("blacklist.txt", "r")
    check2 = check.read()
    if way2 == "add":
      if word != None:
        global word2
        word2 = word.lower()
        if word2 in check2:
          embed2 = discord.Embed(description=f'**`ERROR:`** ```python\n"{word2}" is already in the blacklist.```', color=0xc40000)
          await ctx.send(embed=embed2, content=None, delete_after=10)
          return
        else:
          pass
      else:
        pass
    else:
      pass
    if way2 == "add":
      if word == None:
        embed2 = discord.Embed(description=f"**`ERROR:`** ```python\nInvalid method.\nValid Methods: g!blacklist add/remove/list word/(none if list)```", color=0xc40000)
        await ctx.send(embed=embed2, content=None, delete_after=10)
      else:
        f = open("blacklist.txt", "a")
        f.write(f"{word2}\n")
        f.close()
        embed2 = discord.Embed(description=f'**`SUCCESS:`** ```python\nThe word "{word2}" has been added to the blacklist.```', color=0x1bd13a)
        await ctx.send(embed=embed2, content=None)
    elif way2 == "remove":
      if word == None:
        embed2 = discord.Embed(description=f"**`ERROR:`** ```python\nInvalid method.\nValid Methods: g!blacklist add/remove/list word/(none if list)```", color=0xc40000)
        await ctx.send(embed=embed2, content=None, delete_after=10)
      else:
        with open("blacklist.txt", "r") as f:
          lines = f.readlines()
        with open("blacklist.txt", "w") as f:
          for line in lines:
            if line.strip("\n") == word2:
              f.write(line)
        embed2 = discord.Embed(description=f'**`SUCCESS:`** ```python\nThe word "{word2}" has been removed from the blacklist.```', color=0x1bd13a)
        await ctx.send(embed=embed2, content=None)
    elif way2 == "list":
      file = open("blacklist.txt", "r")
      file2 = file.read()
      embed = discord.Embed(description=f"Blacklisted words:\n{file2}")
      await ctx.send(embed=embed, content=None)
    else:
      embed2 = discord.Embed(description=f"**`ERROR:`** ```python\nInvalid method.\nValid Methods: g!blacklist add/remove/list word/(none if list)```", color=0xc40000)
      await ctx.send(embed=embed2, content=None, delete_after=10)
  
  @commands.command()
  @commands.before_invoke(check)
  @commands.has_permissions(administrator=True)
  async def blacklistchannel(self, ctx, way: str, channelid: discord.TextChannel=None):
    way2 = way.lower()
    if way2 == "add":
      if channelid == None:
        channelid = str(ctx.channel.id)
        check = open("blacklist_channels.txt", "r")
        check2 = check.read()
        if channelid in check2:
          embed2 = discord.Embed(description=f'**`ERROR:`** ```python\n"{ctx.channel.name}" is already in the blacklist.```', color=0xc40000)
          await ctx.send(embed=embed2, content=None, delete_after=10)
        else:
          f = open("blacklist_channels.txt", "a")
          f.write(f"{ctx.channel.id}\n")
          f.close()
          embed2 = discord.Embed(description=f'**`SUCCESS:`** ```python\n"{ctx.channel.name}" has been added to the blacklist.```', color=0x1bd13a)
          await ctx.send(embed=embed2, content=None)
      else:
        check = open("blacklist_channels.txt", "r")
        check2 = check.read()
        if channelid in check2:
          embed2 = discord.Embed(description=f'**`ERROR:`** ```python\n"{ctx.channel.name}" is already in the blacklist.```', color=0xc40000)
          await ctx.send(embed=embed2, content=None, delete_after=10)
        else:
          f = open("blacklist_channels.txt", "a")
          f.write(f"{channelid}\n")
          f.close()
          embed2 = discord.Embed(description=f'**`SUCCESS:`** ```python\n"{channelid.name}" has been added to the blacklist.```', color=0x1bd13a)
          await ctx.send(embed=embed2, content=None)
    elif way2 == "remove":
      if channelid == None:
        with open("blacklist_channels.txt", "r") as f:
          lines = f.readlines()
        with open("blacklist_channels.txt", "w") as f:
          for line in lines:
            if line.strip("\n") == ctx.channel.id:
              f.write(line)
        embed2 = discord.Embed(description=f'**`SUCCESS:`** ```python\n"{ctx.channel.name}" has been removed from the blacklist.```', color=0x1bd13a)
        await ctx.send(embed=embed2, content=None)
      else:
        with open("blacklist_channels.txt", "r") as f:
          lines = f.readlines()
        with open("blacklist_channels.txt", "w") as f:
          for line in lines:
            if line.strip("\n") == channelid:
              f.write(line)
        embed2 = discord.Embed(description=f'**`SUCCESS:`** ```python\n"{channelid.name}" has been removed from the blacklist.```', color=0x1bd13a)
        await ctx.send(embed=embed2, content=None)
    elif way2 == "list":
      file = open("blacklist_channels.txt", "r")
      file2 = file.read()
      embed = discord.Embed(description=f"Blacklisted words:\n{file2}")
      await ctx.send(embed=embed, content=None)
    else:
      embed2 = discord.Embed(description=f"**`ERROR:`** ```python\nInvalid method.\nValid Methods: g!blacklistchannel add/remove/list channel/(none if list)```", color=0xc40000)
      await ctx.send(embed=embed2, content=None, delete_after=10)

def setup(client):
  client.add_cog(Swear(client))