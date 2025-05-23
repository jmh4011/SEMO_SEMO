from discord import app_commands, Interaction
from .dto import TeamCommandInput
from .view import TeamView
from .store import session_store
from shared.config import get_guild_config

def get_team_command():
    @app_commands.command(name="team", description="팀 모집 시작")
    @app_commands.describe(team_count="나눌 팀 수")
    async def team(interaction: Interaction, team_count: int = None):
        config = get_guild_config(interaction.guild_id)
        data = TeamCommandInput(
            user_id=interaction.user.id,
            guild_id=interaction.guild_id,
            team_count=team_count or config["default_team_count"]
        )

        view = TeamView(owner_id=data.user_id, team_count=data.team_count)
        session_store[data.user_id] = view
        await interaction.response.send_message(embed=view.build_embed(), view=view)

    return team
