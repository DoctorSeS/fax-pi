from discord.ext import commands, tasks
import discord
import logging
import traceback
import asyncio
import datetime
from random import randint
from main import client, bot_prefix, currentDT, round_time, ses, red, green
from termcolor import cprint
from cogs.events import check_logs
from database import *

inv3 = []
numm = 0
mtd2 = []
cnter = 0
count2 = 0
count5 = 0
count4 = 0
channels2 = []
roles = []

def add_time(time_add):
  current = datetime.datetime.now()
  add = datetime.timedelta(seconds=int(time_add))
  new_time = current + add

  return str(new_time)

def fixtime(dt):
  dt2 = str(dt)
  timelen = len(dt2)

  dt = dt2[:timelen - 13]
  return dt

class Select_member(discord.ui.View):
  def __init__(self, ctx, member):
    super().__init__(timeout=60)
    self.selected = ""
    self.ctx = ctx
    self.member = member

  @discord.ui.select(placeholder="Choose what you want to edit.", max_values=1, disabled=False, options=[
        discord.SelectOption(
          label="Extend Mute Time",
          description="Extend a Member's mute time."
        ),
        discord.SelectOption(
            label="Shorten Mute Time",
          description="Shorten a Member's mute time."
        )
    ])
  async def sele(self, select, interaction):
    val = str(select.values)
    valre = val.replace("['", "")
    val2 = valre.replace("']", "")
    try:
      if "Extend Mute" in val2:
        await interaction.message.delete()
        await self.ctx.invoke(client.get_command("extend_shorten_time"), chosen="exmute", chosen2=self.member)
        return
      elif "Shorten Mute" in val2:
        await interaction.message.delete()
        await self.ctx.invoke(client.get_command("extend_shorten_time"), chosen="shmute", chosen2=self.member)
        return
    except:
      return

class Select_channel(discord.ui.View):
  def __init__(self, ctx, channel):
    super().__init__(timeout=60)
    self.selected = ""
    self.ctx = ctx
    self.channel = channel

  @discord.ui.select(placeholder="Choose what you want to edit.", max_values=1, disabled=False, options=[
        discord.SelectOption(
            label="Extend Lockdown Time",
            description="Extend a Channel's lockdown time."
        ),
        discord.SelectOption(
            label="Shorten Lockdown Time",
            description="Shorten a Channel's lockdown time."
        )
    ])
  async def sele(self, select, interaction):
    val = str(select.values)
    valre = val.replace("['", "")
    val2 = valre.replace("']", "")
    try:
      if "Extend Lockdown" in val2:
        await interaction.message.delete()
        await self.ctx.invoke(client.get_command("extend_shorten_time"), chosen="exlock", chosen2=self.channel)
        return
      elif "Shorten Lockdown" in val2:
        await interaction.message.delete()
        await self.ctx.invoke(client.get_command("extend_shorten_time"), chosen="shlock", chosen2=self.channel)
        return
    except:
      return

class Mod_coms(commands.Cog):
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


  ### commands ###

  @commands.command()
  async def lastMessage(self, ctx, users_id: int):
    oldestMessage = None
    for channel in ctx.guild.text_channels:
      fetchMessage = await channel.history().find(lambda m: m.author.id == users_id)
      if fetchMessage != None:
        return

    try:
      await ctx.send(f"Oldest message is:\n\n{fetchMessage.content} `at {fetchMessage.created_at}`")
    except:
      await ctx.send("No message found.")

  @commands.command()
  @commands.before_invoke(disabled_check)
  async def role(self, ctx, role: int, gui=None):
    if gui:
      server = client.get_guild(int(gui))
    else:
      server = ctx.guild
        
    try:
      role = discord.utils.get(server.roles, id=int(role))
    except:
      embed2 = discord.Embed(title="Failed to find role", description=f"The provided role ({role}) could not be found.", color=0xd10000)
      await ctx.send(embed=embed2, content=None)

    perms = f"""`Administrator:` {role.permissions.administrator}\n`Ban members:` {role.permissions.ban_members}\n`Kick members:` {role.permissions.kick_members}\n`Can view the logs:` {role.permissions.view_audit_log}\n`Manage channels:` {role.permissions.manage_channels}\n`Manage messages:` {role.permissions.manage_messages}\n`Manage server:` {role.permissions.manage_guild}\n`View insights:` {role.permissions.view_guild_insights}\n`Manage emojis:` {role.permissions.manage_emojis}\n`Manage roles:` {role.permissions.manage_roles}\n`Manage Permissions:` {role.permissions.manage_permissions}\n`View`<#{ctx.channel.id}>`:` {role.permissions.view_channel}"""
      
    embed = discord.Embed(description=f"Permissions:\n{perms}", color=role.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"Information about {role.name}")
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar)
    embed.add_field(name=f'General Information:', value=f"`ID:` {role.id}\n`Color hex:` {role.color}\n`Position:` {role.position}\n`Default?` {role.is_default()}\n`Mentionable?` {role.mentionable}")
        
    async with ctx.typing():
      await asyncio.sleep(0.5)
      await ctx.send(embed=embed, content=None)

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.has_permissions(manage_roles=True)
  async def invites(self, ctx, sv: int=None):
    server = client.get_guild(ctx.guild.id)
    if sv != None:
      server = client.get_guild(sv)
    inv = await server.invites()
    inv2 = len(inv)
    global numm
    global inv3
    while numm != inv2:
      inv3.append(f"`Code:` {inv[numm].code} `Creator:` {inv[numm].inviter.mention} `Created at:` {fixtime(inv[numm].created_at)}")
      numm += 1
    else:
      inv4 = str(inv3)
      inv5 = inv4.replace("'", "")
      inv6 = inv5.replace("[", "")
      inv7 = inv6.replace("]", "")
      inv8 = inv7.replace(",", "\n")
      inv9 = str(inv8)
      embed = discord.Embed(title=f"{server}'s invites: ({numm})", description=f"{inv9}")
      await ctx.send(embed=embed, content=None)
      numm = 0


  @commands.command(alieases=['lockdown'])
  @commands.has_permissions(manage_roles=True)
  @commands.before_invoke(disabled_check)
  async def lock(self, ctx, channel: discord.TextChannel, timer: str, *, reason=None):
    server = client.get_guild(ctx.guild.id)
    msg = ctx.message
    channel2 = "none"
    if check_logs(ctx.guild.id)[0] is True:
      logs2 = check_logs(ctx.guild.id)[1]
      if str(logs2).lower() != "none":
        channel2 = discord.utils.get(server.channels, id=int(logs2))


    log = discord.Embed(description=f"<#{channel.id}> has been locked.\n`Duration:` {timer[:-1]}\n`Reason:` {reason}", color=discord.Color.from_rgb(r=255, g=0, b=0))
    log.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar)
    timer2 = timer.lower()
    timerfinal = int(timer[:-1])
    
    if timer2[-1] == "s":
      lk = discord.Embed(description=f"<#{channel.id}> has been locked.\nDuration: {timerfinal} second(s)\nReason: {reason}", color=discord.Color.from_rgb(r=255, g=0, b=0), timestamp=ctx.message.created_at)
      lk.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar)
      await msg.delete()
      await ctx.channel.set_permissions(server.default_role, send_messages=False)
      await channel.send(embed=lk, content=None)
      if channel2 != "none":
        await channel2.send(embed=log, content=None)
      update_db('guilds', f"{ctx.guild.id}", {f'TimerLock-{channel.id}': add_time(timerfinal)})

    elif timer2[-1] == "m":
      lk = discord.Embed(description=f"<#{channel.id}> has been locked.\nDuration: {timerfinal} minute(s)\nReason: {reason}", color=discord.Color.from_rgb(r=255, g=0, b=0), timestamp=ctx.message.created_at)
      lk.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar)
      await msg.delete()
      await channel.set_permissions(server.default_role, send_messages=False)
      await channel.send(embed=lk, content=None)
      if channel2 != "none":
        await channel2.send(embed=log, content=None)
      tm = int(timerfinal)*60
      update_db('guilds', f"{ctx.guild.id}", {f'TimerLock-{channel.id}': add_time(tm)})
      
    elif timer2[-1] == "h":
      lk = discord.Embed(description=f"<#{channel.id}> has been locked.\nDuration: {timerfinal} hour(s)\nReason: {reason}", color=discord.Color.from_rgb(r=255, g=0, b=0), timestamp=ctx.message.created_at)
      lk.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar)
      await msg.delete()
      await channel.set_permissions(server.default_role, send_messages=False)
      await channel.send(embed=lk, content=None)
      if channel2 != "none":
        await channel2.send(embed=log, content=None)
      tm = int(timerfinal)*60
      tm2 = tm*60
      update_db('guilds', f"{ctx.guild.id}", {f'TimerLock-{channel.id}': add_time(tm2)})


  @commands.command(alieases=['unlockdown'])
  @commands.has_permissions(manage_roles=True)
  @commands.before_invoke(disabled_check)
  async def unlock(self, ctx, channel: discord.TextChannel, *, reason=None):
    try:
      test = get_db('guilds')[f'{ctx.guild.id}'][f'TimerLock-{channel.id}']
    except:
      embed = discord.Embed(description=f"<#{channel.id}> is not locked.\nIf you believe that's an error, try checking the channel permissions.", color=discord.Color.from_rgb(r=0, g=255, b=0), timestamp=ctx.message.created_at)
      embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar)
      await channel.send(embed=embed, content=None)
    else:
      embed = discord.Embed(description=f"<#{channel.id}> has been unlocked.\nReason: {reason}", color=discord.Color.from_rgb(r=0, g=255, b=0), timestamp=ctx.message.created_at)
      embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar)
      await channel.send(embed=embed, content=None)
      await channel.set_permissions(ctx.guild.default_role, add_reactions=True)
      del_db(f'guilds/{ctx.guild.id}', f"TimerLock-{channel.id}")
  
  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 30, commands.BucketType.guild)
  async def server(self, ctx, sv: int=None):
    server = client.get_guild(ctx.guild.id)
    try:
      created_at = server.created_at
    except:
      created_at = None
      pass
    else:
      pass
      
    if sv != None:
      server = client.get_guild(sv)
    embed = discord.Embed(description=f'**About {server}**', color=discord.Color.random(), timestamp=created_at)
    embed.set_footer(text=f'Server ID: {server.id}\nServer created at:')
    embed.set_thumbnail(url=server.icon)

    if server.premium_subscription_count < 2:
      max_boosts = 2
    elif server.premium_subscription_count < 7:
      max_boosts = 7
    elif server.premium_subscription_count <= 14:
      max_boosts = 14

    embed.add_field(name='Information:', value=f'`Owner:` <@{server.owner_id}>\n`Name:` **{server}**\n`Verification level:` **{server.verification_level}**\n`Boosts:` **{server.premium_subscription_count} / {max_boosts}**\n`Boost level:` **{server.premium_tier}**\n`Afk timeout:` **{server.afk_timeout} seconds**\n`Description:` **{server.description}**\n`Afk channel:` **{server.afk_channel}**\n`Total members:` **{server.member_count}**')

    if ctx.author.guild_permissions.manage_roles:
      try:
        logs = get_db('guilds')[f'{ctx.guild.id}']['logs']['active']
      except:
        logs = "False"

      try:
        ai = get_db('guilds')[f'{ctx.guild.id}']['ai']['active']
      except:
        ai = "False"

      try:
        gc = get_db('guilds')[f'{ctx.guild.id}']['global_chat']['active']
      except:
        gc = "False"

      try:
        score = get_db('guilds')[f'{ctx.guild.id}']['score']
      except:
        score = "False"

      embed.add_field(name="Specific Information:", value=f"""`Logs Enabled?` **{logs}**\n`AI Enabled?` **{ai}**\n`Global Chat Enabled?` **{gc}**\n`Score Enabled?` **{score}**""", inline=True)

    await ctx.send(embed=embed, content=None)

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.has_permissions(manage_messages=True)
  async def members(self, ctx):
    server = client.get_guild(ctx.guild.id)
    he = server.members
    count2 = [member for member in he if member.bot]
    count = server.member_count - len(count2)
    embed = discord.Embed(title=f"{server}")
    embed.add_field(name=f"Member count:", value=f"`Users:` **{count}**\n`Bots:` **{len(count2)}**")
    embed.set_thumbnail(url=server.icon)
    embed.set_footer(icon_url=server.icon, text=f"{server} • ID: {server.id}")
    await ctx.send(embed=embed, content=None)

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.has_permissions(manage_messages=True)
  async def say(self, ctx, channel: discord.TextChannel, *, say):
      msg = ctx.message
      channel = discord.utils.get(ctx.message.guild.channels, name=f'{channel}')
      if "@everyone" in say:
          await channel.send(f"{ctx.author.mention}, you can't do that")
      if "@here" in say:
          await channel.send(f"{ctx.author.mention}, you can't do that")
      else:
          async with channel.typing():
              await msg.delete()
              await asyncio.sleep(2)
              await channel.send(f'{say}')

  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member, *, reason=None):
      msg = ctx.message
      mod = client.get_user(id=ctx.author.id)
      if check_logs(ctx.guild.id)[0] is True:
        chan = check_logs(ctx.guild.id)[1]
        channel = ctx.guild.get_channel(int(chan))
        embed2 = discord.Embed(description=f"**{member.mention} has been banned.**\n**Reason:** {reason}", color=discord.Color.from_rgb(r=255, g=0, b=0), timestamp=ctx.message.created_at)
        embed2.set_author(name=f"{member} • ID: {member.id}", icon_url=member.avatar)
        embed2.set_footer(text=f'Moderator: {mod} • ID: {mod.id}', icon_url=mod.avatar)
        await channel.send(embed=embed2, content=None)

      embed = discord.Embed(description=f"**{member.mention} has been banned.**", color=discord.Color.from_rgb(r=255, g=0, b=0))
      embed.set_author(name=f"{member} • ID: {member.id}", icon_url=member.avatar)
      await member.ban(reason=reason)
      await ctx.send(embed=embed, content=None, delete_after=10)
      await msg.delete()


  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, *, member:int, reason=None):
    user = await client.fetch_user(member)
    guild = await client.fetch_guild(ctx.message.guild.id)
    msg = ctx.message
    if user != None:
      async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=1, oldest_first=False):
        if user != None:
          mod = await client.fetch_user(ctx.author.id)
          if check_logs(ctx.guild.id)[0] is True:
            chan = check_logs(ctx.guild.id)[1]
            channel = ctx.guild.get_channel(int(chan))
            embed2 = discord.Embed(description=f"**{user.mention} has been unbanned.**\n\n`Reason:` {reason}", color=discord.Color.from_rgb(r=0, g=255, b=0), timestamp=ctx.message.created_at)
            embed2.set_author(name=f"{user.name} • ID: {user.id}", icon_url=user.avatar)
            embed2.set_footer(text=f'Moderator: {mod} • ID: {mod.id}', icon_url=mod.avatar)
            await channel.send(embed=embed2, content=None)

          embed = discord.Embed(description=f"**{user.mention} has been unbanned.**\n\n`Reason:` {reason}", color=discord.Color.from_rgb(r=0, g=255, b=0))
          embed.set_author(name=f"{user.name} • ID: {user.id}", icon_url=user.avatar)
          await guild.unban(user, reason=None)
          await ctx.send(embed=embed, content=None, delete_after=10)
          await msg.delete()
        else:
          embed = discord.Embed(description=f"**`ERROR:`** ```python\nUser '{user.name}' is not banned.\n```", color=discord.Color.from_rgb(r=255, g=0, b=0))
          await ctx.send(embed=embed, content=None, delete_after=10)
          await msg.delete()
    else:
      embed = discord.Embed(description=f"**`ERROR:`** ```python\nUser not found.\n```", color=discord.Color.from_rgb(r=255, g=0, b=0))
      await ctx.send(embed=embed, content=None, delete_after=10)
      await msg.delete()


  @commands.command()
  @commands.before_invoke(disabled_check)
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member, *, reason=None):
      msg = ctx.message
      mod = client.get_user(id=ctx.author.id)
      if check_logs(ctx.guild.id)[0] is True:
        chan = check_logs(ctx.guild.id)[1]
        channel = ctx.guild.get_channel(int(chan))
        embed2 = discord.Embed(description=f"**{member.mention} has been kicked.**\n**Reason:** {reason}", color=discord.Color.from_rgb(r=255, g=0, b=0), timestamp=ctx.message.created_at)
        embed2.set_author(name=f"{member} • ID: {member.id}", icon_url=member.avatar)
        embed2.set_footer(text=f'Moderator: {mod} • ID: {mod.id}', icon_url=mod.avatar)
        await channel.send(embed=embed2, content=None)

      embed = discord.Embed(description=f"**{member.mention} has been kicked.**", color=discord.Color.from_rgb(r=255, g=0, b=0))
      embed.set_author(name=f"{member} • ID: {member.id}", icon_url=member.avatar)
      await member.kick(reason=reason)
      await ctx.send(embed=embed, content=None, delete_after=10)
      await msg.delete()

  @commands.command(aliases=['clear'])
  @commands.has_permissions(manage_messages=True)
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 3, commands.BucketType.guild)
  async def purge(self, ctx, limit=5, member: discord.Member=None):
    if check_logs(ctx.guild.id)[0] is True:
      chan = check_logs(ctx.guild.id)[1]
      channel = ctx.guild.get_channel(int(chan))
      embed2 = discord.Embed(description=f"Bulk delete in <#{ctx.channel.id}>\n\nDeleted {limit} messages.", color=discord.Color.from_rgb(r=255, g=0, b=0))
      embed2.set_footer(text=f'Moderator: {ctx.author}', icon_url=ctx.author.avatar)
      await channel.send(embed=embed2, content=None)
    await ctx.message.delete()
    msg = []
    if limit >= 101:
      embed = discord.Embed(description="The maximum purge amount is 100.", color=discord.Color.from_rgb(r=255, g=0, b=0))
      await ctx.send(embed=embed, content=None, delete_after=3)
    else:
      try:
        limit = int(limit)
      except:
        return await ctx.send("Please pass in an integer as limit")
      if not member:
        embed = discord.Embed(description=f"Purged {limit} messages", color=discord.Color.from_rgb(r=255, g=0, b=0))
        await ctx.channel.purge(limit=limit)
        await ctx.send(embed=embed, content=None, delete_after=3)
      else:
        async for m in ctx.channel.history():
          if len(msg) == limit:
            break
          if m.author == member:
            msg.append(m)
          embed = discord.Embed(description=f"Purged {limit} messages", color=discord.Color.from_rgb(r=255, g=0, b=0))
          await ctx.channel.delete_messages(msg)
          await ctx.send(embed=embed, content=None, delete_after=3)

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def dm(self, ctx, user: discord.User, *, talking):
    serv = client.get_guild(ctx.guild.id)
    if (ctx.author.guild.id == 508043534071365652) or (ctx.author.guild.id == 863561097604497438):
      user2 = await client.fetch_user(user.id)
      fax = client.user.id
      msg = ctx.message
      if user.id == fax:
        embed = discord.Embed(description="I can't dm myself.", color=discord.Color.from_rgb(r=255, g=0, b=0))
        await ctx.send(embed=embed, content=None, delete_after=5)
        print(f'{ctx.author} tried to dm the bot with the content: {talking}', f'(Date and time: {currentDT})')
        await msg.delete()
      else:
        if talking.startswith("https://"):
          embed = discord.Embed(description=f'Dm sent to <@{user.id}> with the content:\n"{talking}"')
          embed.set_image(url=f'{talking}')
          embed.set_author(name=f"By {ctx.author}", icon_url=f"{ctx.author.avatar}")
          await user2.send(f'{talking}')
          await ctx.send(embed=embed, content=None)
          print(f'Dm sent to {user} with the content: "{talking}"')
          print(f'Dm requested by: {ctx.author}', f'(Date and time: {currentDT})')
          await msg.delete()
        else:
          embed = discord.Embed(description=f'Dm sent to <@{user.id}> with the content:\n"{talking}"')
          embed.set_author(name=f"By {ctx.author}", icon_url=f"{ctx.author.avatar}")
          await user2.send(f'{talking}')
          await ctx.send(embed=embed, content=None)
          print(f'Dm sent to {user} with the content: "{talking}"')
          print(f'Dm requested by: {ctx.author}', f'(Date and time: {currentDT})')
          await msg.delete()
    else:
      embed = discord.Embed(description=f"**`ERROR:`** ```\nThis command is only available to moderators from {serv}.\n```", color=red)
      await ctx.send(embed=embed, content=None, delete_after=5)


  @commands.command(aliases=['removewarn','deletewarn'])
  @commands.has_permissions(manage_roles=True)
  async def unwarn(self, ctx, member: discord.Member, *, reason: str=None):
    try:
      check_warn = get_db('users')[f"{member.id}"][f'warnings-{ctx.guild.id}']
    except:
      embed = discord.Embed(description=f"**`ERROR:`**\n```python\nThis user does not have any warns.\n```", color=red)
      await ctx.message.delete(delay=10)
      await ctx.send(embed=embed, content=None, delete_after=15)
      return
    else:
      embed = discord.Embed(description=f"Please reply with the **ID** of the warn you want to remove from this user.")
      embed.set_footer(text=f"The ids can be found by ivoking {bot_prefix}userinfo.")
      shut = await ctx.send(embed=embed, content=None)

      def check(m):
        return m.content and m.author == ctx.author
  
      msg = await client.wait_for("message", check=check, timeout=20)

      if str(msg.content.lower()) == "all":
        embed3 = discord.Embed(description=f"Successfully removed **ALL** warnings from user {member}.\n\n**`Reason:`** {reason}")
        embed3.set_author(name=f"Moderator: {ctx.author} • ID: {ctx.author.id}", icon_url=f"{ctx.author.avatar}")

        embed2 = discord.Embed(description=f"**All of your warnings from {ctx.guild} have been lifted.**\n\n**`Reason:`** {reason}", color=discord.Color.from_rgb(r=0, b=0, g=255))
        embed2.set_author(name=f"Moderator: {ctx.author} • ID: {ctx.author.id}", icon_url=f"{ctx.author.avatar}")
        
        del_db(f'users/{ctx.author.id}', f"warnings-{ctx.guild.id}")

        if check_logs(ctx.guild.id)[0] is True:
          chan = check_logs(ctx.guild.id)[1]
          channel = ctx.guild.get_channel(int(chan))
          await channel.send(embed=embed3, content=None)

        await shut.edit(embed=embed3, content=None)
        await member.send(embed=embed2, content=None)
        return
      
      if str(msg.content) in check_warn:
        embed3 = discord.Embed(description=f"Successfully removed warn #{int(msg.content)} from user {member}.\n\n**`Reason:`** {reason}")
        embed3.set_author(name=f"Moderator: {ctx.author} • ID: {ctx.author.id}", icon_url=f"{ctx.author.avatar}")

        embed2 = discord.Embed(description=f"**One of your warnings from {ctx.guild} have been lifted. (ID: {msg.content})**\n\n**`Reason:`** {reason}", color=discord.Color.from_rgb(r=0, b=0, g=255))
        embed2.set_author(name=f"Moderator: {ctx.author} • ID: {ctx.author.id}", icon_url=f"{ctx.author.avatar}")

        check_warn2 = check_warn.split(f"ID: {msg.content}")[1].lstrip().split('/', 1)[0]
        check_warn3 = check_warn.replace(f"ID: {msg.content}{check_warn2}/", "")
        update_db('users', f"{member.id}", {f"warnings-{ctx.guild.id}": check_warn3})

        if check_logs(ctx.guild.id)[0] is True:
          chan = check_logs(ctx.guild.id)[1]
          channel = ctx.guild.get_channel(int(chan))
          await channel.send(embed=embed3, content=None)
        
        await msg.delete()
        await shut.edit(embed=embed3, content=None)
        await member.send(embed=embed2, content=None)
        
        
      else:
        embed3 = discord.Embed(description=f"**`ERROR:`** ```python\nCould not find id #{msg.content}\n```", color=red)
        embed3.set_author(name=f"Moderator: {ctx.author} • ID: {ctx.author.id}", icon_url=f"{ctx.author.avatar}")
        await msg.delete()
        await shut.edit(embed=embed3, content=None)
    
  @commands.command()
  @commands.has_permissions(manage_roles=True)
  async def warn(self, ctx, member: discord.Member, *, reason=None):
    if not reason:
      embed = discord.Embed(description=f"**`ERROR:`** ```python\nYou must provide a reason for the warn.\n```", color=red)
      await ctx.message.delete(delay=10)
      await ctx.message.send(embed=embed, content=None, delete_after=15)
      return

    try:
      check = get_db('users')[f"{member.id}"][f'warnings-{ctx.guild.id}']
    except:
      check = ""

    id_gen = randint(1, 99999)
    update_db('users', f"{member.id}", {f"warnings-{ctx.guild.id}": f"{check}ID: {id_gen}=Warning <t:{round(datetime.datetime.now().timestamp())}:R>=Reason: {reason}/"})
    
    embed = discord.Embed(description=f"**`SUCCESS:`**\nUser {member.mention} has been warned.\nReason: {reason}", color=discord.Color.from_rgb(r=0, b=0, g=255))
    embed.set_author(name=f"Moderator: {ctx.author} • ID: {ctx.author.id}", icon_url=f"{ctx.author.avatar}")
    
    embed2 = discord.Embed(description=f"**You have been warned in {ctx.guild}.**\n\n**`Reason:`** {reason}", color=discord.Color.from_rgb(r=255, b=0, g=0))
    embed2.set_author(name=f"Moderator: {ctx.author} • ID: {ctx.author.id}", icon_url=f"{ctx.author.avatar}")
    
    await ctx.message.delete(delay=5)
    await ctx.send(embed=embed, content=None)

    try:
      actual_member = ctx.guild.get_member(member.id)
      await actual_member.send(embed=embed2, content=None)
    except:
      embed = discord.Embed(description=f"**`ERROR:`**\nCouldn't find User from '{member}'\n", color=red)
      await ctx.message.delete(delay=10)
      await ctx.send(embed=embed, content=None, delete_after=15)
                           
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def botreply(self, ctx, chn: int, mes: int, *, rest: str):
    global count2, count4, channels2, mes2
    server = client.get_guild(ctx.guild.id)
    chn2 = server.get_channel(chn)
    mes2 = await chn2.fetch_message(mes)
    if "@everyone" in rest:
      return
    elif "@here" in rest:
      return
    else:
      await mes2.reply(content=f"{rest}")

  @dm.error
  async def clear_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(description=f"{ctx.author.mention}, try: {bot_prefix}dm @person message", color=discord.Color.from_rgb(r=255, b=0, g=0))
      await ctx.send(embed=embed, content=None, delete_after=10)


  @purge.error
  async def clear_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(description=f"Please specify the amount of messages that you want to delete.\n`Examples:` {bot_prefix}purge 10 or {bot_prefix} @member 10", color=discord.Color.from_rgb(r=255, g=0, b=0))
      await ctx.send(embed=embed, content=None, delete_after=10)


  @say.error
  async def clear_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(description=f"{ctx.author.mention}, try: g!say #channel hello", color=discord.Color.from_rgb(r=255, b=0, g=0))
      await ctx.send(embed=embed, content=None, delete_after=10)

  @lock.error
  async def clear_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed= discord.Embed(description=f"{ctx.author.mention}, please fill in all the required arguments.\n`Example:` {bot_prefix}lock #channel 30m reason", color=discord.Color.from_rgb(r=255, g=0, b=0))
      await ctx.send(embed=embed, content=None, delete_after=10)


def setup(client):
  client.add_cog(Mod_coms(client))
