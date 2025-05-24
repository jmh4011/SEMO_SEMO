from discord import app_commands, Message, Interaction
from features.vccheck.dto.check_input import VcCheckInput
from features.vccheck.services.check_service import VcCheckService


class VcCheckContextCommand:
    def __init__(self):
        self.service = VcCheckService()

    def as_context_command(self) -> app_commands.ContextMenu:
        @app_commands.context_menu(name="VC 체크")
        async def context(interaction: Interaction, message: Message):
            try:
                data = VcCheckInput(
                    channel_id=message.channel.id,
                    message_id=message.id,
                    interaction=interaction,
                )
            except Exception as e:
                await interaction.response.send_message(str(e), ephemeral=True)
                return

            await self.service.process(interaction, data)

        return context
