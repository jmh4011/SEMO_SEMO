from discord import Interaction
from features.vccheck.dto.check_input import VcCheckInput
from features.vccheck.internal.team_parser import extract_participants


class VcCheckService:
    async def process(self, interaction: Interaction, data: VcCheckInput) -> None:
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

        not_in_vc = participants - vc_members
        not_in_msg = vc_members - participants

        if author_id not in vc_members:
            await interaction.response.send_message(
                "⚠️ 이 명령어는 VC에 접속 중인 상태에서만 사용할 수 있습니다.",
                ephemeral=True,
            )
            return

        # 모두 포함된 경우
        if not not_in_vc and not not_in_msg:
            await interaction.response.send_message(
                f"✅ VC 참여자와 메시지의 {method}가 완전히 일치합니다!",
                ephemeral=True,
            )
            return

        lines = []

        if not_in_msg:
            mentions = "\n".join(f"・<@{uid}>" for uid in not_in_msg)
            lines.append(f"🔍 VC에 있으나 메시지의 {method}에 없는 유저:\n{mentions}")

        if not_in_vc:
            mentions = "\n".join(f"・<@{uid}>" for uid in not_in_vc)
            lines.append(f"🔇 메시지에 있지만 VC에 없는 유저:\n{mentions}")

        await interaction.response.send_message("\n\n".join(lines), ephemeral=True)
