import discord
from discord.ext import commands
from features.team.command import get_team_command
from shared.config import settings
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    for gid in settings.guild_ids:
        await bot.tree.sync(guild=discord.Object(id=gid))
    print(f"✅ 봇 로그인: {bot.user}")

# 명령 등록
for gid in settings.guild_ids:
    bot.tree.add_command(get_team_command(), guild=discord.Object(id=gid))

bot.run(settings.discord_token)
