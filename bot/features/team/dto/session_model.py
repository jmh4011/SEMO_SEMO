from pydantic import BaseModel
from typing import List


class TeamSession(BaseModel):
    owner_id: int
    team_count: int
    participants: List[int]
