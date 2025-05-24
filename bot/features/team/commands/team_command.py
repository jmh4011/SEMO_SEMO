from discord import app_commands, Interaction
from features.team.views.team_factory import TeamViewFactory
from features.team.dto.command_input import TeamCommandInput
from features.team.dto.session_model import TeamSession
from features.team.internal.session_store import session_store
from core.settings import settings


class TeamCommand:
    def __init__(self):
        self.view_factory = TeamViewFactory()

    def as_app_command(self) -> app_commands.Command:
        @app_commands.command(name="team", description="팀 모집 시작")
        @app_commands.describe(team_count="나눌 팀 수")
        async def command(interaction: Interaction, team_count: int = None):
            data = TeamCommandInput(
                user_id=interaction.user.id,
                guild_id=interaction.guild_id,
                team_count=team_count or 2,
            )
            view = self.view_factory.create(
                owner_id=data.user_id, team_count=data.team_count
            )

            session = TeamSession(
                owner_id=view.owner_id,
                team_count=view.team_count,
                participants=list(view.participants),
            )
            session_store.set(data.user_id, session)

            await interaction.response.send_message(embed=view.build_embed(), view=view)

        return command
