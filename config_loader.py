
import json

with open("guild_config.json", "r", encoding="utf-8") as f:
    GUILD_CONFIG = json.load(f)

def get_guild_config(guild_id: int) -> dict:
    return GUILD_CONFIG.get(str(guild_id), {
        "team_timeout": 600,
        "default_team_count": 2
    })