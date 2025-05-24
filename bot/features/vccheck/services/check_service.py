from discord import Interaction
from features.vccheck.dto.check_input import VcCheckInput
from features.vccheck.internal.team_parser import extract_participants


class VcCheckService:
    async def process(self, interaction: Interaction, data: VcCheckInput) -> str:
        guild = interaction.guild
        author_id = interaction.user.id
        channel = guild.get_channel(data.channel_id)
        message = await channel.fetch_message(data.message_id)

        participants, method = await extract_participants(message)
        vc_members = {
            member.id
            for vc in guild.voice_channels
            for member in vc.members
            if not member.bot
        }

        if author_id not in vc_members:
            await interaction.response.send_message(
                "⚠️ 이 명령어는 VC에 접속 중인 상태에서만 사용할 수 있습니다.",
                ephemeral=True,
            )
            return

        not_joined = vc_members - participants
        if not not_joined:
            await interaction.response.send_message(
                f"✅ 모든 VC 참여자가 해당 메시지의 {method}에 포함되어 있습니다!",
                ephemeral=True,
            )
            return

        mentions = "\n".join(f"・<@{uid}>" for uid in not_joined)
        await interaction.response.send_message(
            f"🔍 VC에 있으나 메시지의 {method}에 포함되지 않은 유저:\n{mentions}",
            ephemeral=True,
        )
        return
