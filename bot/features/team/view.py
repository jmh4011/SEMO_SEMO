import discord
from discord.ui import Button
from . import service, embed

class TeamView(discord.ui.View):
    def __init__(self, owner_id: int, team_count: int):
        super().__init__(timeout=None)
        self.owner_id = owner_id
        self.team_count = team_count
        self.participants: set[int] = set()

        self.join_btn = Button(label="✅ 참여하기", style=discord.ButtonStyle.primary)
        self.leave_btn = Button(label="❌ 취소", style=discord.ButtonStyle.secondary)
        self.end_btn = Button(label="🔒 종료", style=discord.ButtonStyle.danger)

        self.join_btn.callback = lambda i: service.handle_join(self, i)
        self.leave_btn.callback = lambda i: service.handle_leave(self, i)
        self.end_btn.callback = lambda i: service.handle_end_or_cancel(self, i)

        self.add_item(self.join_btn)
        self.add_item(self.leave_btn)
        self.add_item(self.end_btn)

    def build_embed(self) -> discord.Embed:
        return embed.build_team_embed(self.owner_id, self.team_count, self.participants)

    def update_end_button(self) -> None:
        if len(self.participants) < self.team_count:
            self.end_btn.label = "🛑 모집 취소"
            self.end_btn.style = discord.ButtonStyle.secondary
        else:
            self.end_btn.label = "🔒 모집 종료"
            self.end_btn.style = discord.ButtonStyle.danger
