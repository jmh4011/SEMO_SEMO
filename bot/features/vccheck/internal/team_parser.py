import re
import discord
from typing import Set, Tuple


async def extract_participants(message: discord.Message) -> Tuple[Set[int], str]:
    if message.embeds:
        embed = message.embeds[0]
        if embed.title == "팀 모집 중":
            lines = embed.description.splitlines()
            participants = {
                int(line.strip("・<@>"))
                for line in lines
                if line.strip().startswith("・<@")
            }
            return participants, "참여자"

        elif embed.title == "🎲 팀 분배 결과":
            matches = re.findall(r"<@(\d+)>", embed.description)
            participants = {int(uid) for uid in matches}
            return participants, "팀 분배 결과 팀원"

    participants = set()
    for reaction in message.reactions:
        async for user in reaction.users():
            if not user.bot:
                participants.add(user.id)
    return participants, "반응자"
