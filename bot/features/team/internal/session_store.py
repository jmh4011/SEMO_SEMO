from core.redis_client import redis_client
from features.team.dto.session_model import TeamSession


class RedisTeamSessionStore:
    PREFIX = "team_session"

    def _key(self, user_id: int) -> str:
        return f"{self.PREFIX}:{user_id}"

    def set(self, user_id: int, session: TeamSession) -> None:
        redis_client.set(self._key(user_id), session.model_dump_json())

    def get(self, user_id: int) -> TeamSession | None:
        raw = redis_client.get(self._key(user_id))
        if not raw:
            return None
        return TeamSession.model_validate_json(raw)

    def delete(self, user_id: int) -> None:
        redis_client.delete(self._key(user_id))


session_store = RedisTeamSessionStore()
