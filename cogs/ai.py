from discord.ext import commands, tasks
import discord
from main import client, bot_prefix
import os
import asyncio
import sys
import json

messages_channel = 983395530866585702
CHAT_IDS_FILE = "chat_ids.json"

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from characterai import aiocai


class reset_chat(discord.ui.View):
  def __init__(self, author, ai_cog):
    super().__init__(timeout=None)
    self.author = author
    self.ai_cog = ai_cog

  @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="Yes")
  async def yes(self, button, interaction):
    if interaction.user.id == self.author.id:
      if f"{self.author.id}" in self.ai_cog.chat_ids:
        del self.ai_cog.chat_ids[f"{self.author.id}"]
        self.ai_cog.save_chat_ids()
        await interaction.response.edit_message(view=None, content="Chat session has been reset.")

        channel = client.get_channel(messages_channel)
        embed = discord.Embed(description=f"Reset successful from {self.author.mention}.", color=0x001eff)
        embed.set_author(icon_url=self.author.avatar, name=self.author)
        await channel.send(embed=embed)

      else:
        await interaction.response.edit_message(view=None, content="Chat session not found.")

  @discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="No")
  async def no(self, button, interaction):
    await interaction.message.delete()

class Ai(commands.Cog):
  def __init__(self, client):
    self.chat_ids = self.load_chat_ids()
    self.client = client
    self.cai_client = aiocai.Client(os.getenv('C_AI_TOKEN'))

  def load_chat_ids(self):
    if os.path.exists(CHAT_IDS_FILE):
      with open(CHAT_IDS_FILE, 'r') as f:
        return json.load(f)
    return {}

  def save_chat_ids(self):
    with open(CHAT_IDS_FILE, 'w') as f:
      json.dump(self.chat_ids, f)

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


      ### AI SECTION
      if (str(message.content).lower() == 'reset') or (str(message.content).lower() == 'restart') or (str(message.content).lower() == f'{bot_prefix}restart') or (str(message.content).lower() == f'{bot_prefix}reset'):
        await message.channel.send(view=reset_chat(message.author, self), content="Are you sure that you want to reset the chat?")
        return
      else:
        try:
          char = os.getenv('C_AI_FAX')  # Character ID
          user_id = str(message.author.id)

          async with message.channel.typing():
            # Check if user already has an active chat
            if user_id in self.chat_ids:
              chat_id = self.chat_ids[user_id]
            else:
              await message.channel.send('```k\nThis is an introduction message, please type "reset" or "restart" to restart this chat when you want to.```')
              me = await self.cai_client.get_me()
              async with await self.cai_client.connect() as chat:
                # Start a new chat and store the chat ID
                new_chat, _ = await chat.new_chat(char, me.id)
                chat_id = new_chat.chat_id
                self.chat_ids[user_id] = chat_id
                self.save_chat_ids()

            # Send the user's message to the AI
            async with await self.cai_client.connect() as chat:
              response = await chat.send_message(char, chat_id, f"Username: {message.author.name} - Display Name: {message.author.display_name} (username and display name of the user that's trying to talk to you. You can use discord message formatting, if you want to.)\n\n{message.content}")

            await message.channel.send(response.text)

          embed2 = discord.Embed(description=f"Response to {message.author.mention}:\n\n{response.text}", color=0xff2a00)
          embed2.set_author(icon_url=message.author.avatar.url, name=message.author)
          await channel.send(embed=embed2)

        except Exception as e:
          await message.channel.send(f"```diff\nERROR: Something definitely went wrong.\n\n{str(e)}```")

          error_embed = discord.Embed(description=f"Error: {str(e)}", color=discord.Color.red())
          await channel.send(embed=error_embed)
          

def setup(client):
  client.add_cog(Ai(client))