import discord
from discord.ext import commands, tasks
import logging
import traceback
from random import randint
from main import client, bot_prefix, ses, round_time, red, green
import fileinput
from database import *
from termcolor import cprint

slurs = ["nigger", "nigga", "fagg", "nibba", "nigg", "fag", "faggot", "nig", "chink"]


class Select(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.selected = ""
        self.ctx = ctx

    @discord.ui.select(
        placeholder="Choose what you want to edit.",
        max_values=1,
        disabled=False,
        options=[
            discord.SelectOption(label="Enable/Disable",
                                 description="Enable/Disable the module."),
            discord.SelectOption(
                label="Set Channel",
                description="Set the channel for global chat."),
            discord.SelectOption(
                label=f"Ban/Unban User",
                description=
                "Ban/Unban a user, this will make it so their messages won't appear."
            ),
            discord.SelectOption(
                label="Preview Banned Users",
                description="Preview the users that got banned.")
        ])
    async def sele(self, select, interaction):
        val = str(select.values[0])
        try:
            if "Enable/Disable" in val:
                await interaction.message.delete()
                await self.ctx.invoke(client.get_command("gbchat_select"),
                                      chosen="enable")
                return
            elif "Set " in val:
                await interaction.message.delete()
                await self.ctx.invoke(client.get_command("gbchat_select"),
                                      chosen="set")
                return
            elif "Ban/" in val:
                await interaction.message.delete()
                await self.ctx.invoke(client.get_command("gbchat_select"),
                                      chosen="ban")
                return
            elif "Preview" in val:
                await interaction.message.delete()
                await self.ctx.invoke(client.get_command("gbchat_select"),
                                      chosen="preview")
                return
        except discord.HTTPException as error:
            return


class Globalchat(commands.Cog):
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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gbchat_select(self, ctx, chosen: str):
        try:
            if chosen == "enable":
                count = int(ctx.guild.member_count)

                if count > 25:
                    try:
                        val = get_db('guilds')[f'{ctx.guild.id}']['global_chat']['active']
                    except:
                        embed2 = discord.Embed(description=f"**`SUCCESS:`** ```python\nGlobal chat has been activated.\n```", color=0x1bd13a)

                        all_gc = get_db('misc')['global_chat_all']
                        update_db(f'misc', "none", {"global_chat_all": f"{all_gc}{ctx.guild.id},"})
                        update_db(f'guilds/{ctx.guild.id}', "global_chat", {"active": True})
                        await ctx.send(embed=embed2, content=None)
                    else:
                        if val is True:
                            embed2 = discord.Embed(description=f"**`SUCCESS:`** ```python\nGlobal chat has been deactivated.\nYou can re-enable this at anytime with the {bot_prefix}config command.\n```", color=0x1bd13a)

                            update_db(f'guilds/{ctx.guild.id}', "global_chat", {"active": False})
                            await ctx.send(embed=embed2, content=None)
                        else:
                            embed2 = discord.Embed(description=f"**`SUCCESS:`** ```python\nGlobal chat has been activated.\n```", color=0x1bd13a)

                            all_gc = get_db('misc')['global_chat_all']
                            update_db(f'misc', "none", {"global_chat_all": f"{all_gc}{ctx.guild.id},"})
                            update_db(f'guilds/{ctx.guild.id}', "global_chat", {"active": True})
                            await ctx.send(embed=embed2, content=None)
                else:
                  embed = discord.Embed(title="Failed to Set-up", description= f"Your server has {count} members. You need at least 25 members to be able to use this feature.", color=0xd10000)
                  embed.set_footer(text="This feature is made to prevent spam to Global Chat.\nSorry for the inconvenience.")
                  await ctx.send(embed=embed, content=None)

            elif chosen == "set":
                try:
                    value = get_db('guilds')[f'{ctx.guild.id}']['global_chat']
                except:
                    if int(ctx.guild.member_count) >= 25:
                        all_gc = get_db('misc')['global_chat_all']
                        update_db(f'misc', "none", {"global_chat_all": f"{all_gc}{ctx.guild.id},"})

                        update_db(f'guilds/{ctx.guild.id}', "global_chat", {"active": True, "bans": "None"})
                        active = "activated"
                    else:
                        update_db(f'guilds/{ctx.guild.id}', "global_chat", {"active": False, "bans": "None"})
                        active = "deactivated"
                else:
                    if value['active']:
                        active = "activated"
                    else:
                        active = "deactivated"

                embed = discord.Embed(description=f"```markdown\nPlease respond with a channel you want to set as the global chat.\n\nNote: This will change the channel's topic and slowmode duration.```", color=0x1bd13a)
                embed.set_footer(text=f"This module is currently {active}.")
                mes = await ctx.send(embed=embed, content=None)

                def check(m: discord.TextChannel):
                    global msg1
                    msg1 = m.content
                    return m.content and m.author == ctx.author

                msg = await client.wait_for("message", check=check, timeout=60)
                await msg.delete()
                msg2 = str(msg1).replace('<#', "")
                msg3 = msg2.replace("!", "")
                msg4 = msg3.replace(">", "")
                channel = ctx.guild.get_channel(int(msg4))
                embed2 = discord.Embed(
                    title="Channel Set",
                    description=
                    f"The channel (<#{msg4}>) has been set as the global chat for this server.",
                    color=green)

                update_db(f'guilds/{ctx.guild.id}', "global_chat", {"channel": f"{msg4}"})
                await mes.edit(embed=embed2, content=None)
                await channel.edit(slowmode_delay=10, topic=f"A Text Channel for all the servers that <@{client.user.id}> is in. Make sure to respect discord's TOS. This does not allow nsfw.")

            elif chosen == "ban":
                try:
                    bans = get_db('guilds')[f'{ctx.guild.id}']['global_chat']['bans']
                except:
                    bans = ''
                else:
                    if "None" in bans:
                        bans = ''

                embed = discord.Embed(description=f"```markdown\nPlease respond with the user you want to ban from using global chat.\n\nThis will disallow them from using global chat in your server, and will also delete messages that appear from that person on your server.```", color=0x1bd13a)
                mes = await ctx.send(embed=embed, content=None)

                def check(m: discord.User):
                    global msg1
                    msg1 = m.content
                    return m.content and m.author == ctx.author

                msg = await client.wait_for("message", check=check, timeout=60)
                await msg.delete()
                msg2 = str(msg1).replace('<@', "")
                msg3 = msg2.replace("!", "")
                msg4 = msg3.replace(">", "")
                user = client.get_user(int(msg4))
                if str(msg4) in bans:
                    embed2 = discord.Embed(
                        title="User Unbanned",
                        description=
                        f"The user ({user}) has been unbanned from using global chat.",
                        color=green)

                    unbanned = bans.replace(f"{user.id},", f"")
                    update_db(f'guilds/{ctx.guild.id}', "global_chat", {"bans": f"{unbanned}"})


                    await mes.edit(embed=embed2, content=None)
                else:
                    embed2 = discord.Embed(
                        title="User Banned",
                        description=
                        f"The user ({user}) has been banned from using glo-bal chat.",
                        color=green)

                    update_db(f'guilds/{ctx.guild.id}', "global_chat", {"channel": f"{bans}{user.id},"})

                    await mes.edit(embed=embed2, content=None)

            elif chosen == "preview":
                try:
                    value = get_db('guilds')[f'{ctx.guild.id}']['global_chat']
                except:
                    return

                try:
                    chan = value['channel']
                except:
                    chan2 = "not selected"
                else:
                    if chan.lower() != "none":
                        chan2 = f"<#{chan}>"
                    else:
                        chan2 = "not selected"

                try:
                    banned = value['banned'].replace(',', "")
                except:
                    banned = ''

                try:
                    h = value['active']
                except:
                    active = 'deactivated'
                else:
                    if h:
                        active = 'activated'
                    else:
                        active = 'deactivated'


                embed = discord.Embed(description=f"**`Current Settings:`**\n\nStatus: {active}\nChannel: {chan2}\n\nBanned users:\n{banned}")
                await ctx.send(embed=embed, content=None)

        except:
            return

    @commands.command(aliases=["global", "globalchat"])
    @commands.before_invoke(disabled_check)
    @commands.is_owner()
    async def gc(self, ctx):
        view = Select(ctx)
        embed = discord.Embed(
            title="Global Chat Settings",
            description=f"Please select what you want to do with this module.")
        try:
            enabled = get_db('guilds')[f'{ctx.guild.id}']['global_chat']['active']
        except:
            embed.set_footer(text=f"The Global Chat is currently deactivated.")
        else:
            if enabled:
                embed.set_footer(text=f"The Global Chat is currently activated.")
            else:
                embed.set_footer(text=f"The Global Chat is currently deactivated.")

        await ctx.send(embed=embed, content=None, view=view)

    @commands.Cog.listener()
    async def on_message(self, message):
      ### global-chat ###
      if not message.author.bot:
        if message.guild is not None:
          try:
            active = get_db('guilds')[f'{message.guild.id}']['global_chat']['active']
          except:
            return
          else:
            if active is True:
              try:
                channel = get_db('guilds')[f'{message.guild.id}']['global_chat']['channel']
              except:
                return
              else:

                if str(message.channel.id) == str(channel):
                  if message is None:
                    return
                  else:
                    servers1 = get_db('misc')['global_chat_all']
                    servers = servers1.split(",")
                    for guild in servers:
                      if guild == '':
                          continue

                      try:
                          gb_settings = get_db('guilds')[f'{guild}']['global_chat']
                      except:
                          return

                      if gb_settings.get('active') is True:
                          ##check banned##
                          server = client.get_guild(int(guild))
                          try:
                            banned = get_db('guilds')[f'{guild}']['global_chat']['bans']
                          except:
                            banned = ''

                          if str(message.author.id) in banned:
                            embed = discord.Embed(title="You are banned.", description= f"**`You are banned from using global chat in {message.guild}.`**\n\n**`Your messages will also not be visible in {message.guild} when you use global chat from another server.`**", color=0xd10000)
                            await message.delete()

                            if message.content.startswith(f"{bot_prefix}"):
                              await message.channel.purge(limit=1)
                              pass
                            if message.content.startswith(f"<@!{client.user.id}>"):
                              await message.channel.purge(limit=1)
                              pass

                            try:
                              await message.author.send(embed=embed, content=None)
                              return
                            except:
                              return

                          else:
                            if message.content.startswith(f"{bot_prefix}"):
                              return
                            if message.content.startswith(f"<@!{client.user.id}>"):
                              return
                            else:
                              if f"{message.author.id}" in banned:
                                pass
                              else:

                                mes = str(message.content)
                                racial = 0
                                for word in slurs:
                                  if word in mes.lower():
                                    size = len(word)
                                    mes2 = mes.lower().replace(word, f"{word[:1]}፠፠፠")
                                    racial += 1
                                  else:
                                    pass
                                else:
                                  if racial == 0:
                                    mes2 = mes

                                if "reply" in str(message.type):
                                  ### if reply ###
                                  msg = await message.channel.fetch_message(message.reference.message_id)
                                  embeds = msg.embeds
                                  col = discord.Color.dark_theme()
                                  if str(embeds) != "[]":
                                    for embed in embeds:
                                      embeddict = embed.to_dict()


                                    patron_check = list(get_db('misc')['all_patrons'])
                                    if str(message.author.id) in patron_check:
                                      patron_check2 = get_db('misc')['all_patrons'][f'{message.author.id}']['pledge']
                                      if int(patron_check2) == 500:
                                        col = 0x52c400
                                      elif int(patron_check2) == 1000:
                                        col = 0xFFD700
                                    elif message.author.id == ses:
                                      col = 0xad0000

                                    embed = discord.Embed(description=f"Replying to **{embeddict['author']['name']}**:\n{embeddict['description']}\n\n{mes2}", timestamp=message.created_at, color=col)
                                    pass
                                  else:
                                    embed = discord.Embed(description=f"Replying to **{msg.author}**:\n{msg.content}\n\n{mes2}", timestamp=message.created_at, color=col)
                                    pass

                                else:
                                  col = discord.Color.dark_theme()
                                  patron_check = list(get_db('misc')['all_patrons'])
                                  if str(message.author.id) in patron_check:
                                    patron_check2 = get_db('misc')['all_patrons'][f'{message.author.id}']['pledge']
                                    if int(patron_check2) == 500:
                                      col = 0x52c400
                                    elif int(patron_check2) == 1000:
                                      col = 0xFFD700
                                  elif message.author.id == ses:
                                    col = 0xad0000

                                  embed = discord.Embed(description=f"{mes2}", timestamp=message.created_at, color=col)

                                try:
                                  chan = get_db('guilds')[f'{guild}']['global_chat']['channel']
                                except:
                                  return
                                else:
                                  if chan != "None":
                                    channel = server.get_channel(int(chan))


                                content = None
                                name = message.author
                                if len(str(name).split("#")[1]) == 1:
                                  name = message.author.name
                                else:
                                  pass
                                embed.set_author(name=f"{message.author.display_name} • {message.author.name}", icon_url=message.author.avatar)
                                embed.set_footer(text=f"User ID: {message.author.id}\nGuild: {message.guild}", icon_url=f"{message.guild.icon}")

                                if "<:" in str(message.content):
                                  if "http" in str(message.content):
                                    pass
                                  else:
                                    try:
                                      emoji = str(message.content).split(":", 1)[1].lstrip().split(":", 1)[0]
                                      emojicheck = discord.utils.get(server.emojis, name=emoji)
                                      for guild in servers:
                                        servercheck = client.get_guild(int(guild))
                                        emojicheck = discord.utils.get(servercheck.emojis, name=emoji)
                                        if emojicheck != None:
                                          break
                                        else:
                                          pass
                                    except:
                                        pass
                                    else:
                                        if emojicheck == None:
                                          emojia1 = str(message.content).replace(":", "", 1)
                                          emojia2 = emojia1.replace(":", "+", 1)
                                          emojia = emojia2.split("+", 1)[1].lstrip().split(">", 1)[0]
                                          emoji2 = discord.PartialEmoji(name=f"{emoji}", id=int(emojia))
                                          embed.set_image(url=emoji2.url)
                                          pass
                                        else:
                                          pass

                                if message.attachments:
                                  if ".mp4" in str(message.attachments[0].url):
                                    content = f"{message.attachments[0].url}"
                                  elif ".mov" in str(message.attachments[0].url):
                                    content = f"{message.attachments[0].url}"
                                  else:
                                    embed.set_image(url=f"{message.attachments[0].url}")

                                if "http" in str(message.content):
                                  if "/tenor.co" in str(message.content):
                                    content = f"{mes2}"
                                    embed.set_footer(text=f"Tenor links do not work as embeds.\nGuild: {message.guild}", icon_url=f"{message.guild.icon}")
                                    pass
                                  elif "twitter.com" in str(message.content):
                                    content = f"{mes2}"
                                    embed.set_footer(text=f"Twitter links do not work as embeds.\nGuild: {message.guild}", icon_url=f"{message.guild.icon}")

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
                                      if ".mp4" in str(message.content):
                                        content = f"{mes2}"
                                      elif ".mov" in str(message.content):
                                        content = f"{mes2}"
                                      else:
                                        embed.set_image(url=f"{mes2}")

                                if message.stickers:
                                  embed.set_thumbnail(url=f"{message.stickers[0].url}")

                                await channel.send(embed=embed, content=None)
                                if content != None:
                                  await channel.send(f"{content}")


def setup(client):
    client.add_cog(Globalchat(client))
