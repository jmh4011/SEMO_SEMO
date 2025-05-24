import discord
from typing import Set


class TeamEmbedFactory:
    def build_team_embed(
        self, owner_id: int, team_count: int, participants: Set[int]
    ) -> discord.Embed:
        mentions = [f"<@{uid}>" for uid in participants]
        desc = (
            f"👥 <@{owner_id}> 님이 팀을 모집 중입니다!\n\n"
            + f"👤 현재 참여자 ({len(participants)}명):\n"
            + ("\n".join(f"・{m}" for m in mentions) if mentions else "없음")
        )
        return discord.Embed(
            title="팀 모집 중", description=desc, color=discord.Color.blurple()
        ).set_footer(text=f"팀 수: {team_count}")

    def build_cancel_embed(self) -> discord.Embed:
        return discord.Embed(
            title="❌ 모집이 취소되었습니다",
            description="참여 인원이 부족합니다.",
            color=discord.Color.red(),
        )

    def build_result_embed(self, teams: list[list[str]]) -> discord.Embed:
        result = "\n\n".join(
            f"🔹 **Team {i+1}**\n" + "\n".join(team) for i, team in enumerate(teams)
        )
        return discord.Embed(
            title="🎲 팀 분배 결과", description=result, color=discord.Color.green()
        )
