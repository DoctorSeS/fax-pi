from discord.ext import commands, tasks
import discord
from random import randint
from main import client, bot_prefix, round_time, ses, currency
from discord.ui import InputText, Modal
from cogs.score import check_currency, check_folder, check_level
from database import *
from termcolor import cprint

no_badge_emoji = "<:no_badge:1138943658469634171>"
badge_emojies = {
  "role": ["<:role_badge2:1138939944023376025>", "<:role_badge3:1138939947328491622>", "<:role_badge4:1138939949274636328>", "<:role_badge5:1138939953296982257>", "<:role_badge6:1138939957281574962>"],
  "game": ["<:game_badge1:1139236149248938014>", "<:game_badge2:1139236151702601890>", "<:game_badge3:1139236153795555378>", "<:game_badge4:1139236156366671872>", "<:game_badge5:1139236157738205217>", "<:game_badge6:1139236160632262656>"],
  "patreon": ["<:patreon_badge1:1139515938929115307>", "<:patreon_badge2:1139515941491834940>", "<:patreon_badge3:1139515943857438770>", "<:patreon_badge4:1139515946738929665>"],
  "gambler": ["<:gambler_badge1:1205843114691010581>", "<:gambler_badge2:1205843116016271370>", "<:gambler_badge3:1205843117773951047>", "<:gambler_badge4:1205843119778824202>", "<:gambler_badge5:1205843122182164500>", "<:gambler_badge6:1205843124514193449>"],
  "bug_hunter": ["<:bug_hunter1:1176633062419865720>", "<:bug_hunter2:1176633068178645122>", "<:bug_hunter3:1176633077603250296>"],
  "no_badge": "<:no_badge:1176626089901162647>",
  "ARG1": "<:arg1:1297283944806613003>"
}


def get_badge_emoji(name, level):
  if "Beta" in name:
    return badge_emojies["role"][level - 1]
  elif "Game" in name:
    return badge_emojies["game"][level - 1]
  elif "Gambl" in name:
    return badge_emojies["gambler"][level - 1]
  elif "Supporter" in name:
    return badge_emojies["patreon"][level - 1]
  elif "Hunter" in name:
    return badge_emojies["bug_hunter"][level - 1]
  elif "Owner" in name:
    return "<:owner_badge:1139344922495950955>"
  elif "Neco" in name:
    return "<:neco_arc_shrug:1112389684732117133>"
  else:
    return badge_emojies["no_badge"]

def get_filename(name):
  if "Beta" in name:
    return "role_badge"
  elif "Game" in name:
    return "game_badge"
  elif "Gambl" in name:
    return "gambler_badge"
  elif "Supporter" in name:
    return "patreon_badge"
  elif "Owner" in name:
    return "owner_badge"
  elif "Neco" in name:
    return "dumbass"
  elif "Hunter" in name:
    return "bug_hunter"

def role_pos(role):
  if "Common" in role:
    return (990, 260)
  elif "Uncommon" in role:
    return (1040, 260)
  elif "Rare" in role:
    return (890, 260)
  elif "Legendary" in role:
    return (1020, 260)
  elif "Exotic" in role:
    return (890, 260)
  elif "Daredevil" in role:
    return (1025, 260)
  elif "Prophet" in role:
    return (990, 260)

def check_role(name):
  if "None" in name:
    return "pixel"
  elif "Common" in name:
    return "role1"
  elif "Uncommon" in name:
    return "role2"
  elif "Rare" in name:
    return "role3"
  elif "Legendary" in name:
    return "role4"
  elif "Exotic" in name:
    return "role5"
  elif "Daredevil" in name:
    return "role6"
  elif "Prophet" in name:
    return "role7"

def smooth_corners(im, rad):
  circle = im.new('L', (rad * 2, rad * 2), 0)
  draw = im.Draw(circle)
  draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
  alpha = im.new('L', im.size, 255)
  w, h = im.size
  alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
  alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
  alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
  alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
  im.putalpha(alpha)
  return im

#shop
boostprice = 200

role1emoji = "<:Common:1126127286484205598>"
role2emoji = "<:Uncommon:1126127291089563728>"
role3emoji = "<:Rare:1126127295736840242>"
role4emoji = "<:Legendary:1126127297678807151>"
role5emoji = "<:Exotic:1126127301717917757>"
role6emoji = "<:Daredevil:1126127310148481115>"
role7emoji = "<:Prophet:1126127316544794716>"

role1name = role1emoji.split("<:")[1].lstrip().split(":")[0]
role2name = role2emoji.split("<:")[1].lstrip().split(":")[0]
role3name = role3emoji.split("<:")[1].lstrip().split(":")[0]
role4name = role4emoji.split("<:")[1].lstrip().split(":")[0]
role5name = role5emoji.split("<:")[1].lstrip().split(":")[0]
role6name = role6emoji.split("<:")[1].lstrip().split(":")[0]
role7name = role7emoji.split("<:")[1].lstrip().split(":")[0]

def next_role(role):
  if "None" in role:
    return f"you have to buy the roles in order.\nThe next role you can buy is **`{role1name}`** {role1emoji}."
  elif role1name in role:
    return f"you have to buy the roles in order.\nThe next role you can buy is **`{role2name}`** {role2emoji}."
  elif role2name in role:
    return f"you have to buy the roles in order.\nThe next role you can buy is **`{role3name}`** {role3emoji}."
  elif role3name in role:
    return f"you have to buy the roles in order.\nThe next role you can buy is **`{role4name}`** {role4emoji}."
  elif role4name in role:
    return f"you have to buy the roles in order.\nThe next role you can buy is **`{role5name}`** {role5emoji}."
  elif role5name in role:
    return f"the next role you can buy is on [patreon](https://www.patreon.com/doctorses)."
  elif role6name in role:
    return f"the next role you can buy is on [patreon](https://www.patreon.com/doctorses)."
  elif role7name in role:
    return f"you already have the maximum possible role!"

#nodatabase
nodb = discord.Embed(description=f"You don't have any money.", color=discord.Color.from_rgb(r=255, g=0, b=0))

#nomoney
nomoney = discord.Embed(description=f"You don't have enough money to buy that.", color=discord.Color.from_rgb(r=255, g=0, b=0))

all_backgrounds = get_db('misc')['shop']['backgrounds']

class BackgroundPurchase(discord.ui.Button):
  def __init__(self, ctx, name, filename, color, category):
    super().__init__(
      label=name,
      custom_id=filename,
      style=color
      )
    self.ctx = ctx
    self.category = category

  async def callback(self, interaction: discord.Interaction):
    val = str(self.label)
    userid = str(interaction.user.id)
    price = int(all_backgrounds[self.category]['price'])
    if self.ctx.author.id == interaction.user.id:
      if val == "Purchase":
        try:
          inv = get_db('users')[f'{interaction.user.id}']['items']
        except:
          pass
        else:
          if "Backgrounds" in inv.keys():
            if self.custom_id in inv["Backgrounds"]:
              have = discord.Embed(description=f"{interaction.user.mention}, you can't have more than one of each background.")
              await interaction.message.channel.send(embed=have, content=None, delete_after=10)
              await interaction.response.defer()
              return
         
        try:
          money = get_db('users')[f'{interaction.user.id}']['score']
        except:
          nodb = discord.Embed(description=f"You don't have any {check_currency(interaction.guild.id)}.", color=discord.Color.from_rgb(r=255, g=0, b=0))
          await interaction.message.channel.send(embed=nodb, content=interaction.user.mention, delete_after=5)
          await interaction.response.defer()
        else:
          if float(money) >= price:
  
            try:
              inv = get_db('users')[f'{interaction.user.id}']['items']
            except:
              update_db(f'users/{interaction.user.id}', 'items', {"Backgrounds": [f"{self.custom_id}"]})
            else:
              if inv.get("Backgrounds") is None:
                update_db(f'users/{interaction.user.id}', 'items', {"Backgrounds": [f"{self.custom_id}"]})
              else:
                inv["Backgrounds"].append(f"{self.custom_id}")
                update_db(f'users/{interaction.user.id}', 'items', {"Backgrounds": inv["Backgrounds"]})
                

            money2 = float(money) - price
            update_db('users', f"{interaction.user.id}", {"score": money2})
            buy = discord.Embed(description=f"{interaction.user.mention} has bought a new background **{self.custom_id}**\n\n**{self.custom_id}** has been equipped as your background.")
            update_db('users', f'{interaction.user.id}', {'background': self.custom_id})
            await interaction.message.channel.send(embed=buy, content=None)
            await interaction.response.defer()
          else:
            nomoney.clear_fields()
            nomoney.add_field(name=f"Wallet:", value=f"You have: {money} {check_currency(interaction.guild.id)}\n\nYou need: {price} {check_currency(interaction.guild.id)} (Missing {price - float(money)})")
            await interaction.message.channel.send(embed=nomoney, content=f"<@{interaction.user.id}>", delete_after=10)
            await interaction.response.defer()
      
            embed = discord.Embed(description=val)
            await interaction.message.edit(embed=embed, content=None, view=self)
            await interaction.response.defer()

      else:
        f = discord.File(f"{os.getcwd()}/images/assets/backgrounds/{self.category}/{self.custom_id}.png", filename=f"{self.custom_id}.png")

        if price == 5000:
          shoutout = "\n\nSpecial thanks to [**benthecancer**](https://x.com/BenTheCancerer) for making these backgrounds."
        else:
          shoutout = ""
        embed = discord.Embed(description=f"Background Name: {val}\n\nPrice: {price} {check_currency(interaction.guild.id)}{shoutout}")
        embed.set_image(url=f"attachment://{self.custom_id}.png")
        await interaction.message.edit(embed=embed, content=None, view=Backgrounds(self.ctx, userid, change=val, category=self.category), file=f)
        await interaction.response.defer()

class Backgrounds(discord.ui.View):
  def __init__(self, ctx, author, change, category):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.author = author
    self.change = change
    self.category = str(category).lower()
    for x in all_backgrounds[self.category]["name"]:
      color = discord.ButtonStyle.primary
      filename = all_backgrounds[self.category]["filename"][int(all_backgrounds[self.category]["filename"].index(x.lower().replace(' ', '_')))]
      if change:
        if x == change:
          x = "Purchase"
          color = discord.ButtonStyle.green
        
      self.add_item(BackgroundPurchase(self.ctx, name=x, filename=filename, color=color, category=self.category))

  @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, custom_id="back", row=3)
  async def back(self, button, interaction):
    if self.ctx.author.id == interaction.user.id:
      category = discord.Embed(description=f"Please select what category of backgrounds you want to look at.\n\n**{list(all_backgrounds)[1].capitalize()}:** {all_backgrounds[list(all_backgrounds)[1]]['price']} {check_currency(interaction.guild.id)}\n**{list(all_backgrounds)[0].capitalize()}:** {all_backgrounds[list(all_backgrounds)[0]]['price']} {check_currency(interaction.guild.id)}\n**{list(all_backgrounds)[3].capitalize()}:** {all_backgrounds[list(all_backgrounds)[3]]['price']} {check_currency(interaction.guild.id)}\n**{list(all_backgrounds)[2].capitalize()}:** {all_backgrounds[list(all_backgrounds)[2]]['price']} {check_currency(interaction.guild.id)}")
      
      f = discord.File(f"{os.getcwd()}/images/pixel.png", filename="pixel.png")
      category.set_image(url="attachment://pixel.png")
      await interaction.message.edit(embed=category, view=Categories(self.ctx, self.author), file=f)
      await interaction.response.defer()

      
class CategoriesSummon(discord.ui.Button):
  def __init__(self, ctx, name):
    super().__init__(
      label=name.capitalize(),
      custom_id=name,
      style=discord.ButtonStyle.primary
      )
    self.ctx = ctx

  async def callback(self, interaction: discord.Interaction):
    val = str(self.label)
      
    userid = str(interaction.user.id)
    if self.ctx.author.id == interaction.user.id:
      category = discord.Embed(description=f"Please select what category of backgrounds you want to look at.\n\n**{list(all_backgrounds)[1].capitalize()}:** {all_backgrounds[list(all_backgrounds)[1]]['price']} {check_currency(interaction.guild.id)}\n**{list(all_backgrounds)[0].capitalize()}:** {all_backgrounds[list(all_backgrounds)[0]]['price']} {check_currency(interaction.guild.id)}\n**{list(all_backgrounds)[3].capitalize()}:** {all_backgrounds[list(all_backgrounds)[3]]['price']} {check_currency(interaction.guild.id)}\n**{list(all_backgrounds)[2].capitalize()}:** {all_backgrounds[list(all_backgrounds)[2]]['price']} {check_currency(interaction.guild.id)}")

      f = discord.File(f"{os.getcwd()}/images/pixel.png", filename="pixel.png")
      category.set_image(url="attachment://pixel.png")
      await interaction.message.edit(embed=category, content=None, view=Backgrounds(self.ctx, userid, change=None, category=self.custom_id))
      await interaction.response.defer()

class Categories(discord.ui.View):
  def __init__(self, ctx, author):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.author = author
    #for x in all_backgrounds:
    self.add_item(CategoriesSummon(self.ctx, name="Simple"))
    self.add_item(CategoriesSummon(self.ctx, name="Complex"))
    self.add_item(CategoriesSummon(self.ctx, name="Very Complex"))
    self.add_item(CategoriesSummon(self.ctx, name="Special"))

  @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, custom_id="back", row=1)
  async def back(self, button, interaction):
    all_items = get_db('misc')['shop']['items']
    options = []
    shop = discord.Embed(title=f"{check_currency(self.ctx.guild.id)} shop", description=f"Please select an item you want to buy.")
    for item in list(all_items):
      item_name = item.replace("Booster", " Booster")
      emoji = None
      emoji2 = ""
      if "Money" in item:
        emoji = "💰"
        emoji2 = emoji
      options.append(discord.SelectOption(label=item_name, emoji=emoji))
      shop.add_field(name=f"{item_name} {emoji2}", value=f"Price: {all_items[item][list(all_items[item])[0]]} {check_currency(self.ctx.guild.id)}\n{all_items[item][list(all_items[item])[1]]}")
    author = self.ctx.author.id
    view = Select(self.ctx, author, options)
    await interaction.message.edit(embed=shop, content=None, view=view)
    await interaction.response.defer()
  

class Shop_Select(discord.ui.Select):
  def __init__(self, options, ctx):
    super().__init__(
      placeholder="Select an item",
      max_values=1,
      options=options
      )
    self.options = options
    self.ctx = ctx

  async def callback(self, interaction: discord.Interaction):
    val = str(self.values[0])
    val2 = val.replace(" ", "")
    userid = interaction.user.id
    all_items = get_db('misc')['shop']['items']
    for item in list(all_items):
      if item == val2:
        try:
          money = get_db('users')[f"{interaction.user.id}"]["score"]
        except:
          nodb = discord.Embed(description=f"You don't have any {check_currency(interaction.guild.id)}.", color=discord.Color.from_rgb(r=255, g=0, b=0))
          await interaction.message.channel.send(embed=nodb, content=interaction.user.mention, delete_after=5)
          await interaction.response.defer()
        else:
          if money >= int(all_items[item][list(all_items[item])[0]]):
            try:
              inventory = get_db('users')[f'{userid}']['items']
            except:
              inventory = {f"{item}": 0}

            inventory.update({f"{item}": int(inventory[item]) + 1})
            update_db(f'users/{userid}', 'items', inventory)

            final_money = round(money - int(all_items[item][list(all_items[item])[0]]), 2)
            update_db('users', f"{interaction.user.id}", {"score": final_money})


    options = []
    shop = discord.Embed(title=f"{check_currency(self.ctx.guild.id)} shop", description=f"Please select an item you want to buy.")
    for item in list(all_items):
      item_name = item.replace("Booster", " Booster")
      emoji = None
      emoji2 = ""
      if "Money" in item:
        emoji = "💰"
        emoji2 = emoji
      options.append(discord.SelectOption(label=item_name, emoji=emoji))
      shop.add_field(name=f"{item_name} {emoji2}", value=f"Price: {all_items[item][list(all_items[item])[0]]} {check_currency(self.ctx.guild.id)}\n{all_items[item][list(all_items[item])[1]]}")

    shop.set_footer(text=f"{interaction.user.name} - Wallet: {final_money} {check_currency(self.ctx.guild.id)}\nPurchased 1 {val} - Total: {int(inventory[item])}", icon_url=interaction.user.avatar)
    await interaction.message.edit(embed=shop, view=Select(self.ctx, userid, self.options))
    await interaction.response.defer()

class Select(discord.ui.View):
  def __init__(self, ctx, author, options):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.author = author
    self.options = options
    self.add_item(Shop_Select(self.options, self.ctx))

  @discord.ui.button(label="Profile Backgrounds", style=discord.ButtonStyle.primary, custom_id="backgrounds", row=1)
  async def backgrounds(self, button, interaction):
    category = discord.Embed(description=f"Please select what category of backgrounds you want to look at.\n\n**{list(all_backgrounds)[1].capitalize()}:** {all_backgrounds[list(all_backgrounds)[1]]['price']} {check_currency(interaction.guild.id)}\n**{list(all_backgrounds)[0].capitalize()}:** {all_backgrounds[list(all_backgrounds)[0]]['price']} {check_currency(interaction.guild.id)}\n**{list(all_backgrounds)[3].capitalize()}:** {all_backgrounds[list(all_backgrounds)[3]]['price']} {check_currency(interaction.guild.id)}\n**{list(all_backgrounds)[2].capitalize()}:** {all_backgrounds[list(all_backgrounds)[2]]['price']} {check_currency(interaction.guild.id)}")

    await interaction.message.edit(embed=category, view=Categories(self.ctx, self.ctx.author.id))
    await interaction.response.defer()

class EventSelect(discord.ui.Select):
  def __init__(self, options, ctx):
    super().__init__(
      placeholder="Select a background",
      max_values=1,
      options=options
      )
    self.options = options
    self.ctx = ctx

  async def callback(self, interaction: discord.Interaction):
    val = str(self.values[0]).replace('Background: ', '')
    userid = str(interaction.user.id)
    if self.ctx.author.id == interaction.user.id:

      f = discord.File(f"{os.getcwd()}/images/assets/backgrounds/{check_folder(val)}.png", filename=f"{val}.png")

      embed = discord.Embed(description=f"Previewing Background: {val}")
      embed.set_image(url=f"attachment://{val}.png")

      await interaction.message.edit(embed=embed, content=None, view=Use_Background(self.ctx, userid, self.options), file=f)
      await interaction.response.defer()

class Use_Background(discord.ui.View):
  def __init__(self, ctx, author, options):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.author = author
    self.options = options
    self.add_item(EventSelect(self.options, self.ctx))

  @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, custom_id="back", row=1)
  async def back(self, button, interaction):
    userid = str(interaction.user.id)
    if self.ctx.author.id == interaction.user.id:
      options = []
      try:
        inv = get_db('users')[f"{interaction.user.id}"]['items']
      except:
        embed = discord.Embed(description=f"You don't have any items, buy some by invoking `{bot_prefix}shop`.", color=self.ctx.author.color)
      else:
        embed = discord.Embed(description=f"Select an item you want to use.\n\n{self.ctx.author.name}'s Items:")
        if "Backgrounds" in inv.keys():
          embed.add_field(name="Backgrounds:", value=f"You own: **{len(list(inv['Backgrounds']))}**")
        if ("MoneyBooster" in inv.keys()) or ("ExperienceBooster" in inv.keys()):
          moneyboosters = 0
          xpboosters = 0 
          if ("ExperienceBooster" in inv.keys()):
            xpboosters = inv['ExperienceBooster']
            options.append(discord.SelectOption(label="Experience Booster"))
          if ("MoneyBooster" in inv.keys()):
            moneyboosters = inv['MoneyBooster']
            options.append(discord.SelectOption(label="Money Booster"))
  
          embed.add_field(name="Boosters:", value=f"Money Boosters: **{moneyboosters}**\nExperience Boosters: **{xpboosters}**")
        
      options.append(discord.SelectOption(label="Set Background"))
      options.append(discord.SelectOption(label="Remove Background"))
      options.append(discord.SelectOption(label="Add your own Background"))
      options.append(discord.SelectOption(label="Edit Profile Background"))
      options.append(discord.SelectOption(label="Edit Badge Slots"))
      view = use_before(self.ctx, self.ctx.author.id, options)

      f = discord.File(f"{os.getcwd()}/images/pixel.png", filename="pixel.png")
      embed.set_image(url="attachment://pixel.png")
          
      await interaction.message.edit(embed=embed, view=view, file=f)
      await interaction.response.defer()

  @discord.ui.button(label="Apply", style=discord.ButtonStyle.green, custom_id="apply", row=1, disabled=False)
  async def apply(self, button, interaction):
    userid = str(interaction.user.id)
    if self.ctx.author.id == interaction.user.id:
      embeds = interaction.message.embeds
      for embed in embeds:
        embeddict = embed.to_dict()

      if "Previewing Background:" in embeddict['description']:
        background = embeddict['description'].split("Background: ")[1]
  
        update_db('users', f"{interaction.user.id}", {"background": background})
        embed = discord.Embed(description=f"Background applied.\n\n**{background[0].upper()}{background[1:]}** has been set as your profile background.")
        f = discord.File(f"{os.getcwd()}/images/pixel.png", filename="pixel.png")
  
        embed.set_image(url="attachment://pixel.png")
        
        await interaction.message.edit(embed=embed, view=None, file=f)
      else:
        await interaction.response.defer()
        return

class Edit_Modal(Modal):
  def __init__(self) -> None:
    super().__init__(title="Choose your color")
    self.add_item(InputText(label="Type in an RGB value of your wanted color", placeholder=f"Ex: {randint(0, 255)},{randint(0, 255)},{randint(0, 255)} OR Random OR Remove"))

  async def callback(self, interaction: discord.Interaction):
    color = self.children[0].value
    if "remove" in color.lower():
      try:
        del_db(f'users/{interaction.user.id}', 'edited_background')
      except:
        embed = discord.Embed(description=f"There is no edit to be removed.")
        await interaction.response.send_message(embed=embed, view=None)
        return
      else:
        embed = discord.Embed(description=f"Background image has been restored to default settings.")
        await interaction.response.send_message(embed=embed, view=None)
        return
        
    elif "," in color:
      if " " in color:
        color2 = color.replace(" ", "")
      else: 
        color2 = color
      color2 = color2.split(",")
      color4 = []
      for x in color2:
        if int(x) > 255:
          color4.append(255)
        else:
          color4.append(int(x))
          
      color3 = discord.Color.from_rgb(r=int(color4[0]), g=int(color4[1]), b=int(color4[2]))
      embed = discord.Embed(description=f"**Selected color:**\nR: {color4[0]}\nG: {color4[1]}\nB: {color4[2]}", color=color3)
      update_db(f"users", f"{interaction.user.id}", {"edited_background": [{color4[0]}, {color4[1]}, {color4[2]}]})
    else:
      color3 = discord.Color.random()
      embed = discord.Embed(description=f"**Selected color:** Random\n\nYour Background will always have a different color.")
      update_db(f"users", f"{interaction.user.id}", {"edited_background": "random"})
      
    await interaction.response.send_message(embed=embed, view=None)

class Badge_Select(discord.ui.Select):
  def __init__(self, options, ctx, slot):
    super().__init__(
      placeholder="Select a Badge",
      max_values=1,
      options=options
      )
    self.options = options
    self.ctx = ctx
    self.slot = slot

  async def callback(self, interaction: discord.Interaction):
    val = str(self.values[0])
    userid = str(interaction.user.id)
    if self.ctx.author.id == interaction.user.id:
      embeds = interaction.message.embeds
      for embed in embeds:
        embeddict = embed.to_dict()
        
      try:
        all_slots = get_db('users')[f'{interaction.user.id}']["badge_slots"]
      except:
        all_slots = {'1': "None", '2': "None", '3': "None", '4': "None", '5': "None", '6': "None", "holder": True}

      h = embeddict['fields']
      level = 1
      for x in h:
        if val in x["name"]:
          if not "Level 0" in x["value"]:
            level = int(str(x["value"].replace("Level ", ""))[0])

      if "Reset" in val:
        all_slots.update({str(self.slot): "None"})
        update_db(f'users/{interaction.user.id}', f"badge_slots", all_slots)
        await interaction.response.send_message(f"Slot **#{self.slot}** has been reset.", ephemeral=True)
        await interaction.message.edit(view=Badge_Slots2(self.ctx, self.ctx.author.id, self.slot, self.options))
        return

      if all_slots[str(self.slot)] != "None":
        other_badge_name = all_slots[str(self.slot)]

        all_slots.update({str(self.slot): f"{get_filename(val)}{level}"})
        update_db(f'users/{interaction.user.id}', f"badge_slots", all_slots)
        
        await interaction.response.send_message(f"Replaced **`{other_badge_name}`** for **`{val}`** in slot **#{self.slot}**.", ephemeral=True)
        await interaction.message.edit(view=Badge_Slots2(self.ctx, self.ctx.author.id, self.slot, self.options))
        return
        
      a = [1, 2, 3, 4, 5, 6]
      for slotter in a:
        if get_filename(val) == all_slots[str(slotter)]:
          await interaction.response.send_message(f"**`{val}`** is already placed in slot **#{slotter}**.", ephemeral=True)
          await interaction.message.edit(view=Badge_Slots2(self.ctx, self.ctx.author.id, self.slot, self.options))
          break
        else:
          continue
          
      else:
        all_slots.update({str(self.slot): f"{get_filename(val)}{level}"})
        update_db(f'users/{interaction.user.id}', f"badge_slots", all_slots)
          
        await interaction.response.send_message(f"**`{val}`** has been placed in slot **#{self.slot}**.", ephemeral=True)
        await interaction.message.edit(view=Badge_Slots2(self.ctx, self.ctx.author.id, self.slot, self.options))

class Badge_Slots2(discord.ui.View):
  def __init__(self, ctx, author, slot, options):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.author = author
    self.slot = slot
    self.options = options
    self.add_item(Badge_Select(self.options, self.ctx, self.slot))

  @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, custom_id="back", row=1)
  async def back(self, button, interaction):
    if self.ctx.author.id == interaction.user.id:
      await interaction.message.edit(view=Badge_Slots(self.ctx, self.author))
      await interaction.response.defer()
    
class Badge_Slots(discord.ui.View):
  def __init__(self, ctx, author, ):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.author = author

  @discord.ui.button(label="Slot 1", style=discord.ButtonStyle.green, custom_id="1", row=0, disabled=False)
  async def slot_1(self, button, interaction):
    if self.ctx.author.id == interaction.user.id:
      embeds = interaction.message.embeds
      for embed in embeds:
        embeddict = embed.to_dict()
  
      options = []
      h = embeddict['fields']
      for x in h:
        if not "Level 0" in x["value"]:
          level = int(str(x["value"].replace("Level ", ""))[0])
          options.append(discord.SelectOption(label=f"{x['name']}", emoji=get_badge_emoji(x['name'], level)))

      options.append(discord.SelectOption(label=f"Reset Slot", emoji=get_badge_emoji("None", 0)))
      await interaction.message.edit(view=Badge_Slots2(self.ctx, self.author, button.custom_id, options))
      await interaction.response.defer()

  @discord.ui.button(label="Slot 2", style=discord.ButtonStyle.green, custom_id="2", row=0, disabled=False)
  async def slot_2(self, button, interaction):
    if self.ctx.author.id == interaction.user.id:
      embeds = interaction.message.embeds
      for embed in embeds:
        embeddict = embed.to_dict()
  
      options = []
      h = embeddict['fields']
      for x in h:
        if not "Level 0" in x["value"]:
          level = int(str(x["value"].replace("Level ", ""))[0])
          options.append(discord.SelectOption(label=f"{x['name']}", emoji=get_badge_emoji(x['name'], level)))

      options.append(discord.SelectOption(label=f"Reset Slot", emoji=get_badge_emoji("None", 0)))
      await interaction.message.edit(view=Badge_Slots2(self.ctx, self.author, button.custom_id, options))
      await interaction.response.defer()

  @discord.ui.button(label="Slot 3", style=discord.ButtonStyle.green, custom_id="3", row=1, disabled=False)
  async def slot_3(self, button, interaction):
    if self.ctx.author.id == interaction.user.id:
      embeds = interaction.message.embeds
      for embed in embeds:
        embeddict = embed.to_dict()
  
      options = []
      h = embeddict['fields']
      for x in h:
        if not "Level 0" in x["value"]:
          level = int(str(x["value"].replace("Level ", ""))[0])
          options.append(discord.SelectOption(label=f"{x['name']}", emoji=get_badge_emoji(x['name'], level)))

      options.append(discord.SelectOption(label=f"Reset Slot", emoji=get_badge_emoji("None", 0)))
      await interaction.message.edit(view=Badge_Slots2(self.ctx, self.author, button.custom_id, options))
      await interaction.response.defer()

  @discord.ui.button(label="Slot 4", style=discord.ButtonStyle.green, custom_id="4", row=1, disabled=False)
  async def slot_4(self, button, interaction):
    if self.ctx.author.id == interaction.user.id:
      embeds = interaction.message.embeds
      for embed in embeds:
        embeddict = embed.to_dict()
  
      options = []
      h = embeddict['fields']
      for x in h:
        if not "Level 0" in x["value"]:
          level = int(str(x["value"].replace("Level ", ""))[0])
          options.append(discord.SelectOption(label=f"{x['name']}", emoji=get_badge_emoji(x['name'], level)))

      options.append(discord.SelectOption(label=f"Reset Slot", emoji=get_badge_emoji("None", 0)))
      await interaction.message.edit(view=Badge_Slots2(self.ctx, self.author, button.custom_id, options))
      await interaction.response.defer()

  @discord.ui.button(label="Slot 5", style=discord.ButtonStyle.green, custom_id="5", row=2, disabled=False)
  async def slot_5(self, button, interaction):
    if self.ctx.author.id == interaction.user.id:
      embeds = interaction.message.embeds
      for embed in embeds:
        embeddict = embed.to_dict()
  
      options = []
      h = embeddict['fields']
      for x in h:
        if not "Level 0" in x["value"]:
          level = int(str(x["value"].replace("Level ", ""))[0])
          options.append(discord.SelectOption(label=f"{x['name']}", emoji=get_badge_emoji(x['name'], level)))

      options.append(discord.SelectOption(label=f"Reset Slot", emoji=get_badge_emoji("None", 0)))
      await interaction.message.edit(view=Badge_Slots2(self.ctx, self.author, button.custom_id, options))
      await interaction.response.defer()

  @discord.ui.button(label="Slot 6", style=discord.ButtonStyle.green, custom_id="6", row=2, disabled=False)
  async def slot_6(self, button, interaction):
    if self.ctx.author.id == interaction.user.id:
      embeds = interaction.message.embeds
      for embed in embeds:
        embeddict = embed.to_dict()
  
      options = []
      h = embeddict['fields']
      for x in h:
        if not "Level 0" in x["value"]:
          level = int(str(x["value"].replace("Level ", ""))[0])
          options.append(discord.SelectOption(label=f"{x['name']}", emoji=get_badge_emoji(x['name'], level)))

      options.append(discord.SelectOption(label=f"Reset Slot", emoji=get_badge_emoji("None", 0)))
      await interaction.message.edit(view=Badge_Slots2(self.ctx, self.author, button.custom_id, options))
      await interaction.response.defer()

  @discord.ui.button(label="Back", style=discord.ButtonStyle.danger, custom_id="back", row=1)
  async def back(self, button, interaction):
    userid = str(interaction.user.id)
    if self.ctx.author.id == interaction.user.id:
      options = []
      try:
        inv = get_db('users')[f'{interaction.user.id}']['items']
      except:
        embed = discord.Embed(description=f"You don't have any items, buy some by invoking `{bot_prefix}shop`.", color=self.ctx.author.color)
      else:
        embed = discord.Embed(description=f"Select an item you want to use.\n\n{self.ctx.author.name}'s Items:")
        if "Backgrounds" in inv.keys():
          embed.add_field(name="Backgrounds:", value=f"You own: **{len(list(inv['Backgrounds']))}**")
        if ("MoneyBooster" in inv.keys()) or ("ExperienceBooster" in inv.keys()):
          moneyboosters = 0
          xpboosters = 0 
          if ("ExperienceBooster" in inv.keys()):
            xpboosters = inv['ExperienceBooster']
            options.append(discord.SelectOption(label="Experience Booster"))
          if ("MoneyBooster" in inv.keys()):
            moneyboosters = inv['MoneyBooster']
            options.append(discord.SelectOption(label="Money Booster"))
  
          embed.add_field(name="Boosters:", value=f"Money Boosters: **{moneyboosters}**\nExperience Boosters: **{xpboosters}**")
        
      options.append(discord.SelectOption(label="Set Background"))
      options.append(discord.SelectOption(label="Remove Background"))
      options.append(discord.SelectOption(label="Add your own Background"))
      options.append(discord.SelectOption(label="Edit Profile Background"))
      options.append(discord.SelectOption(label="Edit Badge Slots"))
      view = use_before(self.ctx, self.ctx.author.id, options)
      await interaction.message.edit(embed=embed, view=view)
      await interaction.response.defer()

  @discord.ui.button(label="Reset", style=discord.ButtonStyle.danger, custom_id="reset", row=0)
  async def Reset(self, button, interaction):
    if self.ctx.author.id == interaction.user.id:

      try:
        del_db(f'users/{interaction.user.id}', 'badge_slots')
      except:
        pass
      
      await interaction.response.send_message("All Badges have been removed from their slots.", ephemeral=True)
      await interaction.message.edit(view=self)

class Use(discord.ui.Select):
  def __init__(self, options, ctx):
    super().__init__(
      placeholder="Select a background",
      max_values=1,
      options=options
      )
    self.options = options
    self.ctx = ctx
    self.author = self.ctx.author.id

  async def callback(self, interaction: discord.Interaction):
    val = str(self.values[0])
    userid = str(interaction.user.id)
    embeds = interaction.message.embeds
    for embed in embeds:
      embeddict = embed.to_dict()
    if int(userid) == int(self.ctx.author.id):
      if "Booster" in str(val):
        if "Money" in str(val):
          boostertype = 1
        else:
          boostertype = 0
        moneyboosters = 0
        xpboosters = 0 
        try:
          inv = get_db(f'users')[f'{interaction.user.id}']['items']
        except:
          embed = discord.Embed(description=f"You don't have any items, buy some by invoking `{bot_prefix}shop`.", color=self.ctx.author.color)
          inv = None
        else:
          embed = discord.Embed(description=f"Select an item you want to use.\n\n{self.ctx.author.name}'s Items:")
          if "Backgrounds" in inv.keys():
            embed.add_field(name="Backgrounds:", value=f"You own: **{len(list(inv['Backgrounds']))}**")
          if ("MoneyBooster" in inv.keys()) or ("ExperienceBooster" in inv.keys()):
            if ("ExperienceBooster" in inv.keys()):
              xpboosters = int(inv['ExperienceBooster'])
            if ("MoneyBooster" in inv.keys()):
              moneyboosters = int(inv['MoneyBooster'])

        if boostertype == 0:
          if xpboosters > 0:
            xpboosters -= 1
            if (xpboosters <= 0):
              inv.pop("ExperienceBooster")
              update_db(f'users/{userid}', "items", inv)
            else:
              inv.update({"ExperienceBooster": xpboosters})
              update_db(f'users/{userid}', "items", inv)
              
            update_db('users', f'{userid}', {'xpbooster': 100})
        else:
          if moneyboosters > 0:
            moneyboosters -= 1
            if (moneyboosters <= 0):
              inv.pop("MoneyBooster")
              update_db(f'users/{userid}', "items", inv)
            else:
              inv.update({"MoneyBooster": moneyboosters})
              update_db(f'users/{userid}', "items", inv)
              
            update_db('users', f'{userid}', {'moneybooster': 100})

        embed.add_field(name="Boosters:", value=f"Money Boosters: **{moneyboosters}**\nExperience Boosters: **{xpboosters}**")
        embed.set_footer(text=f"Successfully used 1 {val}.")

        await interaction.message.edit(embed=embed, content=None, view=use_before(self.ctx, userid, self.options))
        await interaction.response.defer()
        return
          
      elif "Edit Badge" in str(val):
        try:
          milestones = get_db('users')[f'{interaction.user.id}']['milestones']
        except:
          embed = discord.Embed(description="You have no badges.")
          await interaction.message.edit(embed=embed, content=None, view=None)
          return
        else:
          embed = discord.Embed(description="Your Badges:")
          patrons = get_db('misc')['all_patrons']
          games_used = 0
          role_used = 0
          owner_used = 0
          supporter_used = 0
          gambler_used = 0
          owner_used2 = 0
          bug_hunter_used = 0
          arg1_badge_used = 0
          
          for x in milestones:
            if "Games" in x:
              if games_used == 0:
                games_used += 1
                embed.add_field(name="Mini-Game Wins Badge", value=f"Level {milestones['Mini-Games Won']['level']}/6 {badge_emojies['game'][milestones['Mini-Games Won']['level'] - 1]}\n{check_level('Mini-Games Won', interaction.user.id)['next']} wins")
            if "Role" in x:
              if role_used == 0:
                role_used += 1
                embed.add_field(name="Beta Role Badge", value=f"Level {milestones['Beta Role']['level']} {badge_emojies['role'][milestones['Beta Role']['level'] - 1]}")

            if "Gambler" in x:
              if gambler_used == 0:
                gambler_used += 1
                embed.add_field(name="Compulsive Gambler Badge", value=f"Level {milestones['Compulsive Gambler']['level']}/6 {badge_emojies['gambler'][milestones['Compulsive Gambler']['level'] - 1]}\n{check_level('Compulsive Gambler', interaction.user.id)['next']}")

            if "Hunter" in x:
              if bug_hunter_used == 0:
                bug_hunter_used += 1
                embed.add_field(name="Bug Hunter Badge", value=f"Level {milestones['Bug Hunter']['level']}/3 {badge_emojies['bug_hunter'][milestones['Bug Hunter']['level'] - 1]}")

            if f"{interaction.user.id}" in list(patrons):
              if supporter_used == 0:
                supporter_used += 1
                pledge = patrons[f"{interaction.user.id}"]['pledge']
                if pledge == 100:
                  embed.add_field(name="Supporter Badge", value=f"Tier 1/4 {badge_emojies['patreon'][0]}")
                elif pledge == 300:
                  embed.add_field(name="Supporter Badge", value=f"Tier 2/4 {badge_emojies['patreon'][1]}")
                elif pledge == 500:
                  embed.add_field(name="Supporter Badge", value=f"Tier 2/4 {badge_emojies['patreon'][2]}")
                elif pledge == 1000:
                  embed.add_field(name="Supporter Badge", value=f"Max Tier {badge_emojies['patreon'][3]}")
                else:
                  pass

            if "ARG" in x:
              if arg1_badge_used == 0:
                arg1_badge_used += 1
                embed.add_field(name="ARG Winner Badge", value=f"Level {milestones['ARG']['level']}/3 {badge_emojies['ARG1']}")

            if interaction.user.id == ses:
              if owner_used == 0:
                owner_used += 1
                embed.add_field(name="Owner Badge", value=f"Level 1 <:owner_badge:1139344922495950955>")

            if (interaction.user.id == 446722881079214081) or (interaction.user.id == ses):
              if owner_used2 == 0:
                owner_used2 += 1
                embed.add_field(name="Neco Badge", value=f"Level 1 <:neco_arc_shrug:1112389684732117133>")
                
            else:
              continue
          else:
            await interaction.message.edit(embed=embed, content=None, view=Badge_Slots(self.ctx, self.author))
            await interaction.response.defer()
            return
        
      elif "Set Background" in str(val):
        try:
          bgs = get_db('users')[f"{interaction.user.id}"]['items']['Backgrounds']
        except:
          embed = discord.Embed(description="You have not purchased any backgrounds.")
          await interaction.message.edit(embed=embed, content=None, view=None)
          return
        options = []
        for x in bgs:
          options.append(discord.SelectOption(label=f"Background: {x}"))
        else:
          await interaction.message.edit(embed=embed, content=None, view=Use_Background(self.ctx, self.author, options))
          return

      elif "Remove Background" in str(val):
        embed = discord.Embed(description=f"Your profile background has been reset to the default image.")
        del_db(f'users/{interaction.user.id}', 'background')

      elif "Edit Profile" in str(val):
        patreon = get_db('misc')['all_patrons']
        if (f"{str(self.ctx.author.id)}" not in list(patreon)) and (self.ctx.author.id != ses):
          embed = discord.Embed(description=f"This is a patreon exclusive feature.")
          await interaction.message.edit(embed=embed, content=None, view=None)
          return

        modal = Edit_Modal()
        await interaction.response.send_modal(modal)
        return
      
      elif "Add your own" in str(val):
        patreon = get_db('misc')['all_patrons']
        if (str(self.ctx.author.id) in list(patreon)) or (self.ctx.author.id == ses) or (self.ctx.author.id == 446722881079214081):
          if (self.ctx.author.id == ses) or (self.ctx.author.id == 446722881079214081):
            pledge = 1000
          else:
            pledge = int(patreon[f"{self.ctx.author.id}"]["pledge"])
            
          if (pledge > 500) or (self.ctx.author.id == ses) or (self.ctx.author.id == 446722881079214081):
            await interaction.response.send_message("Your next message will be set as your background.\n**The image has to be an attachment.**\nPlease do not delete the message after sending it.\n\nRecommended resolution: 1500x1000 (.png/.jpg/.jpeg/.gif only)", ephemeral=True)
            pass
          
            def check(m):
              return m.attachments
    
            msg = await client.wait_for("message", check=check, timeout=60)
            pass
            if msg.attachments:
              if (".png" in msg.attachments[0].url) or (".jpg" in msg.attachments[0].url) or (".jpeg" in msg.attachments[0].url) or (".gif" in msg.attachments[0].url):
                formatter = str(msg.attachments[0].url).rsplit(".", 1)[1]
                if not "gif" in formatter:
                  formatter = "png"
    
                for filename in os.listdir('./images/assets/backgrounds/custom'):
                  if f"{self.ctx.author.id}" in filename:  
                    location = "./images/assets/backgrounds/custom"
                    path = os.path.join(location, filename)  
                    os.remove(path)
                
                await msg.attachments[0].save(f"images/assets/backgrounds/custom/{self.ctx.author.id}.{formatter}")
                
                embed = discord.Embed(description=f"Image successfully saved and set as profile background.")
                update_db('users', f"{interaction.user.id}", {"background": f"{self.ctx.author.id}"})
                pass
              else:
                embed = discord.Embed(description=f"Unsupported file format for {msg.attachments[0].url}")
            else:
              embed = discord.Embed(description=f"Link not found in {msg.content}")
          else:
            embed = discord.Embed(description=f"Only patrons of 5 dollars or more are allowed to use this feature.")
            await interaction.message.edit(embed=embed, content=None, view=None)
            return
        else:
          embed = discord.Embed(description=f"Only patrons of 5 dollars or more are allowed to use this feature.")
          await interaction.message.edit(embed=embed, content=None, view=None)
          return
      
      await interaction.message.edit(embed=embed, content=None, view=None)

class use_before(discord.ui.View):
  def __init__(self, ctx, author, options):
    super().__init__(timeout=None)
    self.ctx = ctx
    self.author = author
    self.options = options
    self.add_item(Use(self.options, self.ctx))

class Shop(commands.Cog):
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
      raise discord.ext.commands.CommandError(f"Sorry, this command is currently internally disabled, as it is being worked on.")

  @commands.command(aliases=["store", "buy"])
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 60, commands.BucketType.user)
  async def shop(self, ctx):
    all_items = get_db("misc")['shop']['items']
    options = []
    shop = discord.Embed(title=f"{check_currency(ctx.guild.id)} shop", description=f"Please select an item you want to buy.")
    for item in list(all_items):
      item_name = item.replace("Booster", " Booster")
      emoji = None
      emoji2 = ""
      if "Money" in item:
        emoji = "💰"
        emoji2 = emoji
      options.append(discord.SelectOption(label=item_name, emoji=emoji))
      shop.add_field(name=f"{item_name} {emoji2}", value=f"Price: {all_items[item][list(all_items[item])[0]]} {check_currency(ctx.guild.id)}\n{all_items[item][list(all_items[item])[1]]}")
    author = ctx.author.id
    view = Select(ctx, author, options)
    await ctx.send(embed=shop, content=None, view=view)
  
  @commands.command(aliases=["item", "inv", "storage", "background"])
  @commands.before_invoke(disabled_check)
  @commands.cooldown(1, 30, commands.BucketType.user)
  async def inventory(self, ctx):
    options = []
    try:
      inv = get_db('users')[f'{ctx.author.id}']['items']
    except:
      embed = discord.Embed(description=f"You don't have any items, buy some by invoking `{bot_prefix}shop`.", color=ctx.author.color)
    else:
      embed = discord.Embed(description=f"Select an item you want to use.\n\n{ctx.author.name}'s Items:")
      if "Backgrounds" in inv.keys():
        embed.add_field(name="Backgrounds:", value=f"You own: **{len(list(inv['Backgrounds']))}**")
      if ("MoneyBooster" in inv.keys()) or ("ExperienceBooster" in inv.keys()):
        moneyboosters = 0
        xpboosters = 0 
        if ("ExperienceBooster" in inv.keys()):
          xpboosters = inv['ExperienceBooster']
          options.append(discord.SelectOption(label="Experience Booster"))
        if ("MoneyBooster" in inv.keys()):
          moneyboosters = inv['MoneyBooster']
          options.append(discord.SelectOption(label="Money Booster"))

        embed.add_field(name="Boosters:", value=f"Money Boosters: **{moneyboosters}**\nExperience Boosters: **{xpboosters}**")
      
    options.append(discord.SelectOption(label="Set Background"))
    options.append(discord.SelectOption(label="Remove Background"))
    options.append(discord.SelectOption(label="Add your own Background"))
    options.append(discord.SelectOption(label="Edit Profile Background"))
    options.append(discord.SelectOption(label="Edit Badge Slots"))
    view = use_before(ctx, ctx.author.id, options)
    await ctx.send(embed=embed, content=None, view=view)

  @commands.command()
  @commands.is_owner()
  async def add_badge(self, ctx, user: discord.User, badge:str, level=None):
    if level == None:
      level = 1

    if "game" in badge.lower():
      return


def setup(client):
  client.add_cog(Shop(client))