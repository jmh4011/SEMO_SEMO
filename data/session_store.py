from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from commands.team import TeamView

# 세션 저장소 (owner_id → TeamView)
session_store: dict[int, 'TeamView'] = {}
