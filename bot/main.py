import discord
from discord.ext import commands
from core.settings import settings
from core.logger import setup_logger
from features.team.commands.team_command import TeamCommand
from features.vccheck.commands.check_command import VcCheckCommand
from features.vccheck.commands.check_context import VcCheckContextCommand
import logging

logger = logging.getLogger(__name__)
setup_logger(settings.env, settings.log_level)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)


def register_commands(bot: commands.Bot, commands: list):
    for command in commands:
        if settings.env == "staging":
            bot.tree.add_command(
                command, guilds=[discord.Object(id=gid) for gid in settings.guild_ids]
            )
        else:
            bot.tree.add_command(command)


register_commands(
    bot,
    [
        TeamCommand().as_app_command(),
        VcCheckCommand().as_app_command(),
        VcCheckContextCommand().as_context_command(),
    ],
)


@bot.event
async def on_ready():
    logger.info(f"✅ 봇 로그인 완료: {bot.user}")
    for g in bot.guilds:
        logger.info(f" - {g.name} ({g.id})")

    if settings.env == "staging":
        for gid in settings.guild_ids:
            guild = discord.Object(id=gid)
            try:
                cmds = await bot.tree.sync(guild=guild)
                logger.info(
                    f"📌 {len(cmds)}개 명령어 서버 전용 등록 완료 (서버 ID: {gid})"
                )
                for cmd in cmds:
                    logger.info(f"  - /{cmd.name}")
            except Exception as e:
                logger.exception(f"❌ 서버 {gid}에 명령어 등록 실패: {e}")
    else:
        try:
            cmds = await bot.tree.sync()
            logger.info(f"🌍 글로벌 명령어 {len(cmds)}개 등록 완료")
        except Exception as e:
            logger.exception(f"❌ 글로벌 명령어 등록 실패: {e}")


bot.run(settings.discord_token)
