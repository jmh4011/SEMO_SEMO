import discord
from discord.ui import Button
from utils.team_utils import shuffle_list

class TeamView(discord.ui.View):
    def __init__(self, owner_id: int, team_count: int):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.team_count = team_count
        self.participants: set[int] = set()

        # 종료/취소 버튼 미리 생성
        self.end_button = Button(label="🔒 모집 종료", style=discord.ButtonStyle.danger, custom_id="end_or_cancel")
        self.end_button.callback = self.end_or_cancel
        self.add_item(self.end_button)

    def build_embed(self) -> discord.Embed:
        mentions = [f"<@{uid}>" for uid in self.participants]
        description = (
            f"👥 <@{self.owner_id}> 님이 팀을 모집 중입니다!\n"
            f"✅ 아래 버튼을 눌러 참여하거나 ❌로 취소하세요.\n\n"
            f"👤 **현재 참여자 ({len(self.participants)}명)**\n" +
            ("\n".join(f"・{m}" for m in mentions) if mentions else "없음")
        )
        return discord.Embed(
            title="팀 모집 중",
            description=description,
            color=discord.Color.blurple()
        ).set_footer(text=f"팀 수: {self.team_count}")

    @discord.ui.button(label="✅ 참여하기", style=discord.ButtonStyle.primary)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in self.participants:
            self.participants.add(interaction.user.id)
            await interaction.message.edit(embed=self.build_embed(), view=self)
        await interaction.response.defer()

    @discord.ui.button(label="❌ 참여 취소", style=discord.ButtonStyle.secondary)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.participants:
            self.participants.remove(interaction.user.id)
            await interaction.message.edit(embed=self.build_embed(), view=self)
        await interaction.response.defer()

    @discord.ui.button(label="🔒 모집 종료", style=discord.ButtonStyle.danger)
    async def end(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message("모집자만 종료할 수 있습니다.", ephemeral=True)
            return

        if len(self.participants) < self.team_count:
            await interaction.response.send_message("참여자가 팀 수보다 적습니다.", ephemeral=True)
            return

        members = list(self.participants)
        shuffle_list(members)
        teams = [[] for _ in range(self.team_count)]
        for i, uid in enumerate(members):
            teams[i % self.team_count].append(f"<@{uid}>")

        result = "\n\n".join(
            f"🔹 **Team {i + 1}**\n" + "\n".join(team)
            for i, team in enumerate(teams)
        )
        embed = discord.Embed(title="🎲 팀 분배 결과", description=result, color=discord.Color.green())
        await interaction.message.edit(embed=embed, view=None)
        await interaction.response.defer()

    def update_end_button_label(self):
        if len(self.participants) < self.team_count:
            self.end_button.label = "🛑 모집 취소"
            self.end_button.style = discord.ButtonStyle.secondary
        else:
            self.end_button.label = "🔒 모집 종료"
            self.end_button.style = discord.ButtonStyle.danger

    async def end_or_cancel(self, interaction: discord.Interaction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message("모집자만 가능합니다.", ephemeral=True)
            return

        if len(self.participants) < self.team_count:
            # 모집 취소 처리
            embed = discord.Embed(
                title="❌ 모집이 취소되었습니다.",
                description="참여 인원이 부족하여 자동으로 모집이 종료되었습니다.",
                color=discord.Color.red()
            )
            await interaction.message.edit(embed=embed, view=None)
        else:
            # 팀 분배 처리 (기존 end 버튼 로직 사용)
            await self.perform_team_assignment(interaction)

        from data.session_store import session_store
        session_store.pop(self.owner_id, None)
        await interaction.response.defer()