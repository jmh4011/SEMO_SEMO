from features.team.dto.session_model import TeamSession
from features.team.views.team_view import TeamView
from features.team.services.team_service import TeamService


class TeamViewFactory:
    def __init__(self):
        self.service = TeamService()

    def create(self, owner_id: int, team_count: int) -> TeamView:
        return TeamView(owner_id, team_count, self.service)

    def create_from_session(self, session: TeamSession) -> TeamView:
        view = TeamView(
            owner_id=session.owner_id,
            team_count=session.team_count,
            service=self.service,
        )
        view.participants = set(session.participants)
        view.update_end_button()
        return view
