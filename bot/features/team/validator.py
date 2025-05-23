from discord import Interaction
from .view import TeamView

def is_owner(view: TeamView, interaction: Interaction) -> bool:
    return interaction.user.id == view.owner_id
