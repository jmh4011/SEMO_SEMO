from typing import List
from discord import app_commands, Object
from core.settings import settings


def assign_guilds_if_staging(command: app_commands.Command) -> app_commands.Command:
    if settings.env == "staging":
        command.guilds = [Object(id=gid) for gid in settings.guild_ids]
    return command


def shuffle_and_split(members: List[int], team_count: int) -> List[List[str]]:
    import random

    random.shuffle(members)
    teams: List[List[str]] = [[] for _ in range(team_count)]
    for i, uid in enumerate(members):
        teams[i % team_count].append(f"<@{uid}>")
    return teams
