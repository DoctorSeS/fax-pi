import discord
from discord.ext import commands, tasks
import random
from random import randint
from main import client, bot_prefix, ses, round_time, check_name, green, red
from discord.ui import InputText, Modal
from database import *
import re

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
      active = get_db('guilds')[f'{message.guild.id}']['starboard']['active']
    except:
      return
      
    if active is True:
      if (message.channel.is_nsfw()) or (message.channel.is_news()) or (message.is_system()) or (message.author.bot is True):
        return
    else:
      return

    data = get_db('guilds').get(f'{message.guild.id}', None)
    counter = int((data.get('starboard', {}).get('count', 5)))

    messages = (data.get('starboard_messages', []))
    match = next((item for item in messages if item.get("original_message_id") == message.id), None)
    if match:
      try:
        find_channel = int(get_db('guilds')[f'{message.guild.id}']['starboard']['channel'])
      except:
        return
          
      starboard_message_id = match.get('starboard_message_id', None)
      emoji_id = match.get('emoji_id', None)
      emoji_name = match.get('emoji_name', None)

      number = None
      reactions = str(message.reactions).split(",")
      for x in reactions:
        if str(emoji_id) in str(x):
          number = str(x).split("count=")[1].lstrip().split(">")[0]
          break

      if number is not None:
        msg = message.guild.get_channel(find_channel).get_partial_message(int(starboard_message_id))
        await msg.edit(content=f"<:{emoji_name}:{emoji_id}> **{number}**")

    else:
      if (counter == reaction.count) and (match is None):
        find_channel = int((data.get('starboard', None).get("channel", None)))

        messages = (data.get('starboard_messages', []))
        match = next((item for item in messages if item.get("original_message_id") == message.id), None)
        if match:
          return

        channel = message.guild.get_channel(find_channel)
        ### EMBED START ###
        content = None  ### This is for images
        embed = discord.Embed(description=message.content, timestamp=message.created_at, color=member.color)

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

        embed.set_author(name=f"{message.author.display_name}", icon_url=message.author.display_avatar, url=message.author.display_avatar)
        embed.add_field(name="Source:", value=f"[Jump]({message.jump_url})")
        embed.set_footer(text=f"#{message.channel.name}")

        msg2 = await channel.send(embed=embed, content=f"{reaction.emoji} **{counter}**")
        if content is not None:
          await channel.send(content)

        messages.append({"original_message_id": message.id, "starboard_message_id": msg2.id, "emoji_id": reaction.emoji.id, "emoji_name": reaction.emoji.name})
        update_db("guilds", f'{message.guild.id}', {"starboard_messages": messages})
  

def setup(client):
    client.add_cog(Starboard(client))