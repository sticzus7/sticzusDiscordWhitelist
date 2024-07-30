import disnake
from disnake.ext import commands
import requests

TOKEN = '' # token bota
GUILD_ID = 1261266075908177953  # id discorda
ROLE_ID = 1267939034525733054  # id roli
WEBHOOK_URL = ''  # webhook url
intents = disnake.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.InteractionBot(intents=intents)

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')

    await bot.change_presence(activity=disnake.Game(name="sticzus bo$$"))

@bot.slash_command(name="nadajwl", description="nadaj whiteliste okok", guild_ids=[GUILD_ID])
async def daj_role(ctx, discord_id: str):
    guild = bot.get_guild(GUILD_ID)
    member = guild.get_member(int(discord_id))
    role = disnake.utils.get(guild.roles, id=ROLE_ID)

    if not member:
        await ctx.send(f'Uzytkownik o ID {discord_id} nie zostal znaleziony', ephemeral=True)
        return

    if role:
        await member.add_roles(role)
        await ctx.send(f'Whitelista została nadana uzytkownikowi {member.mention}.', ephemeral=True)
        
        try:
            await member.send(f'Zdales Whiteliste oraz otrzymales role {role.name} na serwerze {guild.name}.')
        except disnake.Forbidden:
            pass  


        embed = {
            "title": "Zdana Whitelist",
            "description": f"Użytkownik {member.mention} otrzymał rolę {role.name}.",
            "color": 0x00ff00,  
            "fields": [
                {"name": "Użytkownik", "value": member.mention, "inline": True},
                {"name": "Discord ID", "value": str(member.id), "inline": True},
            ],
            "footer": {"text": "logs by sticzus"}
        }


        data = {
            "embeds": [embed]
        }
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f'lol webhook rozjebany xDlol {response.status_code}')

    else:
        await ctx.send(f'Rola o ID {ROLE_ID} nie istnieje.', ephemeral=True)

bot.run(TOKEN)
