from discord import Interaction
from .dto import TeamAssignmentResult
from .store import session_store
from .embed import build_result_embed, build_cancel_embed
from .validator import is_owner
from shared.utils import shuffle_and_split
from .view import TeamView

async def handle_join(view: TeamView, interaction: Interaction) -> None:
    view.participants.add(interaction.user.id)
    view.update_end_button()
    await interaction.message.edit(embed=view.build_embed(), view=view)
    await _safe_defer(interaction)

async def handle_leave(view: TeamView, interaction: Interaction) -> None:
    view.participants.discard(interaction.user.id)
    view.update_end_button()
    await interaction.message.edit(embed=view.build_embed(), view=view)
    await _safe_defer(interaction)

async def handle_end_or_cancel(view: TeamView, interaction: Interaction) -> None:
    if not is_owner(view, interaction):
        await interaction.response.send_message("모집자만 가능합니다.", ephemeral=True)
        return

    if len(view.participants) < view.team_count:
        await interaction.message.edit(embed=build_cancel_embed(), view=None)
    else:
        teams = shuffle_and_split(list(view.participants), view.team_count)
        result = TeamAssignmentResult(teams=teams, team_count=view.team_count)
        await interaction.message.edit(embed=build_result_embed(result), view=None)

    session_store.pop(view.owner_id, None)
    await _safe_defer(interaction)

async def _safe_defer(interaction: Interaction) -> None:
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except:
        pass
