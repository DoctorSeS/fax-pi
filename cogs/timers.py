from discord.ext import commands, tasks
import discord
import datetime

from cogs.events import check_logs
from main import client
from termcolor import cprint
import patreon
from database import *
import requests


def refresh_access_token():
  client_id = os.environ.get("PATREON_CLIENT_ID")
  client_secret = os.environ.get("PATREON_KEY")
  refresh_token = os.environ.get("PATREON_REFRESH_TOKEN")

  token_url = "https://www.patreon.com/api/oauth2/token"
  payload = {
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token,
    'client_id': client_id,
    'client_secret': client_secret,
  }

  response = requests.post(token_url, data=payload)
  if response.status_code == 200:
    tokens = response.json()
    os.environ["PATREON_KEY"] = tokens['access_token']
    os.environ["PATREON_REFRESH_TOKEN"] = tokens['refresh_token']
    print("Access token refreshed.")
    update_db('misc', 'none', {'patreon_key': tokens['access_token'], 'patreon_refresh_token': tokens['refresh_token']})
    return True
  else:
    print("Failed to refresh token:", response.json())
    return False

def check_patreon():
  access_token = os.environ.get("PATREON_KEY")
  api_client = patreon.API(access_token)

  campaign_response = api_client.fetch_campaign()
  if "The server could not verify" in str(campaign_response):
    print("Access token expired, refreshing...")
    response = refresh_access_token()
    if response is False:
      return
    else:
      access_token = os.environ.get("PATREON_KEY")
      api_client = patreon.API(access_token)

      campaign_response = api_client.fetch_campaign()
      pass

  campaign_id = campaign_response.data()[0].id()
  
  all_pledges = []
  cursor = None
  while True:
    pledges_response = api_client.fetch_page_of_pledges(campaign_id, 25, cursor=cursor, fields={'pledge': ['total_historical_amount_cents', 'declined_since']})
    cursor = api_client.extract_cursor(pledges_response)
    all_pledges += pledges_response.data()
    if not cursor:
      break
  
  pledges_info = {}
  for pledge in pledges_response.data():
    declined = pledge.attribute('declined_since')
    reward_tier = 0
  
    if pledge.relationships()['reward']['data']:
      reward_tier = pledge.relationship('reward').attribute('amount_cents')
  
    if (not declined) and (reward_tier >= 100):
      discord_id = "None"
      try:
        discord_id = pledge.relationship('patron').attribute('social_connections')['discord']['user_id']
      except:
        pass
      finally:
        pass
      pledges_info.update({f"{discord_id}": {'name': f"{pledge.relationship('patron').attribute('full_name')}", "pledge": f"{pledge.relationship('reward').attribute('amount_cents')}", 'total': f"{pledge.attribute('total_historical_amount_cents')}"}})

      update_db('misc', 'all_patrons', pledges_info)

def add_time(time_add):
  current = datetime.datetime.now()
  add = datetime.timedelta(hours=int(time_add))
  new_time = current + add

  return str(new_time)

class Timers(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    if client.is_ready():
      self.timers.start()
      self.patreon_check.start()
      self.active_check.start()
      self.inactive_check.start()
      self.check_files.start()
      self.check_changes.start()
  
  @tasks.loop(hours=2)
  async def patreon_check(self):
    check_patreon()

  @tasks.loop(hours=1)
  async def check_files(self):
    files = []
    dir_path = ["images/assets/backgrounds/simple", "images/assets/backgrounds/complex", "images/assets/backgrounds/very complex", "images/assets/backgrounds/special"]
    for folder in dir_path:
      for file_path in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, file_path)):
          files.append(file_path.replace(".png", ""))

    files.append('default')
    update_db('misc', 'none', {"background_files": files})

  @tasks.loop(hours=1)
  async def check_changes(self):
    files = list(get_db('misc')['background_files'])
    bgs = get_db('misc')['shop']['backgrounds']
    for x in files:
      if not f"'{x}'" in str(bgs):
        rootdir = 'images/assets/backgrounds'
        path = ""
        for subdir, dirs, files2 in os.walk(rootdir):
          for file in files2:
            if x in file:
              path = os.path.join(subdir, file)
              t = "\ ".replace(" ", "")
              path = path.replace(t, '/')

        path = path.split("backgrounds/")[1].lstrip().split(f"/{x}")[0]
        if "_" in x:
          b_name = x.split("_")
          b_name = [i.title() for i in b_name]
          name = ""
          for word in b_name:
            if len(name) == 0:
              name = name + word
            else:
              name = name + " " + word
        else:
          name = x.capitalize()

        if "default" in x:
          return
        else:
          cprint(f"File missing from Database: {path}/{x}", "red")
          bgs[path]["name"].append(name)
          bgs[path]["filename"].append(x)

          update_db('misc/shop', 'backgrounds', bgs)
          self.client.reload_extension(f'cogs.shop')
          cprint(f"Background {name} has be added to the database.", "green")

  @tasks.loop(hours=2)
  async def inactive_check(self):
    guild = client.get_guild(508043534071365652)
    if guild:
      supporter_role_id = 1129566098170335262
      role = guild.get_role(supporter_role_id)
      members = str(role.members)
      all_ids = []
      while "Member id=" in members:
        members2 = int(members.split("<Member id=")[1].lstrip().split(" name=")[0])
        members = members.replace("<Member id=", "", 1)
        all_ids.append(members2)
      else:
        for id in all_ids:
          value = list(get_db('misc')['all_patrons'])
          if str(id) in value:
            continue
          else:
            user = guild.get_member(int(id))
            await user.remove_roles(role, atomic=True, reason="Not an active supporter anymore.")
    
  @tasks.loop(hours=2)
  async def active_check(self):
    guild = client.get_guild(508043534071365652)
    supporter_role = 1129566098170335262
    users = list(get_db('misc')['all_patrons'])
    for x in users:
      try:
        user = guild.get_member(int(x))
      except:
        continue
      else:
        roles = [role for role in user.roles]
        if str(supporter_role) in roles:
          continue
        else:
          role = guild.get_role(supporter_role)
          await user.add_roles(role, atomic=True)

  @tasks.loop(seconds=20)
  async def timers(self):

    for x in get_db('timers'):
      current = datetime.datetime.now()
      if ("holder" in x) or ("Remind" in x):
        continue

      try:
        value = get_db('timers')[x]
      except:
        continue
      value2 = str(value)

      if "Streak" in x:
        value2 = str(value2.split("/")[1])
        
      date_check = datetime.datetime.strptime(value2, '%Y-%m-%d %H:%M:%S.%f')
        
      if current >= date_check:
        value3 = str(x)
        if "TimerLock-" in value3:
          x2 = value3.replace("TimerLock-", "")
          x3 = int(x2)
          channel = await client.fetch_channel(x3)
          unlk = discord.Embed(description=f"<#{channel.id}> has been unlocked.\nReason: Lockdown timer expired.", color=discord.Color.from_rgb(r=255, g=0, b=0))
          await channel.send(embed=unlk, content=None)
          await channel.set_permissions(channel.guild.default_role, send_messages=True)
          del_db("timers", f"TimerLock-{x2}")
            
        elif "TimerPrint-" in value3:
          x2 = value3.replace("TimerPrint-", "")
          del_db("timers", f"TimerPrint-{x2}")

        elif "TimerXp-" in value3:
          x2 = value3.replace("TimerXp-", "")
          del_db("timers", f"TimerXp-{x2}")
            
        elif "TimerDaily-" in value3:
          x2 = value3.replace("TimerDaily-", "")
          del_db("timers", f"TimerDaily-{x2}")

        elif "TimerStreak-" in value3:
          x2 = value3.replace("TimerStreak-", "")
          del_db("timers", f"TimerStreak-{x2}")
            
        elif "TimerRep-" in value3:
          x2 = value3.replace("TimerRep-", "")
          del_db("timers", f"TimerRep-{x2}")

        elif "TimerBan-" in value3:
          x2 = value3.replace("TimerBan-", "")
          del_db("timers", f"TimerBan-{x2}")

          member_id = x2.split('/')[0]
          guild_id = x2.split('/')[1]

          if check_logs(guild_id)[0] is True:
            chan = check_logs(guild_id)[1]
            channel = client.get_guild(guild_id).get_channel(int(chan))
            user = client.get_user(member_id)
            embed2 = discord.Embed(description=f"**{user.mention} has been unbanned.**\n\n`Reason:` Temporary Ban Expired.", color=discord.Color.from_rgb(r=0, g=255, b=0))
            embed2.set_author(name=f"{user.name} • ID: {user.id}", icon_url=user.avatar)
            await channel.send(embed=embed2, content=None)


def setup(client):
  client.add_cog(Timers(client))