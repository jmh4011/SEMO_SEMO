import discord
from discord import app_commands
from data.session_store import session_store

@app_commands.command(name="vccheck", description="VC에서 미참여자 확인")
async def vccheck_command(interaction: discord.Interaction):
    view = session_store.get(interaction.user.id)
    if not view:
        await interaction.response.send_message("현재 모집 중인 팀이 없습니다.", ephemeral=True)
        return

    if not interaction.user.voice or not interaction.user.voice.channel:
        await interaction.response.send_message("VC에 접속되어야 합니다.", ephemeral=True)
        return

    vc_members = [m for m in interaction.user.voice.channel.members if not m.bot]
    non_participants = [m for m in vc_members if m.id not in view.participants]

    if not non_participants:
        await interaction.response.send_message("VC 내 모든 사용자가 참여했습니다.", ephemeral=True)
        return

    embed = discord.Embed(
        title="❗ VC 미참여자 목록",
        description="\n".join(f"・{m.mention}" for m in non_participants),
        color=discord.Color.orange()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
