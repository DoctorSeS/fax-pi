import asyncio

import discord
from discord import Option
from discord.ext import commands

from cogs import member_coms
from cogs.events import check_logs
from cogs.member_coms import Avatar
from cogs.score import check_currency
from database import *
from main import client, red, green, currency


class Confirm_slash(discord.ui.View):
	def __init__(self, ctx, amount, user, yourvaluefinal, uservaluefinal, yourvalueint, uservalueint):
		super().__init__(timeout=500)
		self.value = 0
		self.ctx = ctx
		self.amount = amount
		self.user = user
		self.yourvaluefinal = yourvaluefinal
		self.uservaluefinal = uservaluefinal
		self.yourvalueint = yourvalueint
		self.uservalueint = uservalueint

	@discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="Yes")
	async def yes(self, button, interaction):
		if interaction.user.id == self.ctx.author.id:
			update_db('users', f"{self.user.id}", {"score": self.uservaluefinal})
			update_db('users', f"{interaction.user.id}", {"score": self.yourvaluefinal})
			finalembed = discord.Embed(description=f"```ini\n[ {check_currency(interaction.guild.id)} has been wired successfully. ]\n\n{interaction.user.name}'s {check_currency(interaction.guild.id)}: {self.yourvalueint} ≫ {self.yourvaluefinal}\n{self.user.name}'s {check_currency(interaction.guild.id)}: {self.uservalueint} ≫ {self.uservaluefinal}```", color=green)
			await interaction.response.edit_message(embed=finalembed, content=None, view=None)

			finalembed2 = discord.Embed(description=f"```ini\n[ {check_currency(interaction.guild.id)} has been wired successfully. ]\n\n{interaction.user.name}'s {check_currency(interaction.guild.id)}: {self.yourvalueint} ≫ {self.yourvaluefinal}\n{self.user.name}'s {check_currency(interaction.guild.id)}: {self.uservalueint} ≫ {self.uservaluefinal}\n\nYou have received {self.amount} {currency} from {interaction.user.name}.```\n[Jump to the message]({interaction.message.jump_url})", color=green)
			await self.user.send(embed=finalembed2, content=None, view=None)
		else:
			return

	@discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="No")
	async def no(self, button, interaction):
		if interaction.user.id == self.ctx.author.id:
			finalembed = discord.Embed(
				description=f"```ini\n[ {check_currency(interaction.guild.id)} transaction cancelled. ]\n\nPlease try again if you mentioned the wrong amount of {check_currency(interaction.guild.id)}.```",
				color=red)
			await interaction.response.edit_message(embed=finalembed, content=None, view=None)
		else:
			return

	async def on_timeout(self):
		for child in self.children:
			child.disabled = True
		else:
			await self.message.edit(view=self, content="Timed out.")


class Slash_commands(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.slash_command(description="Display your avatar, or somebody else's.", default_permissions=True)
	async def avatar(self, ctx, *, member: discord.User = None):
		if ctx.guild:
			if check_logs(ctx.guild.id)[0] is True:
				logs2 = check_logs(ctx.guild.id)[2]
				if logs2 != "None":
					if member == None:
						member2 = "None"
					else:
						member2 = member
					logs2 = ctx.guild.get_channel(int(logs2))
					embed = discord.Embed(description=f"Slash Command used in <#{ctx.channel.id}>.",
					                      color=discord.Color.random())
					embed.add_field(name=f'Command used:', value=f"/avatar {member2}")
					embed.set_author(name=f"{ctx.author} • ID: {ctx.author.id}", icon_url=ctx.author.avatar)
					embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)
					await logs2.send(embed=embed, content=None)

		auth2 = ctx.author
		if member:
			auth2 = member
			avatar = discord.Embed(title=f"{auth2.name}'s avatar:", description=f"[Avatar Url]({auth2.avatar})\n{auth2.mention} - ID: {auth2.id}", color=auth2.color)
			avatar.set_footer(icon_url=ctx.author.avatar, text=f'Requested by {ctx.author}')

		avatar = discord.Embed(title=f"{auth2.name}'s avatar:", description=f"[Avatar Url]({auth2.avatar})\n{auth2.mention} - ID: {auth2.id}", color=auth2.color)
		avatar.set_image(url=f'{auth2.avatar}')
		view = Avatar(ctx, auth2)

		await ctx.respond(embed=avatar, content=None, view=view, ephemeral=True)

	@commands.slash_command(name="userinfo", description="Display information about someone, or yourself. This command isn't ephemeral.", default_permissions=True)
	async def userinfo_slash(self, ctx, *, member: Option(discord.Member, "The person you want information on.", required=False, default=None)):
		if not ctx.guild:
			await ctx.respond("This command cannot be used in private messages.")
			return

		if ctx.guild:
			if check_logs(ctx.guild.id)[0] is True:
				logs2 = check_logs(ctx.guild.id)[2]
				if logs2 != "None":
					if member == None:
						member2 = "None"
					else:
						member2 = member
					logs2 = ctx.guild.get_channel(int(logs2))
					embed = discord.Embed(description=f"Slash Command used in <#{ctx.channel.id}>.",
					                      color=discord.Color.random())
					embed.add_field(name=f'Command used:', value=f"/userinfo {member2}")
					embed.set_author(name=f"{ctx.author} • ID: {ctx.author.id}", icon_url=ctx.author.avatar)
					embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)
					await logs2.send(embed=embed, content=None)
		server = client.get_guild(ctx.guild.id)
		if not member:
			member = ctx.author
			global hype, voice
			if member.premium_since == None:
				nitro = "None"
			else:
				nitro = f"Since <t:{round(member.premium_since.timestamp())}:f>"
			if member.public_flags.hypesquad_bravery == True:
				hype = "Bravery"
			elif member.public_flags.hypesquad_brilliance == True:
				hype = "Brilliance"
			elif member.public_flags.hypesquad_balance == True:
				hype = "Balance"
			else:
				hype = "None"
			if member.voice != None:
				voice = member.voice.channel
			else:
				voice = "None"
			embed = discord.Embed(title=f"**`Information about {member.name}`**", color=member.color,
			                      timestamp=member.created_at)
			embed.set_thumbnail(url=member.avatar)
			embed.set_footer(text=f'Account age:')
			embed.add_field(name='ID:', value=f"{member.id}")
			embed.add_field(name='Nickname:', value=f'{member.display_name}')
			embed.add_field(name='Bot?', value=member.bot)
			embed.add_field(name='Joined:', value=f"<t:{round(member.joined_at.timestamp())}:f>")
			embed.add_field(name='Status:', value=member.status)
			embed.add_field(name='Boost:', value=nitro)
			embed.add_field(name='On Mobile?', value=member.is_on_mobile())
			embed.add_field(name='Voice status:', value=f"Channel: `{voice}`")
			embed.add_field(name='Hypesquad:', value=hype)
			async with ctx.typing():
				await asyncio.sleep(1)
				await ctx.respond(embed=embed, content=None)
		else:
			if member == int or member.mention:
				pass
			else:
				member = server.get_member_named(member)
			if member.premium_since == None:
				nitro = "None"
			else:
				nitro = f"Since <t:{round(member.premium_since.timestamp())}:f>"
			if member.public_flags.hypesquad_bravery == True:
				hype = "Bravery"
			elif member.public_flags.hypesquad_brilliance == True:
				hype = "Brilliance"
			elif member.public_flags.hypesquad_balance == True:
				hype = "Balance"
			else:
				hype = "None"
			if member.voice != None:
				voice = member.voice.channel
			else:
				voice = "None"
			embed = discord.Embed(title=f"**`Information about {member.name}`**", color=member.color,
			                      timestamp=member.created_at)
			embed.set_thumbnail(url=member.avatar)
			embed.set_footer(text=f'Account age:')
			embed.add_field(name='ID:', value=f"{member.id}")
			embed.add_field(name='Nickname:', value=f'{member.display_name}')
			embed.add_field(name='Bot?', value=member.bot)
			embed.add_field(name='Joined:', value=f"<t:{round(member.joined_at.timestamp())}:f>")
			embed.add_field(name='Status:', value=member.status)
			embed.add_field(name='Boost:', value=nitro)
			embed.add_field(name='On Mobile?', value=member.is_on_mobile())
			embed.add_field(name='Voice status:', value=f"Channel: `{voice}`")
			embed.add_field(name='Hypesquad:', value=hype)
			async with ctx.typing():
				await asyncio.sleep(1)
				await ctx.respond(embed=embed, content=None)

	@commands.slash_command(name="roleinfo", description="Display information about someone's roles, or your roles. This command isn't ephemeral.", default_permissions=True)
	async def roleinfo_slash(self, ctx, *, member: Option(discord.Member, "The person you want role information on.", required=False, default=None)):
		if not ctx.guild:
			await ctx.respond("This command cannot be used in private messages.")
			return

		if check_logs(ctx.guild.id)[0] is True:
			logs2 = check_logs(ctx.guild.id)[2]
			if logs2 != "None":
				if member == None:
					member2 = "None"
				else:
					member2 = member
				logs2 = ctx.guild.get_channel(int(logs2))
				embed = discord.Embed(description=f"Slash Command used in <#{ctx.channel.id}>.",
				                      color=discord.Color.random())
				embed.add_field(name=f'Command used:', value=f"/roleinfo {member2}")
				embed.set_author(name=f"{ctx.author} • ID: {ctx.author.id}", icon_url=ctx.author.avatar)
				embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)
				await logs2.send(embed=embed, content=None)

		if not member:
			member = ctx.author
			roles = [role for role in ctx.author.roles]
			rols = str([role.mention for role in roles])
			rols2 = rols.replace("'", '')
			rols3 = rols2.replace("[", '')
			rols4 = rols3.replace("]", '')
			embed = discord.Embed(color=member.color)
			embed.set_author(name=f"Information about {member.name}'s roles")
			embed.set_thumbnail(url=member.avatar)
			embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar)
			embed.add_field(name='Permissions:',
			                value=f"`Administrator:` {member.guild_permissions.administrator}\n`Ban members:` {member.guild_permissions.ban_members}\n`Kick members:` {member.guild_permissions.kick_members}\n`Can view the logs:` {member.guild_permissions.view_audit_log}\n"
			                      f"`Manage channels:` {member.guild_permissions.manage_channels}\n`Manage messages:` {member.guild_permissions.manage_messages}\n`Manage server:` {member.guild_permissions.manage_guild}\n`View insights:` {member.guild_permissions.view_guild_insights}\n"
			                      f"`Manage emojis:` {member.guild_permissions.manage_emojis}\n`Manage roles:` {member.guild_permissions.manage_roles}\n`Manage Permissions:` {member.guild_permissions.manage_permissions}\n`View`<#{ctx.channel.id}>`:` {member.guild_permissions.view_channel}")
			embed.add_field(name=f'Information about `{member.top_role}`:',
			                value=f"`ID:` {member.top_role.id}\n`Color:` {member.top_role.color}\n`Position:` {member.top_role.position}\n`Default?` {member.top_role.is_default()}\n"
			                      f"`Created at:` {member.top_role.created_at}\n`Mentionable?` {member.top_role.mentionable}")
			embed.add_field(name=f'Roles ({len(roles)})', value=f"{rols4}", inline=False)
			embed.add_field(name='Top role:', value=member.top_role.mention, inline=True)
			if member.id == member.guild.owner.id:
				embed.add_field(name='Important:', value=f"**`Server Owner`**", inline=True)
			else:
				pass
			async with ctx.typing():
				await asyncio.sleep(1)
				await ctx.respond(embed=embed, content=None)
		else:
			if member == int or member.mention:
				pass
			else:
				member = ctx.guild.get_member_named(member)
			roles = [role for role in member.roles]
			rols = str([role.mention for role in roles])
			rols2 = rols.replace("'", '')
			rols3 = rols2.replace("[", '')
			rols4 = rols3.replace("]", '')
			embed = discord.Embed(color=member.color)
			embed.set_author(name=f"Information about {member.name}'s roles")
			embed.set_thumbnail(url=member.avatar)
			embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar)
			embed.add_field(name='Permissions:',
			                value=f"`Administrator:` {member.guild_permissions.administrator}\n`Ban members:` {member.guild_permissions.ban_members}\n`Kick members:` {member.guild_permissions.kick_members}\n`Can view the logs:` {member.guild_permissions.view_audit_log}\n"
			                      f"`Manage channels:` {member.guild_permissions.manage_channels}\n`Manage messages:` {member.guild_permissions.manage_messages}\n`Manage server:` {member.guild_permissions.manage_guild}\n`View insights:` {member.guild_permissions.view_guild_insights}\n"
			                      f"`Manage emojis:` {member.guild_permissions.manage_emojis}\n`Manage roles:` {member.guild_permissions.manage_roles}\n`Manage Permissions:` {member.guild_permissions.manage_permissions}\n`View`<#{ctx.channel.id}>`:` {member.guild_permissions.view_channel}")
			embed.add_field(name=f'Information about `{member.top_role}`:',
			                value=f"`ID:` {member.top_role.id}\n`Color:` {member.top_role.color}\n`Position:` {member.top_role.position}\n`Default?` {member.top_role.is_default()}\n"
			                      f"`Created at:` {member.top_role.created_at}\n`Mentionable?` {member.top_role.mentionable}")
			embed.add_field(name=f'Roles ({len(roles)})', value=f"{rols4}", inline=False)
			embed.add_field(name='Top role:', value=member.top_role.mention, inline=True)
			if member.id == member.guild.owner.id:
				embed.add_field(name='Important:', value=f"**`Server Owner`**", inline=True)
			else:
				pass
			async with ctx.typing():
				await asyncio.sleep(1)
				await ctx.respond(embed=embed, content=None)

	@commands.slash_command(description="Display any emoji of your choosing. Must be from a server the bot is in.", default_permissions=True)
	async def emoji(self, ctx, emoji: Option(discord.PartialEmoji, "The emoji you want to enlarge, can be just the name of it.", requried=True)):
		if ctx.guild:
			if check_logs(ctx.guild.id)[0] is True:
				logs2 = check_logs(ctx.guild.id)[2]
				if logs2 != "None":
					logs2 = ctx.guild.get_channel(int(logs2))
					embed = discord.Embed(description=f"Slash Command used in <#{ctx.channel.id}>.", color=discord.Color.random())
					embed.add_field(name=f'Command used:', value=f"/emoji {emoji}")
					embed.set_author(name=f"{ctx.author} • ID: {ctx.author.id}", icon_url=ctx.author.avatar)
					embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)
					await logs2.send(embed=embed, content=None)
		emojistring = str(emoji)
		if emojistring.startswith("<"):
			embed = discord.Embed(description=f"{emoji.name} - `ID: {emoji.id}`\n\n[Download link]({emoji.url})")
			embed.set_thumbnail(url=f'{emoji.url}')
			embed.set_footer(text=f'Created at: {emoji.created_at}')
			await ctx.respond(embed=embed, content=None)

	@commands.slash_command(name="sticker", description="Display any sticker of your choosing. Must be from a server the bot is in.")
	async def sticker_slash(self, ctx, *, sticker: Option(str, "The name of the sticker you want to enlarge.", requried=True)):
		if ctx.guild:
			if check_logs(ctx.guild.id)[0] is True:
				logs2 = check_logs(ctx.guild.id)[2]
				if logs2 != "None":
					logs2 = ctx.guild.get_channel(int(logs2))
					embed = discord.Embed(description=f"Slash Command used in <#{ctx.channel.id}>.", color=discord.Color.random())
					embed.add_field(name=f'Command used:', value=f"/sticker {sticker}")
					embed.set_author(name=f"{ctx.author} • ID: {ctx.author.id}", icon_url=ctx.author.avatar)
					embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)
					await logs2.send(embed=embed, content=None)

		if sticker:
			for x in client.guilds:
				stickers = client.get_guild(x.id).stickers
				if sticker in str(stickers):
					sticker_id = str(str(stickers).split(f"{sticker}' id=")[1].lstrip().split(" ")[0]) + f"-{x.id}"
					break

			if sticker_id != None:
				id = sticker_id.split("-")[0]
				id2 = sticker_id.split("-")[1]
				server = client.get_guild(int(id2))

				get = await server.fetch_sticker(int(id))

				format = str(get.format).replace("StickerFormatType.", "")
				embed = discord.Embed(
					description=f"{get.name} - `ID: {get.id}`\nFormat: `{format}`\n\n[Download link]({get.url})")
				embed.set_thumbnail(url=f"{get.url}")
				await ctx.respond(embed=embed, content=None)
			else:
				embed = discord.Embed(description=f'Could not find sticker "{sticker}"', color=red)
				await ctx.respond(embed=embed, content=None)
		else:
			embed = discord.Embed(description=f'Error.', color=red)
			await ctx.respond(embed=embed, content=None)

	@commands.slash_command(name="transmit", description="Give someone else some of your score.", default_permissions=True)
	async def transmit_slash(self, ctx, user: Option(discord.User, "The person you want to give score to.", required=True), amount: Option(int, "The amount of score you want to give.", required=True)):
		if ctx.guild:
			if check_logs(ctx.guild.id)[0] is True:
				logs2 = check_logs(ctx.guild.id)[2]
				embed = discord.Embed(description=f"Slash Command used in <#{ctx.channel.id}>.",
				                      color=discord.Color.random())
				embed.add_field(name=f'Command used:', value=f"/transmit {user} {amount}")
				embed.set_author(name=f"{ctx.author} • ID: {ctx.author.id}", icon_url=ctx.author.avatar)
				embed.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar)
				await logs2.send(embed=embed, content=None)

		if user == None:
			embed2 = discord.Embed(
				description=f"**`ERROR:`** ```python\nInvalid method.\nValid Methods: g!transmit <user> <amount>(+)```",
				color=red)
			await ctx.respond(embed=embed2, content=None, delete_after=10)
			return
		else:
			if user.id == ctx.author.id:
				embed2 = discord.Embed(
					description=f"**`ERROR:`** ```python\n{ctx.author.name}, you can not give {check_currency(ctx.guild.id)} to yourself.```",
					color=red)
				await ctx.respond(embed=embed2, content=None, delete_after=10)
				return
			else:
				pass
			if amount == None:
				embed2 = discord.Embed(
					description=f"**`ERROR:`** ```python\nInvalid method.\nValid Methods: g!transmit <user> <amount>(+)```",
					color=red)
				await ctx.respond(embed=embed2, content=None, delete_after=10)
				return
			else:
				try:
					uservalue = get_db('users')[f'{user.id}']['score']
				except:
					uservalue = 0

				try:
					yourvalue = get_db('users')[f'{ctx.author.id}']['score']
				except:
					yourvalue = 0

				uservalueint = float(uservalue)
				yourvalueint = float(yourvalue)
				amountstr = str(amount)
				if amountstr.startswith("-"):
					embed2 = discord.Embed(
						description=f"**`ERROR:`** ```python\n{ctx.author.name}, you can not give someone negative {check_currency(ctx.guild.id)}.```",
						color=red)
					await ctx.respond(embed=embed2, content=None, delete_after=30)
					return
				elif yourvalueint < amount:
					embed2 = discord.Embed(
						description=f"**`ERROR:`** ```python\n{ctx.author.name}, you can not give someone something you do not have.\n\nYour {check_currency(ctx.guild.id)}: {yourvalueint}\nAmount needed: {amount}```",
						color=red)
					await ctx.respond(embed=embed2, content=None, delete_after=30)
					return
				else:
					uservaluefinal = uservalueint + amount
					yourvaluefinal = yourvalueint - amount
					buttonembed = discord.Embed(
						description=f"```ini\n[ Are you sure you want to wire {amount} {check_currency(ctx.guild.id)} to {user.name}? ]\n\nThe values below will proceed if confirmation is received.\n{ctx.author.name}'s {check_currency(ctx.guild.id)}: {yourvalueint} ≫ {yourvaluefinal}\n{user.name}'s {check_currency(ctx.guild.id)}: {uservalueint} ≫ {uservaluefinal}```",
						color=0xedbc1c)
					view = Confirm_slash(ctx, amount, user, yourvaluefinal, uservaluefinal, yourvalueint, uservalueint)
					await ctx.respond(embed=buttonembed, content=None, view=view)

def setup(client):
	client.add_cog(Slash_commands(client))
