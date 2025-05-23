from typing import List, Set
from pydantic import BaseModel, Field, field_validator

class TeamCommandInput(BaseModel):
    user_id: int
    guild_id: int
    team_count: int = Field(default=2)

    @field_validator("team_count")
    @classmethod
    def check_min_team(cls, v: int) -> int:
        if v < 2:
            raise ValueError("팀 수는 2 이상이어야 합니다")
        return v

class TeamSession(BaseModel):
    owner_id: int
    team_count: int
    participants: Set[int] = set()

    @field_validator("team_count")
    @classmethod
    def check_team_count(cls, v: int) -> int:
        if v < 2:
            raise ValueError("팀 수는 2 이상이어야 합니다")
        return v

    def add(self, user_id: int) -> None:
        self.participants.add(user_id)

    def remove(self, user_id: int) -> None:
        self.participants.discard(user_id)

    def count(self) -> int:
        return len(self.participants)

class TeamAssignmentResult(BaseModel):
    teams: List[List[str]]
    team_count: int

    def to_embed_text(self) -> str:
        return "\n\n".join(
            f"🔹 **Team {i+1}**\n" + "\n".join(team)
            for i, team in enumerate(self.teams)
        )
