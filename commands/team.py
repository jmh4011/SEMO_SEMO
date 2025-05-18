# ✅ commands/team.py
import discord
from discord import app_commands
from views.team_view import TeamView
from data.session_store import session_store
from config_loader import get_guild_config

@app_commands.command(name="team", description="버튼 기반 팀 모집")
@app_commands.describe(team_count="나눌 팀 수")
async def team_command(interaction: discord.Interaction, team_count: int = None):
    config = get_guild_config(interaction.guild_id)
    if team_count is None:
        team_count = config["default_team_count"]

    if team_count < 2:
        await interaction.response.send_message("팀 수는 2 이상이어야 합니다.", ephemeral=True)
        return

    view = TeamView(owner_id=interaction.user.id, team_count=team_count)
    session_store[interaction.user.id] = view

    embed = view.build_embed()
    await interaction.response.send_message(embed=embed, view=view)