import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from commands.team import team_command
from commands.vccheck import vccheck_command
from config_loader import GUILD_CONFIG

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_IDS = list(map(int, GUILD_CONFIG.keys()))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    for gid in GUILD_IDS:
        await bot.tree.sync(guild=discord.Object(id=gid))
    print(f"✅ 봇 준비 완료: {bot.user}")

for gid in GUILD_IDS:
    bot.tree.add_command(team_command, guild=discord.Object(id=gid))
    bot.tree.add_command(vccheck_command, guild=discord.Object(id=gid))

bot.run(TOKEN)

