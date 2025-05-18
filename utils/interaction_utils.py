import discord

async def safe_defer(interaction: discord.Interaction, ephemeral: bool = False):
    """응답되지 않은 interaction에 대해 안전하게 defer 호출"""
    try:
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=ephemeral)
    except discord.NotFound:
        # interaction expired (ex: 버튼 누르고 너무 늦음)
        pass
    except discord.HTTPException:
        # 기타 HTTP 오류도 무시
        pass
