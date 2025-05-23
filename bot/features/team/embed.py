from discord import Embed
from typing import Set
from .dto import TeamAssignmentResult

def build_team_embed(owner_id: int, team_count: int, participants: Set[int]) -> Embed:
    mentions = [f"<@{uid}>" for uid in participants]
    desc = f"👥 <@{owner_id}> 님이 팀을 모집 중입니다!\n\n" + \
            f"👤 현재 참여자 ({len(participants)}명):\n" + \
            ("\n".join(f"・{m}" for m in mentions) if mentions else "없음")
    return Embed(title="팀 모집 중", description=desc, color=0x5865F2).set_footer(text=f"팀 수: {team_count}")

def build_cancel_embed() -> Embed:
    return Embed(title="❌ 모집이 취소되었습니다", description="참여 인원이 부족합니다.", color=0xFF0000)

def build_result_embed(result: TeamAssignmentResult) -> Embed:
    return Embed(title="🎲 팀 분배 결과", description=result.to_embed_text(), color=0x57F287)
