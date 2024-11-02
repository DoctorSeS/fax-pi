import discord
from discord.ext import commands, tasks
from main import client, bot_prefix, ses, round_time, red, green
from database import *
import re
import unicodedata
import random

slurs = ["nigger", "nigga", "fagg", "nibba", "nigg", "fag", "faggot", "chink", 'niggerman', 'niggerboy', 'cracker', 'queer']

def build_variation_patterns(words):
    patterns = []
    for word in words:
        pattern = ''.join(f"{char}[^\w]*" for char in word)
        patterns.append(pattern)
    return patterns

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

                        update_db(f'guilds/{ctx.guild.id}', "global_chat", {"active": True})
                        await ctx.send(embed=embed2, content=None)
                    else:
                        if val is True:
                            embed2 = discord.Embed(description=f"**`SUCCESS:`** ```python\nGlobal chat has been deactivated.\nYou can re-enable this at anytime with the {bot_prefix}config command.\n```", color=0x1bd13a)


                            update_db(f'guilds/{ctx.guild.id}', "global_chat", {"active": False})
                            await ctx.send(embed=embed2, content=None)
                        else:
                            embed2 = discord.Embed(description=f"**`SUCCESS:`** ```python\nGlobal chat has been activated.\n```", color=0x1bd13a)


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

                        update_db(f'guilds/{ctx.guild.id}', "global_chat", {"active": True, "bans": []})
                        active = "activated"
                    else:
                        update_db(f'guilds/{ctx.guild.id}', "global_chat", {"active": False, "bans": []})
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
                    bans = []
                else:
                    if "None" in bans:
                        bans = []

                embed = discord.Embed(description=f"```markdown\nPlease respond with the user or user id you want to ban from using global chat.\n\nThis will disallow them from using global chat in your server, and will also delete messages that appear from that person on your server.```", color=0x1bd13a)
                mes = await ctx.send(embed=embed, content=None)

                def check(m: str):
                    global msg1
                    msg1 = m.content
                    return m.content and m.author == ctx.author

                msg = await client.wait_for("message", check=check, timeout=60)
                await msg.delete()
                if "<@" in msg1:
                    user_id = msg1.split('<@')[1].lstrip().split(">")[0]
                else:
                    try:
                        user_id = int(msg1)
                    except:
                        embed2 = discord.Embed(title="User Unbanned", description=f"Couldn't convert '{msg1}' to a user id.", color=green)
                        await mes.edit(embed=embed2, content=None)
                    else:
                        try:
                            user = client.get_user(int(user_id))
                        except:
                            user_mention = user_id
                        else:
                            user_mention = user.mention
                            user_id = user.id

                        if user_id in bans:
                            embed2 = discord.Embed(title="User Unbanned", description=f"The user ({user_mention}) has been unbanned from using global chat.", color=green)

                            bans.remove(user_id)
                            update_db(f'guilds/{ctx.guild.id}', "global_chat", {"bans": bans})

                            await mes.edit(embed=embed2, content=None)
                        else:
                            embed2 = discord.Embed(title="User Banned", description=f"The user ({user_mention}) has been banned from using global chat.", color=green)

                            bans.append(user_id)
                            update_db(f'guilds/{ctx.guild.id}', "global_chat", {"bans": bans})

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
        ### if not bot and others ###
        if (not message.author.bot) and (message.guild is not None):
            ### check own server ###
            all_guilds = get_db('guilds')

            if str(message.guild.id) in all_guilds and "global_chat" in all_guilds[str(message.guild.id)] and "active" in all_guilds[str(message.guild.id)]['global_chat'] and all_guilds[str(message.guild.id)]['global_chat']['active'] and str(message.channel.id) == all_guilds[str(message.guild.id)]['global_chat']['channel']:
                ### Everything is working so far ###

                ### Check Banned in original server ###
                banlist = all_guilds[str(message.guild.id)]['global_chat'].get('bans', None)
                if banlist is not None:
                    if message.author.id in banlist:
                        embed = discord.Embed(title="You are banned.", description=f"**`You are banned from using global chat in {message.guild}.`**\n\n**`Your messages will also not be visible in {message.guild} when you use global chat from another server.`**", color=0xd10000)
                        await message.delete()
                        await message.author.send(embed=embed)
                        return

                ### Message content checks ###
                if message.content.startswith(all_guilds[str(message.guild.id)].get('prefix', f'{bot_prefix}')) or (message.content.startswith(f"{client.user.mention}")) or (message.content.startswith(f"{bot_prefix.upper()}")):
                    return

                ### check color ###
                embed_color = discord.Color.dark_theme()
                patron_check = get_db('misc')['all_patrons']
                if str(message.author.id) in list(patron_check):
                    patron_check2 = patron_check[f'{message.author.id}']['pledge']
                    if int(patron_check2) == 500:
                        embed_color = 0x52c400
                    elif int(patron_check2) == 1000:
                        embed_color = 0xFFD700
                elif message.author.id == ses:
                    embed_color = 0xad0000

                ### EMBED START ###
                content = None ### This is for images
                embed = discord.Embed(color=embed_color)

                ### check content ###
                if ("<:" in message.content) or ("<a:" in message.content):
                    custom_emoji_pattern = r'<a?:(\w+):(\d+)>'

                    for match in re.finditer(custom_emoji_pattern, message.content):
                        emoji_name = match.group(1)
                        emoji_id = match.group(2)
                        emoji_found = None

                        # Search for emoji across all servers
                        for guild in client.guilds:
                            server = client.get_guild(int(guild.id))
                            if server:
                                emoji_found = discord.utils.get(server.emojis, name=emoji_name)
                                if emoji_found:
                                    break

                        if emoji_found:
                            continue

                        is_animated = match.group(0).startswith("<a:")
                        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{'gif' if is_animated else 'png'}"
                        embed.set_thumbnail(url=emoji_url)

                ### Sticker Check ###
                if message.stickers:
                    embed.set_thumbnail(url=f"{message.stickers[0].url}")

                ### Attachments check ###
                if message.attachments:
                    if (".mp4" in str(message.attachments[0].url)) or (".mov" in str(message.attachments[0].url)):
                        content = f"{message.attachments[0].url}"
                    else:
                        embed.set_image(url=f"{message.attachments[0].url}")

                ### url checks ###
                if "http" in str(message.content):
                    url_pattern = r'(https?://[^\s]+)'
                    urls = re.findall(url_pattern, message.content)
                    link = ""
                    for url in urls:
                        link += f"{url}\n"

                    if ("/tenor.co" in message.content) or ("fixvx" in message.content) or ("fxtwitter" in message.content) or ("twitter" in message.content) or ("vxtwitter" in message.content) or ("youtube" in message.content) or ("youtu.be" in message.content) or ("x.com" in message.content):
                        content = link
                    else:
                        if (".mp4" in str(message.content)) or (".mov" in str(message.content)):
                            content = link
                        else:
                            try:
                                embed.set_image(url=urls[0])
                            except:
                                content = link

                ### Swear Check ###
                for word in slurs:
                    pattern = re.compile(re.escape(word), re.IGNORECASE)

                    def replace(match2):
                        matched_word = match2.group()
                        return matched_word[0] + '፠' * (len(matched_word) - 1)

                    message.content = pattern.sub(replace, message.content)

                ### Get message Type ###
                if str(message.type) == "MessageType.default":
                    embed.description = message.content

                elif str(message.type) == "MessageType.reply":
                    embed.description = message.content

                    reply_message = await message.channel.fetch_message(message.reference.message_id)
                    embeds = reply_message.embeds
                    if str(embeds) != "[]":
                        for reply_embed in embeds:
                            embeddict = reply_embed.to_dict()

                        try:
                            desc = embeddict['description']
                        except:
                            desc = "Couldn't load message."
                        author = embeddict['author']['name']
                    else:
                        desc = reply_message.content
                        author = reply_message.author.display_name

                    embed.clear_fields()
                    embed.add_field(name=f"Replying to {author}:", value=desc)

                embed.set_author(name=f"{message.author.global_name}", icon_url=message.author.display_avatar, url=message.author.display_avatar)
                embed.set_footer(text=f"Guild: {message.guild}\nGuild ID: {message.guild.id}", icon_url=f"{message.guild.icon}")
                for x in all_guilds:
                    try:
                        if all_guilds[x]['global_chat']['active'] is True:
                            channel = client.get_guild(int(x)).get_channel(int(all_guilds[x]['global_chat']['channel']))
                        else:
                            continue
                    except:
                        continue
                    else:
                        ### Check ban list per server ###
                        banlist = all_guilds[x]['global_chat'].get('bans', None)
                        if banlist is not None:
                            if message.author.id in banlist:
                                continue

                        await channel.send(embed=embed, content=None)
                        if content is not None:
                            await channel.send(content)


def setup(client):
    client.add_cog(Globalchat(client))
