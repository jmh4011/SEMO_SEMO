from __future__ import annotations
import discord
from typing import TYPE_CHECKING
from features.team.internal.team_embed import TeamEmbedFactory
from features.team.internal.session_store import session_store
from core.utils import shuffle_and_split


if TYPE_CHECKING:
    from features.team.views.team_view import TeamView


class TeamService:
    async def handle_join(
        self, view: "TeamView", interaction: discord.Interaction
    ) -> None:
        view.participants.add(interaction.user.id)
        view.update_end_button()
        await interaction.message.edit(embed=view.build_embed(), view=view)
        await self._safe_defer(interaction)

    async def handle_leave(
        self, view: "TeamView", interaction: discord.Interaction
    ) -> None:
        view.participants.discard(interaction.user.id)
        view.update_end_button()
        await interaction.message.edit(embed=view.build_embed(), view=view)
        await self._safe_defer(interaction)

    async def handle_end_or_cancel(
        self, view: "TeamView", interaction: discord.Interaction
    ) -> None:
        if interaction.user.id != view.owner_id:
            await interaction.response.send_message(
                "모집자만 가능합니다.", ephemeral=True
            )
            return

        if len(view.participants) < view.team_count:
            embed = TeamEmbedFactory().build_cancel_embed()
        else:
            teams = shuffle_and_split(list(view.participants), view.team_count)
            embed = TeamEmbedFactory().build_result_embed(teams)

        await interaction.message.edit(embed=embed, view=None)
        session_store.delete(view.owner_id)
        await self._safe_defer(interaction)

    async def _safe_defer(self, interaction: discord.Interaction) -> None:
        try:
            if not interaction.response.is_done():
                await interaction.response.defer()
        except:
            pass
