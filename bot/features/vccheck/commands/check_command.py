from discord import app_commands, Interaction
from features.vccheck.dto.check_input import VcCheckInput
from features.vccheck.services.check_service import VcCheckService


class VcCheckCommand:
    def __init__(self):
        self.service = VcCheckService()

    def as_app_command(self) -> app_commands.Command:
        @app_commands.command(name="vccheck", description="VC 미참여자 확인")
        @app_commands.describe(message="메시지 링크 또는 ID")
        async def command(interaction: Interaction, message: str = None):
            try:
                data = VcCheckInput.from_interaction(interaction, message)
            except ValueError as e:
                await interaction.response.send_message(str(e), ephemeral=True)
                return

            await self.service.process(interaction, data)

        return command
